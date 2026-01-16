"""
Validation utilities for Lukka API requests.

This module provides validation classes for price requests and date normalization,
extracting validation logic from the main API classes for better separation of concerns.
"""

from typing import Union, Optional
from datetime import datetime, date
from dataclasses import dataclass
import logging
import re

logger = logging.getLogger(__name__)


@dataclass
class PriceRequest:
    """
    Validated price request parameters.

    This dataclass holds validated and normalized parameters for a price request,
    ensuring all values are in the correct format before being passed to the API.

    Attributes:
        pair_codes: Trading pair code (e.g., "BTC-USD")
        from_date: Start date in ISO 8601 format ("YYYY-MM-DDTHH:MM:SSZ")
        to_date: End date in ISO 8601 format ("YYYY-MM-DDTHH:MM:SSZ")
        source_id: Source identifier integer
        interval: Data interval in milliseconds (86400000 or 60000)
        fill: Whether to forward-fill gaps in data
        location: Optional directory path for saving results
        file_name: Optional filename for saving results
        file_format: Optional file format (json, csv, parquet)
    """

    pair_codes: str
    from_date: str  # ISO 8601
    to_date: str  # ISO 8601
    source_id: int
    interval: int
    fill: bool
    location: Optional[str] = None
    file_name: Optional[str] = None
    file_format: Optional[str] = None


class PriceRequestValidator:
    """
    Validates and normalizes price request parameters.

    This class provides comprehensive validation for all price request parameters,
    ensuring they meet the API requirements before making requests.

    Example:
        >>> validator = PriceRequestValidator()
        >>> request = validator.validate(
        ...     pair_codes="BTC-USD",
        ...     from_date="2024-01-01",
        ...     to_date="2024-12-31",
        ...     source_id=1000,
        ...     interval=86400000,
        ...     fill=False
        ... )
        >>> print(request.pair_codes)
        'BTC-USD'
    """

    ALLOWED_INTERVALS = [86400000, 60000]  # Daily and minute-level data
    ALLOWED_FORMATS = ["json", "csv", "parquet"]

    def __init__(self):
        """Initialize validator with date normalizer."""
        self.date_normalizer = DateNormalizer()

    def validate(
        self,
        pair_codes: str,
        from_date: Union[str, datetime, date],
        to_date: Union[str, datetime, date],
        source_id: int,
        interval: int,
        fill: bool,
        location: Optional[str] = None,
        file_name: Optional[str] = None,
        file_format: Optional[str] = None,
    ) -> PriceRequest:
        """
        Validate all parameters and return normalized request.

        Args:
            pair_codes: Trading pair code (e.g., "BTC-USD")
            from_date: Start date (multiple formats accepted)
            to_date: End date (multiple formats accepted)
            source_id: Source ID integer
            interval: Data interval in milliseconds
            fill: Whether to forward-fill gaps
            location: Optional save directory
            file_name: Optional filename
            file_format: Optional file format

        Returns:
            PriceRequest with validated and normalized parameters

        Raises:
            ValueError: If any parameter is invalid
            TypeError: If parameter has wrong type

        Example:
            >>> validator = PriceRequestValidator()
            >>> request = validator.validate(
            ...     pair_codes="ETH-USD",
            ...     from_date=datetime(2024, 1, 1),
            ...     to_date=date(2024, 12, 31),
            ...     source_id=1000,
            ...     interval=86400000,
            ...     fill=True
            ... )
        """

        # Validate pair_codes
        if not isinstance(pair_codes, str) or not pair_codes.strip():
            raise ValueError(
                f"pair_codes must be a non-empty string, "
                f"got {type(pair_codes).__name__}: {pair_codes}"
            )

        # Normalize dates
        from_date_iso = self.date_normalizer.normalize(from_date, "from_date")
        to_date_iso = self.date_normalizer.normalize(to_date, "to_date")

        # Validate date range
        self._validate_date_range(from_date_iso, to_date_iso)

        # Validate source_id
        if not isinstance(source_id, int):
            raise TypeError(
                f"source_id must be an integer, " f"got {type(source_id).__name__}: {source_id}"
            )

        # Validate interval
        if not isinstance(interval, int):
            raise TypeError(
                f"interval must be an integer, " f"got {type(interval).__name__}: {interval}"
            )

        if interval not in self.ALLOWED_INTERVALS:
            raise ValueError(
                f"Invalid interval: {interval}. "
                f"Please specify one of the following valid intervals:\n"
                f"  - 86400000 (daily data)\n"
                f"  - 60000 (minute-level data)"
            )

        # Validate fill
        if not isinstance(fill, bool):
            raise TypeError(f"fill must be a boolean, " f"got {type(fill).__name__}: {fill}")

        # Validate file parameters
        self._validate_file_params(location, file_name, file_format)

        return PriceRequest(
            pair_codes=pair_codes.strip(),
            from_date=from_date_iso,
            to_date=to_date_iso,
            source_id=source_id,
            interval=interval,
            fill=fill,
            location=location,
            file_name=file_name,
            file_format=file_format,
        )

    def _validate_date_range(self, from_date: str, to_date: str) -> None:
        """
        Validate that date range is logically consistent.

        Args:
            from_date: Start date in ISO 8601 format
            to_date: End date in ISO 8601 format

        Raises:
            ValueError: If from_date is after to_date or range is unreasonable
        """
        from_dt = datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%SZ")
        to_dt = datetime.strptime(to_date, "%Y-%m-%dT%H:%M:%SZ")

        if from_dt > to_dt:
            raise ValueError(
                f"Invalid date range: from_date ({from_date}) must be "
                f"before or equal to to_date ({to_date})"
            )

        # Warn about large ranges
        days_diff = (to_dt - from_dt).days
        if days_diff > 3650:  # 10 years
            logger.warning(
                f"Large date range detected: {days_diff} days "
                f"({days_diff / 365.25:.1f} years). This may result in "
                f"slow queries and large result sets."
            )

    def _validate_file_params(
        self, location: Optional[str], file_name: Optional[str], file_format: Optional[str]
    ) -> None:
        """
        Validate file saving parameters.

        Args:
            location: Directory path
            file_name: Filename
            file_format: File format

        Raises:
            ValueError: If file parameters are invalid or inconsistent
        """
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

        if file_format is not None:
            if file_format.lower() not in self.ALLOWED_FORMATS:
                raise ValueError(
                    f"Invalid file_format: '{file_format}'. "
                    f"Allowed formats: {self.ALLOWED_FORMATS}"
                )


