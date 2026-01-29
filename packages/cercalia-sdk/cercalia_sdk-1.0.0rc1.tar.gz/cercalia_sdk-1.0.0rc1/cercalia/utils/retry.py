"""
Retry utility for Cercalia SDK.

Provides retry logic with exponential backoff for API calls.
"""

import time
from collections.abc import Callable
from functools import wraps
from typing import Any, Optional, TypeVar

from .logger import logger

T = TypeVar("T")


def with_retry(
    max_attempts: int = 3,
    delay_ms: int = 500,
    log_retries: bool = True,
    operation_name: str = "operation",
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that adds retry logic with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay_ms: Initial delay between retries in milliseconds (default: 500)
        log_retries: Whether to log retry attempts (default: True)
        operation_name: Name of the operation for logging

    Returns:
        Decorated function with retry logic

    Example:
        >>> @with_retry(max_attempts=3, operation_name="API Call")
        ... def make_api_call():
        ...     return requests.get(url)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_error: Optional[Exception] = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e

                    if log_retries:
                        logger.info(
                            f"[Retry] {operation_name} attempt {attempt}/{max_attempts} failed: {e}"
                        )

                    if attempt < max_attempts:
                        # Wait with exponential backoff
                        wait_time = (delay_ms / 1000) * (1.5 ** (attempt - 1))
                        time.sleep(wait_time)

            # All attempts failed, raise the last error
            if last_error is not None:
                raise last_error
            raise RuntimeError(f"All {max_attempts} attempts failed for {operation_name}")

        return wrapper

    return decorator


def retry_request(
    func: Callable[..., T],
    max_attempts: int = 3,
    delay_ms: int = 500,
    log_retries: bool = True,
    operation_name: str = "operation",
) -> T:
    """
    Execute a function with retry logic.

    Non-decorator version for more flexibility.

    Args:
        func: The function to execute
        max_attempts: Maximum number of retry attempts (default: 3)
        delay_ms: Initial delay between retries in milliseconds (default: 500)
        log_retries: Whether to log retry attempts (default: True)
        operation_name: Name of the operation for logging

    Returns:
        The result of the function if successful

    Raises:
        The last exception if all attempts fail

    Example:
        >>> result = retry_request(
        ...     lambda: requests.get(url),
        ...     max_attempts=3,
        ...     operation_name="Fetch data"
        ... )
    """
    last_error: Optional[Exception] = None

    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as e:
            last_error = e

            if log_retries:
                logger.info(
                    f"[Retry] {operation_name} attempt {attempt}/{max_attempts} failed: {e}"
                )

            if attempt < max_attempts:
                # Wait with exponential backoff
                wait_time = (delay_ms / 1000) * (1.5 ** (attempt - 1))
                time.sleep(wait_time)

    # All attempts failed
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"All {max_attempts} attempts failed for {operation_name}")


def with_retry_alternatives(
    attempts: list[Callable[[], Optional[T]]],
    log_retries: bool = True,
    operation_name: str = "operation",
) -> Optional[T]:
    """
    Execute async functions with retries and alternative parameter fallbacks.

    If the first attempt fails or returns None, tries alternative parameter
    functions before giving up.

    Args:
        attempts: List of functions to try in order
        log_retries: Whether to log retry attempts (default: True)
        operation_name: Name of the operation for logging

    Returns:
        The result of the first successful function, or None if all fail

    Raises:
        The last exception if all attempts fail with an exception

    Example:
        >>> result = with_retry_alternatives([
        ...     lambda: search_by_name("Barcelona"),
        ...     lambda: search_by_coordinates(41.38, 2.17),
        ... ], operation_name="Location search")
    """
    last_error: Optional[Exception] = None

    for i, attempt_func in enumerate(attempts):
        try:
            result = attempt_func()
            if result is not None:
                return result
            if log_retries and i < len(attempts) - 1:
                logger.info(
                    f"[Retry] {operation_name} attempt {i + 1}/{len(attempts)} "
                    "returned None, trying alternative"
                )
        except Exception as e:
            last_error = e
            if log_retries:
                logger.info(f"[Retry] {operation_name} attempt {i + 1}/{len(attempts)} failed: {e}")

    # All attempts failed or returned None
    if last_error is not None:
        raise last_error
    return None


def require_non_null(func: Callable[[], Optional[T]], error_message: str) -> T:
    """
    Execute a function and raise an error if it returns None.

    Args:
        func: Function that may return None
        error_message: Error message to raise if result is None

    Returns:
        The non-None result

    Raises:
        ValueError: If the function returns None

    Example:
        >>> result = require_non_null(
        ...     lambda: find_user(user_id),
        ...     "User not found"
        ... )
    """
    result = func()
    if result is None:
        raise ValueError(error_message)
    return result
