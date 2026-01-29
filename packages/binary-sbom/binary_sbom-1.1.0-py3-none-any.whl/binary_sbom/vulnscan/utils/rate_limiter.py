"""
Rate limiter for API request management.

This module provides token bucket rate limiters to manage API request
rates for vulnerability databases (OSV, NVD, GitHub Advisories).
"""

from __future__ import annotations

import time
from threading import Lock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


class RateLimiter:
    """
    Token bucket rate limiter for API requests.

    Prevents exceeding API rate limits by controlling request rate using
    the token bucket algorithm. Tokens are added at a fixed rate, and each
    request consumes one token. If no tokens are available, requests are
    either blocked or rejected based on configuration.

    The token bucket algorithm allows for burst traffic up to the capacity
    while maintaining the long-term rate limit.

    Attributes:
        rate: Requests per second (token refill rate)
        capacity: Maximum burst capacity (tokens)
        tokens: Current available tokens
        last_update: Last token refill timestamp
        lock: Thread safety lock

    Example:
        >>> # Limit to 10 requests per second with burst capacity of 20
        >>> limiter = RateLimiter(requests_per_second=10, capacity=20)
        >>> limiter.acquire()  # Blocks until token available
        >>> make_api_request()

        >>> # Non-blocking acquire
        >>> if limiter.acquire(blocking=False):
        ...     make_api_request()
        ... else:
        ...     # Handle rate limit exceeded

        >>> # Context manager usage
        >>> with limiter:
        ...     make_api_request()
    """

    def __init__(self, requests_per_second: float, capacity: int | None = None):
        """
        Initialize rate limiter.

        Args:
            requests_per_second: Target request rate (tokens per second)
            capacity: Maximum burst capacity in tokens.
                     Defaults to requests_per_second if not specified.

        Raises:
            ValueError: If requests_per_second is less than or equal to zero

        Example:
            >>> limiter = RateLimiter(requests_per_second=10, capacity=20)
            >>> limiter.rate
            10.0
            >>> limiter.capacity
            20
        """
        if requests_per_second <= 0:
            raise ValueError(
                f"requests_per_second must be positive, got {requests_per_second}"
            )

        self.rate = float(requests_per_second)
        self.capacity = capacity or int(requests_per_second)
        self.tokens = float(self.capacity)
        self.last_update = time.time()
        self.lock = Lock()

    def acquire(self, blocking: bool = True, timeout: float | None = None) -> bool:
        """
        Acquire a token from the bucket.

        If blocking is True and no tokens are available, this method will
        sleep until a token becomes available. If timeout is specified and
        no token becomes available within that time, returns False.

        Args:
            blocking: If True, block until token available.
                     If False, return False immediately if no token available.
            timeout: Maximum time to wait in seconds (only when blocking=True).
                    None means wait indefinitely.

        Returns:
            True if token acquired, False if not (when blocking=False or timeout)

        Example:
            >>> limiter = RateLimiter(requests_per_second=1)
            >>> # Non-blocking acquire
            >>> success = limiter.acquire(blocking=False)
            >>> if success:
            ...     make_request()

            >>> # Blocking with timeout
            >>> success = limiter.acquire(blocking=True, timeout=5.0)
        """
        with self.lock:
            self._refill_tokens()

            if self.tokens >= 1:
                self.tokens -= 1
                return True

            if not blocking:
                return False

            # Calculate wait time needed
            tokens_needed = 1 - self.tokens
            wait_time = tokens_needed / self.rate

        # Release lock while waiting
        if timeout is not None and wait_time > timeout:
            time.sleep(timeout)
            with self.lock:
                self._refill_tokens()
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
                return False

        time.sleep(wait_time)

        # Acquire token after waiting
        with self.lock:
            self._refill_tokens()
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    def _refill_tokens(self) -> None:
        """
        Refill tokens based on elapsed time.

        Calculates how many tokens to add based on time elapsed since last
        update, up to maximum capacity. This method must be called while
        holding the lock.

        Example:
            >>> limiter = RateLimiter(requests_per_second=10)
            >>> time.sleep(0.1)  # Wait 100ms
            >>> with limiter.lock:
            ...     limiter._refill_tokens()
            ...     limiter.tokens  # Should be ~capacity - 1 + 1 = capacity
        """
        now = time.time()
        elapsed = now - self.last_update

        # Calculate tokens to add based on elapsed time
        tokens_to_add = elapsed * self.rate

        # Refill tokens up to capacity
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_update = now

    def get_available_tokens(self) -> float:
        """
        Get current available tokens without consuming them.

        Returns:
            Current number of available tokens

        Example:
            >>> limiter = RateLimiter(requests_per_second=10, capacity=20)
            >>> limiter.get_available_tokens()
            20.0
        """
        with self.lock:
            self._refill_tokens()
            return self.tokens

    def reset(self) -> None:
        """
        Reset the rate limiter to initial state.

        Refills tokens to maximum capacity and updates the last refill time.
        Useful for testing or after configuration changes.

        Example:
            >>> limiter = RateLimiter(requests_per_second=10)
            >>> limiter.acquire()  # Consume a token
            >>> limiter.get_available_tokens()
            9.0
            >>> limiter.reset()
            >>> limiter.get_available_tokens()
            10.0
        """
        with self.lock:
            self.tokens = float(self.capacity)
            self.last_update = time.time()

    def __enter__(self) -> "RateLimiter":
        """
        Context manager entry - acquire a token.

        Returns:
            Self

        Example:
            >>> limiter = RateLimiter(requests_per_second=10)
            >>> with limiter:
            ...     make_api_request()
        """
        self.acquire(blocking=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit - no action needed.

        Example:
            >>> limiter = RateLimiter(requests_per_second=10)
            >>> with limiter:
            ...     make_api_request()
        """
        pass

    def __repr__(self) -> str:
        """
        String representation of rate limiter.

        Returns:
            String representation

        Example:
            >>> limiter = RateLimiter(requests_per_second=10, capacity=20)
            >>> repr(limiter)
            'RateLimiter(rate=10.0, capacity=20)'
        """
        return f"RateLimiter(rate={self.rate}, capacity={self.capacity})"


class RateLimiterManager:
    """
    Manages multiple rate limiters for different API sources.

    Provides a centralized way to manage rate limiters for different
    vulnerability databases (OSV, NVD, GitHub) with their respective
    rate limits.

    Attributes:
        limiters: Dictionary mapping source names to rate limiters

    Example:
        >>> manager = RateLimiterManager()
        >>> manager.register("OSV", requests_per_second=10)
        >>> manager.register("NVD", requests_per_second=1.67)
        >>> manager.acquire("OSV")  # Blocks until OSV token available
        >>> query_osv_api()
    """

    # Default rate limits for each source
    DEFAULT_RATES = {
        "OSV": 10.0,  # 10 requests per second (recommended)
        "NVD": 0.167,  # 5 requests per 30 seconds (~0.167 req/s) without API key
        "NVD_WITH_KEY": 1.67,  # 50 requests per 30 seconds (~1.67 req/s) with API key
        "GITHUB": 0.017,  # 60 requests per hour (~0.017 req/s) unauthenticated
        "GITHUB_WITH_TOKEN": 1.39,  # 5000 requests per hour (~1.39 req/s) authenticated
    }

    def __init__(self):
        """
        Initialize rate limiter manager.

        Example:
            >>> manager = RateLimiterManager()
            >>> len(manager.limiters)
            0
        """
        self.limiters: dict[str, RateLimiter] = {}
        self._lock = Lock()

    def register(
        self,
        source: str,
        requests_per_second: float | None = None,
        capacity: int | None = None,
    ) -> RateLimiter:
        """
        Register or update a rate limiter for a source.

        Args:
            source: API source name (e.g., "OSV", "NVD", "GitHub")
            requests_per_second: Rate limit in requests per second.
                                If None, uses default rate for source.
            capacity: Burst capacity. If None, uses requests_per_second.

        Returns:
            The registered RateLimiter instance

        Raises:
            ValueError: If source is empty or requests_per_second is invalid

        Example:
            >>> manager = RateLimiterManager()
            >>> limiter = manager.register("OSV", requests_per_second=10, capacity=20)
            >>> limiter.rate
            10.0
        """
        if not source:
            raise ValueError("Source name cannot be empty")

        # Use default rate if not specified
        if requests_per_second is None:
            requests_per_second = self.DEFAULT_RATES.get(source, 1.0)

        with self._lock:
            limiter = RateLimiter(requests_per_second, capacity)
            self.limiters[source] = limiter
            return limiter

    def acquire(self, source: str, blocking: bool = True, timeout: float | None = None) -> bool:
        """
        Acquire a token from a specific source's rate limiter.

        Args:
            source: API source name
            blocking: If True, block until token available
            timeout: Maximum time to wait in seconds

        Returns:
            True if token acquired, False otherwise

        Raises:
            ValueError: If source is not registered

        Example:
            >>> manager = RateLimiterManager()
            >>> manager.register("OSV", requests_per_second=10)
            >>> manager.acquire("OSV")
            True
        """
        if source not in self.limiters:
            raise ValueError(f"Source '{source}' not registered")

        return self.limiters[source].acquire(blocking=blocking, timeout=timeout)

    def get_limiter(self, source: str) -> RateLimiter:
        """
        Get the rate limiter for a source.

        Args:
            source: API source name

        Returns:
            RateLimiter instance for the source

        Raises:
            ValueError: If source is not registered

        Example:
            >>> manager = RateLimiterManager()
            >>> manager.register("OSV", requests_per_second=10)
            >>> limiter = manager.get_limiter("OSV")
            >>> limiter.rate
            10.0
        """
        if source not in self.limiters:
            raise ValueError(f"Source '{source}' not registered")

        return self.limiters[source]

    def remove(self, source: str) -> None:
        """
        Remove a rate limiter for a source.

        Args:
            source: API source name

        Example:
            >>> manager = RateLimiterManager()
            >>> manager.register("OSV", requests_per_second=10)
            >>> "OSV" in manager.limiters
            True
            >>> manager.remove("OSV")
            >>> "OSV" in manager.limiters
            False
        """
        with self._lock:
            self.limiters.pop(source, None)

    def get_available_tokens(self, source: str) -> float:
        """
        Get available tokens for a source.

        Args:
            source: API source name

        Returns:
            Current available tokens

        Raises:
            ValueError: If source is not registered

        Example:
            >>> manager = RateLimiterManager()
            >>> manager.register("OSV", requests_per_second=10, capacity=20)
            >>> manager.get_available_tokens("OSV")
            20.0
        """
        if source not in self.limiters:
            raise ValueError(f"Source '{source}' not registered")

        return self.limiters[source].get_available_tokens()

    def reset(self, source: str | None = None) -> None:
        """
        Reset one or all rate limiters.

        Args:
            source: API source name to reset, or None to reset all

        Example:
            >>> manager = RateLimiterManager()
            >>> manager.register("OSV", requests_per_second=10)
            >>> manager.register("NVD", requests_per_second=1)
            >>> manager.reset("OSV")  # Reset only OSV
            >>> manager.reset()  # Reset all
        """
        with self._lock:
            if source is None:
                for limiter in self.limiters.values():
                    limiter.reset()
            elif source in self.limiters:
                self.limiters[source].reset()

    def __repr__(self) -> str:
        """
        String representation of manager.

        Returns:
            String representation

        Example:
            >>> manager = RateLimiterManager()
            >>> manager.register("OSV", requests_per_second=10)
            >>> manager.register("NVD", requests_per_second=1)
            >>> repr(manager)
            'RateLimiterManager(sources=2)'
        """
        return f"RateLimiterManager(sources={len(self.limiters)})"
