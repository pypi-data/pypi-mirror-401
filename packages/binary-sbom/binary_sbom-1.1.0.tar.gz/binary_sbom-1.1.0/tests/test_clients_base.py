"""
Unit tests for the BaseHTTPClient module.

Tests session management, retry logic, rate limiting, and error handling.
"""

import json
import socket
import time
from unittest.mock import MagicMock, Mock, patch

import pytest
from urllib.error import HTTPError, URLError

from binary_sbom.clients.base import (
    BaseHTTPClient,
    HTTPClientError,
)


class TestBaseHTTPClientInit:
    """Test BaseHTTPClient initialization and validation."""

    def test_init_with_default_parameters(self):
        """Test initialization with default parameters."""
        client = BaseHTTPClient()

        assert client.timeout == 30
        assert client.max_retries == 3
        assert client.retry_backoff_factor == 0.5
        assert client.rate_limit_delay == 0.1
        assert client.user_agent == "Binary-SBOM/0.1.0"
        assert "User-Agent" in client.headers
        assert "Accept" in client.headers

    def test_init_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        client = BaseHTTPClient(
            timeout=10,
            max_retries=5,
            retry_backoff_factor=1.0,
            rate_limit_delay=0.5,
            user_agent="CustomAgent/1.0"
        )

        assert client.timeout == 10
        assert client.max_retries == 5
        assert client.retry_backoff_factor == 1.0
        assert client.rate_limit_delay == 0.5
        assert client.user_agent == "CustomAgent/1.0"

    def test_init_with_invalid_timeout_zero(self):
        """Test that zero timeout raises ValueError."""
        with pytest.raises(ValueError, match="Timeout must be positive"):
            BaseHTTPClient(timeout=0)

    def test_init_with_invalid_timeout_negative(self):
        """Test that negative timeout raises ValueError."""
        with pytest.raises(ValueError, match="Timeout must be positive"):
            BaseHTTPClient(timeout=-10)

    def test_init_with_invalid_max_retries(self):
        """Test that negative max_retries raises ValueError."""
        with pytest.raises(ValueError, match="Max retries must be non-negative"):
            BaseHTTPClient(max_retries=-1)

    def test_init_with_zero_max_retries(self):
        """Test that zero max_retries is accepted (disables retries)."""
        client = BaseHTTPClient(max_retries=0)
        assert client.max_retries == 0

    def test_init_with_invalid_backoff_factor(self):
        """Test that negative backoff_factor raises ValueError."""
        with pytest.raises(ValueError, match="Retry backoff factor must be non-negative"):
            BaseHTTPClient(retry_backoff_factor=-0.5)

    def test_init_with_zero_backoff_factor(self):
        """Test that zero backoff_factor is accepted."""
        client = BaseHTTPClient(retry_backoff_factor=0)
        assert client.retry_backoff_factor == 0

    def test_init_with_invalid_rate_limit_delay(self):
        """Test that negative rate_limit_delay raises ValueError."""
        with pytest.raises(ValueError, match="Rate limit delay must be non-negative"):
            BaseHTTPClient(rate_limit_delay=-1.0)

    def test_init_with_zero_rate_limit_delay(self):
        """Test that zero rate_limit_delay is accepted (disables rate limiting)."""
        client = BaseHTTPClient(rate_limit_delay=0)
        assert client.rate_limit_delay == 0


