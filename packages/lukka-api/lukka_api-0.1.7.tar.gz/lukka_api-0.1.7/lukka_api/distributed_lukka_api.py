import os
import json
import time
import socket
import platform
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import requests
import portalocker
from dotenv import load_dotenv

from .base_client import BaseLukkaAPIClient
from .file_utils import atomic_write_json, secure_read_json
from .decorators import log_performance, retry_on_failure

# Optional Redis support
try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

# Configure logging - default to WARNING to avoid cluttering output
# Users can set LUKKA_LOG_LEVEL environment variable to change this
log_level = os.environ.get("LUKKA_LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
logger = logging.getLogger(__name__)


def get_default_cache_path() -> str:
    """
    Get platform-specific default cache path following industry standards.

    Returns:
        str: Platform-appropriate cache file path

    Platform defaults:
        - Windows: %LOCALAPPDATA%\\lukka-api\\cache\\lukka_token.json
                  (e.g., C:\\Users\\john\\AppData\\Local\\lukka-api\\cache\\lukka_token.json)
        - Linux: ~/.local/share/lukka-api/cache/lukka_token.json (XDG Base Directory)
        - macOS: ~/Library/Application Support/lukka-api/cache/lukka_token.json
        - Other: ~/.lukka-api/cache/lukka_token.json

    Examples:
        >>> path = get_default_cache_path()
        >>> # Windows: 'C:\\Users\\john\\AppData\\Local\\lukka-api\\cache\\lukka_token.json'
        >>> # Linux: '/home/john/.local/share/lukka-api/cache/lukka_token.json'
    """
    system = platform.system().lower()

    if system == "windows":
        # Windows: %LOCALAPPDATA%\lukka-api\cache\lukka_token.json
        base_dir = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
        return str(Path(base_dir) / "lukka-api" / "cache" / "lukka_token.json")

    elif system == "linux":
        # Linux: ~/.local/share/lukka-api/cache/lukka_token.json (XDG Base Directory)
        base_dir = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
        return str(Path(base_dir) / "lukka-api" / "cache" / "lukka_token.json")

    elif system == "darwin":  # macOS
        # macOS: ~/Library/Application Support/lukka-api/cache/lukka_token.json
        return str(
            Path.home()
            / "Library"
            / "Application Support"
            / "lukka-api"
            / "cache"
            / "lukka_token.json"
        )

    else:
        # Fallback for other platforms
        return str(Path.home() / ".lukka-api" / "cache" / "lukka_token.json")


class DistributedLukkaAPIClient(BaseLukkaAPIClient):
    """
    Distributed Lukka API client with cross-platform file-based token caching.

    Designed for distributed systems (Apache Airflow, Docker, Kubernetes) where
    multiple machines need to share OAuth2 tokens while respecting rate limits.

    Features:
    - Cross-platform file locking with portalocker
    - Atomic token refresh operations
    - Machine usage tracking
    - Comprehensive error handling with fallbacks
    - Platform-specific default cache paths (Windows/Linux/macOS)

    Cache Path Priority:
        1. Explicit cache_path parameter
        2. LUKKA_CACHE_PATH environment variable
        3. Platform-specific default (recommended for most users)

    Credentials Priority:
        1. Explicit username/password parameters
        2. LUKKA_USERNAME/LUKKA_PASSWORD environment variables
        3. .env file (backward compatibility)
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        cache_path: Optional[str] = None,
    ):
        """
        Initialize distributed API client.

        Args:
            username: Lukka API username. If None, uses environment variable or .env file.
                     Priority: explicit parameter > LUKKA_USERNAME env var > .env file
            password: Lukka API password. If None, uses environment variable or .env file.
                     Priority: explicit parameter > LUKKA_PASSWORD env var > .env file
            cache_path: Custom cache file path. If None, uses platform-specific default.
                       Priority: explicit parameter > LUKKA_CACHE_PATH env var > platform default

        Examples:
            # Explicit credentials (recommended for production)
            >>> client = DistributedLukkaAPIClient(
            ...     username="your_username",
            ...     password="your_password"
            ... )

            # Use environment variables for credentials
            >>> import os
            >>> os.environ['LUKKA_USERNAME'] = 'user123'
            >>> os.environ['LUKKA_PASSWORD'] = 'pass456'
            >>> client = DistributedLukkaAPIClient()

            # Mix explicit and environment-based configuration
            >>> client = DistributedLukkaAPIClient(
            ...     username="user123",
            ...     password="pass456",
            ...     cache_path="S:/shared/cache/token.json"
            ... )

            # Use .env file (backward compatible)
            >>> client = DistributedLukkaAPIClient()  # Reads from .env automatically
        """
        # Initialize base class (handles credentials and session)
        super().__init__(username=username, password=password)

        # File-based client specific setup
        self.cache_file = self._resolve_cache_path(cache_path)

        logger.info(f"Initialized DistributedLukkaAPIClient on {self.machine_id}")
        logger.info(f"Using cache file: {self.cache_file}")

    def _resolve_cache_path(self, cache_path: Optional[str]) -> Path:
        """
        Resolve cache path with priority: explicit > env var > default.

        Args:
            cache_path: Optional explicit cache path

        Returns:
            Path: Resolved cache file path

        Priority order:
            1. Explicit cache_path parameter (highest priority)
            2. LUKKA_CACHE_PATH environment variable (backward compatibility)
            3. Platform-specific default path (recommended)
        """
        # Priority 1: Explicit parameter
        if cache_path:
            logger.debug(f"Using explicit cache path: {cache_path}")
            return Path(cache_path)

        # Priority 2: Environment variable (backward compatibility)
        load_dotenv()
        if env_path := os.getenv("LUKKA_CACHE_PATH"):
            logger.debug(f"Using cache path from LUKKA_CACHE_PATH: {env_path}")
            return Path(env_path)

        # Priority 3: Platform-specific default
        default_path = get_default_cache_path()
        logger.debug(f"Using platform default cache path: {default_path}")
        return Path(default_path)

    @log_performance
    def get_api_key(self, hostname: Optional[str] = None, in_use: bool = True) -> str:
        """
        Get OAuth2 token from shared cache or request new one.

        Args:
            hostname: Machine hostname for tracking. If None, uses self.machine_id
            in_use: True to register machine as active, False to unregister

        Returns:
            str: Valid OAuth2 access token

        Raises:
            requests.RequestException: If token request fails
        """
        try:
            return self._get_api_key_with_fallback(hostname, in_use)
        except Exception as e:
            logger.error(f"Failed to get API key: {e}")
            raise

    def _get_api_key_with_fallback(
        self, hostname: Optional[str] = None, in_use: bool = True
    ) -> str:
        """Robust token retrieval with comprehensive error handling."""
        machine_name = hostname or self.machine_id

        try:
            # Try to read from cache with timeout
            token_data = self._read_token_cache_with_timeout(timeout=5.0)

            if self._is_token_valid(token_data):
                # Only update machine tracking, not during cache read/write
                if in_use:
                    self._register_machine_as_active(token_data, machine_name)
                else:
                    self._unregister_machine(token_data, machine_name)

                logger.debug(
                    f"Using cached token (expires in {token_data.get('expires_at', 0) - time.time():.0f}s)"
                )
                return token_data["access_token"]

        except TimeoutError:
            logger.warning("Cache read timeout - requesting fresh token")
        except Exception as e:
            logger.warning(f"Cache read error: {e} - requesting fresh token")

        # Cache miss or error - refresh token with fallback
        try:
            return self._refresh_token_with_fallback()
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            # Last resort: direct token request without caching
            return self._request_new_token_direct()

    @retry_on_failure(max_retries=2, delay=0.5, exceptions=(TimeoutError,))
    def _read_token_cache_with_timeout(self, timeout: float = 10.0) -> Dict[str, Any]:
        """
        Secure read of token cache with lock coordination.

        Uses secure_read_json for proper lock handling and graceful degradation.
        Returns empty dict on corruption instead of raising exception.

        Args:
            timeout: Maximum time to wait for lock

        Returns:
            Token cache data, or {} if missing/corrupted

        Raises:
            TimeoutError: If lock cannot be acquired
        """
        try:
            return secure_read_json(self.cache_file, timeout=timeout)
        except FileNotFoundError:
            # Cache doesn't exist yet - normal on first run
            return {}

    def _write_token_cache_with_timeout(self, token_data: Dict[str, Any], timeout: float = 30.0):
        """
        Atomic write of token cache with proper permissions.

        Uses atomic_write_json for guaranteed atomicity and 0o600 permissions.
        No partial files on crash, no permission vulnerabilities.

        Args:
            token_data: OAuth2 token response data
            timeout: Maximum time to wait (unused with atomic write)

        Raises:
            IOError: If atomic write fails
        """
        expires_timestamp = time.time() + token_data.get("expires_in", 3600) - 300  # 5min buffer
        expires_formatted = datetime.fromtimestamp(expires_timestamp).strftime(
            "%Y-%m-%d_%H-%M-%S_%f"
        )

        cache_data = {
            "access_token": token_data["access_token"],
            "expires_at": expires_timestamp,
            "expires_at_formatted": expires_formatted,
            "created_at": time.time(),
            "created_by": self.machine_id,
            "active_machines": {self.machine_id: time.time()},
            "request_count": 0,
            "last_request_times": [],
        }

        # Atomic write with automatic 0o600 permissions!
        atomic_write_json(self.cache_file, cache_data)

        logger.info(
            f"Token cached atomically (expires at {datetime.fromtimestamp(cache_data['expires_at'])})"
        )

    def _register_machine_as_active(self, token_data: Dict[str, Any], machine_name: str):
        """Register machine as actively using the token."""
        now = time.time()

        # Update active machines list
        active_machines = token_data.get("active_machines", {})

        # Remove machines inactive for >5 minutes
        active_machines = {
            machine: last_seen
            for machine, last_seen in active_machines.items()
            if now - last_seen < 300
        }

        # Add/update this machine
        active_machines[machine_name] = now
        token_data["active_machines"] = active_machines

        # Update cache atomically
        try:
            atomic_write_json(self.cache_file, token_data)
            logger.debug(f"Registered machine {machine_name} as active (atomic write)")
        except Exception as e:
            logger.warning(f"Failed to register machine {machine_name}: {e}")

    def _unregister_machine(self, token_data: Dict[str, Any], machine_name: str):
        """Remove machine from active machines list."""
        active_machines = token_data.get("active_machines", {})

        # Remove the specified machine
        if machine_name in active_machines:
            del active_machines[machine_name]
            token_data["active_machines"] = active_machines

            # Update cache atomically
            try:
                atomic_write_json(self.cache_file, token_data)
                logger.debug(f"Unregistered machine {machine_name} (atomic write)")
            except Exception as e:
                logger.warning(f"Failed to unregister machine {machine_name}: {e}")
        else:
            logger.debug(f"Machine {machine_name} was not in active list")

    def _check_rate_limit(self) -> bool:
        """
        Check if we can make an API call without exceeding 5 requests/second limit.

        Returns:
            bool: True if request can proceed, False if rate limited
        """
        try:
            # Read current rate limit data from cache
            token_data = self._read_token_cache_with_timeout(timeout=2.0)

            now = time.time()
            request_times = token_data.get("last_request_times", [])

            # Remove requests older than 1 second
            recent_requests = [t for t in request_times if now - t < 1.0]

            # Check if we're under the 5 requests/second limit
            if len(recent_requests) < 5:
                # Add current request time
                recent_requests.append(now)
                token_data["last_request_times"] = recent_requests
                token_data["request_count"] = token_data.get("request_count", 0) + 1

                # Update cache with new rate limit data
                try:
                    with open(self.cache_file, "w") as f:
                        portalocker.lock(f, portalocker.LOCK_EX)
                        json.dump(token_data, f, indent=2)
                        portalocker.unlock(f)
                except Exception as e:
                    logger.warning(f"Failed to update rate limit data: {e}")

                return True
            else:
                logger.warning("Rate limit exceeded: 5 requests/second")
                return False

        except Exception as e:
            logger.warning(f"Rate limit check failed: {e}, allowing request")
            return True  # Allow request if rate limit check fails

    @log_performance
    def _refresh_token_with_fallback(self) -> str:
        """Token refresh with comprehensive error handling."""
        # Double-check pattern with timeout
        try:
            token_data = self._read_token_cache_with_timeout(timeout=3.0)
            if self._is_token_valid(token_data):
                logger.debug("Token was refreshed by another process")
                return token_data["access_token"]
        except Exception as e:
            logger.debug(f"Token cache read failed, will refresh: {e}")
            # Continue to refresh

        # Request new token
        logger.info("Requesting new OAuth2 token")
        new_token_data = self._request_new_token()

        # Try to cache with timeout
        try:
            self._write_token_cache_with_timeout(new_token_data, timeout=10.0)
        except TimeoutError:
            logger.warning("Cache write timeout - token retrieved but not cached")
        except Exception as e:
            logger.warning(f"Cache write error: {e} - token retrieved but not cached")

        return new_token_data["access_token"]

    def _request_new_token_direct(self) -> str:
        """Direct token request without caching as last resort."""
        logger.warning("Using direct token request - caching unavailable")
        token_data = self._request_new_token()
        return token_data["access_token"]

    def get_active_machines(self) -> Dict[str, float]:
        """Get list of machines currently using the API."""
        try:
            token_data = self._read_token_cache_with_timeout(timeout=5.0)
            active_machines = token_data.get("active_machines", {})
            now = time.time()

            # Filter machines active in last 5 minutes
            active = {
                machine: timestamp
                for machine, timestamp in active_machines.items()
                if now - timestamp < 300
            }

            return active
        except Exception as e:
            logger.error(f"Failed to get active machines: {e}")
            return {self.machine_id: time.time()}

    def get_cache_statistics(self) -> Dict[str, Any]:
        """Get distributed cache statistics."""
        try:
            active_machines = self.get_active_machines()
            token_data = self._read_token_cache_with_timeout(timeout=5.0)

            return {
                "active_machines": len(active_machines),
                "machines": list(active_machines.keys()),
                "token_expires_in": max(0, token_data.get("expires_at", 0) - time.time()),
                "token_created_by": token_data.get("created_by"),
                "cache_file": str(self.cache_file),
                "cache_exists": self.cache_file.exists(),
            }
        except Exception as e:
            logger.error(f"Failed to get cache statistics: {e}")
            return {"error": str(e)}


class RedisDistributedLukkaAPIClient(BaseLukkaAPIClient):
    """
    Redis-based distributed Lukka API client with atomic operations and rate limiting.

    Recommended for high-performance distributed systems requiring:
    - Atomic token refresh operations
    - Distributed rate limiting coordination
    - Real-time machine usage tracking
    - High availability and performance
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        redis_host="localhost",
        redis_port=6379,
        redis_db=0,
        redis_password=None,
    ):
        """
        Initialize Redis-based distributed API client.

        Args:
            username: Lukka API username. If None, uses environment variable or .env file.
            password: Lukka API password. If None, uses environment variable or .env file.
            redis_host: Redis server hostname
            redis_port: Redis server port
            redis_db: Redis database number
            redis_password: Redis password (optional)
        """
        if not REDIS_AVAILABLE:
            raise ImportError("Redis is not available. Install with: pip install redis")

        # Initialize base class (handles credentials and session)
        super().__init__(username=username, password=password)

        # Redis-specific setup
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            decode_responses=True,
        )

        # Redis keys
        self.token_key = "lukka_api_token"  # nosec B105 - Redis key name, not a password
        self.machines_key = "lukka_active_machines"
        self.rate_limit_key = "lukka_rate_limit"

        # Test Redis connection
        try:
            self.redis_client.ping()
            logger.info(f"Initialized RedisDistributedLukkaAPIClient on {self.machine_id}")
            logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
        except redis.RedisError as e:
            raise ConnectionError(f"Failed to connect to Redis: {e}")

    @log_performance
    def get_api_key(self, hostname: Optional[str] = None, in_use: bool = True) -> str:
        """
        Get OAuth2 token from Redis cache or request new one.

        Args:
            hostname: Machine hostname for tracking. If None, uses self.machine_id
            in_use: True to register machine as active, False to unregister

        Returns:
            str: Valid OAuth2 access token

        Raises:
            requests.RequestException: If token request fails
        """
        machine_name = hostname or self.machine_id
        token_data = self._get_cached_token()

        if token_data and self._is_token_valid(token_data):
            if in_use:
                self._register_machine_usage(machine_name)
            else:
                self._unregister_machine(machine_name)
            logger.debug(
                f"Using cached token (expires in {token_data.get('expires_at', 0) - time.time():.0f}s)"
            )
            return token_data["access_token"]

        return self._refresh_token_atomic()

    def _get_cached_token(self) -> Optional[Dict[str, Any]]:
        """Get token from Redis."""
        try:
            data = self.redis_client.get(self.token_key)
            return json.loads(data) if data else None
        except (json.JSONDecodeError, redis.RedisError) as e:
            logger.warning(f"Failed to get cached token: {e}")
            return None

    @log_performance
    def _refresh_token_atomic(self) -> str:
        """Atomically refresh token using Redis locks."""
        lock_key = f"{self.token_key}:lock"
        lock = self.redis_client.lock(lock_key, timeout=30, blocking_timeout=10)

        try:
            if lock.acquire():
                logger.info("Acquired token refresh lock")

                # Double-check pattern
                token_data = self._get_cached_token()
                if token_data and self._is_token_valid(token_data):
                    logger.debug("Token was refreshed by another process")
                    return token_data["access_token"]

                # Request new token
                logger.info("Requesting new OAuth2 token")
                new_token_data = self._request_new_token()

                # Cache in Redis with expiration
                expires_timestamp = time.time() + new_token_data.get("expires_in", 3600) - 300
                expires_formatted = datetime.fromtimestamp(expires_timestamp).strftime(
                    "%Y-%m-%d_%H-%M-%S_%f"
                )

                cache_data = {
                    "access_token": new_token_data["access_token"],
                    "expires_at": expires_timestamp,
                    "expires_at_formatted": expires_formatted,
                    "created_at": time.time(),
                    "created_by": self.machine_id,
                }

                # Set with TTL slightly longer than token expiry
                ttl = new_token_data.get("expires_in", 3600)
                self.redis_client.setex(self.token_key, ttl, json.dumps(cache_data))

                logger.info(f"Token cached in Redis (expires in {ttl}s)")
                return new_token_data["access_token"]
            else:
                raise Exception("Could not acquire token refresh lock")
        finally:
            if lock.owned():
                lock.release()
                logger.debug("Released token refresh lock")

    def _register_machine_usage(self, machine_name: str):
        """Register machine as active."""
        try:
            self.redis_client.hset(self.machines_key, machine_name, time.time())
            self.redis_client.expire(self.machines_key, 3600)  # Expire in 1 hour
            logger.debug(f"Registered machine {machine_name} as active in Redis")
        except redis.RedisError as e:
            logger.warning(f"Failed to register machine {machine_name}: {e}")

    def _unregister_machine(self, machine_name: str):
        """Remove machine from active machines list in Redis."""
        try:
            self.redis_client.hdel(self.machines_key, machine_name)
            logger.debug(f"Unregistered machine {machine_name} from Redis")
        except redis.RedisError as e:
            logger.warning(f"Failed to unregister machine {machine_name}: {e}")

    def _check_distributed_rate_limit(self) -> bool:
        """Check rate limit across all machines (5 requests per second)."""
        try:
            pipe = self.redis_client.pipeline()
            now = time.time()

            # Remove old requests (older than 1 second)
            pipe.zremrangebyscore(self.rate_limit_key, 0, now - 1)

            # Count current requests in the last second
            pipe.zcard(self.rate_limit_key)

            # Add this request
            pipe.zadd(self.rate_limit_key, {f"{self.machine_id}:{now}": now})
            pipe.expire(self.rate_limit_key, 2)  # Expire in 2 seconds

            results = pipe.execute()
            current_count = results[1]

            return current_count < 5  # Max 5 requests per second
        except redis.RedisError as e:
            logger.warning(f"Rate limit check failed: {e} - allowing request")
            return True

    def make_api_call(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make rate-limited API call across all machines.

        Args:
            endpoint: API endpoint URL
            **kwargs: Additional arguments for requests

        Returns:
            requests.Response: API response
        """
        # Wait if rate limit exceeded
        while not self._check_distributed_rate_limit():
            time.sleep(0.1)

        token = self.get_api_key()
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers

        return self.session.get(endpoint, **kwargs)

    def get_active_machines(self) -> Dict[str, float]:
        """Get list of machines currently using the API."""
        try:
            machines = self.redis_client.hgetall(self.machines_key)
            now = time.time()

            # Filter machines active in last 5 minutes
            active = {
                machine: float(timestamp)
                for machine, timestamp in machines.items()
                if now - float(timestamp) < 300
            }

            return active
        except redis.RedisError as e:
            logger.error(f"Failed to get active machines: {e}")
            return {self.machine_id: time.time()}

    def get_cache_statistics(self) -> Dict[str, Any]:
        """Get distributed cache statistics."""
        try:
            active_machines = self.get_active_machines()
            token_data = self._get_cached_token()

            return {
                "active_machines": len(active_machines),
                "machines": list(active_machines.keys()),
                "token_expires_in": (
                    max(0, token_data.get("expires_at", 0) - time.time()) if token_data else 0
                ),
                "token_created_by": token_data.get("created_by") if token_data else None,
                "redis_connected": self.redis_client.ping(),
            }
        except Exception as e:
            logger.error(f"Failed to get cache statistics: {e}")
            return {"error": str(e)}

    def close(self):
        """Properly close connections including Redis."""
        super().close()  # Close session
        if self.redis_client:
            self.redis_client.close()
            logger.debug("Redis connection closed")


if __name__ == "__main__":
    client = DistributedLukkaAPIClient()
    try:
        token = client.get_api_key()
        print("Token retrieved successfully")
        print(token)
    except Exception as e:
        print(f"Error: {e}")
