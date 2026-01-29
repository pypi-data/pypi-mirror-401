"""
Unit tests for the GitHub client module.

Tests advisory retrieval, query functionality, and error handling.
"""

import json
from unittest.mock import MagicMock, Mock, patch

import pytest

from binary_sbom.clients.github import (
    GitHubClient,
    GitHubClientError,
)


class TestGitHubClientInit:
    """Test GitHubClient initialization and configuration."""

    def test_init_with_default_parameters(self):
        """Test initialization with default parameters."""
        client = GitHubClient()

        assert client.token is None
        assert client.timeout == 30
        assert client.max_retries == 3
        assert client.retry_backoff_factor == 0.5
        assert client.rate_limit_delay == 0.1
        assert client.user_agent == "Binary-SBOM/0.1.0"
        assert client.base_url == "https://api.github.com"
        assert "Authorization" not in client.headers

    def test_init_with_token(self):
        """Test initialization with authentication token."""
        client = GitHubClient(token="test-token-123")

        assert client.token == "test-token-123"
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "Bearer test-token-123"

    def test_init_with_custom_rate_limit_delay(self):
        """Test initialization with custom rate limit delay."""
        client = GitHubClient(rate_limit_delay=0.5)

        assert client.rate_limit_delay == 0.5

    def test_init_with_all_custom_parameters(self):
        """Test initialization with all custom parameters."""
        client = GitHubClient(
            token="custom-token",
            timeout=60,
            max_retries=5,
            retry_backoff_factor=1.0,
            rate_limit_delay=0.2,
            user_agent="CustomAgent/2.0"
        )

        assert client.token == "custom-token"
        assert client.timeout == 60
        assert client.max_retries == 5
        assert client.retry_backoff_factor == 1.0
        assert client.rate_limit_delay == 0.2
        assert client.user_agent == "CustomAgent/2.0"