class TestBaseHTTPClientRequest:
    """Test HTTP request functionality."""

    def setup_method(self):
        """Set up test client with base_url."""
        self.client = BaseHTTPClient()
        self.client.base_url = "https://api.example.com"

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_request_get_success(self, mock_urlopen):
        """Test successful GET request."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"result": "success"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        response = self.client.request("GET", "/test")

        assert response == '{"result": "success"}'
        mock_urlopen.assert_called_once()

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_request_post_success(self, mock_urlopen):
        """Test successful POST request."""
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.read.return_value = b'{"created": true}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        response = self.client.request("POST", "/create", data={"name": "test"})

        assert response == '{"created": true}'
        mock_urlopen.assert_called_once()

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_request_with_query_params(self, mock_urlopen):
        """Test request with query parameters."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'[]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        response = self.client.request("GET", "/search", params={"q": "test"})

        assert response == '[]'
        # Check that URL includes query parameters
        call_args = mock_urlopen.call_args[0][0]
        assert "q=test" in call_args.full_url

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_request_with_custom_headers(self, mock_urlopen):
        """Test request with custom headers."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        response = self.client.request(
            "GET",
            "/test",
            headers={"Authorization": "Bearer token123"}
        )

        assert response == '{}'
        # Check that custom headers are included
        call_args = mock_urlopen.call_args[0][0]
        assert call_args.headers["Authorization"] == "Bearer token123"

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_request_with_json_body(self, mock_urlopen):
        """Test POST request with JSON body."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"id": 123}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        data = {"name": "test", "value": 42}
        response = self.client.request("POST", "/data", data=data)

        assert response == '{"id": 123}'
        # Check that Content-Type is set to application/json (case-insensitive)
        call_args = mock_urlopen.call_args[0][0]
        headers_dict = dict(call_args.headers)
        # Check for both Content-Type and Content-type (header names can be case-insensitive)
        content_type = headers_dict.get("Content-Type") or headers_dict.get("Content-type", "")
        assert "application/json" in content_type

    def test_request_with_invalid_method(self):
        """Test that invalid HTTP method raises ValueError."""
        with pytest.raises(ValueError, match="Invalid HTTP method"):
            self.client.request("DELETE", "/test")

    def test_request_with_empty_endpoint(self):
        """Test that empty endpoint raises ValueError."""
        with pytest.raises(ValueError, match="Endpoint cannot be empty"):
            self.client.request("GET", "")

    def test_request_without_base_url(self):
        """Test that missing base_url raises ValueError."""
        client = BaseHTTPClient()
        # Don't set base_url

        with pytest.raises(ValueError, match="base_url is not set"):
            client.request("GET", "/test")


class TestBaseHTTPClientGet:
    """Test GET convenience method."""

    def setup_method(self):
        """Set up test client with base_url."""
        self.client = BaseHTTPClient()
        self.client.base_url = "https://api.example.com"

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_get_success(self, mock_urlopen):
        """Test successful GET request."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"data": "value"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        response = self.client.get("/resource")

        assert response == '{"data": "value"}'

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_get_with_params(self, mock_urlopen):
        """Test GET request with query parameters."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'[]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        response = self.client.get("/search", params={"key": "value"})

        assert response == '[]'


