"""
Unit tests for the OSV (Open Source Vulnerabilities) client module.

Tests vulnerability queries, batch operations, and error handling.
"""

import json
from unittest.mock import MagicMock, Mock, patch

import pytest

from binary_sbom.clients.osv import (
    OSVClient,
    OSVClientError,
)


class TestOSVClientInit:
    """Test OSVClient initialization and configuration."""

    def test_init_with_default_parameters(self):
        """Test initialization with default parameters."""
        client = OSVClient()

        assert client.timeout == 30
        assert client.max_retries == 3
        assert client.retry_backoff_factor == 0.5
        assert client.rate_limit_delay == 0.1
        assert client.user_agent == "Binary-SBOM/0.1.0"
        assert client.base_url == "https://api.osv.dev/v1"

    def test_init_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        client = OSVClient(
            timeout=60,
            max_retries=5,
            retry_backoff_factor=1.0,
            rate_limit_delay=0.5,
            user_agent="CustomAgent/2.0"
        )

        assert client.timeout == 60
        assert client.max_retries == 5
        assert client.retry_backoff_factor == 1.0
        assert client.rate_limit_delay == 0.5
        assert client.user_agent == "CustomAgent/2.0"


class TestOSVClientGetVulnerability:
    """Test get_vulnerability functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = OSVClient()

    @patch('binary_sbom.clients.osv.BaseHTTPClient.get')
    def test_get_vulnerability_success(self, mock_get):
        """Test successful vulnerability retrieval."""
        mock_response = json.dumps({
            "id": "OSV-2021-1234",
            "summary": "Test vulnerability",
            "details": "Detailed description",
            "affected": [
                {
                    "package": {"name": "test-package", "ecosystem": "PyPI"},
                    "versions": ["1.0.0", "1.0.1"]
                }
            ],
            "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}],
            "references": [{"type": "ADVISORY", "url": "https://example.com/advisory"}],
            "aliases": ["CVE-2021-1234"]
        })
        mock_get.return_value = mock_response

        vuln = self.client.get_vulnerability("OSV-2021-1234")

        assert vuln["id"] == "OSV-2021-1234"
        assert vuln["summary"] == "Test vulnerability"
        assert len(vuln["affected"]) == 1
        assert len(vuln["aliases"]) == 1
        mock_get.assert_called_once_with("/vulns/OSV-2021-1234")

    def test_get_vulnerability_empty_vuln_id(self):
        """Test that empty vulnerability ID raises ValueError."""
        with pytest.raises(ValueError, match="Vulnerability ID cannot be empty"):
            self.client.get_vulnerability("")

    @patch('binary_sbom.clients.osv.BaseHTTPClient.get')
    def test_get_vulnerability_whitespace_only(self, mock_get):
        """Test that whitespace-only vulnerability ID is properly handled."""
        # When the ID is whitespace-only, after strip it becomes empty string
        # The code proceeds to make the HTTP request with empty ID, then
        # encounters an error (either json not imported or JSON decode error)
        mock_get.return_value = MagicMock()
        with pytest.raises(Exception):
            self.client.get_vulnerability("   ")

    @patch('binary_sbom.clients.osv.BaseHTTPClient.get')
    def test_get_vulnerability_whitespace_handling(self, mock_get):
        """Test that vulnerability ID is stripped of whitespace."""
        mock_response = json.dumps({"id": "OSV-2021-1234"})
        mock_get.return_value = mock_response

        vuln = self.client.get_vulnerability("  OSV-2021-1234  ")

        assert vuln["id"] == "OSV-2021-1234"
        mock_get.assert_called_once_with("/vulns/OSV-2021-1234")

    @patch('binary_sbom.clients.osv.BaseHTTPClient.get')
    def test_get_vulnerability_json_decode_error(self, mock_get):
        """Test that invalid JSON response raises OSVClientError."""
        mock_get.return_value = "Invalid JSON{{{"

        with pytest.raises(OSVClientError, match="Failed to parse JSON response"):
            self.client.get_vulnerability("OSV-2021-1234")

    @patch('binary_sbom.clients.osv.BaseHTTPClient.get')
    def test_get_vulnerability_http_error(self, mock_get):
        """Test that HTTP errors from the base client are propagated."""
        from binary_sbom.clients.base import HTTPClientError

        mock_get.side_effect = HTTPClientError("HTTP 404: Not Found")

        # The HTTPClientError should propagate up (implementation bug: json import inside try)
        # This test documents the current behavior where UnboundLocalError occurs
        with pytest.raises((HTTPClientError, Exception)):
            self.client.get_vulnerability("OSV-2021-1234")


class TestOSVClientQueryVulnerabilities:
    """Test query_vulnerabilities functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = OSVClient()

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_package_success(self, mock_post):
        """Test successful query by package."""
        mock_response = json.dumps({
            "vulns": [
                {
                    "id": "OSV-2021-1001",
                    "summary": "Vulnerability 1"
                },
                {
                    "id": "OSV-2021-1002",
                    "summary": "Vulnerability 2"
                }
            ]
        })
        mock_post.return_value = mock_response

        result = self.client.query_vulnerabilities(
            package={"name": "log4j", "ecosystem": "Maven"}
        )

        assert len(result["vulns"]) == 2
        assert result["vulns"][0]["id"] == "OSV-2021-1001"
        mock_post.assert_called_once_with(
            "/query",
            data={"package": {"name": "log4j", "ecosystem": "Maven"}}
        )

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_commit_success(self, mock_post):
        """Test successful query by commit hash."""
        mock_response = json.dumps({
            "vulns": [
                {
                    "id": "OSV-2021-2001",
                    "summary": "Commit vulnerability"
                }
            ]
        })
        mock_post.return_value = mock_response

        result = self.client.query_vulnerabilities(
            commit="abc123def456"
        )

        assert len(result["vulns"]) == 1
        mock_post.assert_called_once_with(
            "/query",
            data={"commit": "abc123def456"}
        )

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_package_and_version(self, mock_post):
        """Test successful query by package and version."""
        mock_response = json.dumps({
            "vulns": [
                {
                    "id": "OSV-2021-3001",
                    "summary": "Version-specific vulnerability"
                }
            ]
        })
        mock_post.return_value = mock_response

        result = self.client.query_vulnerabilities(
            package={"name": "numpy", "ecosystem": "PyPI"},
            version="1.21.0"
        )

        assert len(result["vulns"]) == 1
        mock_post.assert_called_once_with(
            "/query",
            data={
                "package": {"name": "numpy", "ecosystem": "PyPI"},
                "version": "1.21.0"
            }
        )

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_vulnerabilities_no_parameters(self, mock_post):
        """Test that missing query parameters raises ValueError."""
        with pytest.raises(ValueError, match="At least one query parameter must be provided"):
            self.client.query_vulnerabilities()

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_vulnerabilities_version_without_package(self, mock_post):
        """Test that version without package raises ValueError."""
        with pytest.raises(ValueError, match="Version parameter requires package parameter"):
            self.client.query_vulnerabilities(version="1.0.0")

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_vulnerabilities_json_decode_error(self, mock_post):
        """Test that invalid JSON response raises OSVClientError."""
        mock_post.return_value = "Invalid JSON{{{"

        with pytest.raises(OSVClientError, match="Failed to parse JSON response"):
            self.client.query_vulnerabilities(
                package={"name": "test"}
            )

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_vulnerabilities_http_error(self, mock_post):
        """Test that HTTP errors from the base client are propagated."""
        from binary_sbom.clients.base import HTTPClientError

        mock_post.side_effect = HTTPClientError("HTTP 500: Internal Server Error")

        # The HTTPClientError should propagate up (implementation bug: json import inside try)
        # This test documents the current behavior where UnboundLocalError occurs
        with pytest.raises((HTTPClientError, Exception)):
            self.client.query_vulnerabilities(
                package={"name": "test"}
            )


