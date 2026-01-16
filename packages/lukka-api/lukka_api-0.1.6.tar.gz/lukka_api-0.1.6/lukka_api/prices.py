"""
Prices module for retrieving Lukka API pricing data.

This module provides functionality to retrieve both latest and historical
pricing data from the Lukka API using distributed token caching.
"""

import json
import requests
import logging
import time
import socket
import os
import platform
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, date, timedelta

# Relative imports within package
from . import distributed_lukka_api as dla
from .write import WriteData
from .validators import PriceRequestValidator
from .pagination import APIPageIterator
from .decorators import log_performance

# Configure logging - default to WARNING to avoid cluttering output
# Users can set LUKKA_LOG_LEVEL environment variable to change this
log_level = os.environ.get("LUKKA_LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
logger = logging.getLogger(__name__)


class LukkaPrices:
    """
    Client for retrieving Lukka API pricing data.

    This class provides methods to fetch both latest and historical pricing data
    using the distributed token caching system with automatic platform-specific
    cache directory selection.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        cache_path: Optional[str] = None,
        use_redis: bool = False,
        **redis_kwargs,
    ):
        """
        Initialize the Lukka Prices client.

        Args:
            username: Lukka API username. If None, uses environment variable or .env file.
                     Priority: explicit parameter > LUKKA_USERNAME env var > .env file
            password: Lukka API password. If None, uses environment variable or .env file.
                     Priority: explicit parameter > LUKKA_PASSWORD env var > .env file
            cache_path: Custom cache file path. If None, uses platform-specific default.
                       Priority: explicit parameter > LUKKA_CACHE_PATH env var > platform default

                       Platform defaults:
                       - Windows: %LOCALAPPDATA%\\lukka-api\\cache\\lukka_token.json
                       - Linux: ~/.local/share/lukka-api/cache/lukka_token.json
                       - macOS: ~/Library/Application Support/lukka-api/cache/lukka_token.json

            use_redis: Whether to use Redis-based caching (default: False)
            **redis_kwargs: Redis connection parameters (host, port, db, password)

        Examples:
            # Explicit credentials (recommended for production)
            >>> prices = LukkaPrices(username="your_user", password="your_pass")

            # Environment variables for credentials
            >>> import os
            >>> os.environ['LUKKA_USERNAME'] = 'user123'
            >>> os.environ['LUKKA_PASSWORD'] = 'pass456'
            >>> prices = LukkaPrices()

            # Mix explicit credentials with custom cache path
            >>> prices = LukkaPrices(
            ...     username="user123",
            ...     password="pass456",
            ...     cache_path="S:/shared/cache/token.json"
            ... )

            # Use .env file (backward compatible)
            >>> prices = LukkaPrices()  # Reads credentials from .env

            # Use Redis for distributed caching
            >>> prices = LukkaPrices(
            ...     username="user123",
            ...     password="pass456",
            ...     use_redis=True,
            ...     redis_host='localhost',
            ...     redis_port=6379
            ... )
        """
        if use_redis:
            self.api_client = dla.RedisDistributedLukkaAPIClient(
                username=username, password=password, **redis_kwargs
            )
        else:
            self.api_client = dla.DistributedLukkaAPIClient(
                username=username, password=password, cache_path=cache_path
            )

        self.base_url = "https://data-pricing-api.lukka.tech/v1/pricing"
        self.validator = PriceRequestValidator()

    @log_performance
    def get_historical_price(
        self,
        pair_codes: str,
        from_date: Optional[Union[str, datetime, date]] = None,
        to_date: Optional[Union[str, datetime, date]] = None,
        source_id: int = 1000,
        location: Optional[str] = None,
        fill: bool = False,
        interval: int = 86400000,
        file_name: str = None,
        file_format: str = None,
        max_pages: int = 100,
    ) -> Optional[Dict[str, Any]]:
        """
        Get historical price data using pagination to retrieve complete dataset.

        This method automatically handles pagination to retrieve all available data
        between the specified dates, not just the first 1440 records.

        Args:
            pair_codes: Pair code (e.g., "XBT-USD", required)
            from_date: Start date (optional). Accepts multiple formats:
                - datetime object: datetime(2024, 1, 1)
                - date object: date(2024, 1, 1)
                - ISO 8601 string: "2024-01-01T00:00:00Z"
                - Simple date string: "2024-01-01" (assumes UTC midnight)
                - None: Defaults to 30 days ago (safer than API default of 1970-01-01)
            to_date: End date (optional). Accepts same formats as from_date:
                - None: Defaults to current time
            source_id: Source ID (integer, default: 1000)
            location: Optional directory path to save data. If None, prints to terminal
            fill: Forward fill gaps in prices with last known price (default: False)
            interval: Frequency in milliseconds (default: 86400000). Valid values:
                - 86400000 (daily data)
                - 60000 (minute-level data)
            file_name: Name of file to save (optional, defaults to "historical_price_yyyy-mm-dd" if location is provided)
            file_format: Format to save ('json', 'csv', 'parquet', defaults to 'json' if location is provided)
            max_pages: Maximum number of pages to retrieve (safety limit, default: 100)

        Returns:
            Dict containing complete price history data with all prices combined

        Raises:
            ValueError: If required parameters are missing or invalid, or if file_name/file_format specified without location
            TypeError: If parameters have incorrect types
            requests.RequestException: If API request fails

        Notes:
            API Default Behavior (if you need to override):
            - from_date=None uses 30 days ago (client default for safety)
            - to_date=None uses current time
            - API itself defaults from=1970-01-01T00:00:00Z, to=now

        Examples:
            # Get last 30 days of data (using defaults)
            >>> prices.get_historical_price(pair_codes="BTC-USD")

            # Using datetime objects (recommended)
            >>> from datetime import datetime
            >>> prices.get_historical_price(
            ...     pair_codes="BTC-USD",
            ...     from_date=datetime(2024, 1, 1),
            ...     to_date=datetime(2024, 12, 31),
            ...     source_id=1000
            ... )

            # Using simple date strings
            >>> prices.get_historical_price(
            ...     pair_codes="BTC-USD",
            ...     from_date="2024-01-01",
            ...     to_date="2024-12-31",
            ...     source_id=1000
            ... )

            # Using ISO 8601 strings (backward compatible)
            >>> prices.get_historical_price(
            ...     pair_codes="BTC-USD",
            ...     from_date="2024-01-01T00:00:00Z",
            ...     to_date="2024-12-31T23:59:59Z",
            ...     source_id=1000
            ... )

            # Save to file with custom format
            >>> prices.get_historical_price(
            ...     pair_codes="BTC-USD",
            ...     from_date="2024-01-01",
            ...     to_date="2024-12-31",
            ...     source_id=1000,
            ...     location="C:/data",
            ...     file_name="btc_history_2024",
            ...     file_format="csv"
            ... )

            # Get data from specific start date to now
            >>> prices.get_historical_price(
            ...     pair_codes="BTC-USD",
            ...     from_date="2024-01-01"
            ... )
        """
        # ============================================================================
        # INPUT VALIDATION - Using PriceRequestValidator for comprehensive validation
        # ============================================================================

        # Apply sensible defaults for optional date parameters
        # Note: API defaults are from=1970-01-01T00:00:00Z, to=now
        # We use safer defaults to prevent accidental large data retrievals
        if from_date is None:
            from_date = datetime.now() - timedelta(days=30)
            logger.info("from_date not specified, defaulting to 30 days ago")

        if to_date is None:
            to_date = datetime.now()
            logger.info("to_date not specified, defaulting to current time")

        # Validate all parameters and get normalized request object
        request = self.validator.validate(
            pair_codes=pair_codes,
            from_date=from_date,
            to_date=to_date,
            source_id=source_id,
            interval=interval,
            fill=fill,
            location=location,
            file_name=file_name,
            file_format=file_format,
        )

        # Validate max_pages separately (not part of standard price request)
        if not isinstance(max_pages, int) or max_pages <= 0:
            raise ValueError(f"max_pages must be a positive integer, got: {max_pages}")

        # ============================================================================
        # END OF VALIDATION - All inputs are valid, proceed with operations
        # ============================================================================

        # Set defaults when location is provided (same as get_latest_price)
        if request.location is not None:
            if request.file_name is None:
                # Generate default filename with current date
                current_date = datetime.now().strftime("%Y-%m-%d")
                request.file_name = f"historical_price_{current_date}"

            if request.file_format is None:
                # Default to json format (matches API response format)
                request.file_format = "json"

        machine_hostname = socket.gethostname()

        try:
            # Prepare API request parameters
            url = f"{self.base_url}/sources/{request.source_id}/prices/pairs/{request.pair_codes}"
            params = {
                "from": request.from_date,  # Already normalized to ISO 8601
                "to": request.to_date,  # Already normalized to ISO 8601
                "fill": str(request.fill).lower(),
                "limit": 1440,  # Use maximum limit for efficiency
                "interval": request.interval,
            }

            # Get API token and register machine as active
            token = self.api_client.get_api_key(hostname=machine_hostname, in_use=True)

            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "User-Agent": f"LukkaPrices/1.0 ({machine_hostname})",
            }

            logger.info(
                f"Starting paginated retrieval: {request.pair_codes} from {request.source_id} "
                f"({request.from_date} to {request.to_date})"
            )

            # Use APIPageIterator to handle pagination
            iterator = APIPageIterator(
                url=url,
                headers=headers,
                params=params,
                max_pages=max_pages,
                max_retries=3,
                retry_delay=0.5,
                page_delay=0.1,
                timeout=30,
            )

            # Collect all pages
            pagination_result = iterator.collect_all()

            # Unregister machine when done
            self.api_client.get_api_key(hostname=machine_hostname, in_use=False)

            # Create combined result from pagination
            combined_result = {
                "pairCode": request.pair_codes,
                "sourceId": request.source_id,
                "firstDate": pagination_result["firstDate"],
                "lastDate": pagination_result["lastDate"],
                "totalPages": pagination_result["totalPages"],
                "pricesCount": pagination_result["pricesCount"],
                "totalPricesReported": pagination_result["totalPricesReported"],
                "prices": pagination_result["prices"],
            }
            # print(combined_result)
            # Handle location parameter
            if request.location:
                try:
                    # Create WriteData instance
                    writer = WriteData()

                    # Convert to pandas DataFrame (if format is not json, otherwise keep raw)
                    if request.file_format.lower() in ["csv", "parquet"]:
                        df = writer.convert_to_pandas(combined_result)
                        # Save locally using WriteData
                        saved_path = writer.write_locally(
                            df=df,
                            file_name=request.file_name,
                            file_format=request.file_format,
                            location=request.location,
                        )
                    else:  # json format - save raw API response
                        # Ensure directory exists
                        save_dir = Path(request.location)
                        save_dir.mkdir(parents=True, exist_ok=True)

                        # Create full file path
                        file_path = save_dir / f"{request.file_name}.json"

                        # Write JSON data
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(combined_result, f, indent=2)

                        saved_path = str(file_path)

                    logger.info(f"📁 Complete dataset saved to: {saved_path}")
                except Exception as e:
                    logger.error(f"Failed to save data: {e}")
                    raise
            else:
                # Print summary to terminal
                print(
                    f"\n🎯 Historical Prices for {request.pair_codes} (Source {request.source_id})"
                )
                print(
                    f"📅 Period: {pagination_result['firstDate']} to {pagination_result['lastDate']}"
                )

                # Display interval information
                interval_display = {
                    86400000: "Daily (86400000 ms)",
                    60000: "Minute-level (60000 ms)",
                }.get(request.interval, f"{request.interval} ms")
                print(f"⏱️ Interval: {interval_display}")

                print(f"📄 Pages Retrieved: {pagination_result['totalPages']}")
                print(f"📊 Total Prices: {pagination_result['pricesCount']:,}")

                if pagination_result["prices"]:
                    print(f"\n📈 Sample Data (first 5 and last 5):")
                    print(f"{'Timestamp':<25} {'Price':>15}")
                    print(f"{'-' * 25} {'-' * 15}")

                    # Show first 5
                    for i, price_point in enumerate(pagination_result["prices"][:5]):
                        ts = price_point.get("ts", "N/A")
                        price = price_point.get("price", "N/A")
                        print(f"{ts:<25} ${price:>14}")

                    if len(pagination_result["prices"]) > 10:
                        print(f"{'...':<25} {'...':>15}")
                        # Show last 5
                        for price_point in pagination_result["prices"][-5:]:
                            ts = price_point.get("ts", "N/A")
                            price = price_point.get("price", "N/A")
                            print(f"{ts:<25} ${price:>14}")

            logger.info(
                f"🎉 Complete dataset retrieved: {pagination_result['pricesCount']:,} prices "
                f"across {pagination_result['totalPages']} pages"
            )

            # Only return data if not already displayed to terminal
            # When location is None, we've printed sample data, so don't return the full JSON
            if request.location is None:
                return None
            else:
                return combined_result

        except Exception as e:
            logger.error(f"Paginated retrieval failed: {e}")
            # Unregister machine on error
            try:
                self.api_client.get_api_key(hostname=machine_hostname, in_use=False)
            except Exception as cleanup_error:
                logger.debug(f"Cleanup unregister failed (non-critical): {cleanup_error}")
            raise

    @log_performance
    def get_latest_price(
        self,
        source_id: int = 2000,
        pair_codes: Union[str, List[str]] = None,
        lookback: int = 3600000,  # Default to 1 hour in milliseconds
        location: Optional[str] = None,
        file_name: Optional[str] = None,
        file_format: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get latest price data for one or more pairs from a specific source.

        Args:
            source_id: Source ID (integer, default: 2000)
            pair_codes: Single pair code string or list of pair codes. If None, API defaults to all pairs
            lookback: Latest price to retrieve in specified window milliseconds (default: 3600000 = 1 hour)
            location: Optional directory path to save data. If None, prints to terminal
            file_name: Name of file to save (optional, defaults to "latest_price_yyyy-mm-dd" if location is provided)
            file_format: Format to save ('json', 'csv', 'parquet', defaults to 'json' if location is provided)

        Returns:
            Dict containing latest price data if location is specified, None otherwise.
            When location is None, data is printed to terminal and None is returned.

        Raises:
            ValueError: If file_name or file_format specified without location
            requests.RequestException: If API request fails

        Examples:
            # Print to terminal
            >>> prices.get_latest_price(source_id=1000, pair_codes="BTC-USD")

            # Save to file with defaults (json format, auto-generated filename)
            >>> prices.get_latest_price(source_id=1000, pair_codes="BTC-USD", location="C:/data")

            # Save with custom filename and format
            >>> prices.get_latest_price(
            ...     source_id=1000,
            ...     pair_codes="BTC-USD",
            ...     location="C:/data",
            ...     file_name="btc_latest",
            ...     file_format="csv"
            ... )
        """
        # ============================================================================
        # INPUT VALIDATION - All validations happen FIRST before any operations
        # This ensures users get immediate feedback on invalid inputs
        # ============================================================================

        # 1. Validate source_id
        if not isinstance(source_id, int):
            raise TypeError(
                f"source_id must be an integer, got {type(source_id).__name__}: {source_id}"
            )

        # 2. Validate pair_codes
        if pair_codes is not None:
            if isinstance(pair_codes, str):
                if not pair_codes.strip():
                    raise ValueError("pair_codes cannot be an empty string")
            elif isinstance(pair_codes, list):
                if len(pair_codes) == 0:
                    raise ValueError("pair_codes list cannot be empty")
                for pair in pair_codes:
                    if not isinstance(pair, str) or not pair.strip():
                        raise ValueError(
                            f"All pair_codes elements must be non-empty strings, got: {pair}"
                        )
            else:
                raise TypeError(
                    f"pair_codes must be a string, list of strings, or None, got {type(pair_codes).__name__}"
                )

        # 3. Validate lookback
        if not isinstance(lookback, int):
            raise TypeError(
                f"lookback must be an integer, got {type(lookback).__name__}: {lookback}"
            )

        if lookback <= 0:
            raise ValueError(f"lookback must be a positive integer, got: {lookback}")

        # 4. Validate file parameter combinations
        if file_name is not None and location is None:
            raise ValueError(
                "Parameter 'file_name' requires 'location' to be specified. "
                "Please provide a directory path for the 'location' parameter."
            )

        if file_format is not None and location is None:
            raise ValueError(
                "Parameter 'file_format' requires 'location' to be specified. "
                "Please provide a directory path for the 'location' parameter."
            )

        # 5. Validate file_format value
        if file_format is not None:
            allowed_formats = ["json", "csv", "parquet"]
            if not isinstance(file_format, str) or file_format.lower() not in allowed_formats:
                raise ValueError(
                    f"Invalid file_format: '{file_format}'. " f"Allowed formats: {allowed_formats}"
                )

        # 6. Validate location and file_name types
        if location is not None:
            if not isinstance(location, str) or not location.strip():
                raise ValueError(
                    f"location must be a non-empty string, got {type(location).__name__}: {location}"
                )

            if file_name is not None and (not isinstance(file_name, str) or not file_name.strip()):
                raise ValueError(
                    f"file_name must be a non-empty string, got {type(file_name).__name__}: {file_name}"
                )

        # ============================================================================
        # END OF VALIDATION - All inputs are valid, proceed with operations
        # ============================================================================

        # Set defaults when location is provided
        if location is not None:
            if file_name is None:
                # Generate default filename with current date
                current_date = datetime.now().strftime("%Y-%m-%d")
                file_name = f"latest_price_{current_date}"

            if file_format is None:
                # Default to json format (matches API response format)
                file_format = "json"

        machine_hostname = socket.gethostname()
        retry_count = 0
        max_retries = 3

        # Convert single pair_codes to list for consistent processing
        if isinstance(pair_codes, str):
            pair_codes_list = [pair_codes]
        elif pair_codes is None:
            pair_codes_list = None  # Allow API to default to all pairs
        else:
            pair_codes_list = pair_codes

        while retry_count < max_retries:
            try:
                # Get API token and register machine as active
                token = self.api_client.get_api_key(hostname=machine_hostname, in_use=True)

                # Construct URL for latest prices
                # Note: This is a placeholder URL - adjust based on actual API endpoint
                url = f"{self.base_url}/sources/{source_id}/prices"

                # Prepare parameters
                params = {"lookback": lookback}

                # Only add pairCodes parameter if pair_codes_list is not None
                if pair_codes_list is not None:
                    params["pairCodes"] = ",".join(pair_codes_list)

                # Prepare headers
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                    "User-Agent": f"LukkaPrices/1.0 ({machine_hostname})",
                }

                pair_display = (
                    ",".join(pair_codes_list) if pair_codes_list is not None else "all pairs"
                )
                logger.info(
                    f"Requesting latest prices: {pair_display} from source {source_id} (lookback: {lookback})"
                )

                # Make API request
                response = requests.get(url, headers=headers, params=params, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"✅ Latest prices retrieved successfully")

                    # Handle location parameter
                    if location:
                        try:
                            # Create WriteData instance
                            writer = WriteData()

                            # Convert to pandas DataFrame (if format is not json, otherwise keep raw)
                            if file_format.lower() in ["csv", "parquet"]:
                                df = writer.convert_to_pandas(data)
                                # Save locally using WriteData
                                saved_path = writer.write_locally(
                                    df=df,
                                    file_name=file_name,
                                    file_format=file_format,
                                    location=location,
                                )
                            else:  # json format - save raw API response
                                # Ensure directory exists
                                save_dir = Path(location)
                                save_dir.mkdir(parents=True, exist_ok=True)

                                # Create full file path
                                file_path = save_dir / f"{file_name}.json"

                                # Write JSON data
                                with open(file_path, "w", encoding="utf-8") as f:
                                    json.dump(data, f, indent=2)

                                saved_path = str(file_path)

                            logger.info(f"📁 Data saved to: {saved_path}")
                        except Exception as e:
                            logger.error(f"Failed to save data: {e}")
                            raise
                    else:
                        # Print to terminal
                        print(f"\n🎯 Latest Prices (Source {source_id})")
                        print(f"📊 Pairs: {pair_display}")

                        # Display lookback information
                        lookback_hours = lookback / 3600000  # Convert ms to hours
                        if lookback_hours >= 24:
                            lookback_display = f"{lookback_hours / 24:.1f} day(s) ({lookback} ms)"
                        else:
                            lookback_display = f"{lookback_hours:.1f} hour(s) ({lookback} ms)"
                        print(f"🔍 Lookback: {lookback_display}")

                        # Show structure of returned data
                        if isinstance(data, list):
                            print(f"📈 Number of records: {len(data)}")

                            if data:  # Only show table if there's data
                                print(f"\n{'Pair Code':<15} {'Timestamp':<25} {'Price':>15}")
                                print(f"{'-' * 15} {'-' * 25} {'-' * 15}")

                                for i, record in enumerate(data[:5]):  # Show first 5
                                    if isinstance(record, dict):
                                        pair = record.get("pairCode", f"Record {i+1}")
                                        timestamp = record.get("ts", "N/A")
                                        price = record.get("price", "N/A")
                                        print(f"{pair:<15} {timestamp:<25} ${price:>14}")
                        elif isinstance(data, dict):
                            print(f"🔍 Response keys: {list(data.keys())}")

                    # Unregister machine when done
                    self.api_client.get_api_key(hostname=machine_hostname, in_use=False)

                    # Only return data if saved to file, otherwise return None
                    # This prevents data from being printed to console when displayed
                    if location is None:
                        return None
                    else:
                        return data

                elif response.status_code == 429:
                    retry_count += 1
                    logger.warning(f"Rate limit hit. Retry {retry_count}/{max_retries}")
                    if retry_count < max_retries:
                        time.sleep(0.2)
                    else:
                        raise Exception("Rate limit exceeded: too many concurrent requests")
                else:
                    response.raise_for_status()

            except requests.RequestException as e:
                logger.error(f"API request failed: {e}")
                # Unregister machine on error
                try:
                    self.api_client.get_api_key(hostname=machine_hostname, in_use=False)
                except Exception as cleanup_error:
                    logger.debug(f"Cleanup unregister failed (non-critical): {cleanup_error}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                # Unregister machine on error
                try:
                    self.api_client.get_api_key(hostname=machine_hostname, in_use=False)
                except Exception as cleanup_error:
                    logger.debug(f"Cleanup unregister failed (non-critical): {cleanup_error}")
                raise


def main():
    """
    Example usage: Retrieve historical prices for BTC-USD.
    """
    source = 1000
    pair = "XBT-USD"
    sDate = "2025-10-27T00:00:00Z"
    eDate = "2025-10-31T00:00:00Z"
    location = "C:/temp"

    historical_data = LukkaPrices().get_historical_price(
        source_id=source, pair_codes=pair, from_date=sDate, to_date=eDate, location=location
    )


if __name__ == "__main__":
    main()
