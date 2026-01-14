"""
CLI module for Binary SBOM Generator.

This module provides the command-line interface for analyzing binary files
and generating SPDX SBOM documents. It uses Click for argument parsing
and integrates the analyzer and generator modules.
"""

import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import click as click_type  # noqa: F401

try:
    import click
except ImportError:
    click = None  # type: ignore[assignment]  # pragma: no cover

from binary_sbom.analyzer import analyze_binary, BinaryAnalysisError
from binary_sbom.generator import (
    create_spdx_document,
    write_spdx_file,
    SPDXGenerationError,
)
from binary_sbom.config import load_config


class CLIError(Exception):
    """Exception raised when CLI execution fails."""

    pass


def main() -> int:
    """
    Main entry point for the CLI.

    This function is invoked when the binary-sbom command is run.
    It parses command-line arguments and orchestrates the SBOM generation workflow.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    if click is None:
        print(
            "Error: Click library is required. "
            "Install it with: pip install click",
            file=sys.stderr,
        )
        return 1

    # Run the Click command
    try:
        # pylint: disable=missing-kwoa
        cli(standalone_mode=False)
        return 0
    except click.exceptions.Exit as e:
        return e.exit_code
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1


@click.command()
@click.option(
    '--input',
    '-i',
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help='Input binary file to analyze (.bin, .elf, .exe, etc.)',
)
@click.option(
    '--output',
    '-o',
    required=True,
    type=click.Path(),
    help='Output SBOM file path (e.g., sbom.json, sbom.xml)',
)
@click.option(
    '--format',
    '-f',
    default='json',
    type=click.Choice(['json', 'xml', 'yaml', 'tag-value'], case_sensitive=False),
    help='SPDX output format (default: json)',
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Enable verbose output with progress messages',
)
def cli(input: str, output: str, format: str, verbose: bool) -> None:
    """
    Generate SBOM from binary files.

    This command analyzes a binary file and generates a Software Bill of Materials (SBOM)
    in SPDX format. The tool supports multiple binary formats (ELF, PE, MachO, raw) and
    can output SPDX documents in JSON, XML, YAML, or Tag-Value format.

    Example usage:

        binary-sbom --input firmware.bin --output sbom.json

        binary-sbom -i app.exe -o sbom.xml --format xml --verbose

    For more information, visit: https://github.com/your-org/binary-sbom-generator
    """
    try:
        # Load configuration
        config = load_config()

        # Validate input file
        try:
            file_size_mb = os.path.getsize(input) / (1024 * 1024)
            max_file_size_mb = config.get('max_file_size_mb', 100)

            if file_size_mb > max_file_size_mb:
                raise CLIError(
                    f"Input file too large: {file_size_mb:.2f}MB "
                    f"(maximum allowed: {max_file_size_mb}MB)"
                )
        except OSError as e:
            raise CLIError(f"Cannot access input file: {e}")

        # Override format from CLI if not explicitly provided
        # (Click already sets the default, so we just use the CLI value)
        output_format = format

        # Verbose: Analyzing binary
        if verbose:
            click.echo(f"Analyzing binary file: {input}")

        # Step 1: Analyze binary file
        try:
            metadata = analyze_binary(
                input, max_file_size_mb=config.get('max_file_size_mb', 100)
            )
        except (BinaryAnalysisError, FileNotFoundError, ImportError) as e:
            raise CLIError(f"Failed to analyze binary file: {e}")

        if verbose:
            click.echo(f"  - Binary Type: {metadata.get('type', 'Unknown')}")
            click.echo(f"  - Architecture: {metadata.get('architecture', 'Unknown')}")
            click.echo(f"  - Sections: {len(metadata.get('sections', []))}")
            click.echo(f"  - Dependencies: {len(metadata.get('dependencies', []))}")

        # Verbose: Creating SPDX document
        if verbose:
            click.echo("Creating SPDX document...")

        # Step 2: Create SPDX document
        try:
            document = create_spdx_document(metadata)
        except (SPDXGenerationError, ValueError, ImportError) as e:
            raise CLIError(f"Failed to create SPDX document: {e}")

        # Verbose: Writing output
        if verbose:
            click.echo(f"Writing SBOM to: {output}")
            click.echo(f"  - Format: {output_format}")

        # Step 3: Write SPDX document to file
        try:
            write_spdx_file(document, output, output_format)
        except (SPDXGenerationError, ValueError, IOError, ImportError) as e:
            raise CLIError(f"Failed to write SBOM file: {e}")

        # Success message
        if verbose:
            click.echo(f"✓ SBOM generated successfully: {output}")
        else:
            # Non-verbose mode: just print output file
            click.echo(output)

    except CLIError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())


__all__ = [
    'main',
    'cli',
    'CLIError',
]
