# Binary SBOM Generator

[![PyPI version](https://badge.fury.io/py/binary-sbom.svg)](https://pypi.org/project/binary-sbom/)
[![Python Version](https://img.shields.io/pypi/pyversions/binary-sbom)](https://pypi.org/project/binary-sbom/)
[![License](https://img.shields.io/pypi/l/binary-sbom)](https://pypi.org/project/binary-sbom/)

A command-line tool for analyzing binary files (`.bin`, `.elf`, `.exe`, etc.) and generating Software Bill of Materials (SBOM) documents in [SPDX](https://spdx.dev/) format.

## Features

- **Multi-Format Binary Support**: Analyzes ELF, PE, MachO, and raw binary files
- **SPDX 2.3 Compliant**: Generates SBOM documents following SPDX 2.3 specification
- **Multiple Output Formats**: JSON, XML, YAML, and Tag-Value formats
- **Metadata Extraction**: Extracts binary name, type, architecture, entrypoint, sections, and dependencies
- **Configuration File Support**: Customize behavior with `.binary-sbom.yml`
- **Verbose Mode**: Progress messages for debugging and monitoring
- **Supply Chain Security**: Enhances security and compliance through transparency

## Installation

### Install via PyPI (Recommended)

The easiest way to install `binary-sbom` is via PyPI:

```bash
pip install binary-sbom
```

This installs the tool and all required dependencies automatically.

**Requirements:**
- Python 3.8 or higher
- pip (Python package installer)

### Install from Source

To install from source, clone the repository and install in development mode:

```bash
# Clone the repository
git clone https://github.com/your-org/binary-sbom.git
cd binary-sbom

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies (optional, for testing)
pip install -e ".[dev]"
```

### Verify Installation

```bash
binary-sbom --help
```

## Usage

### Basic Usage

Generate a SBOM from a binary file:

```bash
binary-sbom --input firmware.bin --output sbom.json
```

### Command-Line Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--input` | `-i` | Yes | Input binary file to analyze |
| `--output` | `-o` | Yes | Output SBOM file path |
| `--format` | `-f` | No | SPDX output format: `json`, `xml`, `yaml`, `tag-value` (default: `json`) |
| `--verbose` | `-v` | No | Enable verbose output with progress messages |
| `--help` | `-h` | No | Show help message and exit |

### Examples

#### Generate JSON SBOM (default format)

```bash
binary-sbom --input application.bin --output sbom.json
```

#### Generate XML SBOM with verbose output

```bash
binary-sbom -i app.exe -o sbom.xml --format xml --verbose
```

#### Generate YAML SBOM

```bash
binary-sbom --input firmware.elf --output sbom.yaml --format yaml
```

#### Generate Tag-Value SBOM

```bash
binary-sbom -i binary.bin -o sbom.spdx --format tag-value
```

#### Short options

```bash
binary-sbom -i input.bin -o output.json -f json -v
```

### Verbose Output

Verbose mode provides detailed progress information:

```bash
$ binary-sbom --input firmware.bin --output sbom.json --verbose
Analyzing binary file: firmware.bin
  - Binary Type: ELF
  - Architecture: x86_64
  - Sections: 12
  - Dependencies: 5
Creating SPDX document...
Writing SBOM to: sbom.json
  - Format: json
✓ SBOM generated successfully: sbom.json
```

### Non-Verbose Output

Non-verbose mode prints only the output file path (useful for scripting):

```bash
$ binary-sbom --input firmware.bin --output sbom.json
sbom.json
```

## Configuration

You can customize tool behavior using a YAML configuration file.

### Configuration File Locations

The tool searches for configuration files in the following order (first found is used):

1. Environment variable `BINARY_SBOM_CONFIG`
2. Current directory: `.binary-sbom.yml`
3. Home directory: `~/.binary-sbom.yml`

### Configuration Options

Create a `.binary-sbom.yml` file:

```yaml
# SPDX output format (json, xml, yaml, tag-value)
output_format: json

# Logging level (DEBUG, INFO, WARNING, ERROR)
log_level: INFO

# Temporary directory for intermediate files
temp_dir: /tmp/binary-sbom

# Maximum input file size in MB
max_file_size_mb: 100
```

### Using Custom Configuration Path

```bash
export BINARY_SBOM_CONFIG=/path/to/config.yml
binary-sbom --input firmware.bin --output sbom.json
```

## Binary Format Support

The tool supports the following binary formats:

| Format | Description | Common Extensions |
|--------|-------------|-------------------|
| **ELF** | Executable and Linkable Format (Linux/Unix) | `.elf`, `.so`, `.bin` |
| **PE** | Portable Executable (Windows) | `.exe`, `.dll` |
| **MachO** | Mach Object (macOS/iOS) | `.dylib`, `.app` |
| **Raw** | Raw binary data (fallback) | `.bin`, `.raw` |

### Extracted Metadata

For each binary, the tool extracts:

- **Name**: Binary file name or internal name
- **Type**: Binary format (ELF, PE, MachO, Raw)
- **Architecture**: Target architecture (x86_64, ARM, etc.)
- **Entrypoint**: Entry point address (if available)
- **Sections**: Code and data sections with sizes and addresses
- **Dependencies**: Imported libraries and shared objects

## SPDX Output Formats

### JSON Format

```bash
binary-sbom --input app.bin --output sbom.json --format json
```

Structured JSON output following SPDX 2.3 schema. Ideal for automated processing and web applications.

### XML Format

```bash
binary-sbom --input app.bin --output sbom.xml --format xml
```

XML output following SPDX 2.3 schema. Suitable for enterprise tools and legacy systems.

### YAML Format

```bash
binary-sbom --input app.bin --output sbom.yaml --format yaml
```

Human-readable YAML format. Great for configuration management and version control.

### Tag-Value Format

```bash
binary-sbom --input app.bin --output sbom.spdx --format tag-value
```

Plain text Tag-Value format. The original SPDX format, widely supported and human-readable.

## Development

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-org/binary-sbom.git
cd binary-sbom

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_analyzer.py -v

# Run with coverage report
pytest tests/ --cov=src/binary_sbom --cov-report=html

# Run coverage in terminal
pytest tests/ --cov=src/binary_sbom --cov-report=term-missing
```

### Code Quality

```bash
# Type checking
mypy src/binary_sbom/ --ignore-missing-imports

# Linting
flake8 src/binary_sbom/ --max-line-length=100

# Code formatting
black src/binary_sbom/ tests/

# Run all quality checks
pytest tests/ && mypy src/binary_sbom/ && flake8 src/binary_sbom/
```

### Project Structure

```
binary-sbom/
├── pyproject.toml          # Package configuration
├── README.md               # This file
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore patterns
├── src/
│   └── binary_sbom/
│       ├── __init__.py     # Package initialization
│       ├── cli.py          # CLI interface
│       ├── analyzer.py     # Binary analysis logic
│       ├── generator.py    # SPDX document generation
│       └── config.py       # Configuration handling
└── tests/
    ├── __init__.py
    ├── test_analyzer.py    # Analyzer tests
    ├── test_generator.py   # Generator tests
    ├── test_cli.py         # CLI tests
    ├── test_config.py      # Config tests
    ├── test_integration.py # Integration tests
    ├── test_e2e.py         # End-to-end tests
    └── fixtures/
        ├── __init__.py
        └── binaries.py     # Test fixtures
```

## Error Handling

The tool provides clear error messages for common issues:

```bash
# File not found
$ binary-sbom --input missing.bin --output sbom.json
Error: File 'missing.bin' does not exist.

# File too large
$ binary-sbom --input huge.bin --output sbom.json
Error: Input file too large: 150.25MB (maximum allowed: 100MB)

# Invalid format
$ binary-sbom --input app.bin --output sbom.txt --format txt
Error: Invalid value for '--format': 'txt' is not one of 'json', 'xml', 'yaml', 'tag-value'.
```

## Exit Codes

- `0`: Success
- `1`: Error (file not found, parse error, write error, etc.)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Write unit tests for new features
- Ensure code coverage remains ≥ 80%
- Follow PEP 8 style guidelines
- Add docstrings to public functions
- Update documentation for user-facing changes

## Support

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/your-org/binary-sbom/issues)
- **SPDX Specification**: [https://spdx.dev/](https://spdx.dev/)

## Acknowledgments

- [LIEF](https://lief.re/) - Library to Instrument Executable Formats
- [spdx-tools](https://github.com/spdx/spdx-tools) - SPDX Python tools
- [Click](https://click.palletsprojects.com/) - CLI framework

## Security

For security considerations or to report vulnerabilities, please email security@your-org.com.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a complete history of changes, including the latest [v1.0.0](CHANGELOG.md#100---2026-01-12) release.
