"""
Unit tests for the NVD (National Vulnerability Database) client module.

Tests CVE retrieval, search functionality, and error handling.
"""

import json
from unittest.mock import MagicMock, Mock, patch

import pytest

from binary_sbom.clients.nvd import (
    NVDClient,
    NVDClientError,
)


class TestNVDClientInit:
    """Test NVDClient initialization and configuration."""

    def test_init_with_default_parameters(self):
        """Test initialization with default parameters."""
        client = NVDClient()

        assert client.api_key is None
        assert client.timeout == 30
        assert client.max_retries == 3
        assert client.retry_backoff_factor == 0.5
        assert client.rate_limit_delay == 6.0
        assert client.user_agent == "Binary-SBOM/0.1.0"
        assert client.base_url == "https://services.nvd.nist.gov/rest/json/cves/2.0"
        assert "apiKey" not in client.headers

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = NVDClient(api_key="test-api-key-123")

        assert client.api_key == "test-api-key-123"
        assert "apiKey" in client.headers
        assert client.headers["apiKey"] == "test-api-key-123"

    def test_init_with_custom_rate_limit_delay(self):
        """Test initialization with custom rate limit delay."""
        client = NVDClient(rate_limit_delay=1.0)

        assert client.rate_limit_delay == 1.0

    def test_init_with_all_custom_parameters(self):
        """Test initialization with all custom parameters."""
        client = NVDClient(
            api_key="custom-key",
            timeout=60,
            max_retries=5,
            retry_backoff_factor=1.0,
            rate_limit_delay=2.0,
            user_agent="CustomAgent/2.0"
        )

        assert client.api_key == "custom-key"
        assert client.timeout == 60
        assert client.max_retries == 5
        assert client.retry_backoff_factor == 1.0
        assert client.rate_limit_delay == 2.0
        assert client.user_agent == "CustomAgent/2.0"


class TestNVDClientGetCve:
    """Test get_cve functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = NVDClient()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_success(self, mock_get):
        """Test successful CVE retrieval."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [
                {
                    "cve": {
                        "id": "CVE-2021-44228",
                        "sourceIdentifier": "nvd@nist.gov",
                        "published": "2021-12-10T12:00:00.000",
                        "vulnStatus": "Analyzed",
                        "descriptions": [{"lang": "en", "value": "Test description"}]
                    }
                }
            ]
        })
        mock_get.return_value = mock_response

        cve = self.client.get_cve("CVE-2021-44228")

        assert cve["id"] == "CVE-2021-44228"
        assert cve["sourceIdentifier"] == "nvd@nist.gov"
        mock_get.assert_called_once_with("", params={"cveId": "CVE-2021-44228"})

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_empty_cve_id(self, mock_get):
        """Test that empty CVE ID raises ValueError."""
        with pytest.raises(ValueError, match="CVE ID cannot be empty"):
            self.client.get_cve("")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_whitespace_only_cve_id(self, mock_get):
        """Test that whitespace-only CVE ID raises ValueError."""
        # After stripping, empty string doesn't start with 'CVE-'
        with pytest.raises(ValueError, match="Invalid CVE ID format"):
            self.client.get_cve("   ")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_invalid_format_no_prefix(self, mock_get):
        """Test that CVE ID without CVE- prefix raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CVE ID format"):
            self.client.get_cve("2021-44228")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_invalid_format_wrong_prefix(self, mock_get):
        """Test that CVE ID with wrong prefix raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CVE ID format"):
            self.client.get_cve("ABC-2021-44228")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_lowercase_normalized(self, mock_get):
        """Test that lowercase CVE ID is normalized to uppercase."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [
                {"cve": {"id": "CVE-2021-44228"}}
            ]
        })
        mock_get.return_value = mock_response

        self.client.get_cve("cve-2021-44228")

        # Should be called with uppercase CVE ID
        mock_get.assert_called_once_with("", params={"cveId": "CVE-2021-44228"})

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_with_whitespace_trimmed(self, mock_get):
        """Test that CVE ID with whitespace is trimmed."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [
                {"cve": {"id": "CVE-2021-44228"}}
            ]
        })
        mock_get.return_value = mock_response

        self.client.get_cve("  CVE-2021-44228  ")

        # Should be called with trimmed CVE ID
        mock_get.assert_called_once_with("", params={"cveId": "CVE-2021-44228"})

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_not_found(self, mock_get):
        """Test that non-existent CVE raises NVDClientError."""
        mock_response = json.dumps({
            "totalResults": 0,
            "vulnerabilities": []
        })
        mock_get.return_value = mock_response

        with pytest.raises(NVDClientError, match="CVE CVE-2021-44228 not found"):
            self.client.get_cve("CVE-2021-44228")

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_invalid_response_missing_vulnerabilities(self, mock_get):
        """Test that response without vulnerabilities field raises NVDClientError."""
        mock_response = json.dumps({
            "totalResults": 1
        })
        mock_get.return_value = mock_response

        with pytest.raises(NVDClientError, match="Invalid response format"):
            self.client.get_cve("CVE-2021-44228")

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_invalid_response_empty_vulnerabilities(self, mock_get):
        """Test that response with empty vulnerabilities raises NVDClientError."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": []
        })
        mock_get.return_value = mock_response

        with pytest.raises(NVDClientError, match="Invalid response format"):
            self.client.get_cve("CVE-2021-44228")

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_invalid_json(self, mock_get):
        """Test that invalid JSON raises NVDClientError."""
        mock_get.return_value = "invalid json"

        with pytest.raises(NVDClientError, match="Failed to parse JSON"):
            self.client.get_cve("CVE-2021-44228")

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_empty_cve_object(self, mock_get):
        """Test that empty CVE object is returned without error."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [
                {"cve": {}}
            ]
        })
        mock_get.return_value = mock_response

        # Empty CVE object is still a valid response
        cve = self.client.get_cve("CVE-2021-44228")
        assert cve == {}

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cve_with_complete_response(self, mock_get):
        """Test CVE retrieval with complete response data."""
        mock_response = json.dumps({
            "totalResults": 1,
            "startIndex": 0,
            "resultsPerPage": 20,
            "vulnerabilities": [
                {
                    "cve": {
                        "id": "CVE-2021-44228",
                        "sourceIdentifier": "nvd@nist.gov",
                        "published": "2021-12-10T12:00:00.000",
                        "lastModified": "2021-12-15T08:30:00.000",
                        "vulnStatus": "Analyzed",
                        "descriptions": [
                            {"lang": "en", "value": "Apache Log4j2 vulnerability"}
                        ],
                        "metrics": {
                            "cvssMetricV31": [
                                {
                                    "cvssData": {
                                        "baseScore": 10.0,
                                        "baseSeverity": "CRITICAL"
                                    }
                                }
                            ]
                        },
                        "references": [
                            {"url": "https://nvd.nist.gov/vuln/detail/CVE-2021-44228"}
                        ]
                    }
                }
            ]
        })
        mock_get.return_value = mock_response

        cve = self.client.get_cve("CVE-2021-44228")

        assert cve["id"] == "CVE-2021-44228"
        assert cve["vulnStatus"] == "Analyzed"
        assert len(cve["descriptions"]) == 1
        assert cve["descriptions"][0]["lang"] == "en"
        assert "metrics" in cve
        assert "references" in cve


