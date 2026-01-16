"""
Write module for saving Lukka API data locally.

This module provides functionality to convert API response data to pandas DataFrames
and save them locally in various formats with cross-platform path compatibility.
"""

import pandas as pd
import os
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path
import json
import pyarrow  # Ensure PyArrow is installed for Parquet support

# Configure logging - default to WARNING to avoid cluttering output
# Users can set LUKKA_LOG_LEVEL environment variable to change this
log_level = os.environ.get("LUKKA_LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
logger = logging.getLogger(__name__)


class WriteData:
    """
    Data writer class for converting and saving Lukka API data locally.

    This class provides methods to convert API response data to pandas DataFrames
    and save them in various formats with cross-platform path compatibility.
    """

    def __init__(self, base_location: Optional[str] = None):
        """
        Initialize the WriteData class.

        Args:
            base_location: Base directory for saving files. If None, no default location is set.
                          You must specify location parameter when calling write_locally().
        """
        self.base_location = base_location

        # Only create directory if base_location is explicitly provided
        if self.base_location is not None:
            self._ensure_directory_exists(self.base_location)
            logger.info(f"WriteData initialized with base location: {self.base_location}")
        else:
            logger.info("WriteData initialized with no default base location")

    def convert_sources_to_pandas(self, source_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Convert source details data from get_source_details() to pandas DataFrame.

        Args:
            source_data: Dictionary containing source details from Lukka API

        Returns:
            pandas.DataFrame: Converted data ready for saving

        Raises:
            ValueError: If source_data is invalid or cannot be converted
        """
        try:
            # Handle different response formats
            if isinstance(source_data, dict):
                # Check if it's a single source detail response
                if "sourceId" in source_data or "sourceName" in source_data:
                    # Single source - convert to list for consistent processing
                    sources_list = [source_data]
                elif "sources" in source_data:
                    # Multiple sources in 'sources' key
                    sources_list = source_data["sources"]
                else:
                    # Assume the dict itself contains the source data
                    sources_list = [source_data]
            elif isinstance(source_data, list):
                # Already a list of sources
                sources_list = source_data
            else:
                raise ValueError(f"Unsupported source_data type: {type(source_data)}")

            if not sources_list:
                logger.warning("No source data to convert")
                return pd.DataFrame()

            # Flatten nested data for DataFrame creation
            flattened_data = []

            for source in sources_list:
                if not isinstance(source, dict):
                    logger.warning(f"Skipping invalid source data: {source}")
                    continue

                # Base source information
                base_record = {
                    "sourceId": source.get("sourceId"),
                    "sourceName": source.get("sourceName"),
                    "status": source.get("status"),
                    "sourceType": source.get("sourceType"),
                    "description": source.get("description"),
                    "website": source.get("website"),
                    "apiDocumentation": source.get("apiDocumentation"),
                    "createdAt": source.get("createdAt"),
                    "updatedAt": source.get("updatedAt"),
                }

                # Handle pairs - flatten if exists (API returns 'pairs', not 'supportedPairs')
                pairs = source.get("pairs", source.get("supportedPairs", []))
                if pairs:
                    # Create a record for each pair
                    for pair in pairs:
                        record = base_record.copy()

                        # Handle different pair formats
                        if isinstance(pair, dict):
                            # Complex pair object with detailed information
                            record["pairCode"] = pair.get("pairCode")
                            record["firstDate"] = pair.get("firstDate")
                            record["lastDate"] = pair.get("lastDate")
                            record["baseAsset"] = pair.get("baseAsset")
                            record["counterAsset"] = pair.get("counterAsset")
                            record["baseAssetLukkaId"] = pair.get("baseAssetLukkaId")
                            record["counterAssetLukkaId"] = pair.get("counterAssetLukkaId")
                            record["baseAssetName"] = pair.get("baseAssetName")
                            record["counterAssetName"] = pair.get("counterAssetName")
                            record["baseAssetWhitepaperCode"] = pair.get("baseAssetWhitepaperCode")
                            record["baseAssetCommonStreetCode"] = pair.get(
                                "baseAssetCommonStreetCode"
                            )
                            record["counterAssetCommonStreetCode"] = pair.get(
                                "counterAssetCommonStreetCode"
                            )
                            record["instrumentType"] = pair.get("instrumentType")
                            record["pairStatus"] = pair.get(
                                "status"
                            )  # Renamed to avoid conflict with source status
                        else:
                            # Simple pair string (backward compatibility)
                            record["pairCode"] = pair
                            record["firstDate"] = None
                            record["lastDate"] = None
                            record["baseAsset"] = None
                            record["counterAsset"] = None
                            record["baseAssetLukkaId"] = None
                            record["counterAssetLukkaId"] = None
                            record["baseAssetName"] = None
                            record["counterAssetName"] = None
                            record["baseAssetWhitepaperCode"] = None
                            record["baseAssetCommonStreetCode"] = None
                            record["counterAssetCommonStreetCode"] = None
                            record["instrumentType"] = None
                            record["pairStatus"] = None

                        flattened_data.append(record)
                else:
                    # No pairs, add base record
                    base_record.update(
                        {
                            "pairCode": None,
                            "firstDate": None,
                            "lastDate": None,
                            "baseAsset": None,
                            "counterAsset": None,
                            "baseAssetLukkaId": None,
                            "counterAssetLukkaId": None,
                            "baseAssetName": None,
                            "counterAssetName": None,
                            "baseAssetWhitepaperCode": None,
                            "baseAssetCommonStreetCode": None,
                            "counterAssetCommonStreetCode": None,
                            "instrumentType": None,
                            "pairStatus": None,
                        }
                    )
                    flattened_data.append(base_record)

            # Create DataFrame
            df = pd.DataFrame(flattened_data)

            # Convert timestamp columns to datetime if they exist
            timestamp_columns = ["createdAt", "updatedAt"]
            for col in timestamp_columns:
                if col in df.columns and not df[col].isna().all():
                    try:
                        df[col] = pd.to_datetime(df[col], errors="coerce")
                    except Exception as e:
                        logger.warning(f"Failed to convert {col} to datetime: {e}")

            logger.info(f"Successfully converted {len(flattened_data)} records to DataFrame")
            logger.info(f"DataFrame shape: {df.shape}")
            logger.info(f"DataFrame columns: {list(df.columns)}")

            return df

        except Exception as e:
            logger.error(f"Error converting source data to pandas DataFrame: {e}")
            raise ValueError(f"Failed to convert source data: {e}")

    def convert_prices_to_pandas(self, price_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Convert historical price data from get_historical_data() to pandas DataFrame.

        Extracts just the prices array and converts it to a clean DataFrame with
        timestamp and price columns.

        Args:
            price_data: Dictionary containing historical price data from Lukka API
                       Expected format: {'prices': [{'ts': str, 'price': str}], ...}
                       OR a list of price entries directly: [{'ts': str, 'price': str}]

        Returns:
            pandas.DataFrame: Clean DataFrame with 'ts' and 'price' columns

        Raises:
            ValueError: If price_data is invalid or cannot be converted
        """
        try:
            # Handle different input formats
            if isinstance(price_data, dict) and "prices" in price_data:
                # Full response format with 'prices' key
                prices = price_data["prices"]
            elif isinstance(price_data, list):
                # Direct list of price entries
                prices = price_data
            elif isinstance(price_data, dict) and "ts" in price_data and "price" in price_data:
                # Single price entry
                prices = [price_data]
            else:
                raise ValueError(
                    "Price data must contain 'prices' key with list of price entries, "
                    "or be a list of price entries directly"
                )

            if not prices:
                logger.warning("No price data to convert")
                return pd.DataFrame()

            # Convert prices to DataFrame records
            records = []
            for price_entry in prices:
                if not isinstance(price_entry, dict):
                    logger.warning(f"Skipping invalid price entry: {price_entry}")
                    continue

                if "ts" not in price_entry or "price" not in price_entry:
                    logger.warning(f"Skipping price entry missing 'ts' or 'price': {price_entry}")
                    continue

                record = {"ts": price_entry["ts"], "price": price_entry["price"]}
                records.append(record)

            if not records:
                logger.warning("No valid price records found")
                return pd.DataFrame()

            # Create DataFrame
            df = pd.DataFrame(records)

            # Convert data types
            if "ts" in df.columns:
                try:
                    df["ts"] = pd.to_datetime(df["ts"], errors="coerce")
                except Exception as e:
                    logger.warning(f"Failed to convert ts to datetime: {e}")

            if "price" in df.columns:
                try:
                    df["price"] = pd.to_numeric(df["price"], errors="coerce")
                except Exception as e:
                    logger.warning(f"Failed to convert price to numeric: {e}")

            logger.info(f"Successfully converted {len(records)} price records to DataFrame")
            logger.info(f"DataFrame shape: {df.shape}")
            logger.info(f"DataFrame columns: {list(df.columns)}")

            return df

        except Exception as e:
            logger.error(f"Error converting price data to pandas DataFrame: {e}")
            raise ValueError(f"Failed to convert price data: {e}")

    def convert_to_pandas(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Intelligently convert Lukka API data to pandas DataFrame.

        This method automatically detects the data type (sources or prices) and calls
        the appropriate conversion method.

        Args:
            data: Dictionary containing either source details or price data from Lukka API

        Returns:
            pandas.DataFrame: Converted data ready for saving

        Raises:
            ValueError: If data format is not recognized or conversion fails
        """
        try:
            if not isinstance(data, dict):
                raise ValueError(f"Data must be a dictionary, got {type(data)}")

            # Detect data type based on structure
            if "prices" in data and "pairCode" in data:
                # Historical price data format
                logger.info("Detected price data format, using convert_prices_to_pandas()")
                return self.convert_prices_to_pandas(data)

            elif (
                "sourceId" in data
                or "sourceName" in data
                or "sources" in data
                or (
                    isinstance(data, dict)
                    and any(
                        "sourceId" in item or "sourceName" in item
                        for item in (data.values() if isinstance(data, dict) else [])
                        if isinstance(item, dict)
                    )
                )
            ):
                # Source data format
                logger.info("Detected source data format, using convert_sources_to_pandas()")
                return self.convert_sources_to_pandas(data)

            else:
                # Try to infer from data structure
                if isinstance(data, list) and len(data) > 0:
                    first_item = data[0]
                    if isinstance(first_item, dict):
                        if "ts" in first_item and "price" in first_item:
                            # Looks like price data in list format
                            logger.info(
                                "Detected price data in list format, converting to expected structure"
                            )
                            converted_data = {"prices": data, "pairCode": None, "sourceId": None}
                            return self.convert_prices_to_pandas(converted_data)
                        elif "sourceId" in first_item or "sourceName" in first_item:
                            # Looks like source data
                            logger.info(
                                "Detected source data in list format, using convert_sources_to_pandas()"
                            )
                            return self.convert_sources_to_pandas(data)

                # If no clear pattern is detected, raise an error
                raise ValueError(
                    "Could not determine data format. Expected either:\n"
                    "- Price data: dictionary with 'prices' and 'pairCode' keys\n"
                    "- Source data: dictionary with 'sourceId', 'sourceName', or 'sources' keys\n"
                    f"Received keys: {list(data.keys()) if isinstance(data, dict) else 'not a dict'}"
                )

        except Exception as e:
            logger.error(f"Error in convert_to_pandas: {e}")
            raise

    def write_locally(
        self,
        df: pd.DataFrame,
        file_name: str,
        file_format: str = "csv",
        location: Optional[str] = None,
    ) -> str:
        """
        Save pandas DataFrame locally in specified format.

        Args:
            df: pandas DataFrame to save
            file_name: Name of the file (without extension)
            file_format: Format to save ('csv' or 'parquet')
            location: Custom location to save file. If None, uses base_location

        Returns:
            str: Full path of the saved file

        Raises:
            ValueError: If file_format is not supported or no location is specified
            IOError: If file cannot be written
        """
        # Validate file format
        supported_formats = ["csv", "parquet", "json"]
        if file_format.lower() not in supported_formats:
            raise ValueError(
                f"Unsupported file format: {file_format}. Supported: {supported_formats}"
            )

        # Determine save location
        if location is None:
            if self.base_location is None:
                raise ValueError(
                    "No save location specified. Please provide 'location' parameter or set base_location during initialization."
                )
            save_location = self.base_location
        else:
            save_location = location

        # Ensure directory exists
        self._ensure_directory_exists(save_location)

        # Create full file path
        file_extension = file_format.lower()
        if not file_name.endswith(f".{file_extension}"):
            if file_format.lower() == "csv":
                file_name = f"{file_name}.{file_extension}"
            elif file_format.lower() == "parquet":
                file_name = f"{file_name}.{'snappy'}.{file_extension}"
            elif file_format.lower() == "json":
                file_name = f"{file_name}.{file_extension}"

        file_path = os.path.join(save_location, file_name)

        try:
            # Save based on format
            if file_format.lower() == "csv":
                df.to_csv(file_path, index=False, encoding="utf-8")
                logger.info(f"Successfully saved DataFrame as CSV: {file_path}")
            elif file_format.lower() == "parquet":
                # Use pandas built-in parquet functionality (no PyArrow required)
                df.to_parquet(file_path, index=False, engine="pyarrow", compression="snappy")
                logger.info(f"Successfully saved DataFrame as Parquet: {file_path}")
            elif file_format.lower() == "json":
                df.to_json(file_path, orient="records", indent=2)
                logger.info(f"Successfully saved DataFrame as JSON: {file_path}")

            # Log file info
            file_size = os.path.getsize(file_path)
            logger.info(f"File size: {file_size:,} bytes")
            logger.info(f"Records saved: {len(df)}")

            return file_path

        except Exception as e:
            logger.error(f"Error saving file {file_path}: {e}")
            raise IOError(f"Failed to save file: {e}")

    def _ensure_directory_exists(self, directory: str) -> None:
        """
        Ensure that the specified directory exists, create if it doesn't.

        Args:
            directory: Directory path to check/create
        """
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory ensured: {directory}")
        except Exception as e:
            logger.error(f"Failed to create directory {directory}: {e}")
            raise IOError(f"Cannot create directory: {e}")

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get information about a saved file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file information
        """
        try:
            if not os.path.exists(file_path):
                return {"exists": False}

            stat = os.stat(file_path)
            return {
                "exists": True,
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": pd.to_datetime(stat.st_ctime, unit="s"),
                "modified": pd.to_datetime(stat.st_mtime, unit="s"),
                "extension": os.path.splitext(file_path)[1],
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
            return {"exists": False, "error": str(e)}


def main():
    """
    Example usage of the WriteData class.
    """
    print("💾 Lukka Data Writer Example")
    print("=" * 50)

    try:
        # Initialize writer
        writer = WriteData()

        # Example source data (simulated response from get_source_details)
        example_source_data = {
            "sourceId": 3000,
            "sourceName": "Example Exchange",
            "status": "active",
            "sourceType": "exchange",
            "description": "Example cryptocurrency exchange",
            "website": "https://example.com",
            "supportedPairs": ["BTC-USD", "ETH-USD", "ADA-USD"],
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-15T12:30:00Z",
        }

        print("📊 Converting source data to DataFrame...")
        df = writer.convert_to_pandas(example_source_data)
        print(f"✅ DataFrame created with shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

        # Show sample data
        print("\n📋 Sample data:")
        print(df.head())

        # Save as CSV
        print("\n💾 Saving as CSV...")
        csv_path = writer.write_locally(df=df, file_name="example_source_data", file_format="csv")
        print(f"✅ CSV saved: {csv_path}")

        # Save as Parquet
        print("\n💾 Saving as Parquet...")
        parquet_path = writer.write_locally(
            df=df, file_name="example_source_data", file_format="parquet"
        )
        print(f"✅ Parquet saved: {parquet_path}")

        # Show file info
        print("\n📈 File Information:")
        for file_path in [csv_path, parquet_path]:
            info = writer.get_file_info(file_path)
            if info["exists"]:
                print(f"  {os.path.basename(file_path)}: {info['size_mb']} MB")

        print("\n🎉 Data writing example completed successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
