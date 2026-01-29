"""
Base HTTP Client Module

This module provides a base HTTP client class with common patterns for session
management, retry logic with exponential backoff, rate limiting, error handling,
and configurable timeouts. This base class is inherited by specific HTTP client
implementations for external services (NVD, OSV, GitHub).
"""

import http.client
import json
import socket
import time
import urllib.error
import urllib.request
from typing import TYPE_CHECKING, Any, Dict, Optional, Union, cast

if TYPE_CHECKING:
    from urllib.request import Request


class HTTPClientError(Exception):
    """Exception raised when an HTTP client request fails."""

    pass


class BaseHTTPClient:
    """
    Base HTTP client with session management, retry logic, and error handling.

    This class provides a foundation for making HTTP requests with robust error
    handling, automatic retries with exponential backoff, rate limiting, and
    configurable timeouts. It uses the standard library's urllib and http.client
    modules for HTTP operations.

    Attributes:
        base_url (str): Base URL for all requests (must be set by subclasses).
        timeout (int): Connection and read timeout in seconds.
        max_retries (int): Maximum number of retry attempts for failed requests.
        retry_backoff_factor (float): Multiplier for exponential backoff calculation.
        rate_limit_delay (float): Minimum delay between requests in seconds.
        user_agent (str): User-Agent header for HTTP requests.
        headers (Dict[str, str]): Default headers to include with all requests.

    Args:
        timeout: Connection and read timeout in seconds (default: 30).
        max_retries: Maximum number of retry attempts (default: 3).
        retry_backoff_factor: Exponential backoff multiplier (default: 0.5).
        rate_limit_delay: Minimum delay between requests in seconds (default: 0.1).
        user_agent: User-Agent string for HTTP requests (default: "Binary-SBOM/0.1.0").

    Raises:
        ValueError: If timeout, max_retries, or rate_limit_delay are invalid.

    Example:
        >>> client = BaseHTTPClient(timeout=10, max_retries=2)
        >>> client.base_url = "https://api.example.com"
        >>> response = client.request("GET", "/endpoint")
        >>> data = json.loads(response)
    """

    # Base URL should be overridden by subclasses
    base_url: str = ""

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        retry_backoff_factor: float = 0.5,
        rate_limit_delay: float = 0.1,
        user_agent: str = "Binary-SBOM/0.1.0",
    ) -> None:
        """
        Initialize the BaseHTTPClient with configurable parameters.

        Args:
            timeout: Connection and read timeout in seconds.
            max_retries: Maximum number of retry attempts for failed requests.
            retry_backoff_factor: Multiplier for exponential backoff calculation.
            rate_limit_delay: Minimum delay between requests in seconds.
            user_agent: User-Agent string for HTTP requests.
        """
        # Validate timeout
        if timeout <= 0:
            raise ValueError(
                f"Timeout must be positive, got {timeout}. "
                "Recommended values: 10-60 seconds."
            )

        # Validate max_retries
        if max_retries < 0:
            raise ValueError(
                f"Max retries must be non-negative, got {max_retries}. "
                "Use 0 to disable retries, or >=1 to enable."
            )

        # Validate retry_backoff_factor
        if retry_backoff_factor < 0:
            raise ValueError(
                f"Retry backoff factor must be non-negative, got {retry_backoff_factor}. "
                "Recommended values: 0.1-2.0."
            )

        # Validate rate_limit_delay
        if rate_limit_delay < 0:
            raise ValueError(
                f"Rate limit delay must be non-negative, got {rate_limit_delay}. "
                "Use 0 to disable rate limiting."
            )

        self.timeout: int = timeout
        self.max_retries: int = max_retries
        self.retry_backoff_factor: float = retry_backoff_factor
        self.rate_limit_delay: float = rate_limit_delay
        self.user_agent: str = user_agent
        self.headers: Dict[str, str] = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }

        # Track last request time for rate limiting
        self._last_request_time: Optional[float] = None

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Make an HTTP request with retry logic and error handling.

        This method sends an HTTP request to the specified endpoint with automatic
        retries on failure, exponential backoff, rate limiting, and comprehensive
        error handling. It supports both GET and POST requests.

        Args:
            method: HTTP method ("GET" or "POST").
            endpoint: API endpoint path (will be appended to base_url).
            params: Query parameters for GET requests (optional).
            data: Request body data for POST requests (optional).
            headers: Additional headers to include with the request (optional).

        Returns:
            Response body as string.

        Raises:
            ValueError: If method is invalid or endpoint is empty.
            HTTPClientError: If the request fails after all retries.
            urllib.error.HTTPError: If the server returns an HTTP error status.
            urllib.error.URLError: If the URL is invalid or the server is unreachable.
            socket.timeout: If the request times out.

        Example:
            >>> client = BaseHTTPClient()
            >>> client.base_url = "https://api.example.com"
            >>> response = client.request("GET", "/users/123")
            >>> data = json.loads(response)
        """
        # Validate method
        method = method.upper()
        if method not in ("GET", "POST"):
            raise ValueError(
                f"Invalid HTTP method: {method}. "
                "Supported methods: GET, POST."
            )

        # Validate endpoint
        if not endpoint:
            raise ValueError(
                "Endpoint cannot be empty. "
                "Provide a valid API endpoint path (e.g., '/api/v1/resource')."
            )

        # Validate base_url is set
        if not self.base_url:
            raise ValueError(
                "base_url is not set. "
                "Set base_url to the API base URL before making requests."
            )

        # Build full URL
        url = self._build_url(endpoint, params)

        # Prepare request
        request = self._prepare_request(method, url, data, headers)

        # Apply rate limiting
        self._apply_rate_limiting()

        # Execute request with retry logic
        response = self._execute_request_with_retry(request)

        return response

    def _build_url(
        self, endpoint: str, params: Optional[Dict[str, Any]]
    ) -> str:
        """
        Build full URL by combining base_url, endpoint, and query parameters.

        Args:
            endpoint: API endpoint path.
            params: Query parameters (optional).

        Returns:
            Complete URL with query string if params are provided.
        """
        # Ensure endpoint starts with / if base_url doesn't end with /
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Add query parameters if provided
        if params:
            from urllib.parse import urlencode

            query_string = urlencode(params)
            url = f"{url}?{query_string}"

        return url

    def _prepare_request(
        self,
        method: str,
        url: str,
        data: Optional[Dict[str, Any]],
        headers: Optional[Dict[str, str]],
    ) -> "Request":
        """
        Prepare urllib Request object with method, headers, and body.

        Args:
            method: HTTP method (GET or POST).
            url: Full URL with query parameters.
            data: Request body data for POST requests.
            headers: Additional headers to merge with default headers.

        Returns:
            Configured urllib.request.Request object.
        """
        # Merge default headers with custom headers
        merged_headers = self.headers.copy()
        if headers:
            merged_headers.update(headers)

        # Prepare request body
        body = None
        if data:
            body = json.dumps(data).encode("utf-8")
            merged_headers["Content-Type"] = "application/json"

        # Create Request object
        request = urllib.request.Request(
            url=url,
            data=body,
            headers=merged_headers,
            method=method,
        )

        return request

    def _apply_rate_limiting(self) -> None:
        """
        Apply rate limiting by sleeping if necessary.

        Ensures that requests are spaced at least rate_limit_delay seconds apart.
        """
        if self._last_request_time is not None:
            elapsed = time.time() - self._last_request_time
            if elapsed < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - elapsed
                time.sleep(sleep_time)

        self._last_request_time = time.time()

    def _execute_request_with_retry(self, request: "Request") -> str:
        """
        Execute HTTP request with automatic retry logic and exponential backoff.

        Args:
            request: Configured urllib.request.Request object.

        Returns:
            Response body as string.

        Raises:
            HTTPClientError: If request fails after all retries.
        """
        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                # Make the HTTP request
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    # Read response body
                    response_data: str = response.read().decode("utf-8")

                    # Check for HTTP error status codes
                    if response.status >= 400:
                        error_msg = (
                            f"HTTP {response.status}: {response.reason}"
                        )
                        raise HTTPClientError(error_msg)

                    return response_data

            except urllib.error.HTTPError as e:
                # Server returned an error response
                last_exception = e

                # Don't retry client errors (4xx)
                if 400 <= e.code < 500:
                    raise HTTPClientError(
                        f"Client error HTTP {e.code}: {e.reason}. "
                        f"Request: {request.full_url if hasattr(request, 'full_url') else request.host}"
                    ) from e

                # Retry server errors (5xx) and rate limit errors (429)
                if attempt < self.max_retries:
                    backoff_time = self._calculate_backoff(attempt)
                    time.sleep(backoff_time)
                    continue

                # Re-raise if all retries exhausted
                raise HTTPClientError(
                    f"Server error HTTP {e.code}: {e.reason} after {attempt + 1} attempts. "
                    f"Request: {request.full_url if hasattr(request, 'full_url') else request.host}"
                ) from e

            except urllib.error.URLError as e:
                # Network or URL error
                last_exception = e

                if attempt < self.max_retries:
                    backoff_time = self._calculate_backoff(attempt)
                    time.sleep(backoff_time)
                    continue

                # Re-raise if all retries exhausted
                raise HTTPClientError(
                    f"Network error: {e.reason} after {attempt + 1} attempts. "
                    f"Request: {request.full_url if hasattr(request, 'full_url') else request.host}"
                ) from e

            except socket.timeout as e:
                # Request timeout
                last_exception = e

                if attempt < self.max_retries:
                    backoff_time = self._calculate_backoff(attempt)
                    time.sleep(backoff_time)
                    continue

                # Re-raise if all retries exhausted
                raise HTTPClientError(
                    f"Request timeout after {self.timeout}s on {request.full_url if hasattr(request, 'full_url') else request.host} "
                    f"after {attempt + 1} attempts"
                ) from e

            except (http.client.HTTPException, OSError) as e:
                # HTTP protocol error or connection error
                last_exception = e

                if attempt < self.max_retries:
                    backoff_time = self._calculate_backoff(attempt)
                    time.sleep(backoff_time)
                    continue

                # Re-raise if all retries exhausted
                raise HTTPClientError(
                    f"Connection error: {e} after {attempt + 1} attempts. "
                    f"Request: {request.full_url if hasattr(request, 'full_url') else request.host}"
                ) from e

        # This should never be reached, but handle the case
        if last_exception:
            raise HTTPClientError(
                f"Request failed after {self.max_retries + 1} attempts: {last_exception}"
            )

        raise HTTPClientError("Request failed: Unknown error")

    def _calculate_backoff(self, attempt: int) -> float:
        """
        Calculate exponential backoff delay for retry attempts.

        Args:
            attempt: Current attempt number (0-indexed).

        Returns:
            Delay in seconds before next retry.
        """
        backoff_delay: float = self.retry_backoff_factor * (2**attempt)
        return backoff_delay

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Convenience method for making GET requests.

        Args:
            endpoint: API endpoint path.
            params: Query parameters (optional).
            headers: Additional headers (optional).

        Returns:
            Response body as string.

        Raises:
            HTTPClientError: If the request fails.
            ValueError: If endpoint is empty.

        Example:
            >>> client = BaseHTTPClient()
            >>> client.base_url = "https://api.example.com"
            >>> response = client.get("/users/123")
            >>> data = json.loads(response)
        """
        return self.request("GET", endpoint, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Convenience method for making POST requests.

        Args:
            endpoint: API endpoint path.
            data: Request body data (optional).
            headers: Additional headers (optional).

        Returns:
            Response body as string.

        Raises:
            HTTPClientError: If the request fails.
            ValueError: If endpoint is empty.

        Example:
            >>> client = BaseHTTPClient()
            >>> client.base_url = "https://api.example.com"
            >>> response = client.post("/users", data={"name": "John"})
            >>> result = json.loads(response)
        """
        return self.request("POST", endpoint, data=data, headers=headers)


__all__ = [
    "BaseHTTPClient",
    "HTTPClientError",
]
