# Copyright (c) 2025 Divyanshu Sinha
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
pythonaibrain-llm: LLM extension for pythonaibrain.

This package provides quantized LLM model support for pythonaibrain with
automatic model downloading, caching, and system validation.

Minimal Requirements:
    - Python >= 3.9
    - System RAM >= 4 GB
    - pythonaibrain >= 1.1.9

Example:
    >>> from pythonaibrain_llm import load_llm_model
    >>> model_path = load_llm_model()
    >>> print(f"Model ready at: {model_path}")
"""

from .__version__ import __version__
from .model_loader import load_llm_model, get_model_info, model_exists
from .system_check import (
    validate_system,
    get_system_ram_gb,
    check_ram_requirement,
    check_engine_version,
)
from .exceptions import (
    LLMError,
    InsufficientRAMError,
    EngineVersionError,
    ModelDownloadError,
    ModelValidationError,
)

__all__ = [
    "__version__",
    # Main API
    "load_llm_model",
    "get_model_info",
    "model_exists",
    # System checks
    "validate_system",
    "get_system_ram_gb",
    "check_ram_requirement",
    "check_engine_version",
    # Exceptions
    "LLMError",
    "InsufficientRAMError",
    "EngineVersionError",
    "ModelDownloadError",
    "ModelValidationError",