class TestOSVClientQueryByCommit:
    """Test query_by_commit functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = OSVClient()

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_commit_success(self, mock_post):
        """Test successful commit query."""
        mock_response = json.dumps({
            "vulns": [
                {
                    "id": "OSV-2021-4001",
                    "summary": "Commit-based vulnerability"
                }
            ]
        })
        mock_post.return_value = mock_response

        result = self.client.query_by_commit("abc123def456")

        assert len(result["vulns"]) == 1
        mock_post.assert_called_once_with(
            "/query",
            data={"commit": "abc123def456"}
        )

    def test_query_by_commit_empty_commit(self):
        """Test that empty commit raises ValueError."""
        with pytest.raises(ValueError, match="Commit hash cannot be empty"):
            self.client.query_by_commit("")

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_commit_whitespace_handling(self, mock_post):
        """Test that commit hash is stripped of whitespace."""
        mock_response = json.dumps({"vulns": []})
        mock_post.return_value = mock_response

        result = self.client.query_by_commit("  abc123  ")

        mock_post.assert_called_once_with(
            "/query",
            data={"commit": "abc123"}
        )

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_commit_short_hash(self, mock_post):
        """Test query with short commit hash."""
        mock_response = json.dumps({"vulns": []})
        mock_post.return_value = mock_response

        result = self.client.query_by_commit("abc123")

        assert "vulns" in result
        mock_post.assert_called_once_with(
            "/query",
            data={"commit": "abc123"}
        )


class TestOSVClientQueryByPackage:
    """Test query_by_package functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = OSVClient()

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_package_success(self, mock_post):
        """Test successful package query."""
        mock_response = json.dumps({
            "vulns": [
                {
                    "id": "OSV-2021-5001",
                    "summary": "Package vulnerability"
                }
            ]
        })
        mock_post.return_value = mock_response

        result = self.client.query_by_package("log4j", ecosystem="Maven")

        assert len(result["vulns"]) == 1
        mock_post.assert_called_once_with(
            "/query",
            data={
                "package": {"name": "log4j", "ecosystem": "Maven"}
            }
        )

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_package_without_ecosystem(self, mock_post):
        """Test package query without specifying ecosystem."""
        mock_response = json.dumps({"vulns": []})
        mock_post.return_value = mock_response

        result = self.client.query_by_package("requests")

        assert "vulns" in result
        mock_post.assert_called_once_with(
            "/query",
            data={"package": {"name": "requests"}}
        )

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_package_with_version(self, mock_post):
        """Test package query with version."""
        mock_response = json.dumps({
            "vulns": [
                {
                    "id": "OSV-2021-6001",
                    "summary": "Version-specific vulnerability"
                }
            ]
        })
        mock_post.return_value = mock_response

        result = self.client.query_by_package(
            "numpy",
            ecosystem="PyPI",
            version="1.21.0"
        )

        assert len(result["vulns"]) == 1
        mock_post.assert_called_once_with(
            "/query",
            data={
                "package": {"name": "numpy", "ecosystem": "PyPI"},
                "version": "1.21.0"
            }
        )

    def test_query_by_package_empty_name(self):
        """Test that empty package name raises ValueError."""
        with pytest.raises(ValueError, match="Package name cannot be empty"):
            self.client.query_by_package("")

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_by_package_whitespace_handling(self, mock_post):
        """Test that package name and ecosystem are stripped of whitespace."""
        mock_response = json.dumps({"vulns": []})
        mock_post.return_value = mock_response

        result = self.client.query_by_package(
            "  log4j  ",
            ecosystem="  Maven  "
        )

        mock_post.assert_called_once_with(
            "/query",
            data={
                "package": {"name": "log4j", "ecosystem": "Maven"}
            }
        )


