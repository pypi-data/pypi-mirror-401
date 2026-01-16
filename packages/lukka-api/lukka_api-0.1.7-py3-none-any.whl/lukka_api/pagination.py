"""
Pagination utilities for Lukka API requests.

This module provides iterator-based pagination for handling large datasets,
extracting pagination logic from the main API classes for better separation of concerns.
"""

import requests
import logging
import time
from typing import Dict, Any, Optional, Iterator, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PageResult:
    """
    Result from a single page request.

    Attributes:
        data: Raw JSON response data from the API
        page_number: Current page number (1-indexed)
        next_url: URL for the next page, or None if this is the last page
        prices: List of price data points from this page
        prices_count: Number of prices in this page
    """

    data: Dict[str, Any]
    page_number: int
    next_url: Optional[str]
    prices: list
    prices_count: int


class APIPageIterator:
    """
    Iterator for paginated API requests with automatic retry logic.

    This class provides a reusable iterator pattern for handling paginated responses
    from the Lukka API, including automatic retry on rate limits and request failures.

    Example:
        >>> headers = {"Authorization": f"Bearer {token}"}
        >>> iterator = APIPageIterator(
        ...     url="https://api.example.com/data",
        ...     headers=headers,
        ...     params={"limit": 1440},
        ...     max_pages=100
        ... )
        >>> for page in iterator:
        ...     prices = page.prices
        ...     print(f"Page {page.page_number}: {page.prices_count} prices")
    """

    def __init__(
        self,
        url: str,
        headers: Dict[str, str],
        params: Optional[Dict[str, Any]] = None,
        max_pages: int = 100,
        max_retries: int = 3,
        retry_delay: float = 0.5,
        page_delay: float = 0.1,
        timeout: int = 30,
    ):
        """
        Initialize the page iterator.

        Args:
            url: Base URL for the first request
            headers: HTTP headers including authorization
            params: Query parameters for the first request
            max_pages: Maximum number of pages to retrieve (safety limit)
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay in seconds between retries
            page_delay: Delay in seconds between successful page requests
            timeout: Request timeout in seconds

        Raises:
            ValueError: If max_pages or max_retries is not positive
        """
        if max_pages <= 0:
            raise ValueError(f"max_pages must be positive, got: {max_pages}")

        if max_retries <= 0:
            raise ValueError(f"max_retries must be positive, got: {max_retries}")

        self.initial_url = url
        self.headers = headers
        self.params = params
        self.max_pages = max_pages
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.page_delay = page_delay
        self.timeout = timeout

        # State tracking
        self.page_count = 0
        self.next_url: Optional[str] = None
        self.is_first_request = True

    def __iter__(self) -> Iterator[PageResult]:
        """
        Return the iterator object (self).

        Returns:
            Self as an iterator
        """
        return self

    def __next__(self) -> PageResult:
        """
        Fetch and return the next page of results.

        Returns:
            PageResult containing the next page of data

        Raises:
            StopIteration: When no more pages are available or max_pages reached
            requests.RequestException: If API request fails after all retries
            Exception: If rate limit exceeded after all retries
        """
        # Check if we've reached the maximum page limit
        if self.page_count >= self.max_pages:
            logger.info(f"Maximum page limit ({self.max_pages}) reached")
            raise StopIteration

        # Check if we have more pages to fetch
        if not self.is_first_request and self.next_url is None:
            logger.info("No more pages available")
            raise StopIteration

        # Perform the request with retry logic
        retry_count = 0

        while retry_count < self.max_retries:
            try:
                # Determine which URL and params to use
                if self.is_first_request:
                    request_url = self.initial_url
                    request_params = self.params
                    self.is_first_request = False
                else:
                    # nextPageUrl is a complete URL path, we need to add the base domain if needed
                    if self.next_url.startswith("/v1/"):
                        request_url = f"https://data-pricing-api.lukka.tech{self.next_url}"
                    else:
                        request_url = self.next_url
                    request_params = None  # Next page URL already includes params

                # Make the API request
                response = requests.get(
                    request_url,
                    headers=self.headers,
                    params=request_params,
                    timeout=self.timeout,
                )

                # Handle successful response
                if response.status_code == 200:
                    self.page_count += 1
                    data = response.json()

                    # Extract pagination info
                    prices = data.get("prices", [])
                    prices_count = data.get("pricesCount", 0)
                    self.next_url = data.get("nextPageUrl")

                    logger.info(f"📄 Page {self.page_count}: {prices_count} prices retrieved")

                    # Small delay to respect rate limits
                    if self.next_url:
                        time.sleep(self.page_delay)

                    # Return page result
                    return PageResult(
                        data=data,
                        page_number=self.page_count,
                        next_url=self.next_url,
                        prices=prices,
                        prices_count=prices_count,
                    )

                # Handle rate limiting
                elif response.status_code == 429:
                    retry_count += 1
                    logger.warning(
                        f"Rate limit hit on page {self.page_count + 1}. "
                        f"Retry {retry_count}/{self.max_retries}"
                    )
                    if retry_count < self.max_retries:
                        time.sleep(self.retry_delay)
                    else:
                        raise Exception("Rate limit exceeded: too many concurrent requests")

                # Handle other HTTP errors
                else:
                    response.raise_for_status()

            except requests.RequestException as e:
                logger.error(f"API request failed on page {self.page_count + 1}: {e}")
                raise

        # Should not reach here, but safety fallback
        raise Exception(f"Failed to fetch page after {self.max_retries} retries")

    def collect_all(self) -> Dict[str, Any]:
        """
        Convenience method to collect all pages into a single result.

        This method iterates through all pages and combines them into a single
        response dictionary with all prices aggregated.

        Returns:
            Dict containing combined results with structure:
                - firstDate: First date from all pages
                - lastDate: Last date from all pages
                - totalPages: Number of pages retrieved
                - pricesCount: Total number of prices
                - totalPricesReported: Sum of pricesCount from all pages
                - prices: Combined list of all prices

        Raises:
            requests.RequestException: If any API request fails
            Exception: If rate limit exceeded

        Example:
            >>> iterator = APIPageIterator(url, headers, params)
            >>> result = iterator.collect_all()
            >>> print(f"Retrieved {result['pricesCount']} prices")
        """
        all_prices = []
        total_prices = 0
        first_date = None
        last_date = None

        for page in self:
            # Collect prices from this page
            all_prices.extend(page.prices)
            total_prices += page.prices_count

            # Track date range
            if first_date is None:
                first_date = page.data.get("firstDate")
            last_date = page.data.get("lastDate")

        return {
            "firstDate": first_date,
            "lastDate": last_date,
            "totalPages": self.page_count,
            "pricesCount": len(all_prices),
            "totalPricesReported": total_prices,
            "prices": all_prices,
        }