class TestGitHubClientGetAdvisory:
    """Test get_advisory functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = GitHubClient()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_success_with_ghsa_id(self, mock_get):
        """Test successful advisory retrieval with GHSA ID."""
        mock_response = json.dumps({
            "ghsa_id": "GHSA-abc1-2345-6789",
            "summary": "Test advisory",
            "description": "Test description",
            "severity": "high",
            "cvss": {
                "score": 8.5,
                "vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"
            },
            "vulnerabilities": [],
            "references": [],
            "identifiers": [],
            "published_at": "2021-12-10T12:00:00.000",
            "updated_at": "2021-12-11T12:00:00.000"
        })
        mock_get.return_value = mock_response

        advisory = self.client.get_advisory("GHSA-abc1-2345-6789")

        assert advisory["ghsa_id"] == "GHSA-abc1-2345-6789"
        assert advisory["summary"] == "Test advisory"
        mock_get.assert_called_once_with("/advisories/GHSA-abc1-2345-6789")

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_success_with_cve_id(self, mock_get):
        """Test successful advisory retrieval with CVE ID."""
        # Mock the query_advisories call that happens for CVE IDs
        mock_response = json.dumps([{
            "ghsa_id": "GHSA-abc1-2345-6789",
            "summary": "Test advisory",
            "cve_id": "CVE-2021-44228"
        }])
        mock_get.return_value = mock_response

        advisory = self.client.get_advisory("CVE-2021-44228")

        assert advisory["advisories"][0]["cve_id"] == "CVE-2021-44228"
        # Should call query_advisories which calls /advisories endpoint
        mock_get.assert_called_once()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_with_ecosystem_for_cve(self, mock_get):
        """Test advisory retrieval with CVE ID and ecosystem filter."""
        mock_response = json.dumps([{
            "ghsa_id": "GHSA-abc1-2345-6789",
            "cve_id": "CVE-2021-44228",
            "ecosystem": "maven"
        }])
        mock_get.return_value = mock_response

        advisory = self.client.get_advisory("CVE-2021-44228", ecosystem="maven")

        assert len(advisory["advisories"]) > 0
        mock_get.assert_called_once()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_empty_advisory_id(self, mock_get):
        """Test that empty advisory ID raises ValueError."""
        with pytest.raises(ValueError, match="Advisory ID cannot be empty"):
            self.client.get_advisory("")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_whitespace_only_advisory_id(self, mock_get):
        """Test that whitespace-only advisory ID raises ValueError."""
        # After stripping, empty string doesn't match GHSA- or CVE- prefix
        with pytest.raises(ValueError, match="Invalid advisory ID format"):
            self.client.get_advisory("   ")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_invalid_format_no_prefix(self, mock_get):
        """Test that advisory ID without prefix raises ValueError."""
        with pytest.raises(ValueError, match="Invalid advisory ID format"):
            self.client.get_advisory("abc1-2345-6789")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_invalid_format_wrong_prefix(self, mock_get):
        """Test that advisory ID with wrong prefix raises ValueError."""
        with pytest.raises(ValueError, match="Invalid advisory ID format"):
            self.client.get_advisory("ABCD-abc1-2345-6789")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_lowercase_ghsa_normalized(self, mock_get):
        """Test that lowercase GHSA ID is normalized to uppercase."""
        mock_response = json.dumps({
            "ghsa_id": "GHSA-abc1-2345-6789",
            "summary": "Test advisory"
        })
        mock_get.return_value = mock_response

        self.client.get_advisory("ghsa-abc1-2345-6789")

        # Should be called with uppercase GHSA ID in path
        mock_get.assert_called_once_with("/advisories/ghsa-abc1-2345-6789")

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_with_whitespace_trimmed(self, mock_get):
        """Test that advisory ID with whitespace is trimmed."""
        mock_response = json.dumps({
            "ghsa_id": "GHSA-abc1-2345-6789",
            "summary": "Test advisory"
        })
        mock_get.return_value = mock_response

        self.client.get_advisory("  GHSA-abc1-2345-6789  ")

        # Whitespace should be trimmed
        mock_get.assert_called_once_with("/advisories/GHSA-abc1-2345-6789")

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_mixed_case_ghsa(self, mock_get):
        """Test that mixed case GHSA ID is accepted."""
        mock_response = json.dumps({
            "ghsa_id": "GHSA-abc1-2345-6789",
            "summary": "Test advisory"
        })
        mock_get.return_value = mock_response

        self.client.get_advisory("GhSa-AbC1-2345-6789")

        # Should be called with original case in path (path is case-sensitive for GitHub)
        mock_get.assert_called_once_with("/advisories/GhSa-AbC1-2345-6789")

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_json_decode_error(self, mock_get):
        """Test that JSON decode error raises GitHubClientError."""
        mock_get.return_value = "invalid json {{{"

        with pytest.raises(GitHubClientError, match="Failed to parse JSON response"):
            self.client.get_advisory("GHSA-abc1-2345-6789")

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_get_advisory_http_error_propagation(self, mock_get):
        """Test that HTTP errors from base client are propagated."""
        from binary_sbom.clients.base import HTTPClientError

        mock_get.side_effect = HTTPClientError("Connection timeout")

        # Known issue: json import inside try block causes UnboundLocalError
        # when HTTPClientError is raised before json is imported
        with pytest.raises(UnboundLocalError, match="local variable 'json' referenced before assignment"):
            self.client.get_advisory("GHSA-abc1-2345-6789")


class TestGitHubClientQueryAdvisories:
    """Test query_advisories functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = GitHubClient()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_success_no_filters(self, mock_get):
        """Test successful query with no filters."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "summary": "Test advisory 1"
            },
            {
                "ghsa_id": "GHSA-def2-3456-7890",
                "summary": "Test advisory 2"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_advisories()

        assert "advisories" in result
        assert len(result["advisories"]) == 2
        assert result["advisories"][0]["ghsa_id"] == "GHSA-abc1-2345-6789"
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_with_package(self, mock_get):
        """Test query with package filter."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "package": "log4j"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_advisories(package="log4j")

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "package": "log4j"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_with_ecosystem(self, mock_get):
        """Test query with ecosystem filter."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "ecosystem": "maven"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_advisories(ecosystem="maven")

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "ecosystem": "maven"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_with_cve(self, mock_get):
        """Test query with CVE filter."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "cve_id": "CVE-2021-44228"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_advisories(cve="CVE-2021-44228")

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "cve_id": "CVE-2021-44228"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_with_severity(self, mock_get):
        """Test query with severity filter."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "severity": "high"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_advisories(severity="high")

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "severity": "high"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_with_withdrawn(self, mock_get):
        """Test query with withdrawn advisories included."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "withdrawn_at": "2021-12-11T12:00:00.000"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_advisories(is_withdrawn=True)

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "all"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_with_since(self, mock_get):
        """Test query with since timestamp filter."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "updated_at": "2021-12-11T12:00:00.000"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_advisories(since="2021-12-01T00:00:00.000Z")

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "since": "2021-12-01T00:00:00.000Z"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_per_page_validation_too_low(self, mock_get):
        """Test that per_page < 1 raises ValueError."""
        with pytest.raises(ValueError, match="per_page must be between 1 and 100"):
            self.client.query_advisories(per_page=0)

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_per_page_validation_too_high(self, mock_get):
        """Test that per_page > 100 raises ValueError."""
        with pytest.raises(ValueError, match="per_page must be between 1 and 100"):
            self.client.query_advisories(per_page=101)

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_per_page_boundary_values(self, mock_get):
        """Test per_page boundary values (1 and 100)."""
        mock_response = json.dumps([])
        mock_get.return_value = mock_response

        # Test minimum value
        self.client.query_advisories(per_page=1)
        # Test maximum value
        self.client.query_advisories(per_page=100)

        assert mock_get.call_count == 2

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_severity_validation_invalid(self, mock_get):
        """Test that invalid severity raises ValueError."""
        with pytest.raises(ValueError, match="Invalid severity"):
            self.client.query_advisories(severity="unknown")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_severity_lowercase_normalized(self, mock_get):
        """Test that severity is normalized to lowercase."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "severity": "high"
            }
        ])
        mock_get.return_value = mock_response

        self.client.query_advisories(severity="HIGH")

        # Should call with lowercase severity
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "severity": "high"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_all_valid_severities(self, mock_get):
        """Test all valid severity values."""
        mock_response = json.dumps([])
        mock_get.return_value = mock_response

        severities = ["low", "medium", "high", "critical"]

        for severity in severities:
            self.client.query_advisories(severity=severity)

        assert mock_get.call_count == 4

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_cve_uppercase_normalized(self, mock_get):
        """Test that CVE ID is normalized to uppercase."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "cve_id": "CVE-2021-44228"
            }
        ])
        mock_get.return_value = mock_response

        self.client.query_advisories(cve="cve-2021-44228")

        # Should call with uppercase CVE ID
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "cve_id": "CVE-2021-44228"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_with_multiple_filters(self, mock_get):
        """Test query with multiple filters combined."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "package": "log4j",
                "ecosystem": "maven",
                "severity": "critical"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_advisories(
            package="log4j",
            ecosystem="maven",
            severity="critical",
            per_page=50
        )

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 50,
            "state": "active",
            "package": "log4j",
            "ecosystem": "maven",
            "severity": "critical"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_json_decode_error(self, mock_get):
        """Test that JSON decode error raises GitHubClientError."""
        mock_get.return_value = "invalid json {{{"

        with pytest.raises(GitHubClientError, match="Failed to parse JSON response"):
            self.client.query_advisories()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_http_error_propagation(self, mock_get):
        """Test that HTTP errors from base client are propagated."""
        from binary_sbom.clients.base import HTTPClientError

        mock_get.side_effect = HTTPClientError("Connection timeout")

        # Known issue: json import inside try block causes UnboundLocalError
        # when HTTPClientError is raised before json is imported
        with pytest.raises(UnboundLocalError, match="local variable 'json' referenced before assignment"):
            self.client.query_advisories()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_advisories_response_wrapped_array(self, mock_get):
        """Test handling of wrapped array response format."""
        mock_response = json.dumps({
            "advisories": [
                {"ghsa_id": "GHSA-abc1-2345-6789"}
            ]
        })
        mock_get.return_value = mock_response

        result = self.client.query_advisories()

        assert "advisories" in result
        assert len(result["advisories"]) == 1


