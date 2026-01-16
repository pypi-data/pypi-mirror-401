"""
Sources module for retrieving Lukka API sources reference data.

This module provides functionality to retrieve pricing sources information
from the Lukka API using distributed token caching.
"""

import json
import requests
import logging
import time
import os
import platform
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, date

# Relative imports within package
from . import distributed_lukka_api as dla
from .write import WriteData
from .validators import DateNormalizer

# Configure logging - default to WARNING to avoid cluttering output
# Users can set LUKKA_LOG_LEVEL environment variable to change this
log_level = os.environ.get("LUKKA_LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
logger = logging.getLogger(__name__)


class LukkaSources:
    """
    Client for retrieving Lukka API sources reference data.

    This class provides methods to fetch pricing sources information
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
        Initialize the Lukka Sources client.

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
            >>> sources = LukkaSources(username="your_user", password="your_pass")

            # Environment variables for credentials
            >>> import os
            >>> os.environ['LUKKA_USERNAME'] = 'user123'
            >>> os.environ['LUKKA_PASSWORD'] = 'pass456'
            >>> sources = LukkaSources()

            # Mix explicit credentials with custom cache path
            >>> sources = LukkaSources(
            ...     username="user123",
            ...     password="pass456",
            ...     cache_path="S:/shared/cache/token.json"
            ... )

            # Use .env file (backward compatible)
            >>> sources = LukkaSources()  # Reads credentials from .env

            # Use Redis for distributed caching
            >>> sources = LukkaSources(
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
        self.date_normalizer = DateNormalizer()

    def get_sources(
        self,
        pair_codes: Optional[List[str]] = None,
        source_names: Optional[List[str]] = None,
        start_date: Union[str, datetime, date, None] = None,
        end_date: Union[str, datetime, date, None] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve pricing sources reference data.

        Args:
            pair_codes: List of trading pair codes (e.g., ['BTC-USD', 'ETH-USD'])
            source_names: List of specific source names to filter by
            start_date: Start date (optional). Accepts:
                - datetime object: datetime(2024, 1, 1)
                - date object: date(2024, 1, 1)
                - Simple string: "2024-01-01"
                - ISO 8601 string: "2024-01-01T00:00:00Z"
            end_date: End date (optional). Accepts same formats as start_date

        Returns:
            Dictionary containing sources data from the API response

        Raises:
            requests.RequestException: If the API request fails
        """
        machine_hostname = None  # Will use default machine_id

        try:
            # Register machine as active user
            token = self.api_client.get_api_key(hostname=machine_hostname, in_use=True)

            # Check rate limit before making API call
            if (
                hasattr(self.api_client, "_check_rate_limit")
                and not self.api_client._check_rate_limit()
            ):
                # Wait briefly and retry once
                import time

                time.sleep(0.2)
                if not self.api_client._check_rate_limit():
                    raise Exception("Rate limit exceeded: too many concurrent requests")

            # Prepare headers with proper format (dictionary, not string)
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Normalize dates if provided
            start_date_normalized = self.date_normalizer.normalize_to_simple_date(
                start_date, "start_date"
            )
            end_date_normalized = self.date_normalizer.normalize_to_simple_date(
                end_date, "end_date"
            )

            # Prepare payload/parameters
            params = {}
            if pair_codes:
                params["pairCodes"] = ",".join(pair_codes)
            if source_names:
                params["sourceNames"] = ",".join(source_names)
            if start_date_normalized:
                params["startDate"] = start_date_normalized
            if end_date_normalized:
                params["endDate"] = end_date_normalized

            # Make API request
            url = f"{self.base_url}/sources"
            logger.info(f"Requesting sources data from: {url}")
            logger.debug(f"Parameters: {params}")

            response = self.api_client.session.get(url, headers=headers, params=params, timeout=30)

            response.raise_for_status()

            # Unregister machine immediately after successful API call
            try:
                self.api_client.get_api_key(hostname=machine_hostname, in_use=False)
            except Exception as e:
                logger.warning(f"Failed to unregister machine: {e}")

            data = response.json()

            # Handle the actual API response format (list of sources, not dict with 'sources' key)
            if isinstance(data, list):
                logger.info(f"Successfully retrieved sources data: {len(data)} sources")
                # Return in consistent format for easier handling
                return {"sources": data, "total_count": len(data)}
            else:
                # Handle case where API returns dict format
                sources_count = len(data.get("sources", [])) if isinstance(data, dict) else 0
                logger.info(f"Successfully retrieved sources data: {sources_count} sources")
                return data

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving sources: {e}")
            raise
        finally:
            # Backup unregister in case of early exceptions
            try:
                self.api_client.get_api_key(hostname=machine_hostname, in_use=False)
            except Exception as cleanup_error:
                logger.debug(f"Cleanup unregister failed (non-critical): {cleanup_error}")
                # Ignore errors since this is backup cleanup

    def _validate_location_path(self, location: str) -> str:
        """
        Validate and normalize cross-platform directory path.

        Args:
            location: Directory path to validate

        Returns:
            str: Validated and normalized path

        Raises:
            ValueError: If path format is invalid
            OSError: If path is inaccessible
        """
        # First check for obviously invalid paths
        if not location or location.isspace():
            raise ValueError("Location cannot be empty or whitespace")

        # Validate path format based on platform
        system = platform.system().lower()

        if system == "windows":
            # Windows path validation - must start with drive letter or UNC path
            if not (re.match(r"^[A-Za-z]:[\\|/]", location) or location.startswith("\\\\")):
                raise ValueError(
                    f"Invalid Windows path format: {location}. Expected format like 'C:\\Data\\' or 'S:\\Data\\'"
                )
        elif system in ["linux", "darwin"]:
            # Unix-like path validation - must be absolute path starting with /
            if not location.startswith("/"):
                raise ValueError(
                    f"Invalid Unix path format: {location}. Expected absolute path like '/home/user/data/'"
                )

        # Now normalize the path for cross-platform compatibility
        try:
            normalized_path = Path(location).resolve()
        except Exception as e:
            raise ValueError(f"Cannot resolve path {location}: {e}")

        # Check if the directory exists, create if it doesn't
        try:
            normalized_path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise OSError(f"Permission denied: Cannot access or create directory {normalized_path}")
        except Exception as e:
            raise OSError(f"Invalid or inaccessible path {normalized_path}: {e}")

        # Verify the path is writable
        if not os.access(normalized_path, os.W_OK):
            raise OSError(f"Directory is not writable: {normalized_path}")

        return str(normalized_path)

    def get_source_details(
        self,
        source_id: int,
        file_format: Optional[str] = None,
        file_name: Optional[str] = None,
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve detailed information for a specific source by ID.

        This method retrieves comprehensive details about a particular source,
        including supported currency pairs and other source-specific information.
        Optionally saves the data to a local file.

        Args:
            source_id: The source ID to retrieve details for (e.g., 3000)
            file_format: Optional file format ('csv', 'json', 'parquet').
                        Requires location to be specified.
            file_name: Optional filename for saving (e.g., "source_data").
                      Requires location to be specified.
            location: Optional directory path for saving file (e.g., "C:\\Data\\" or "/tmp/data/").
                     When specified, automatically saves data to file.

        Returns:
            Dictionary containing detailed information for the specified source

        Raises:
            requests.RequestException: If the API request fails
            ValueError: If file parameters are invalid or incomplete
            TypeError: If parameter types are incorrect
            OSError: If the location path is invalid or inaccessible

        Examples:
            >>> sources = LukkaSources()
            >>>
            >>> # Get source details (returns data only)
            >>> details = sources.get_source_details(source_id=1000)
            >>>
            >>> # Get and save to file
            >>> details = sources.get_source_details(
            ...     source_id=1000,
            ...     location="C:/Data/",
            ...     file_name="source_1000",
            ...     file_format="csv"
            ... )
        """
        machine_hostname = None  # Will use default machine_id

        try:
            # Register machine as active user
            token = self.api_client.get_api_key(hostname=machine_hostname, in_use=True)

            # Check rate limit before making API call
            if (
                hasattr(self.api_client, "_check_rate_limit")
                and not self.api_client._check_rate_limit()
            ):
                # Wait briefly and retry once
                import time

                time.sleep(0.2)
                if not self.api_client._check_rate_limit():
                    raise Exception("Rate limit exceeded: too many concurrent requests")

            # Prepare headers
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Make API request to specific source endpoint
            url = f"{self.base_url}/sources/{source_id}"
            logger.info(f"Requesting source details from: {url}")

            response = self.api_client.session.get(url, headers=headers, timeout=30)

            response.raise_for_status()

            # Unregister machine immediately after successful API call
            try:
                # time.sleep(5)
                self.api_client.get_api_key(hostname=machine_hostname, in_use=False)
            except Exception as e:
                logger.warning(f"Failed to unregister machine: {e}")

            data = response.json()
            logger.info(f"Successfully retrieved source details for ID {source_id}")

            # If location is specified, save to file
            if location is not None:
                # Validate file parameters
                if file_format is None:
                    raise ValueError(
                        "file_format is required when location is specified. "
                        "Supported formats: 'csv', 'json', 'parquet'"
                    )
                if not isinstance(file_format, str) or file_format.lower() not in [
                    "csv",
                    "json",
                    "parquet",
                ]:
                    raise ValueError(
                        f"file_format must be one of ['csv', 'json', 'parquet'], got: {file_format}"
                    )

                if file_name is None:
                    raise ValueError(
                        "file_name is required when location is specified. "
                        "Please provide a file name (e.g., 'source_data')"
                    )
                if not isinstance(file_name, str) or not file_name.strip():
                    raise TypeError(
                        f"file_name must be a non-empty string, got {type(file_name).__name__}: {file_name}"
                    )

                if not isinstance(location, str) or not location.strip():
                    raise TypeError(
                        f"location must be a non-empty string, got {type(location).__name__}: {location}"
                    )

                # Validate and normalize the location path
                validated_location = self._validate_location_path(location)

                # Convert to pandas DataFrame and save
                logger.info("Converting data to pandas DataFrame")
                df_data = WriteData().convert_to_pandas(data)

                logger.info(f"Writing data to {validated_location}/{file_name}.{file_format}")
                WriteData().write_locally(
                    df_data,
                    file_name=file_name,
                    file_format=file_format,
                    location=validated_location,
                )

                logger.info(
                    f"✅ Source details saved to {validated_location}/{file_name}.{file_format}"
                )

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for source ID {source_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving source {source_id}: {e}")
            raise
        finally:
            # Backup unregister in case of early exceptions
            try:
                self.api_client.get_api_key(hostname=machine_hostname, in_use=False)
            except Exception as cleanup_error:
                logger.debug(f"Cleanup unregister failed (non-critical): {cleanup_error}")
                # Ignore errors since this is backup cleanup

    def close(self):
        """Close the API client and clean up resources."""
        if hasattr(self.api_client, "close"):
            self.api_client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def main():
    """
    Example usage of the LukkaSources class.
    """
    print("🔍 Lukka Sources API Client Example")
    print("=" * 50)

    try:
        # Initialize sources client with distributed caching
        with LukkaSources() as sources_client:

            # Example 1: Get all sources
            print("\n📊 Retrieving all sources...")
            all_sources = sources_client.get_sources()

            if "sources" in all_sources:
                print(f"✅ Found {len(all_sources['sources'])} total sources")

                # Show first few sources
                for i, source in enumerate(all_sources["sources"][:3]):
                    source_name = source.get("sourceName", "Unknown")
                    pairs_count = len(source.get("supportedPairs", []))
                    print(f"  {i+1}. {source_name}: {pairs_count} pairs supported")

            # Example 2: Get sources for specific trading pair
            print("\n🎯 Retrieving sources for BTC-USD...")
            btc_sources = sources_client.get_sources(pair_codes=["BTC-USD"])

            if "sources" in btc_sources:
                print(f"✅ Found {len(btc_sources['sources'])} sources for BTC-USD")

            # Example 3: Get detailed information for a specific source
            print("\n🔍 Retrieving detailed information for source ID 3000...")
            try:
                source_details = sources_client.get_source_details(3000)
                if source_details:
                    source_name = source_details.get("sourceName", "Unknown")
                    status = source_details.get("status", "Unknown")
                    print(f"✅ Source Details: {source_name} - Status: {status}")

                    # Show supported pairs if available
                    if "supportedPairs" in source_details:
                        pairs_count = len(source_details["supportedPairs"])
                        print(f"   Supported pairs: {pairs_count}")
                        if pairs_count > 0:
                            # Show first few pairs
                            for pair in source_details["supportedPairs"][:3]:
                                print(f"     - {pair}")
                            if pairs_count > 3:
                                print(f"     ... and {pairs_count - 3} more")
            except Exception as e:
                print(f"⚠️  Could not retrieve details for source 3000: {e}")

            # Example 4: Get sources with date filter
            print("\n📅 Retrieving recent sources...")
            recent_sources = sources_client.get_sources(
                start_date="2024-01-01", end_date="2024-12-31"
            )

            if "sources" in recent_sources:
                print(f"✅ Found {len(recent_sources['sources'])} sources for 2024")

            print("\n🎉 Sources retrieval completed successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Simple example - get all sources
    print(LukkaSources().get_sources())