class TestNVDClientSearchCves:
    """Test search_cves functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = NVDClient()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_success(self, mock_get):
        """Test successful CVE search."""
        mock_response = json.dumps({
            "totalResults": 2,
            "startIndex": 0,
            "resultsPerPage": 20,
            "vulnerabilities": [
                {"cve": {"id": "CVE-2021-44228"}},
                {"cve": {"id": "CVE-2021-45105"}}
            ]
        })
        mock_get.return_value = mock_response

        results = self.client.search_cves(keyword="log4j")

        assert results["totalResults"] == 2
        assert results["startIndex"] == 0
        assert results["resultsPerPage"] == 20
        assert len(results["vulnerabilities"]) == 2

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_with_all_parameters(self, mock_get):
        """Test search with all parameters."""
        mock_response = json.dumps({
            "totalResults": 1,
            "startIndex": 10,
            "resultsPerPage": 50,
            "vulnerabilities": [
                {"cve": {"id": "CVE-2021-44228"}}
            ]
        })
        mock_get.return_value = mock_response

        results = self.client.search_cves(
            keyword="apache",
            cpe_name="cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*",
            cvss_severity="CRITICAL",
            is_vulnerable=True,
            results_per_page=50,
            start_index=10
        )

        assert results["totalResults"] == 1
        # Verify the parameters were passed correctly
        call_args = mock_get.call_args
        assert call_args[0][0] == ""
        params = call_args[1]["params"]
        assert params["keyword"] == "apache"
        assert params["cpeName"] == "cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*"
        assert params["cvssSeverity"] == "CRITICAL"
        assert params["isVulnerable"] == "true"
        assert params["resultsPerPage"] == 50
        assert params["startIndex"] == 10

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_with_keyword_only(self, mock_get):
        """Test search with only keyword parameter."""
        mock_response = json.dumps({
            "totalResults": 1,
            "startIndex": 0,
            "resultsPerPage": 20,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        results = self.client.search_cves(keyword="log4j")

        assert results["totalResults"] == 1
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["keyword"] == "log4j"
        assert "cpeName" not in params
        assert "cvssSeverity" not in params

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_with_severity_lowercase(self, mock_get):
        """Test that lowercase severity is normalized to uppercase."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        self.client.search_cves(cvss_severity="critical")

        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["cvssSeverity"] == "CRITICAL"

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_invalid_results_per_page_too_low(self, mock_get):
        """Test that results_per_page < 1 raises ValueError."""
        with pytest.raises(ValueError, match="results_per_page must be between 1 and 2000"):
            self.client.search_cves(results_per_page=0)

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_invalid_results_per_page_too_high(self, mock_get):
        """Test that results_per_page > 2000 raises ValueError."""
        with pytest.raises(ValueError, match="results_per_page must be between 1 and 2000"):
            self.client.search_cves(results_per_page=2001)

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_invalid_results_per_page_negative(self, mock_get):
        """Test that negative results_per_page raises ValueError."""
        with pytest.raises(ValueError, match="results_per_page must be between 1 and 2000"):
            self.client.search_cves(results_per_page=-10)

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_valid_results_per_page_boundaries(self, mock_get):
        """Test that boundary values for results_per_page are accepted."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        # Test minimum boundary
        self.client.search_cves(results_per_page=1)
        assert mock_get.call_count == 1

        # Test maximum boundary
        self.client.search_cves(results_per_page=2000)
        assert mock_get.call_count == 2

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_invalid_start_index_negative(self, mock_get):
        """Test that negative start_index raises ValueError."""
        with pytest.raises(ValueError, match="start_index must be non-negative"):
            self.client.search_cves(start_index=-1)

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_valid_start_index_zero(self, mock_get):
        """Test that start_index=0 is accepted."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        self.client.search_cves(start_index=0)

        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["startIndex"] == 0

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_invalid_cvss_severity(self, mock_get):
        """Test that invalid CVSS severity raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CVSS severity"):
            self.client.search_cves(cvss_severity="INVALID")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_valid_cvss_severities(self, mock_get):
        """Test that all valid CVSS severities are accepted."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        valid_severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

        for severity in valid_severities:
            self.client.search_cves(cvss_severity=severity)

        assert mock_get.call_count == 4

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_is_vulnerable_false(self, mock_get):
        """Test search with is_vulnerable=False."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        self.client.search_cves(is_vulnerable=False)

        call_args = mock_get.call_args
        params = call_args[1]["params"]
        # When False, isVulnerable parameter is not included
        assert "isVulnerable" not in params

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_invalid_response_format(self, mock_get):
        """Test that invalid response format raises NVDClientError."""
        mock_response = json.dumps({
            "totalResults": 1
        })
        mock_get.return_value = mock_response

        with pytest.raises(NVDClientError, match="Invalid response format"):
            self.client.search_cves()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_search_cves_json_decode_error(self, mock_get):
        """Test that JSON decode error raises NVDClientError."""
        mock_get.return_value = "invalid json{{"

        with pytest.raises(NVDClientError, match="Failed to parse JSON"):
            self.client.search_cves()


class TestNVDClientGetCvesByCpe:
    """Test get_cves_by_cpe functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = NVDClient()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_cpe_success(self, mock_get):
        """Test successful CVE retrieval by CPE."""
        mock_response = json.dumps({
            "totalResults": 3,
            "startIndex": 0,
            "resultsPerPage": 20,
            "vulnerabilities": [
                {"cve": {"id": "CVE-2021-44228"}},
                {"cve": {"id": "CVE-2021-45105"}},
                {"cve": {"id": "CVE-2021-44832"}}
            ]
        })
        mock_get.return_value = mock_response

        results = self.client.get_cves_by_cpe(
            "cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*"
        )

        assert results["totalResults"] == 3
        assert len(results["vulnerabilities"]) == 3

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_cpe_empty_cpe_name(self, mock_get):
        """Test that empty CPE name raises ValueError."""
        with pytest.raises(ValueError, match="CPE name cannot be empty"):
            self.client.get_cves_by_cpe("")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_cpe_with_pagination(self, mock_get):
        """Test get_cves_by_cpe with pagination parameters."""
        mock_response = json.dumps({
            "totalResults": 100,
            "startIndex": 20,
            "resultsPerPage": 20,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        results = self.client.get_cves_by_cpe(
            "cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*",
            results_per_page=20,
            start_index=20
        )

        assert results["startIndex"] == 20
        assert results["resultsPerPage"] == 20

        # Verify parameters were passed correctly
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["cpeName"] == "cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*"
        assert params["resultsPerPage"] == 20
        assert params["startIndex"] == 20

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_cpe_passes_to_search_cves(self, mock_get):
        """Test that get_cves_by_cpe properly delegates to search_cves."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        # This will fail if parameters aren't passed correctly
        self.client.get_cves_by_cpe(
            "cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*",
            results_per_page=10,
            start_index=5
        )

        # Verify the call was made with the right parameters
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["cpeName"] == "cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*"
        assert params["resultsPerPage"] == 10
        assert params["startIndex"] == 5


class TestNVDClientGetCvesBySeverity:
    """Test get_cves_by_severity functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = NVDClient()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_severity_success(self, mock_get):
        """Test successful CVE retrieval by severity."""
        mock_response = json.dumps({
            "totalResults": 15,
            "startIndex": 0,
            "resultsPerPage": 20,
            "vulnerabilities": [
                {"cve": {"id": "CVE-2021-44228"}},
                {"cve": {"id": "CVE-2021-34527"}}
            ]
        })
        mock_get.return_value = mock_response

        results = self.client.get_cves_by_severity("CRITICAL")

        assert results["totalResults"] == 15
        assert len(results["vulnerabilities"]) == 2

        # Verify severity was passed correctly
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["cvssSeverity"] == "CRITICAL"

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_severity_with_keyword(self, mock_get):
        """Test get_cves_by_severity with keyword filter."""
        mock_response = json.dumps({
            "totalResults": 5,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        results = self.client.get_cves_by_severity("HIGH", keyword="apache")

        assert results["totalResults"] == 5

        # Verify both parameters were passed
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["cvssSeverity"] == "HIGH"
        assert params["keyword"] == "apache"

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_severity_lowercase_normalized(self, mock_get):
        """Test that lowercase severity is normalized to uppercase."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        self.client.get_cves_by_severity("medium")

        # Verify severity was uppercased
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["cvssSeverity"] == "MEDIUM"

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_severity_invalid_severity(self, mock_get):
        """Test that invalid severity raises ValueError."""
        with pytest.raises(ValueError, match="Invalid severity"):
            self.client.get_cves_by_severity("INVALID")

        mock_get.assert_not_called()

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_severity_all_valid_severities(self, mock_get):
        """Test that all valid severities work correctly."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        valid_severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        for severity in valid_severities:
            self.client.get_cves_by_severity(severity)

        assert mock_get.call_count == 4

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_severity_with_pagination(self, mock_get):
        """Test get_cves_by_severity with pagination parameters."""
        mock_response = json.dumps({
            "totalResults": 100,
            "startIndex": 40,
            "resultsPerPage": 20,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        results = self.client.get_cves_by_severity(
            "HIGH",
            results_per_page=20,
            start_index=40
        )

        assert results["startIndex"] == 40
        assert results["resultsPerPage"] == 20

        # Verify parameters were passed correctly
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["cvssSeverity"] == "HIGH"
        assert params["resultsPerPage"] == 20
        assert params["startIndex"] == 40

    @patch('binary_sbom.clients.nvd.BaseHTTPClient.get')
    def test_get_cves_by_severity_passes_to_search_cves(self, mock_get):
        """Test that get_cves_by_severity properly delegates to search_cves."""
        mock_response = json.dumps({
            "totalResults": 1,
            "vulnerabilities": [{"cve": {"id": "CVE-2021-44228"}}]
        })
        mock_get.return_value = mock_response

        # This will fail if parameters aren't passed correctly
        self.client.get_cves_by_severity(
            "CRITICAL",
            keyword="log4j",
            results_per_page=50,
            start_index=0
        )

        # Verify the call was made with the right parameters
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["cvssSeverity"] == "CRITICAL"
        assert params["keyword"] == "log4j"
        assert params["resultsPerPage"] == 50
        assert params["startIndex"] == 0


class TestNVDClientError:
    """Test NVDClientError exception."""

    def test_nvd_client_error_is_exception(self):
        """Test that NVDClientError is an Exception subclass."""
        assert issubclass(NVDClientError, Exception)

    def test_nvd_client_error_can_be_raised(self):
        """Test that NVDClientError can be raised and caught."""
        with pytest.raises(NVDClientError):
            raise NVDClientError("Test error")

    def test_nvd_client_error_message(self):
        """Test that NVDClientError preserves error message."""
        error_msg = "Test NVD client error"
        with pytest.raises(NVDClientError, match=error_msg):
            raise NVDClientError(error_msg)

    def test_nvd_client_error_with_cause(self):
        """Test that NVDClientError can wrap another exception."""
        original_error = ValueError("Original error")
        with pytest.raises(NVDClientError) as exc_info:
            raise NVDClientError("Request failed") from original_error

        assert exc_info.value.__cause__ is original_error
