"""
Retry Utilities for Unified AI SDK

Provides safe retry strategies that avoid wasting API credits on non-retryable errors.
Ported from: services/tts/elevenlabs_client.py SafeRetryStrategy
"""
import asyncio
import functools
from typing import Callable, Optional, Tuple, TypeVar, Any

from ..breadcrumbs import BreadcrumbLevel, SDKLayer, get_collector

T = TypeVar("T")


class SafeRetryStrategy:
    """
    Safe retry strategy that avoids wasting API credits.

    Does NOT retry errors that would burn tokens/credits:
    - 400: Bad Request - invalid params
    - 401: Unauthorized - bad API key
    - 402: Payment Required - out of credits
    - 403: Forbidden - no access
    - 422: Unprocessable Entity

    Retries only temporary/transient errors:
    - 408: Request Timeout
    - 429: Rate Limited
    - 500-504: Server errors
    """

    NO_RETRY_ERRORS = {
        400: "Bad Request - invalid params",
        401: "Unauthorized - bad API key",
        402: "Payment Required - out of credits",
        403: "Forbidden - no access",
        422: "Unprocessable Entity",
    }

    RETRYABLE_ERRORS = {
        408: "Request Timeout",
        429: "Rate Limited",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
    }

    def should_retry(
        self, status_code: int, attempt: int, max_retries: int = 3
    ) -> Tuple[bool, int]:
        """
        Determine if a request should be retried.

        Args:
            status_code: HTTP status code from response
            attempt: Current attempt number (0-based)
            max_retries: Maximum number of retry attempts

        Returns:
            Tuple of (should_retry, wait_seconds)
        """
        if status_code in self.NO_RETRY_ERRORS:
            return False, 0

        if attempt >= max_retries:
            return False, 0

        if status_code == 429:
            return True, 10

        if status_code in self.RETRYABLE_ERRORS:
            wait_time = min(2 ** attempt, 8)
            return True, wait_time

        return False, 0

    def get_error_message(self, status_code: int) -> str:
        """
        Get human-readable error message for a status code.

        Args:
            status_code: HTTP status code

        Returns:
            Human-readable error description
        """
        if status_code in self.NO_RETRY_ERRORS:
            return self.NO_RETRY_ERRORS[status_code]
        if status_code in self.RETRYABLE_ERRORS:
            return self.RETRYABLE_ERRORS[status_code]
        return f"Unknown error (status {status_code})"

    def is_quota_error(self, status_code: int) -> bool:
        """
        Check if the error indicates a quota/payment issue.

        Args:
            status_code: HTTP status code

        Returns:
            True if error is quota-related (402 or 403)
        """
        return status_code in (402, 403)


class ExponentialBackoff:
    """
    Exponential backoff calculator for retry delays.

    Calculates delay as: min(initial_delay * base^attempt, max_delay)
    """

    def __init__(
        self,
        initial_delay: float = 1.0,
        max_delay: float = 30.0,
        base: float = 2.0,
    ):
        """
        Initialize exponential backoff.

        Args:
            initial_delay: Starting delay in seconds
            max_delay: Maximum delay cap in seconds
            base: Exponential base multiplier
        """
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.base = base

    def get_delay(self, attempt: int) -> float:
        """
        Calculate delay for a given attempt.

        Args:
            attempt: Attempt number (0-based)

        Returns:
            Delay in seconds
        """
        delay = self.initial_delay * (self.base ** attempt)
        return min(delay, self.max_delay)

    async def wait(self, attempt: int) -> None:
        """
        Async sleep with calculated delay.

        Args:
            attempt: Attempt number (0-based)
        """
        delay = self.get_delay(attempt)
        await asyncio.sleep(delay)


def with_retry(
    max_retries: int = 3,
    strategy: Optional[SafeRetryStrategy] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for adding retry logic to async functions.

    Wraps async functions with automatic retry handling based on
    SafeRetryStrategy. Logs retry attempts via breadcrumbs if a
    collector is active.

    Args:
        max_retries: Maximum number of retry attempts
        strategy: Retry strategy instance (default: SafeRetryStrategy)

    Returns:
        Decorator function

    Example:
        @with_retry(max_retries=3)
        async def make_api_call():
            ...
    """
    if strategy is None:
        strategy = SafeRetryStrategy()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Optional[Exception] = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    status_code = getattr(e, "status_code", None)
                    if status_code is None:
                        status_code = getattr(e, "status", None)

                    if status_code is None:
                        collector = get_collector()
                        if collector:
                            collector.add(
                                layer=SDKLayer.RETRY,
                                action="retry_failed",
                                level=BreadcrumbLevel.ERROR,
                                message=f"No status code, cannot retry: {e}",
                                attempt=attempt,
                                error=str(e),
                            )
                        raise

                    should_retry, wait_seconds = strategy.should_retry(
                        status_code, attempt, max_retries
                    )

                    collector = get_collector()
                    if collector:
                        if should_retry:
                            collector.add(
                                layer=SDKLayer.RETRY,
                                action="retry_scheduled",
                                level=BreadcrumbLevel.WARN,
                                message=f"Retrying after {wait_seconds}s",
                                attempt=attempt,
                                status_code=status_code,
                                wait_seconds=wait_seconds,
                                error_message=strategy.get_error_message(status_code),
                            )
                        else:
                            collector.add(
                                layer=SDKLayer.RETRY,
                                action="retry_skipped",
                                level=BreadcrumbLevel.ERROR,
                                message=f"Not retrying: {strategy.get_error_message(status_code)}",
                                attempt=attempt,
                                status_code=status_code,
                                is_quota_error=strategy.is_quota_error(status_code),
                            )

                    if not should_retry:
                        raise

                    await asyncio.sleep(wait_seconds)

            if last_exception:
                raise last_exception
            raise RuntimeError("Retry loop exited unexpectedly")

        return wrapper  # type: ignore[return-value]

    return decorator


__all__ = [
    "SafeRetryStrategy",
    "ExponentialBackoff",
    "with_retry",
]