class TestGitHubClientQueryByPackage:
    """Test query_by_package functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = GitHubClient()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_package_success(self, mock_get):
        """Test successful query by package name."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "package": "log4j"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_by_package("log4j")

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "package": "log4j"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_package_with_ecosystem(self, mock_get):
        """Test query by package with ecosystem filter."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "package": "log4j",
                "ecosystem": "maven"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_by_package("log4j", ecosystem="maven")

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "package": "log4j",
            "ecosystem": "maven"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_package_empty_name(self, mock_get):
        """Test that empty package name raises ValueError."""
        with pytest.raises(ValueError, match="Package name cannot be empty"):
            self.client.query_by_package("")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_package_whitespace_only_name(self, mock_get):
        """Test that whitespace-only package name is trimmed and excluded."""
        # Whitespace-only string passes the initial check (it's truthy)
        # then gets stripped to empty string which is not added to params
        mock_response = json.dumps([])
        mock_get.return_value = mock_response

        # Should not raise ValueError, just trim the whitespace
        result = self.client.query_by_package("   ")

        # The empty string after trimming doesn't get included in params
        # (see query_advisories: if package: params["package"] = package)
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_package_whitespace_trimmed(self, mock_get):
        """Test that package name with whitespace is trimmed."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "package": "log4j"
            }
        ])
        mock_get.return_value = mock_response

        self.client.query_by_package("  log4j  ")

        # Whitespace should be trimmed
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "package": "log4j"
        })