class TestBaseHTTPClientPost:
    """Test POST convenience method."""

    def setup_method(self):
        """Set up test client with base_url."""
        self.client = BaseHTTPClient()
        self.client.base_url = "https://api.example.com"

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_post_success(self, mock_urlopen):
        """Test successful POST request."""
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.read.return_value = b'{"created": true}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        response = self.client.post("/create", data={"name": "test"})

        assert response == '{"created": true}'

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_post_without_data(self, mock_urlopen):
        """Test POST request without data."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        response = self.client.post("/endpoint")

        assert response == '{}'


class TestBaseHTTPClientRetry:
    """Test retry logic with exponential backoff."""

    def setup_method(self):
        """Set up test client with base_url."""
        self.client = BaseHTTPClient(max_retries=3, retry_backoff_factor=0.1)
        self.client.base_url = "https://api.example.com"

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    @patch('binary_sbom.clients.base.time.sleep')
    def test_retry_on_server_error_500(self, mock_sleep, mock_urlopen):
        """Test retry on HTTP 500 server error."""
        # First two calls fail, third succeeds
        mock_error = HTTPError(
            url="https://api.example.com/test",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None
        )

        # Create success response with proper __enter__ support
        mock_success_response = MagicMock()
        mock_success_response.status = 200
        mock_success_response.read.return_value = b'{"success": true}'
        mock_success_context = MagicMock()
        mock_success_context.__enter__ = MagicMock(return_value=mock_success_response)
        mock_success_context.__exit__ = MagicMock(return_value=False)

        mock_urlopen.side_effect = [
            mock_error,
            mock_error,
            mock_success_context
        ]

        response = self.client.request("GET", "/test")

        assert response == '{"success": true}'
        assert mock_urlopen.call_count == 3
        # Verify sleep was called twice (between retries)
        assert mock_sleep.call_count == 2

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    @patch('binary_sbom.clients.base.time.sleep')
    def test_retry_on_server_error_503(self, mock_sleep, mock_urlopen):
        """Test retry on HTTP 503 service unavailable."""
        mock_error = HTTPError(
            url="https://api.example.com/test",
            code=503,
            msg="Service Unavailable",
            hdrs={},
            fp=None
        )

        # Create success response with proper __enter__ support
        mock_success_response = MagicMock()
        mock_success_response.status = 200
        mock_success_response.read.return_value = b'OK'
        mock_success_context = MagicMock()
        mock_success_context.__enter__ = MagicMock(return_value=mock_success_response)
        mock_success_context.__exit__ = MagicMock(return_value=False)

        mock_urlopen.side_effect = [
            mock_error,
            mock_success_context
        ]

        response = self.client.request("GET", "/test")

        assert response == 'OK'
        assert mock_urlopen.call_count == 2

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    @patch('binary_sbom.clients.base.time.sleep')
    def test_retry_on_url_error(self, mock_sleep, mock_urlopen):
        """Test retry on URLError (network error)."""
        # Create success response with proper __enter__ support
        mock_success_response = MagicMock()
        mock_success_response.status = 200
        mock_success_response.read.return_value = b'{"recovered": true}'
        mock_success_context = MagicMock()
        mock_success_context.__enter__ = MagicMock(return_value=mock_success_response)
        mock_success_context.__exit__ = MagicMock(return_value=False)

        mock_urlopen.side_effect = [
            URLError("Network unreachable"),
            URLError("Network unreachable"),
            mock_success_context
        ]

        response = self.client.request("GET", "/test")

        assert response == '{"recovered": true}'
        assert mock_urlopen.call_count == 3

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    @patch('binary_sbom.clients.base.time.sleep')
    def test_retry_on_socket_timeout(self, mock_sleep, mock_urlopen):
        """Test retry on socket timeout."""
        # Create success response with proper __enter__ support
        mock_success_response = MagicMock()
        mock_success_response.status = 200
        mock_success_response.read.return_value = b'{"data": "value"}'
        mock_success_context = MagicMock()
        mock_success_context.__enter__ = MagicMock(return_value=mock_success_response)
        mock_success_context.__exit__ = MagicMock(return_value=False)

        mock_urlopen.side_effect = [
            socket.timeout("Connection timed out"),
            mock_success_context
        ]

        response = self.client.request("GET", "/test")

        assert response == '{"data": "value"}'
        assert mock_urlopen.call_count == 2

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_no_retry_on_client_error_400(self, mock_urlopen):
        """Test that client errors (4xx) are not retried."""
        mock_error = HTTPError(
            url="https://api.example.com/test",
            code=400,
            msg="Bad Request",
            hdrs={},
            fp=None
        )
        mock_urlopen.side_effect = [mock_error]

        with pytest.raises(HTTPClientError, match="Client error HTTP 400"):
            self.client.request("GET", "/test")

        # Should only be called once (no retry)
        assert mock_urlopen.call_count == 1

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_no_retry_on_client_error_404(self, mock_urlopen):
        """Test that 404 errors are not retried."""
        mock_error = HTTPError(
            url="https://api.example.com/test",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=None
        )
        mock_urlopen.side_effect = [mock_error]

        with pytest.raises(HTTPClientError, match="Client error HTTP 404"):
            self.client.request("GET", "/test")

        assert mock_urlopen.call_count == 1

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    @patch('binary_sbom.clients.base.time.sleep')
    def test_max_retries_exhausted(self, mock_sleep, mock_urlopen):
        """Test that max retries limit is respected."""
        mock_urlopen.side_effect = URLError("Network unreachable")

        with pytest.raises(HTTPClientError, match="Network error"):
            self.client.request("GET", "/test")

        # Should be called max_retries + 1 times (initial attempt + retries)
        assert mock_urlopen.call_count == 4

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_no_retries_when_disabled(self, mock_urlopen):
        """Test that retries can be disabled."""
        client = BaseHTTPClient(max_retries=0)
        client.base_url = "https://api.example.com"

        mock_urlopen.side_effect = URLError("Network error")

        with pytest.raises(HTTPClientError, match="Network error"):
            client.request("GET", "/test")

        # Should only be called once (no retries)
        assert mock_urlopen.call_count == 1


class TestBaseHTTPClientBackoff:
    """Test exponential backoff calculation."""

    def test_backoff_calculation(self):
        """Test exponential backoff calculation."""
        client = BaseHTTPClient(retry_backoff_factor=0.5)

        # Attempt 0: 0.5 * 2^0 = 0.5
        assert client._calculate_backoff(0) == 0.5
        # Attempt 1: 0.5 * 2^1 = 1.0
        assert client._calculate_backoff(1) == 1.0
        # Attempt 2: 0.5 * 2^2 = 2.0
        assert client._calculate_backoff(2) == 2.0
        # Attempt 3: 0.5 * 2^3 = 4.0
        assert client._calculate_backoff(3) == 4.0

    def test_backoff_with_zero_factor(self):
        """Test backoff with zero factor (no delay)."""
        client = BaseHTTPClient(retry_backoff_factor=0)

        assert client._calculate_backoff(0) == 0
        assert client._calculate_backoff(1) == 0
        assert client._calculate_backoff(2) == 0

    def test_backoff_with_custom_factor(self):
        """Test backoff with custom factor."""
        client = BaseHTTPClient(retry_backoff_factor=1.0)

        # Attempt 0: 1.0 * 2^0 = 1.0
        assert client._calculate_backoff(0) == 1.0
        # Attempt 1: 1.0 * 2^1 = 2.0
        assert client._calculate_backoff(1) == 2.0
        # Attempt 2: 1.0 * 2^2 = 4.0
        assert client._calculate_backoff(2) == 4.0


class TestBaseHTTPClientRateLimiting:
    """Test rate limiting functionality."""

    def setup_method(self):
        """Set up test client with base_url."""
        self.client = BaseHTTPClient(rate_limit_delay=0.2)
        self.client.base_url = "https://api.example.com"

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    @patch('binary_sbom.clients.base.time.sleep')
    @patch('binary_sbom.clients.base.time.time')
    def test_rate_limit_first_request_no_delay(self, mock_time, mock_sleep, mock_urlopen):
        """Test that first request has no delay."""
        mock_time.return_value = 1000.0
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'OK'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        self.client.request("GET", "/test")

        # sleep should not be called for first request
        mock_sleep.assert_not_called()

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    @patch('binary_sbom.clients.base.time.sleep')
    @patch('binary_sbom.clients.base.time.time')
    def test_rate_limit_subsequent_request_within_delay(self, mock_time, mock_sleep, mock_urlopen):
        """Test rate limiting when requests are too close."""
        # First request at t=1000
        mock_time.side_effect = [1000.0, 1000.1, 1000.2]
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'OK'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # First request
        self.client.request("GET", "/test1")

        # Reset mock for second request
        mock_sleep.reset_mock()

        # Second request after 0.1s (less than 0.2s delay)
        self.client.request("GET", "/test2")

        # Should sleep for approximately 0.1s (0.2 - 0.1)
        assert mock_sleep.call_count == 1
        sleep_time = mock_sleep.call_args[0][0]
        assert abs(sleep_time - 0.1) < 0.001  # Allow small floating point error

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    @patch('binary_sbom.clients.base.time.sleep')
    @patch('binary_sbom.clients.base.time.time')
    def test_rate_limit_subsequent_request_after_delay(self, mock_time, mock_sleep, mock_urlopen):
        """Test no rate limiting delay when enough time has passed."""
        # First request at t=1000, second at t=1000.3 (more than 0.2s delay)
        mock_time.side_effect = [1000.0, 1000.3, 1000.3]
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'OK'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # First request
        self.client.request("GET", "/test1")

        # Reset mock for second request
        mock_sleep.reset_mock()

        # Second request after 0.3s (more than 0.2s delay)
        self.client.request("GET", "/test2")

        # Should not sleep
        mock_sleep.assert_not_called()

    def test_rate_limit_disabled(self):
        """Test that rate limiting can be disabled."""
        client = BaseHTTPClient(rate_limit_delay=0)
        client.base_url = "https://api.example.com"

        with patch('binary_sbom.clients.base.urllib.request.urlopen') as mock_urlopen:
            with patch('binary_sbom.clients.base.time.sleep') as mock_sleep:
                mock_response = MagicMock()
                mock_response.status = 200
                mock_response.read.return_value = b'OK'
                mock_urlopen.return_value.__enter__.return_value = mock_response

                # Make multiple requests rapidly
                for _ in range(5):
                    client.request("GET", "/test")

                # Sleep should never be called
                mock_sleep.assert_not_called()


class TestBaseHTTPClientErrorHandling:
    """Test error handling and error messages."""

    def setup_method(self):
        """Set up test client with base_url."""
        self.client = BaseHTTPClient(max_retries=2)
        self.client.base_url = "https://api.example.com"

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_http_client_error_on_server_error(self, mock_urlopen):
        """Test HTTPClientError raised after retries on server error."""
        mock_error = HTTPError(
            url="https://api.example.com/test",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None
        )
        mock_urlopen.side_effect = mock_error

        with pytest.raises(HTTPClientError, match="Server error HTTP 500"):
            self.client.request("GET", "/test")

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_http_client_error_on_network_error(self, mock_urlopen):
        """Test HTTPClientError raised after retries on network error."""
        mock_urlopen.side_effect = URLError("Network unreachable")

        with pytest.raises(HTTPClientError, match="Network error"):
            self.client.request("GET", "/test")

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_http_client_error_on_timeout(self, mock_urlopen):
        """Test HTTPClientError raised after retries on timeout."""
        mock_urlopen.side_effect = socket.timeout("Connection timed out")

        with pytest.raises(HTTPClientError, match="Request timeout"):
            self.client.request("GET", "/test")

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_http_client_error_includes_attempt_count(self, mock_urlopen):
        """Test that error message includes attempt count."""
        mock_urlopen.side_effect = URLError("Network error")

        with pytest.raises(HTTPClientError, match="after 3 attempts"):
            self.client.request("GET", "/test")

    @patch('binary_sbom.clients.base.urllib.request.urlopen')
    def test_http_client_error_on_4xx_no_retry(self, mock_urlopen):
        """Test that 4xx errors raise HTTPClientError immediately."""
        mock_error = HTTPError(
            url="https://api.example.com/test",
            code=403,
            msg="Forbidden",
            hdrs={},
            fp=None
        )
        mock_urlopen.side_effect = mock_error

        with pytest.raises(HTTPClientError, match="Client error HTTP 403"):
            self.client.request("GET", "/test")


class TestBuildURL:
    """Test URL building functionality."""

    def setup_method(self):
        """Set up test client with base_url."""
        self.client = BaseHTTPClient()
        self.client.base_url = "https://api.example.com"

    def test_build_url_basic(self):
        """Test basic URL building."""
        url = self.client._build_url("/test", None)
        assert url == "https://api.example.com/test"

    def test_build_url_with_trailing_slash(self):
        """Test URL building with trailing slash in base_url."""
        self.client.base_url = "https://api.example.com/"
        url = self.client._build_url("test", None)
        assert url == "https://api.example.com/test"

    def test_build_url_with_leading_slash(self):
        """Test URL building with leading slash in endpoint."""
        url = self.client._build_url("/test", None)
        assert url == "https://api.example.com/test"

    def test_build_url_without_leading_slash(self):
        """Test URL building without leading slash in endpoint."""
        url = self.client._build_url("test", None)
        assert url == "https://api.example.com/test"

    def test_build_url_with_query_params(self):
        """Test URL building with query parameters."""
        url = self.client._build_url("/search", {"q": "test", "limit": "10"})
        assert url == "https://api.example.com/search?q=test&limit=10"

    def test_build_url_with_special_chars_in_params(self):
        """Test URL building with special characters in parameters."""
        url = self.client._build_url("/search", {"q": "hello world"})
        assert "q=hello+world" in url or "q=hello%20world" in url


class TestHTTPClientError:
    """Test HTTPClientError exception."""

    def test_http_client_error_is_exception(self):
        """Test that HTTPClientError is an Exception subclass."""
        assert issubclass(HTTPClientError, Exception)

    def test_http_client_error_can_be_raised(self):
        """Test that HTTPClientError can be raised and caught."""
        with pytest.raises(HTTPClientError):
            raise HTTPClientError("Test error")

    def test_http_client_error_message(self):
        """Test that HTTPClientError preserves error message."""
        error_msg = "Test HTTP client error"
        with pytest.raises(HTTPClientError, match=error_msg):
            raise HTTPClientError(error_msg)

    def test_http_client_error_with_cause(self):
        """Test that HTTPClientError can wrap another exception."""
        original_error = URLError("Network unreachable")
        with pytest.raises(HTTPClientError) as exc_info:
            raise HTTPClientError("Request failed") from original_error

        assert exc_info.value.__cause__ is original_error
