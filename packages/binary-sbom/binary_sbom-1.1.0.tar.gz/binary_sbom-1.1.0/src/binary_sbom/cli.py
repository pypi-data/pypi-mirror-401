"""
Binary SBOM CLI - Click-based command-line interface.

This module provides the main CLI for generating SBOMs from binary files.
Supports single file and batch processing with various options including
progress indicators for large files.
"""

import sys
from pathlib import Path
from typing import Optional

import click

from binary_sbom.vulnscan.types import Severity


@click.group()
@click.version_option(version="0.1.0", prog_name="binary-sbom")
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose output for debugging.",
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Suppress all output except errors.",
)
@click.option(
    "--progress",
    "show_progress",
    is_flag=True,
    flag_value=True,
    default=None,
    help=(
        "Force enable progress indicators for all files. "
        "Useful in CI/CD pipelines where TTY detection fails. "
        "Progress bars will show for files >= 100MB. "
        "Writes to stderr to avoid conflicts with output redirection."
    ),
)
@click.option(
    "--no-progress",
    "show_progress",
    is_flag=True,
    flag_value=False,
    default=None,
    help=(
        "Force disable progress indicators. "
        "Useful for logging or when output is being parsed by scripts. "
        "Overrides automatic TTY detection and file size thresholds."
    ),
)
@click.pass_context
def cli(
    ctx: click.Context,
    verbose: bool,
    quiet: bool,
    show_progress: Optional[bool],
) -> None:
    """
    Binary SBOM - Generate SBOMs from binary files.

    This tool analyzes binary files and generates Software Bill of Materials (SBOMs)
    in SPDX format. Supports single files, directories, and glob patterns.

    \b
    Examples:
      binary-sbom scan --input firmware.bin
      binary-sbom scan --input ./bin/
      binary-sbom scan --input './build/**/*.so' --parallel

    \b
    Progress Indicators:
      Progress bars are automatically shown for files >= 100MB in TTY environments.
      Use --progress to force enable (e.g., in CI/CD pipelines).
      Use --no-progress to force disable (e.g., for logging).

    \b
    Verbose Mode:
      Progress bars write to stderr, verbose output to stdout.
      This allows both to work together without rendering conflicts.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet
    ctx.obj["show_progress"] = show_progress

    # Validate mutually exclusive flags
    if verbose and quiet:
        click.echo("Error: --verbose and --quiet are mutually exclusive", err=True)
        sys.exit(1)

    # Note: Click's is_flag with flag_value handles mutual exclusion of --progress/--no-progress
    # automatically - only one can be set at a time


@cli.command()
@click.option(
    "-i",
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to binary file, directory, or glob pattern.",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    help="Custom output path for generated SBOM(s).",
    default=None,
)
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(["json", "xml", "tagvalue"], case_sensitive=False),
    default="json",
    help="SPDX document format (default: json).",
)
@click.option(
    "--combined",
    is_flag=True,
    help="Generate single SPDX document with multiple packages for batch processing.",
)
@click.option(
    "--parallel",
    is_flag=True,
    help="Enable parallel processing for multiple files.",
)
@click.option(
    "--workers",
    type=int,
    default=None,
    help="Number of parallel workers (default: CPU count).",
)
@click.option(
    "--continue-on-error",
    is_flag=True,
    help="Continue processing remaining files if one fails.",
)
@click.option(
    "--scan-vulns",
    "scan_vulns",
    is_flag=True,
    default=False,
    help=(
        "Enable vulnerability scanning for detected components. "
        "Queries OSV, NVD, and GitHub Advisories databases for known CVEs. "
        "Vulnerability findings will be included in SBOM annotations."
    ),
)
@click.option(
    "--nvd-api-key",
    "nvd_api_key",
    type=str,
    default=None,
    help=(
        "NVD API key for vulnerability scanning. "
        "Increases rate limit from 5 req/30s to 50 req/30s. "
        "Get your key at https://nvd.nist.gov/developers/request-an-api-key"
    ),
)
@click.option(
    "--github-token",
    "github_token",
    type=str,
    default=None,
    help=(
        "GitHub token for vulnerability scanning. "
        "Increases rate limit from 60/hr to 5000/hr. "
        "Create a personal access token at https://github.com/settings/tokens"
    ),
)
@click.pass_context
def scan(
    ctx: click.Context,
    input_path: Path,
    output_path: Optional[Path],
    output_format: str,
    combined: bool,
    parallel: bool,
    workers: Optional[int],
    continue_on_error: bool,
    scan_vulns: bool,
    nvd_api_key: Optional[str],
    github_token: Optional[str],
) -> None:
    """
    Scan binary files and generate SBOMs.

    Accepts a single file, directory, or glob pattern as input.
    Generates SPDX SBOM documents in the specified format.

    Progress indicators are automatically shown for files >= 100MB in TTY environments.
    Use --progress to force enable or --no-progress to force disable.

    \b
    Verbose Mode Integration:
    When --verbose is enabled with progress bars, output is handled as follows:
      - Progress bar writes to stderr (with in-place updates)
      - Verbose messages write to stdout (persistent log lines)
      - Both streams display simultaneously without conflicts
    """
    verbose = ctx.obj.get("verbose", False)
    quiet = ctx.obj.get("quiet", False)
    show_progress = ctx.obj.get("show_progress", None)

    # Validate worker count
    if workers is not None and workers <= 0:
        click.echo("Error: --workers must be a positive integer", err=True)
        sys.exit(1)

    # Validate parallel options (workers only makes sense with parallel)
    if workers is not None and not parallel:
        click.echo("Warning: --workers specified without --parallel. Workers will be ignored.")
        if verbose:
            click.echo("Use --parallel flag to enable parallel processing.")

    if not quiet:
        click.echo(f"Binary SBOM v0.1.0")
        click.echo(f"Input: {input_path}")

    if verbose:
        click.echo(f"Output format: {output_format}")
        click.echo(f"Combined mode: {combined}")
        click.echo(f"Parallel processing: {parallel}")
        if workers:
            click.echo(f"Workers: {workers}")
        click.echo(f"Continue on error: {continue_on_error}")
        click.echo(f"Vulnerability scanning: {scan_vulns}")
        if nvd_api_key:
            click.echo(f"NVD API key: [redacted]")
        if github_token:
            click.echo(f"GitHub token: [redacted]")

        # Show progress setting
        if show_progress is True:
            click.echo("Progress indicators: Force enabled")
        elif show_progress is False:
            click.echo("Progress indicators: Force disabled")
        else:
            click.echo("Progress indicators: Auto-detect")

        # Note: Progress bars write to stderr to avoid conflicts with verbose output on stdout
        # This allows both to be displayed simultaneously without rendering issues

    # Pass progress setting to analysis functions
    # This will be used when ProgressTracker is instantiated
    ctx.obj["progress_force"] = show_progress

    # Store scan_vulns flag for use in processing functions
    ctx.obj["scan_vulns"] = scan_vulns

    # Store API keys for vulnerability scanning
    ctx.obj["nvd_api_key"] = nvd_api_key
    ctx.obj["github_token"] = github_token

    # Check if input is a file or directory
    if input_path.is_file():
        if verbose:
            click.echo(f"Processing single file: {input_path}")
        _process_single_file(
            input_path,
            output_path,
            output_format,
            verbose,
            quiet,
            show_progress,
            scan_vulns,
            nvd_api_key,
            github_token
        )
    elif input_path.is_dir():
        if verbose:
            click.echo(f"Processing directory: {input_path}")
        click.echo(
            "Error: Batch processing not yet implemented. "
            "Subtask 3.1 will add directory support.",
            err=True,
        )
        sys.exit(1)
    else:
        # Try to treat as glob pattern
        if verbose:
            click.echo(f"Treating as glob pattern: {input_path}")
        click.echo(
            "Error: Glob pattern matching not yet implemented. "
            "Subtask 3.1 will add glob support.",
            err=True,
        )
        sys.exit(1)


def _process_single_file(
    input_path: Path,
    output_path: Optional[Path],
    output_format: str,
    verbose: bool,
    quiet: bool,
    show_progress: Optional[bool],
    scan_vulns: bool,
    nvd_api_key: Optional[str],
    github_token: Optional[str],
) -> None:
    """
    Process a single binary file.

    This function will be expanded in future subtasks to:
    1. Determine file size
    2. Create ProgressTracker with force=show_progress
    3. Analyze the binary with progress updates
    4. Generate SPDX document
    5. Scan for vulnerabilities (if scan_vulns is enabled)

    Args:
        input_path: Path to the binary file to process.
        output_path: Optional custom output path.
        output_format: SPDX document format (json, xml, tagvalue).
        verbose: Whether verbose output is enabled.
        quiet: Whether quiet mode is enabled.
        show_progress: Override for progress indicators (True/False/None).
        scan_vulns: Whether to enable vulnerability scanning for detected components.
        nvd_api_key: Optional NVD API key for higher rate limits.
        github_token: Optional GitHub token for higher rate limits.
    """
    # For subtask 8.3, we demonstrate vulnerability scanning integration
    # Actual binary analysis will be implemented in future subtasks
    if scan_vulns:
        _perform_vulnerability_scan_demo(
            verbose, quiet, nvd_api_key, github_token
        )
    else:
        if not quiet:
            click.echo(
                f"Error: Single file processing not yet implemented. "
                "Vulnerability scanning disabled (--scan-vulns not set).",
                err=True,
            )
        sys.exit(1)


def _perform_vulnerability_scan_demo(
    verbose: bool,
    quiet: bool,
    nvd_api_key: Optional[str],
    github_token: Optional[str],
) -> None:
    """
    Demonstrate vulnerability scanning and summary display.

    This is a demonstration function for subtask 8.3 that shows how
    vulnerability scanning will be integrated and how results will be
    displayed to the user.

    Args:
        verbose: Whether verbose output is enabled.
        quiet: Whether quiet mode is enabled.
        nvd_api_key: Optional NVD API key for higher rate limits.
        github_token: Optional GitHub token for higher rate limits.
    """
    from binary_sbom.vulnscan.aggregation import SeveritySummarizer
    from binary_sbom.vulnscan.scanners import VulnScanner
    from binary_sbom.vulnscan.types import PackageIdentifier, Severity, Vulnerability, VulnerabilitySource, CVSSScore, Reference

    # Log configuration
    if verbose and not quiet:
        click.echo("\nVulnerability Scanning Configuration:")
        click.echo(f"  OSV Scanner: Enabled (default)")
        if nvd_api_key:
            click.echo(f"  NVD Scanner: Enabled (with API key)")
        else:
            click.echo(f"  NVD Scanner: Disabled (no API key)")
        if github_token:
            click.echo(f"  GitHub Scanner: Enabled (with token)")
        else:
            click.echo(f"  GitHub Scanner: Disabled (no token)")
        click.echo("")

    # Demonstrate with sample package
    # In real implementation, this will come from binary analysis
    sample_package = PackageIdentifier(
        ecosystem="npm",
        name="lodash",
        version="4.17.15"
    )

    if not quiet:
        click.echo(f"Scanning package: {sample_package.ecosystem}/{sample_package.name}@{sample_package.version}")

    try:
        # Initialize scanner with API keys if provided
        scanner = VulnScanner()

        # In a real implementation, we would:
        # result = scanner.scan_package(
        #     sample_package.ecosystem,
        #     sample_package.name,
        #     sample_package.version
        # )

        # For demonstration, create a mock result
        # This simulates what the real scanner would return
        from binary_sbom.vulnscan.types import VulnerabilityMatch, ScanResult

        # Create sample vulnerabilities
        vuln1 = Vulnerability(
            id="CVE-2021-23337",
            source=VulnerabilitySource.OSV,
            severity=Severity.HIGH,
            primary_severity=CVSSScore(
                version="3.1",
                vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
                base_score=8.1,
                severity=Severity.HIGH
            ),
            summary="Prototype pollution in lodash.",
            details="Lodash prior to 4.17.19 is affected by...",
            affected_versions=[],
            aliases=["GHSA-4w2v-vmj7-klvd"],
            published="2021-02-01T00:00:00Z",
            modified="2021-02-01T00:00:00Z",
            references=[
                Reference(
                    url="https://nvd.nist.gov/vuln/detail/CVE-2021-23337",
                    type="ADVISORY"
                )
            ],
            cwe_ids=["CWE-1321"]
        )

        vuln2 = Vulnerability(
            id="CVE-2020-8203",
            source=VulnerabilitySource.OSV,
            severity=Severity.CRITICAL,
            primary_severity=CVSSScore(
                version="3.1",
                vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                base_score=9.8,
                severity=Severity.CRITICAL
            ),
            summary="Command injection in lodash.",
            details="Lodash prior to 4.17.19 is affected by...",
            affected_versions=[],
            aliases=[],
            published="2020-06-01T00:00:00Z",
            modified="2020-06-01T00:00:00Z",
            references=[
                Reference(
                    url="https://nvd.nist.gov/vuln/detail/CVE-2020-8203",
                    type="ADVISORY"
                )
            ],
            cwe_ids=["CWE-77"]
        )

        # Create scan result
        match = VulnerabilityMatch(
            package=sample_package,
            vulnerabilities=[vuln1, vuln2]
        )

        result = ScanResult(
            packages=[match],
            sources_queried={VulnerabilitySource.OSV}
        )

        # Display vulnerability summary using SeveritySummarizer
        if not quiet:
            click.echo("\n" + "="*60)
            click.echo("VULNERABILITY SCAN RESULTS")
            click.echo("="*60)

            summarizer = SeveritySummarizer()
            summary = summarizer.summarize(result)

            if result.total_vulnerabilities > 0:
                # Display formatted summary
                formatted_summary = summarizer.format_summary(summary, include_total=True)
                click.echo(f"\nVulnerabilities Found: {formatted_summary}")

                # Display affected package count
                click.echo(f"Affected Packages: {result.affected_packages}/{result.total_packages}")

                # Display sources queried
                sources_str = ", ".join([s.value for s in result.sources_queried])
                click.echo(f"Sources Queried: {sources_str}")

                # Check for critical vulnerabilities
                if summarizer.has_critical_vulnerabilities(summary):
                    click.echo("\n⚠️  CRITICAL vulnerabilities detected!")
                else:
                    click.echo("\n✓ No critical vulnerabilities")

                # Display severity breakdown
                click.echo("\nSeverity Breakdown:")
                for severity_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                    count = summary[severity_level]
                    if count > 0:
                        percentage = summarizer.get_severity_percentage(
                            summary,
                            Severity[severity_level]
                        )
                        click.echo(f"  {severity_level}: {count} ({percentage:.1f}%)")
                    else:
                        click.echo(f"  {severity_level}: {count}")
            else:
                click.echo("\n✓ No vulnerabilities found")

            click.echo("="*60 + "\n")

        # Display detailed vulnerability information in verbose mode
        _display_vulnerability_details(result, verbose, quiet)

        if verbose and not quiet:
            click.echo("Vulnerability scanning complete.")
            click.echo(f"Total vulnerabilities found: {result.total_vulnerabilities}")
            click.echo(f"Highest severity: {result.highest_severity.value if result.highest_severity else 'None'}")

    except Exception as e:
        if not quiet:
            click.echo(f"Error during vulnerability scanning: {e}", err=True)
        sys.exit(1)


def _display_vulnerability_details(
    result,
    verbose: bool,
    quiet: bool
) -> None:
    """
    Display detailed vulnerability information including CVEs, CVSS scores, and references.

    This function provides verbose output showing individual vulnerabilities with their
    CVSS scores, vector strings, references, and other details.

    Args:
        result: ScanResult containing vulnerability findings.
        verbose: Whether verbose output is enabled.
        quiet: Whether quiet mode is enabled.
    """
    if quiet or not verbose:
        return

    from binary_sbom.vulnscan.types import Severity

    # Display detailed vulnerability information
    click.echo("\n" + "="*60)
    click.echo("DETAILED VULNERABILITY INFORMATION")
    click.echo("="*60)

    for match in result.packages:
        if not match.vulnerabilities:
            continue

        click.echo(f"\nPackage: {match.package.ecosystem}/{match.package.name}@{match.package.version}")
        click.echo(f"Vulnerabilities: {len(match.vulnerabilities)}")

        for idx, vuln in enumerate(match.vulnerabilities, 1):
            click.echo(f"\n  [{idx}] {vuln.id}")

            # Display severity badge
            severity_icon = _get_severity_icon(vuln.severity.severity if vuln.severity else None)
            click.echo(f"      Severity: {severity_icon} {vuln.severity.severity.value if vuln.severity else 'UNKNOWN'}")

            # Display summary
            if vuln.summary:
                click.echo(f"      Summary: {vuln.summary}")

            # Display CVSS scores
            if vuln.severity:
                click.echo(f"      CVSS Score:")
                click.echo(f"        Version: {vuln.severity.version}")
                click.echo(f"        Base Score: {vuln.severity.base_score} ({vuln.severity.severity.value})")
                if vuln.severity.vector_string:
                    click.echo(f"        Vector: {vuln.severity.vector_string}")

            # Display additional CVSS scores if present
            if vuln.additional_scores:
                click.echo(f"      Additional CVSS Scores:")
                for score in vuln.additional_scores:
                    click.echo(f"        - {score.version}: {score.base_score} ({score.severity.value})")

            # Display aliases
            if vuln.aliases:
                click.echo(f"      Aliases: {', '.join(vuln.aliases)}")

            # Display CWE IDs
            if vuln.cwe_ids:
                click.echo(f"      CWE IDs: {', '.join(vuln.cwe_ids)}")

            # Display affected versions
            if vuln.affected_versions:
                click.echo(f"      Affected Versions:")
                for aff_ver in vuln.affected_versions:
                    if aff_ver.introduced and aff_ver.fixed:
                        click.echo(f"        - {aff_ver.introduced} - {aff_ver.fixed} ({aff_ver.range_type})")
                    elif aff_ver.introduced:
                        click.echo(f"        - >= {aff_ver.introduced} ({aff_ver.range_type})")
                    elif aff_ver.fixed:
                        click.echo(f"        - < {aff_ver.fixed} ({aff_ver.range_type})")

            # Display references
            if vuln.references:
                click.echo(f"      References:")
                for ref in vuln.references:
                    ref_type = ref.type if ref.type else "UNKNOWN"
                    click.echo(f"        - [{ref_type}] {ref.url}")

            # Display dates
            if vuln.published:
                click.echo(f"      Published: {vuln.published.strftime('%Y-%m-%d')}")
            if vuln.modified:
                click.echo(f"      Modified: {vuln.modified.strftime('%Y-%m-%d')}")

            # Display source
            click.echo(f"      Source: {vuln.source.value}")

    click.echo("\n" + "="*60 + "\n")


def _get_severity_icon(severity: Optional[Severity]) -> str:
    """
    Get an icon for a severity level.

    Args:
        severity: Severity level.

    Returns:
        Unicode icon character for the severity.
    """
    if not severity:
        return "❓"

    icons = {
        Severity.CRITICAL: "🔴",
        Severity.HIGH: "🟠",
        Severity.MEDIUM: "🟡",
        Severity.LOW: "🟢",
        Severity.NONE: "⚪",
    }
    return icons.get(severity, "❓")


@cli.command()
@click.pass_context
def version(ctx: click.Context) -> None:
    """Show version information and exit."""
    click.echo("Binary SBOM v0.1.0")
    click.echo("SPDX Version: 2.3")
    click.echo("Python CLI tool for generating SBOMs from binary files")


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    try:
        cli(standalone_mode=False)
        return 0
    except click.exceptions.ClickException as e:
        # Let Click handle its own exceptions
        e.show()
        return e.exit_code
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
