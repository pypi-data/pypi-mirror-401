# Copyright (c) 2025 Divyanshu Sinha
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Cross-platform system requirements validation."""

import platform
import psutil
from packaging import version

from .exceptions import InsufficientRAMError, EngineVersionError


MIN_RAM_GB = 4.0


def get_system_ram_gb() -> float:
    """
    Get total system RAM in GB across all platforms.
    
    Returns:
        Total RAM in gigabytes (rounded to 2 decimals).
    
    Raises:
        RuntimeError: If RAM detection fails.
    """
    try:
        mem = psutil.virtual_memory()
        ram_gb = mem.total / (1024 ** 3)
        return round(ram_gb, 2)
    except Exception as e:
        raise RuntimeError(f"Failed to detect system RAM: {e}") from e


def check_ram_requirement(min_gb: float = MIN_RAM_GB) -> None:
    """
    Verify system has minimum required RAM.
    
    Args:
        min_gb: Minimum RAM required in GB (default: 4.0).
    
    Raises:
        InsufficientRAMError: If available RAM is below minimum.
    """
    available = get_system_ram_gb()
    if available < min_gb:
        raise InsufficientRAMError(available, min_gb)


def check_engine_version(min_version: str = "1.1.9") -> None:
    """
    Verify pythonaibrain meets minimum version requirement.
    
    Args:
        min_version: Minimum required version string.
    
    Raises:
        EngineVersionError: If installed version is too old.
        ImportError: If pythonaibrain is not installed.
    """
    try:
        import pythonaibrain
        current = pythonaibrain.__version__
    except ImportError as e:
        raise ImportError(
            "pythonaibrain not found. Install with: pip install pythonaibrain>=1.1.9"
        ) from e
    except AttributeError as e:
        raise ImportError(
            "pythonaibrain installation is corrupted (missing __version__). "
            "Reinstall with: pip install --force-reinstall pythonaibrain>=1.1.9"
        ) from e
    
    if version.parse(current) < version.parse(min_version):
        raise EngineVersionError(current, min_version)


def validate_system() -> dict:
    """
    Run all system validation checks.
    
    Returns:
        Dictionary with system information and validation status.
    
    Raises:
        InsufficientRAMError: If RAM requirement not met.
        EngineVersionError: If engine version incompatible.
    """
    import pythonaibrain
    
    check_ram_requirement()
    check_engine_version()
    
    return {
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "ram_gb": get_system_ram_gb(),
        "pythonaibrain_version": pythonaibrain.__version__,
        "status": "ready",
    }