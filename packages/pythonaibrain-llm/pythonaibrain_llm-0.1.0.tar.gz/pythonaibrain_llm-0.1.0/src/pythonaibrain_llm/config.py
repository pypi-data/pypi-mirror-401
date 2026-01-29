# Copyright (c) 2025 Divyanshu Sinha
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Model configuration and constants."""

from pathlib import Path


# Model repository configuration
MODEL_REPO_ID = "DivyanshuSinha/TIGER"
MODEL_FILENAME = "model.safetensors"
MODEL_SIZE_MB = 988

# Local cache configuration
CACHE_DIR = Path.home() / ".cache" / "pythonaibrain-llm"
MODEL_CACHE_PATH = CACHE_DIR / MODEL_FILENAME

# Download configuration
CHUNK_SIZE = 8 * 1024 * 1024  # 8 MB chunks for resumable downloads
DOWNLOAD_TIMEOUT = 600  # 10 minutes
MAX_RETRIES = 3

# Version requirements
MIN_ENGINE_VERSION = "1.1.9"
