"""
Exception classes for vulnerability scanning.

Defines custom exceptions for various error conditions that may occur
during vulnerability scanning operations.
"""


class VulnerabilityScanError(Exception):
    """
    Base exception for vulnerability scanning errors.

    All vulnerability-scanning-related exceptions inherit from this class,
    allowing applications to catch all scanning errors with a single except clause.
    """

    pass


class APIError(VulnerabilityScanError):
    """
    Exception raised when an API request fails.

    Attributes:
        source: The API source that failed (e.g., "OSV", "NVD", "GitHub")
        status_code: HTTP status code (if available)
        message: Error message
        retry_after: Suggested retry delay in seconds (if available)

    Example:
        >>> try:
        ...     query_osv(...)
        ... except APIError as e:
        ...     if e.source == "NVD" and e.retry_after:
        ...         time.sleep(e.retry_after)
        ...         # retry request
    """

    def __init__(
        self,
        message: str,
        source: str,
        status_code: int = None,
        retry_after: int = None,
    ):
        self.source = source
        self.status_code = status_code
        self.retry_after = retry_after
        self.message = message
        super().__init__(f"{source} API error: {message}")


class RateLimitError(APIError):
    """
    Exception raised when API rate limit is exceeded.

    Attributes:
        source: The API source
        retry_after: Suggested retry delay in seconds
        limit: Rate limit that was exceeded (optional)

    Example:
        >>> try:
        ...     query_nvd(...)
        ... except RateLimitError as e:
        ...     print(f"Rate limited. Retry after {e.retry_after} seconds")
        ...     time.sleep(e.retry_after)
    """

    def __init__(self, message: str, source: str, retry_after: int, limit: str = None):
        self.limit = limit
        super().__init__(message, source, retry_after=retry_after)


class AuthenticationError(APIError):
    """
    Exception raised when API authentication fails.

    Attributes:
        source: The API source
        reason: Reason for authentication failure

    Example:
        >>> try:
        ...     query_github(...)
        ... except AuthenticationError as e:
        ...     print(f"Authentication failed for {e.source}: {e.reason}")
    """

    def __init__(self, message: str, source: str, reason: str = None):
        self.reason = reason
        super().__init__(message, source)


class PackageNotFoundError(VulnerabilityScanError):
    """
    Exception raised when a package is not found in vulnerability database.

    This is not necessarily an error condition - many packages have no
    known vulnerabilities. Applications may choose to handle this
    differently from other errors.

    Attributes:
        package: Package identifier that was not found
        source: Database that was queried

    Example:
        >>> try:
        ...     vulns = query_package(ecosystem="npm", name="safe-package", version="1.0.0")
        ... except PackageNotFoundError:
        ...     print("No vulnerabilities found - package is safe")
    """

    def __init__(self, package: str, source: str):
        self.package = package
        self.source = source
        super().__init__(f"Package not found in {source}: {package}")


class InvalidVersionError(VulnerabilityScanError):
    """
    Exception raised when a package version is invalid or cannot be parsed.

    Attributes:
        version: The invalid version string
        reason: Why the version is invalid

    Example:
        >>> try:
        ...     check_version_affected("not-a-version")
        ... except InvalidVersionError as e:
        ...     print(f"Invalid version: {e.version} - {e.reason}")
    """

    def __init__(self, version: str, reason: str):
        self.version = version
        self.reason = reason
        super().__init__(f"Invalid version '{version}': {reason}")


class ConfigurationError(VulnerabilityScanError):
    """
    Exception raised when vulnerability scanner is misconfigured.

    Attributes:
        setting: The configuration setting that is invalid
        reason: Why the configuration is invalid

    Example:
        >>> try:
        ...     scanner = VulnerabilityScanner(api_keys=invalid_keys)
        ... except ConfigurationError as e:
        ...     print(f"Configuration error in {e.setting}: {e.reason}")
    """

    def __init__(self, setting: str, reason: str):
        self.setting = setting
        self.reason = reason
        super().__init__(f"Configuration error in '{setting}': {reason}")


class CacheError(VulnerabilityScanError):
    """
    Exception raised when cache operations fail.

    Attributes:
        operation: The cache operation that failed
        reason: Reason for failure

    Example:
        >>> try:
        ...     cache.get(package_key)
        ... except CacheError as e:
        ...     print(f"Cache {e.operation} failed: {e.reason}")
    """

    def __init__(self, operation: str, reason: str):
        self.operation = operation
        self.reason = reason
        super().__init__(f"Cache {operation} failed: {reason}")


class TimeoutError(VulnerabilityScanError):
    """
    Exception raised when API request times out.

    Attributes:
        source: The API source that timed out
        timeout: Timeout duration in seconds

    Example:
        >>> try:
        ...     query_with_timeout(...)
        ... except TimeoutError as e:
        ...     print(f"Request to {e.source} timed out after {e.timeout}s")
    """

    def __init__(self, source: str, timeout: float):
        self.source = source
        self.timeout = timeout
        super().__init__(f"{source} request timed out after {timeout} seconds")


class CancellationError(VulnerabilityScanError):
    """
    Exception raised when an operation is cancelled.

    This exception is raised when a long-running operation is cancelled
    through a CancellationContext, allowing graceful interruption of
    vulnerability scanning operations.

    Attributes:
        message: Human-readable error message describing the cancellation

    Example:
        >>> try:
        ...     with CancellationContext() as ctx:
        ...         # Long operation that checks ctx.is_cancelled()
        ...         ctx.raise_if_cancelled()
        ... except CancellationError as e:
        ...     print(f"Operation cancelled: {e.message}")
    """

    def __init__(self, message: str = "Operation was cancelled"):
        self.message = message
        super().__init__(message)
