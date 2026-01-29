# Copyright (c) 2025 Divyanshu Sinha
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Command-line interface for pythonaibrain-llm."""

import sys
import argparse
from pathlib import Path

from .exceptions import LLMError
from .system_check import validate_system, get_system_ram_gb
from .model_loader import load_llm_model, get_model_info, model_exists
from .config import MIN_RAM_GB, MODEL_SIZE_MB


def cmd_check(args) -> int:
    """Run system readiness check."""
    print("=" * 60)
    print("pythonaibrain-llm System Check")
    print("=" * 60)
    
    try:
        info = validate_system()
        
        print(f"✓ Platform: {info['platform']}")
        print(f"✓ Python: {info['python_version']}")
        print(f"✓ System RAM: {info['ram_gb']:.2f} GB (minimum: {MIN_RAM_GB} GB)")
        print(f"✓ pythonaibrain: {info['pythonaibrain_version']} (minimum: 1.1.9)")
        
        model_info = get_model_info()
        if model_info['cached']:
            print(f"✓ Model: Cached at {model_info['cache_path']}")
        else:
            print(f"⚠ Model: Not cached (~{MODEL_SIZE_MB} MB will be downloaded)")
            print(f"  Repository: {model_info['repo_id']}")
        
        print()
        print(f"Status: {info['status'].upper()}")
        print("Your system meets all requirements for pythonaibrain-llm.")
        return 0
        
    except LLMError as e:
        print(f"✗ Validation Failed")
        print(f"  {e}")
        return 1
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
        return 1


def cmd_download(args) -> int:
    """Download model to cache."""
    print("Downloading model...")
    
    try:
        path = load_llm_model(force_download=args.force)
        print(f"✓ Model ready at: {path}")
        
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"  Size: {size_mb:.2f} MB")
        return 0
        
    except LLMError as e:
        print(f"✗ Download Failed: {e}")
        return 1
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
        return 1


def cmd_info(args) -> int:
    """Show model information."""
    info = get_model_info()
    
    print("Model Information:")
    print(f"  Repository: {info['repo_id']}")
    print(f"  Filename: {info['filename']}")
    print(f"  Cached: {'Yes' if info['cached'] else 'No'}")
    print(f"  Cache Path: {info['cache_path']}")
    
    if info['cached']:
        path = Path(info['cache_path'])
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"  Size: {size_mb:.2f} MB")
    
    return 0


def cmd_clear(args) -> int:
    """Clear model cache."""
    info = get_model_info()
    cache_path = Path(info['cache_path'])
    
    if not cache_path.exists():
        print("No cached model to clear.")
        return 0
    
    if not args.force:
        response = input(f"Delete {cache_path}? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return 0
    
    try:
        cache_path.unlink()
        print(f"✓ Removed {cache_path}")
        return 0
    except Exception as e:
        print(f"✗ Failed to remove cache: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="pythonaibrain-llm",
        description="LLM extension for pythonaibrain",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # check command
    parser_check = subparsers.add_parser(
        "check",
        help="Validate system requirements and readiness"
    )
    parser_check.set_defaults(func=cmd_check)
    
    # download command
    parser_download = subparsers.add_parser(
        "download",
        help="Download model to cache"
    )
    parser_download.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if cached"
    )
    parser_download.set_defaults(func=cmd_download)
    
    # info command
    parser_info = subparsers.add_parser(
        "info",
        help="Show model information"
    )
    parser_info.set_defaults(func=cmd_info)
    
    # clear command
    parser_clear = subparsers.add_parser(
        "clear",
        help="Clear model cache"
    )
    parser_clear.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt"
    )
    parser_clear.set_defaults(func=cmd_clear)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())