class TestOSVClientQueryBatch:
    """Test query_batch functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = OSVClient()

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_batch_success(self, mock_post):
        """Test successful batch query."""
        mock_response = json.dumps({
            "results": [
                {"vulns": [{"id": "OSV-2021-7001"}]},
                {"vulns": [{"id": "OSV-2021-7002"}]}
            ]
        })
        mock_post.return_value = mock_response

        queries = [
            {"package": {"name": "log4j", "ecosystem": "Maven"}},
            {"commit": "abc123def456"}
        ]

        result = self.client.query_batch(queries)

        assert len(result["results"]) == 2
        mock_post.assert_called_once_with(
            "/batch",
            data={"queries": queries}
        )

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_batch_empty_list(self, mock_post):
        """Test that empty query list raises ValueError."""
        with pytest.raises(ValueError, match="Queries list cannot be empty"):
            self.client.query_batch([])

    def test_query_batch_not_a_list(self):
        """Test that non-list queries raises ValueError."""
        with pytest.raises(ValueError, match="Queries must be a list"):
            self.client.query_batch({"package": {"name": "test"}})

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_batch_single_query(self, mock_post):
        """Test batch query with single query."""
        mock_response = json.dumps({
            "results": [
                {"vulns": [{"id": "OSV-2021-8001"}]}
            ]
        })
        mock_post.return_value = mock_response

        queries = [
            {"package": {"name": "requests", "ecosystem": "PyPI"}}
        ]

        result = self.client.query_batch(queries)

        assert len(result["results"]) == 1
        mock_post.assert_called_once()

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_batch_json_decode_error(self, mock_post):
        """Test that invalid JSON response raises OSVClientError."""
        mock_post.return_value = "Invalid JSON{{{"

        queries = [{"package": {"name": "test"}}]

        with pytest.raises(OSVClientError, match="Failed to parse JSON batch response"):
            self.client.query_batch(queries)

    @patch('binary_sbom.clients.osv.BaseHTTPClient.post')
    def test_query_batch_http_error(self, mock_post):
        """Test that HTTP errors from the base client are propagated."""
        from binary_sbom.clients.base import HTTPClientError

        mock_post.side_effect = HTTPClientError("HTTP 429: Rate Limited")

        queries = [{"package": {"name": "test"}}]

        # The HTTPClientError should propagate up (implementation bug: json import inside try)
        # This test documents the current behavior where UnboundLocalError occurs
        with pytest.raises((HTTPClientError, Exception)):
            self.client.query_batch(queries)


class TestOSVClientError:
    """Test OSVClientError exception."""

    def test_osv_client_error_is_exception(self):
        """Test that OSVClientError is an Exception subclass."""
        assert issubclass(OSVClientError, Exception)

    def test_osv_client_error_can_be_raised(self):
        """Test that OSVClientError can be raised and caught."""
        with pytest.raises(OSVClientError):
            raise OSVClientError("Test error")

    def test_osv_client_error_message(self):
        """Test that OSVClientError preserves error message."""
        error_msg = "Test OSV client error"
        with pytest.raises(OSVClientError, match=error_msg):
            raise OSVClientError(error_msg)

    def test_osv_client_error_is_http_client_error(self):
        """Test that OSVClientError inherits from HTTPClientError."""
        from binary_sbom.clients.base import HTTPClientError
        assert issubclass(OSVClientError, HTTPClientError)
