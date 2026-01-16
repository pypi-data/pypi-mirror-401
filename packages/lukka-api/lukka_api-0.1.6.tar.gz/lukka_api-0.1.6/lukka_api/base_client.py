"""
Base client for Lukka API OAuth2 authentication.

This module provides the base class for distributed Lukka API clients,
containing shared OAuth2 token request logic and credential management.
"""

import os
import json
import socket
import logging
import base64
from typing import Optional, Dict, Any, Tuple

import requests
from dotenv import load_dotenv

from .decorators import log_performance, retry_on_failure

logger = logging.getLogger(__name__)


class BaseLukkaAPIClient:
    """
    Base class for Lukka API clients with OAuth2 authentication.

    This class provides shared functionality for all Lukka API client implementations:
    - OAuth2 token request logic
    - Credential resolution (explicit > env vars > .env file)
    - HTTP session management with connection pooling
    - Context manager support

    Subclasses must implement:
    - get_api_key(): Token retrieval and caching strategy
    """

    # OAuth2 endpoint URL
    OAUTH2_URL = "https://sso.lukka.tech/oauth2/aus1imo2fqcx5Ik4Q0h8/v1/token"

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize base API client.

        Args:
            username: Lukka API username. If None, uses environment variable or .env file.
                     Priority: explicit parameter > LUKKA_USERNAME env var > .env file
            password: Lukka API password. If None, uses environment variable or .env file.
                     Priority: explicit parameter > LUKKA_PASSWORD env var > .env file

        Raises:
            ValueError: If credentials not found or incomplete
        """
        self.url = self.OAUTH2_URL
        self.session = self._create_session()
        self.username, self.password = self._resolve_credentials(username, password)
        self.machine_id = socket.gethostname()

        logger.debug(f"Initialized {self.__class__.__name__} on {self.machine_id}")
        logger.debug(f"Using username: {self.username}")

    def _resolve_credentials(
        self, username: Optional[str], password: Optional[str]
    ) -> Tuple[str, str]:
        """
        Resolve credentials with priority: explicit > env var > .env file.

        Args:
            username: Optional explicit username
            password: Optional explicit password

        Returns:
            tuple: (username, password)

        Raises:
            ValueError: If credentials not found anywhere or incomplete

        Priority order:
            1. Explicit username/password parameters (highest priority)
            2. LUKKA_USERNAME/LUKKA_PASSWORD environment variables
            3. .env file (backward compatibility)

        Example:
            >>> # Explicit credentials
            >>> client = BaseLukkaAPIClient(username="user", password="pass")

            >>> # Environment variables
            >>> os.environ['LUKKA_USERNAME'] = 'user'
            >>> os.environ['LUKKA_PASSWORD'] = 'pass'
            >>> client = BaseLukkaAPIClient()
        """
        # Priority 1: Explicit parameters (both must be provided)
        if username and password:
            logger.debug(f"Using explicit credentials for user: {username}")
            return (username, password)

        # Check for partial explicit credentials (error condition)
        if username or password:
            raise ValueError(
                "Both username and password must be provided together.\n"
                "You provided only one of them explicitly."
            )

        # Priority 2 & 3: Environment variables (may come from .env file via load_dotenv)
        # Load .env file first to populate environment
        load_dotenv()

        env_username = os.getenv("LUKKA_USERNAME")
        env_password = os.getenv("LUKKA_PASSWORD")

        if env_username and env_password:
            logger.debug(f"Using credentials from environment for user: {env_username}")
            return (env_username, env_password)

        # Check for partial environment credentials (error condition)
        if env_username or env_password:
            raise ValueError(
                "Both LUKKA_USERNAME and LUKKA_PASSWORD must be set.\n"
                "Found only one in environment variables or .env file."
            )

        # No credentials found anywhere
        raise ValueError(
            "Lukka API credentials not found. Please provide credentials using one of:\n"
            "1. Explicit parameters (recommended):\n"
            "   LukkaPrices(username='...', password='...')\n"
            "2. Environment variables:\n"
            "   export LUKKA_USERNAME='...'\n"
            "   export LUKKA_PASSWORD='...'\n"
            "3. .env file (backward compatible):\n"
            "   LUKKA_USERNAME=...\n"
            "   LUKKA_PASSWORD=..."
        )

    def _create_session(self) -> requests.Session:
        """
        Create configured session with retry strategy and connection pooling.

        Returns:
            requests.Session: Configured session with adapter and timeout

        Configuration:
            - Max retries: 3
            - Connection pool: 10 connections
            - Max pool size: 20 connections
            - Default timeout: 30 seconds

        Example:
            >>> session = self._create_session()
            >>> response = session.get(url, timeout=30)
        """
        session = requests.Session()

        # Configure retry strategy with connection pooling
        adapter = requests.adapters.HTTPAdapter(
            max_retries=3,
            pool_connections=10,  # Connection pool size
            pool_maxsize=20,  # Max connections in pool
        )
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        # Set default timeout
        session.timeout = 30

        return session

    @log_performance
    @retry_on_failure(max_retries=3, delay=1.0, exceptions=(requests.exceptions.RequestException,))
    def _request_new_token(self) -> Dict[str, Any]:
        """
        Request new OAuth2 token from Lukka API using stored credentials.

        Returns:
            Dict containing OAuth2 response with keys:
                - access_token: OAuth2 access token string
                - expires_in: Token lifetime in seconds
                - token_type: Token type (usually "Bearer")

        Raises:
            ValueError: If no access token received
            requests.RequestException: If token request fails or times out

        Example:
            >>> token_data = self._request_new_token()
            >>> access_token = token_data["access_token"]
            >>> expires_in = token_data["expires_in"]
        """
        # Use credentials resolved during initialization
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        payload = "grant_type=client_credentials&scope=pricing"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
        }

        try:
            response = self.session.post(self.url, data=payload, headers=headers, timeout=30)
            response.raise_for_status()

            response_data = response.json()
            access_token = response_data.get("access_token")

            if not access_token:
                raise ValueError("No access token received from OAuth2 response")

            logger.info(
                f"OAuth2 token retrieved successfully (expires in {response_data.get('expires_in', 3600)}s)"
            )
            return response_data

        except requests.exceptions.Timeout:
            raise requests.RequestException("Request timed out while retrieving OAuth2 token")
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {response.status_code}"
            try:
                error_detail = response.json().get("error_description", response.text)
                error_msg += f": {error_detail}"
            except (json.JSONDecodeError, AttributeError) as parse_error:
                logger.debug(f"Could not parse error response: {parse_error}")
                error_msg += f": {response.text}"
            raise requests.RequestException(error_msg)
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"Failed to retrieve OAuth2 token: {e}")

    def _is_token_valid(self, token_data: Optional[Dict[str, Any]]) -> bool:
        """
        Check if token is valid and not expired.

        Args:
            token_data: Token cache data dictionary containing:
                - access_token: OAuth2 access token
                - expires_at: Unix timestamp when token expires

        Returns:
            bool: True if token exists and is not expired, False otherwise

        Example:
            >>> token_data = {"access_token": "abc123", "expires_at": time.time() + 3600}
            >>> self._is_token_valid(token_data)
            True
        """
        if not token_data:
            return False

        if "access_token" not in token_data:
            return False

        # Check if token is expired (with 60s buffer for safety)
        import time

        expires_at = token_data.get("expires_at", 0)
        is_valid = time.time() < expires_at - 60

        if not is_valid:
            logger.debug("Token expired or expiring soon")

        return is_valid

    def get_api_key(self, hostname: Optional[str] = None, in_use: bool = True) -> str:
        """
        Get OAuth2 token - must be implemented by subclasses.

        Args:
            hostname: Machine hostname for tracking. If None, uses self.machine_id
            in_use: True to register machine as active, False to unregister

        Returns:
            str: Valid OAuth2 access token

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement get_api_key()")

    def close(self):
        """
        Properly close session and cleanup resources.

        Subclasses should override to add additional cleanup.

        Example:
            >>> client = BaseLukkaAPIClient(username="user", password="pass")
            >>> try:
            ...     token = client.get_api_key()
            ... finally:
            ...     client.close()
        """
        if self.session:
            self.session.close()
            logger.debug("Session closed")

    def __enter__(self):
        """
        Enter context manager.

        Returns:
            self: The client instance

        Example:
            >>> with BaseLukkaAPIClient(username="user", password="pass") as client:
            ...     token = client.get_api_key()
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager and cleanup.

        Args:
            exc_type: Exception type if error occurred
            exc_val: Exception value if error occurred
            exc_tb: Exception traceback if error occurred
        """
        self.close()
