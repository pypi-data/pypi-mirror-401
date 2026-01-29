# Copyright (c) 2025 Divyanshu Sinha
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Custom exceptions for pythonaibrain-llm."""


class LLMError(Exception):
    """Base exception for all LLM-related errors."""
    pass


class InsufficientRAMError(LLMError):
    """Raised when system RAM is below minimum requirements."""
    
    def __init__(self, available_gb: float, required_gb: float = 4.0):
        self.available_gb = available_gb
        self.required_gb = required_gb
        msg = (
            f"Insufficient system RAM: {available_gb:.2f} GB available, "
            f"but {required_gb:.2f} GB minimum required.\n"
            f"The LLM model requires at least {required_gb} GB of RAM to operate safely.\n"
            f"Consider upgrading your system or using a machine with more memory."
        )
        super().__init__(msg)


class EngineVersionError(LLMError):
    """Raised when pythonaibrain version is incompatible."""
    
    def __init__(self, current_version: str, required_version: str = "1.1.9"):
        self.current_version = current_version
        self.required_version = required_version
        msg = (
            f"Incompatible pythonaibrain version: {current_version} installed, "
            f"but >={required_version} required.\n"
            f"Upgrade with: pip install --upgrade 'pythonaibrain>={required_version}'"
        )
        super().__init__(msg)


class ModelDownloadError(LLMError):
    """Raised when model download fails."""
    
    def __init__(self, repo_id: str, reason: str):
        self.repo_id = repo_id
        self.reason = reason
        msg = (
            f"Failed to download model from {repo_id}.\n"
            f"Reason: {reason}\n"
            f"Check your internet connection and Hugging Face access."
        )
        super().__init__(msg)


class ModelValidationError(LLMError):
    """Raised when downloaded model fails validation."""
    
    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        msg = (
            f"Model validation failed for {path}.\n"
            f"Reason: {reason}\n"
            f"The model file may be corrupted. Try deleting it and re-downloading."
        )
        super().__init__(msg)