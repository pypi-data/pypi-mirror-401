"""
Performance monitoring and utility decorators for Lukka API.

This module provides decorators for performance monitoring, retry logic,
and caching to improve reliability and observability.
"""

import time
import logging
import functools
from typing import Any, Callable, Dict, Optional, TypeVar, cast
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Type variable for generic function return types
T = TypeVar("T")


def log_performance(func: Callable[..., T]) -> Callable[..., T]:
    """
    Log execution time and performance metrics for decorated function.

    Measures and logs execution time, function name, arguments, and result status.
    Useful for identifying performance bottlenecks and monitoring API operations.

    Args:
        func: Function to decorate

    Returns:
        Decorated function with performance logging

    Example:
        >>> @log_performance
        ... def fetch_data(api_key: str) -> dict:
        ...     return {"data": "value"}
        >>> result = fetch_data("test_key")
        INFO: fetch_data completed in 0.123s

    Performance:
        - Overhead: <1ms for timing and logging
        - Log level: INFO for normal operations, WARNING for slow operations (>5s)
        - Captures function name, args (sanitized), execution time
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start_time = time.time()
        func_name = func.__name__

        # Sanitize arguments for logging (avoid logging sensitive data)
        safe_args = _sanitize_args(args, kwargs)

        try:
            logger.debug(f"{func_name} called with args={safe_args}")
            result = func(*args, **kwargs)

            execution_time = time.time() - start_time

            # Log at appropriate level based on execution time
            if execution_time > 5.0:
                logger.warning(
                    f"{func_name} completed in {execution_time:.3f}s (SLOW) - args={safe_args}"
                )
            else:
                logger.info(f"{func_name} completed in {execution_time:.3f}s")

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"{func_name} failed after {execution_time:.3f}s with {type(e).__name__}: {e}"
            )
            raise

    return cast(Callable[..., T], wrapper)


def retry_on_failure(
    max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0, exceptions: tuple = (Exception,)
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Retry decorator with exponential backoff for transient failures.

    Automatically retries failed operations with exponential backoff delay.
    Useful for network requests, API calls, and other operations that may
    experience transient failures.

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Backoff multiplier for exponential delay (default: 2.0)
        exceptions: Tuple of exception types to catch and retry (default: (Exception,))

    Returns:
        Decorator function that adds retry logic

    Raises:
        Exception: Re-raises the last exception if all retries are exhausted

    Example:
        >>> @retry_on_failure(max_retries=3, delay=1.0, backoff=2.0)
        ... def fetch_api_data(url: str) -> dict:
        ...     response = requests.get(url)
        ...     response.raise_for_status()
        ...     return response.json()

    Retry Strategy:
        - Attempt 1: Immediate execution
        - Attempt 2: Wait 1.0s (delay)
        - Attempt 3: Wait 2.0s (delay * backoff)
        - Attempt 4: Wait 4.0s (delay * backoff^2)
        - Total time: ~7s for 3 retries with default settings

    Performance:
        - Best case: No retries, <1ms overhead
        - Worst case: (max_retries * delay * backoff) seconds
        - Default: ~7 seconds maximum for 3 retries
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            func_name = func.__name__
            current_delay = delay

            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        logger.info(
                            f"{func_name} retry attempt {attempt}/{max_retries} "
                            f"after {current_delay:.1f}s delay"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff

                    return func(*args, **kwargs)

                except exceptions as e:
                    is_last_attempt = attempt == max_retries

                    if is_last_attempt:
                        logger.error(
                            f"{func_name} failed after {max_retries} retries with "
                            f"{type(e).__name__}: {e}"
                        )
                        raise
                    else:
                        logger.warning(
                            f"{func_name} attempt {attempt + 1} failed with "
                            f"{type(e).__name__}: {e}, retrying..."
                        )

            # This should never be reached, but type checker needs it
            raise RuntimeError(f"{func_name} exceeded retry limit")

        return cast(Callable[..., T], wrapper)

    return decorator


class CacheEntry:
    """
    Cache entry with TTL (Time To Live) support.

    Stores cached value along with expiration timestamp for TTL-based
    cache invalidation.

    Attributes:
        value: Cached value of any type
        expires_at: Unix timestamp when entry expires
    """

    def __init__(self, value: Any, ttl: float):
        """
        Initialize cache entry with value and TTL.

        Args:
            value: Value to cache
            ttl: Time to live in seconds
        """
        self.value = value
        self.expires_at = time.time() + ttl

    def is_expired(self) -> bool:
        """
        Check if cache entry has expired.

        Returns:
            bool: True if expired, False otherwise
        """
        return time.time() > self.expires_at


def cache_result(ttl: float = 300.0) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Cache function results with TTL-based expiration.

    Caches function results based on arguments to avoid redundant computations
    or API calls. Cache entries expire after TTL seconds.

    Args:
        ttl: Time to live in seconds (default: 300 = 5 minutes)

    Returns:
        Decorator function that adds result caching

    Example:
        >>> @cache_result(ttl=60.0)  # Cache for 1 minute
        ... def expensive_computation(x: int) -> int:
        ...     time.sleep(5)  # Simulated expensive operation
        ...     return x * x
        >>> result1 = expensive_computation(10)  # Takes 5s
        >>> result2 = expensive_computation(10)  # Returns instantly from cache

    Cache Key Generation:
        - Based on function arguments (args + kwargs)
        - Uses repr() for hashable representation
        - Different arguments = different cache entries

    Performance:
        - Cache hit: <1ms overhead
        - Cache miss: Function execution time + <1ms
        - Memory: O(n) where n is number of unique argument combinations

    Thread Safety:
        - NOT thread-safe for concurrent access
        - Use external locking for multi-threaded environments

    Limitations:
        - Only caches based on arguments, not function closure
        - Arguments must be hashable (or have repr())
        - No cache size limit (grows unbounded)
        - Not persistent (in-memory only)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[str, CacheEntry] = {}

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Generate cache key from arguments
            cache_key = _generate_cache_key(func.__name__, args, kwargs)

            # Check if cached result exists and is valid
            if cache_key in cache:
                entry = cache[cache_key]

                if not entry.is_expired():
                    logger.debug(f"Cache hit for {func.__name__} (key={cache_key})")
                    return entry.value
                else:
                    logger.debug(f"Cache expired for {func.__name__} (key={cache_key})")
                    del cache[cache_key]

            # Cache miss - execute function and cache result
            logger.debug(f"Cache miss for {func.__name__} (key={cache_key})")
            result = func(*args, **kwargs)
            cache[cache_key] = CacheEntry(result, ttl)

            return result

        # Add cache management methods
        wrapper.cache_clear = lambda: cache.clear()  # type: ignore
        wrapper.cache_info = lambda: {  # type: ignore
            "size": len(cache),
            "ttl": ttl,
            "entries": len([e for e in cache.values() if not e.is_expired()]),
        }

        return cast(Callable[..., T], wrapper)

    return decorator


def _sanitize_args(args: tuple, kwargs: dict) -> str:
    """
    Sanitize function arguments for safe logging.

    Removes or masks sensitive information like passwords, tokens, and API keys
    before logging function arguments.

    Args:
        args: Positional arguments tuple
        kwargs: Keyword arguments dictionary

    Returns:
        str: Sanitized string representation of arguments

    Security:
        - Masks password, token, api_key, secret arguments
        - Replaces sensitive values with '***REDACTED***'
        - Preserves non-sensitive argument structure
    """
    sensitive_keys = {"password", "token", "api_key", "secret", "access_token"}

    # Sanitize kwargs
    safe_kwargs = {}
    for key, value in kwargs.items():
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            safe_kwargs[key] = "***REDACTED***"
        else:
            safe_kwargs[key] = value

    # Create safe representation
    if safe_kwargs:
        return f"args={args}, kwargs={safe_kwargs}"
    else:
        return f"args={args}"


def _generate_cache_key(func_name: str, args: tuple, kwargs: dict) -> str:
    """
    Generate cache key from function name and arguments.

    Creates a unique string key based on function name and arguments
    for use in result caching.

    Args:
        func_name: Name of the function
        args: Positional arguments tuple
        kwargs: Keyword arguments dictionary

    Returns:
        str: Unique cache key string

    Example:
        >>> _generate_cache_key("fetch_data", ("BTC-USD",), {"interval": 86400000})
        "fetch_data:('BTC-USD',):{'interval': 86400000}"
    """
    args_repr = repr(args)
    kwargs_repr = repr(sorted(kwargs.items()))
    return f"{func_name}:{args_repr}:{kwargs_repr}"
