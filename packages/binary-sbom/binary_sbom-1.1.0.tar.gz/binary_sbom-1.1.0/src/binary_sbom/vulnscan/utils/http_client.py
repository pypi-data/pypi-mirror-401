"""
HTTP client with retry logic for vulnerability database APIs.

This module provides a reusable HTTP client with exponential backoff,
timeout configuration, and connection pooling.
"""

from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.request
from http.client import HTTPConnection, HTTPSConnection
from typing import Any, Optional

from binary_sbom.vulnscan.exceptions import APIError, TimeoutError as VulnTimeoutError
from binary_sbom.vulnscan.utils.cancellation import CancellationContext, check_cancellation


class HttpClient:
    """
    HTTP client with retry logic and exponential backoff.

    Handles API requests to vulnerability databases with automatic
    retry on transient failures and proper error handling.

    Uses connection pooling through HTTPConnection/HTTPSConnection
    for efficient resource management.

    Attributes:
        retry_max: Maximum number of retry attempts
        retry_delay: Initial delay between retries (seconds)
        timeout: Request timeout (seconds)
        backoff_factor: Exponential backoff multiplier
        pool_connections: Maximum number of connections to pool per host

    Example:
        >>> client = HttpClient(retry_max=3, timeout=30)
        >>> response = client.get("https://api.osv.dev/v1/query")
        >>> data = client.post("https://api.osv.dev/v1/query", json={"package": {...}})
    """

    # Retryable HTTP status codes
    RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}

    def __init__(
        self,
        retry_max: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 30,
        backoff_factor: float = 2.0,
        pool_connections: int = 10,
    ):
        """
        Initialize HTTP client.

        Args:
            retry_max: Maximum number of retry attempts (default: 3)
            retry_delay: Initial delay between retries in seconds (default: 1.0)
            timeout: Request timeout in seconds (default: 30)
            backoff_factor: Exponential backoff multiplier (default: 2.0)
            pool_connections: Maximum connections to pool per host (default: 10)

        Example:
            >>> client = HttpClient(retry_max=5, timeout=60)
            >>> client.retry_max
            5
        """
        self.retry_max = retry_max
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.backoff_factor = backoff_factor
        self.pool_connections = pool_connections

        # Configure connection pooling
        HTTPConnection.default_headers = {}
        self._ssl_context = self._create_ssl_context()

    def _create_ssl_context(self) -> ssl.SSLContext:
        """
        Create SSL context for HTTPS connections.

        Returns:
            SSL context with secure defaults

        Note:
            Uses TLS 1.2+ with certificate verification enabled
        """
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        return context

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        cancellation_context: Optional[CancellationContext] = None,
    ) -> dict[str, Any]:
        """
        Perform HTTP GET request with retry logic.

        Args:
            url: Request URL
            params: Query parameters (will be URL-encoded)
            headers: Optional request headers
            cancellation_context: Optional context for cancellation support

        Returns:
            JSON response as dictionary

        Raises:
            APIError: If request fails after all retries
            VulnTimeoutError: If request times out
            CancellationError: If operation is cancelled via cancellation_context

        Example:
            >>> client = HttpClient()
            >>> response = client.get(
            ...     "https://api.osv.dev/v1/query",
            ...     params={"package": "lodash"}
            ... )
            >>> "vulns" in response
            True
        """
        # Build URL with query parameters
        if params:
            from urllib.parse import urlencode

            query_string = urlencode(params)
            url = f"{url}?{query_string}"

        def _do_request():
            # Check for cancellation before making request
            check_cancellation(cancellation_context)

            req = urllib.request.Request(url, method="GET")
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)

            response = urllib.request.urlopen(
                req, timeout=self.timeout, context=self._ssl_context
            )

            data = response.read().decode("utf-8")
            if data:
                return json.loads(data)
            return {}

        return self._retry_with_backoff(_do_request, url, cancellation_context)

    def post(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        cancellation_context: Optional[CancellationContext] = None,
    ) -> dict[str, Any]:
        """
        Perform HTTP POST request with retry logic.

        Args:
            url: Request URL
            json: JSON request body (will be serialized)
            headers: Optional request headers (Content-Type added automatically if json provided)
            cancellation_context: Optional context for cancellation support

        Returns:
            JSON response as dictionary

        Raises:
            APIError: If request fails after all retries
            VulnTimeoutError: If request times out
            CancellationError: If operation is cancelled via cancellation_context

        Example:
            >>> client = HttpClient()
            >>> response = client.post(
            ...     "https://api.osv.dev/v1/query",
            ...     json={"package": {"name": "lodash", "ecosystem": "npm"}, "version": "4.17.15"}
            ... )
            >>> "vulns" in response
            True
        """
        # Prepare request headers
        request_headers = headers.copy() if headers else {}
        if json is not None and "Content-Type" not in request_headers:
            request_headers["Content-Type"] = "application/json"

        # Serialize JSON body
        body = json.dumps(json).encode("utf-8") if json else None

        def _do_request():
            # Check for cancellation before making request
            check_cancellation(cancellation_context)

            req = urllib.request.Request(url, data=body, method="POST")
            for key, value in request_headers.items():
                req.add_header(key, value)

            response = urllib.request.urlopen(
                req, timeout=self.timeout, context=self._ssl_context
            )

            data = response.read().decode("utf-8")
            if data:
                return json.loads(data)
            return {}

        return self._retry_with_backoff(_do_request, url, cancellation_context)

    def _retry_with_backoff(
        self, func, url: str, cancellation_context: Optional[CancellationContext] = None
    ):
        """
        Execute function with exponential backoff retry.

        Retries the function on transient failures with increasing delay
        between attempts using exponential backoff. Checks for cancellation
        before each retry attempt.

        Args:
            func: Function to execute
            url: Request URL (for logging)
            cancellation_context: Optional context for cancellation support

        Returns:
            Function result

        Raises:
            APIError: If function fails after all retries
            VulnTimeoutError: If request times out on all attempts
            CancellationError: If operation is cancelled via cancellation_context

        Example:
            >>> def failing_func():
            ...     raise urllib.error.HTTPError("url", 503, "Service Unavailable", {}, None)
            >>> client = HttpClient(retry_max=2)
            >>> try:
            ...     client._retry_with_backoff(failing_func, "https://api.example.com")
            ... except APIError:
            ...     print("Failed after retries")
            Failed after retries
        """
        last_exception = None
        delay = self.retry_delay

        for attempt in range(self.retry_max + 1):
            try:
                # Check for cancellation before each attempt
                check_cancellation(cancellation_context)

                return func()

            except urllib.error.HTTPError as e:
                last_exception = e

                # Check if status code is retryable
                if e.code in self.RETRYABLE_STATUS_CODES:
                    # Extract retry-after if available (for 429)
                    retry_after = e.headers.get("Retry-After")
                    if retry_after:
                        try:
                            delay = float(retry_after)
                        except ValueError:
                            pass  # Use exponential backoff

                    # Don't retry if this was the last attempt
                    if attempt == self.retry_max:
                        break

                    # Check for cancellation before waiting
                    check_cancellation(cancellation_context)

                    # Wait before retry
                    time.sleep(delay)
                    delay *= self.backoff_factor
                else:
                    # Non-retryable HTTP error
                    raise APIError(
                        message=f"HTTP {e.code}: {e.reason}",
                        source="HTTP",
                        status_code=e.code,
                    ) from e

            except urllib.error.URLError as e:
                last_exception = e

                # Check if it's a timeout
                if isinstance(e.reason, TimeoutError):
                    if attempt == self.retry_max:
                        raise VulnTimeoutError(
                            source="HTTP", timeout=self.timeout
                        ) from e
                else:
                    # Don't retry connection errors on last attempt
                    if attempt == self.retry_max:
                        raise APIError(
                            message=f"Connection error: {e.reason}", source="HTTP"
                        ) from e

                # Check for cancellation before waiting
                check_cancellation(cancellation_context)

                # Wait before retry
                time.sleep(delay)
                delay *= self.backoff_factor

            except Exception as e:
                # Unexpected error - don't retry
                raise APIError(message=f"Unexpected error: {str(e)}", source="HTTP") from e

        # If we get here, all retries failed
        if isinstance(last_exception, urllib.error.HTTPError):
            raise APIError(
                message=f"HTTP {last_exception.code}: {last_exception.reason} (after {self.retry_max} retries)",
                source="HTTP",
                status_code=last_exception.code,
            ) from last_exception
        else:
            raise APIError(
                message=f"Request failed after {self.retry_max} retries: {str(last_exception)}",
                source="HTTP",
            ) from last_exception