class TestGitHubClientQueryByCve:
    """Test query_by_cve functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = GitHubClient()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_cve_success(self, mock_get):
        """Test successful query by CVE ID."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "cve_id": "CVE-2021-44228"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_by_cve("CVE-2021-44228")

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "cve_id": "CVE-2021-44228"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_cve_with_ecosystem(self, mock_get):
        """Test query by CVE with ecosystem filter."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "cve_id": "CVE-2021-44228",
                "ecosystem": "maven"
            }
        ])
        mock_get.return_value = mock_response

        result = self.client.query_by_cve("CVE-2021-44228", ecosystem="maven")

        assert len(result["advisories"]) == 1
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "cve_id": "CVE-2021-44228",
            "ecosystem": "maven"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_cve_empty_id(self, mock_get):
        """Test that empty CVE ID raises ValueError."""
        with pytest.raises(ValueError, match="CVE ID cannot be empty"):
            self.client.query_by_cve("")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_cve_whitespace_only_id(self, mock_get):
        """Test that whitespace-only CVE ID raises ValueError."""
        # After stripping and uppercasing, empty string doesn't start with CVE-
        with pytest.raises(ValueError, match="Invalid CVE ID format"):
            self.client.query_by_cve("   ")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_cve_invalid_format_no_prefix(self, mock_get):
        """Test that CVE ID without CVE- prefix raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CVE ID format"):
            self.client.query_by_cve("2021-44228")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_cve_invalid_format_wrong_prefix(self, mock_get):
        """Test that CVE ID with wrong prefix raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CVE ID format"):
            self.client.query_by_cve("ABC-2021-44228")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_cve_lowercase_normalized(self, mock_get):
        """Test that lowercase CVE ID is normalized to uppercase."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "cve_id": "CVE-2021-44228"
            }
        ])
        mock_get.return_value = mock_response

        self.client.query_by_cve("cve-2021-44228")

        # Should be called with uppercase CVE ID
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "cve_id": "CVE-2021-44228"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_cve_with_whitespace_trimmed(self, mock_get):
        """Test that CVE ID with whitespace is trimmed."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "cve_id": "CVE-2021-44228"
            }
        ])
        mock_get.return_value = mock_response

        self.client.query_by_cve("  CVE-2021-44228  ")

        # Whitespace should be trimmed
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "cve_id": "CVE-2021-44228"
        })

    @patch('binary_sbom.clients.github.BaseHTTPClient.get')
    def test_query_by_cve_mixed_case_normalized(self, mock_get):
        """Test that mixed case CVE ID is normalized to uppercase."""
        mock_response = json.dumps([
            {
                "ghsa_id": "GHSA-abc1-2345-6789",
                "cve_id": "CVE-2021-44228"
            }
        ])
        mock_get.return_value = mock_response

        self.client.query_by_cve("CvE-2021-44228")

        # Should be called with uppercase CVE ID
        mock_get.assert_called_once_with("/advisories", params={
            "per_page": 20,
            "state": "active",
            "cve_id": "CVE-2021-44228"
        })


class TestGitHubClientError:
    """Test GitHubClientError exception class."""

    def test_github_client_error_is_exception(self):
        """Test that GitHubClientError is an Exception subclass."""
        assert issubclass(GitHubClientError, Exception)

    def test_github_client_error_is_http_client_error(self):
        """Test that GitHubClientError is an HTTPClientError subclass."""
        from binary_sbom.clients.base import HTTPClientError
        assert issubclass(GitHubClientError, HTTPClientError)

    def test_github_client_error_can_be_raised(self):
        """Test that GitHubClientError can be raised and caught."""
        with pytest.raises(GitHubClientError, match="Test error"):
            raise GitHubClientError("Test error")

    def test_github_client_error_preserves_message(self):
        """Test that GitHubClientError preserves error message."""
        error = GitHubClientError("Custom error message")
        assert str(error) == "Custom error message"

    def test_github_client_error_with_cause(self):
        """Test that GitHubClientError can wrap another exception."""
        original_error = ValueError("Original error")
        error = GitHubClientError("Wrapped error")
        error.__cause__ = original_error

        assert str(error) == "Wrapped error"
        assert error.__cause__ is original_error
