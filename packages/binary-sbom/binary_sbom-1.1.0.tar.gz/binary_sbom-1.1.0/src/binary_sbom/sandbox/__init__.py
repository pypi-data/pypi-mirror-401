"""
Sandboxed binary processing for Binary SBOM Generator.

This package provides process isolation, resource limits, and secure temporary
file handling to protect against malicious binary exploits during LIEF parsing.

The sandbox architecture uses:
- multiprocessing.Process for process isolation
- resource module for kernel-enforced limits (memory, CPU)
- tempfile module for isolated temporary directories
- multiprocessing.Queue for secure IPC

Example:
    >>> from binary_sbom.sandbox import SandboxManager
    >>> manager = SandboxManager()
    >>> metadata = manager.parse_binary('/path/to/binary')
    >>> print(metadata['type'])
    'ELF'

    >>> # With configuration
    >>> from binary_sbom.sandbox import SandboxManager, SandboxConfig
    >>> config = SandboxConfig(memory_mb=1000)
    >>> manager = SandboxManager(sandbox_config=config)
    >>> metadata = manager.parse_binary('/path/to/binary')
"""

from binary_sbom.sandbox.config import SandboxConfig, load_config
from binary_sbom.sandbox.errors import (
    SandboxCrashedError,
    SandboxError,
    SandboxFileError,
    SandboxMemoryError,
    SandboxSecurityError,
    SandboxTimeoutError,
)
from binary_sbom.sandbox.manager import SandboxManager
from binary_sbom.sandbox.metrics import SandboxMetrics, get_global_metrics, reset_global_metrics

__all__ = [
    "SandboxManager",
    "SandboxConfig",
    "load_config",
    "SandboxError",
    "SandboxTimeoutError",
    "SandboxMemoryError",
    "SandboxSecurityError",
    "SandboxFileError",
    "SandboxCrashedError",
    "SandboxMetrics",
    "get_global_metrics",
    "reset_global_metrics",
]

__version__ = "0.1.0"