class DateNormalizer:
    """
    Handles date normalization to ISO 8601 format.

    This class provides flexible date parsing, accepting multiple input formats
    and converting them to the ISO 8601 format required by the Lukka API.

    Example:
        >>> normalizer = DateNormalizer()
        >>> normalizer.normalize("2024-01-01", "start_date")
        '2024-01-01T00:00:00Z'
        >>> normalizer.normalize(datetime(2024, 1, 1, 12, 30), "start_date")
        '2024-01-01T12:30:00Z'
    """

    def normalize(self, date_input: Union[str, datetime, date], param_name: str) -> str:
        """
        Convert various date formats to ISO 8601 string.

        Args:
            date_input: Date in multiple formats:
                - datetime object: datetime(2024, 1, 1)
                - date object: date(2024, 1, 1)
                - ISO 8601 string: "2024-01-01T00:00:00Z"
                - Simple date string: "2024-01-01"
            param_name: Parameter name for error messages

        Returns:
            ISO 8601 formatted string: "YYYY-MM-DDTHH:MM:SSZ"

        Raises:
            ValueError: If date format is invalid
            TypeError: If date type is not supported

        Example:
            >>> normalizer = DateNormalizer()
            >>> normalizer.normalize("2024-03-15", "test_date")
            '2024-03-15T00:00:00Z'
        """
        # Case 1: datetime object
        if isinstance(date_input, datetime):
            if date_input.tzinfo is None:
                logger.debug(f"{param_name}: Assuming UTC for naive datetime")
            return date_input.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Case 2: date object (no time component)
        if isinstance(date_input, date):
            dt = datetime.combine(date_input, datetime.min.time())
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Case 3: String input
        if isinstance(date_input, str):
            date_input = date_input.strip()

            if not date_input:
                raise ValueError(f"{param_name} cannot be an empty string")

            # Try ISO 8601 format first (fast path)
            if self._is_valid_iso8601(date_input):
                return date_input

            # Try simple YYYY-MM-DD format
            if self._is_simple_date_format(date_input):
                return f"{date_input}T00:00:00Z"

            # Unrecognized format
            raise ValueError(
                f"Invalid date format for '{param_name}': {date_input}\n"
                f"Accepted formats:\n"
                f"  - ISO 8601: '2024-01-01T00:00:00Z'\n"
                f"  - Simple date: '2024-01-01'\n"
                f"  - datetime object: datetime(2024, 1, 1)\n"
                f"  - date object: date(2024, 1, 1)"
            )

        # Invalid type
        raise TypeError(
            f"{param_name} must be str, datetime, or date object, "
            f"got {type(date_input).__name__}"
        )

    def _is_valid_iso8601(self, date_str: str) -> bool:
        """
        Quick check if string is valid ISO 8601 format.

        Args:
            date_str: Date string to validate

        Returns:
            True if valid ISO 8601 format, False otherwise
        """
        # Pattern: YYYY-MM-DDTHH:MM:SS with optional Z
        pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?$"
        if not re.match(pattern, date_str):
            return False

        try:
            datetime.strptime(date_str.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
            return True
        except ValueError:
            return False

    def _is_simple_date_format(self, date_str: str) -> bool:
        """
        Check if string is simple YYYY-MM-DD format.

        Args:
            date_str: Date string to validate

        Returns:
            True if valid YYYY-MM-DD format, False otherwise
        """
        if len(date_str) != 10 or date_str.count("-") != 2:
            return False

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def normalize_to_simple_date(
        self, date_input: Union[str, datetime, date, None], param_name: str
    ) -> Optional[str]:
        """
        Convert various date formats to simple YYYY-MM-DD format.

        This is used by the sources API which requires simple date format
        rather than full ISO 8601 format.

        Args:
            date_input: Date in multiple formats (or None):
                - datetime object: datetime(2024, 1, 1)
                - date object: date(2024, 1, 1)
                - Simple string: "2024-01-01"
                - ISO 8601 string: "2024-01-01T00:00:00Z" (time stripped)
                - None (returns None)
            param_name: Parameter name for error messages

        Returns:
            Simple date string "YYYY-MM-DD" or None if input is None

        Raises:
            ValueError: If date format is invalid
            TypeError: If date type is not supported

        Example:
            >>> normalizer = DateNormalizer()
            >>> normalizer.normalize_to_simple_date("2024-01-01T12:30:00Z", "start_date")
            '2024-01-01'
            >>> normalizer.normalize_to_simple_date(datetime(2024, 1, 1), "start_date")
            '2024-01-01'
            >>> normalizer.normalize_to_simple_date(None, "start_date")
            None
        """
        if date_input is None:
            return None

        # Case 1: datetime object - extract date component
        if isinstance(date_input, datetime):
            return date_input.strftime("%Y-%m-%d")

        # Case 2: date object
        if isinstance(date_input, date):
            return date_input.strftime("%Y-%m-%d")

        # Case 3: String input
        if isinstance(date_input, str):
            date_input = date_input.strip()

            if not date_input:
                raise ValueError(f"{param_name} cannot be an empty string")

            # Try simple YYYY-MM-DD format first (fast path)
            if self._is_simple_date_format(date_input):
                return date_input

            # Try ISO 8601 format and extract date part
            if self._is_valid_iso8601(date_input):
                # Parse and extract date component
                dt = datetime.strptime(date_input.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
                return dt.strftime("%Y-%m-%d")

            # Unrecognized format
            raise ValueError(
                f"Invalid date format for '{param_name}': {date_input}\n"
                f"Accepted formats:\n"
                f"  - Simple date: '2024-01-01'\n"
                f"  - ISO 8601: '2024-01-01T00:00:00Z'\n"
                f"  - datetime object: datetime(2024, 1, 1)\n"
                f"  - date object: date(2024, 1, 1)"
            )

        # Invalid type
        raise TypeError(
            f"{param_name} must be str, datetime, date object, or None, "
            f"got {type(date_input).__name__}"
        )
