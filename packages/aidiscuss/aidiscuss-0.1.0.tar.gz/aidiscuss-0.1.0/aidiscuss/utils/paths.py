"""Path management for multi-environment data isolation."""

import os
import sys
from pathlib import Path


def get_virtualenv_path() -> Path | None:
    """
    Detect if running in a virtual environment.

    Returns:
        Path to virtual environment root if detected, None otherwise.

    Detection methods:
        - sys.real_prefix (virtualenv)
        - sys.base_prefix != sys.prefix (venv, Python 3.3+)
    """
    # Check for virtualenv or venv
    if hasattr(sys, "real_prefix"):
        # Old virtualenv
        return Path(sys.prefix)
    elif hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix:
        # Python 3.3+ venv or modern virtualenv
        return Path(sys.prefix)
    return None


def get_data_directory() -> Path:
    """
    Get environment-specific data directory for AIDiscuss.

    Directory selection logic:
    1. If AIDISCUSS_DATA_DIR environment variable is set, use it (user override)
    2. If running in virtual environment, use {venv_path}/.aidiscuss_data/
    3. Otherwise (global install), use ~/.aidiscuss/

    The directory is created if it doesn't exist.

    Returns:
        Path to data directory where database, logs, and config are stored.

    Environment Variables:
        AIDISCUSS_DATA_DIR: Override data directory location

    Data Structure:
        {data_dir}/
          ├── aidiscuss.db          # SQLite database
          ├── logs/              # Application logs
          ├── .env               # User configuration (optional)
          ├── vector_stores/     # ChromaDB vector database storage
          └── uploads/           # Uploaded documents for RAG
    """
    # User override takes precedence
    if override := os.getenv("AIDISCUSS_DATA_DIR"):
        data_dir = Path(override).resolve()
    else:
        # Detect virtual environment
        venv_path = get_virtualenv_path()

        if venv_path:
            # Store data inside virtual environment for isolation
            data_dir = venv_path / ".aidiscuss_data"
        else:
            # Global installation - use user home directory
            data_dir = Path.home() / ".aidiscuss"

    # Create directory structure if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "logs").mkdir(exist_ok=True)

    return data_dir


def get_env_type() -> str:
    """
    Get human-readable environment type.

    Returns:
        "virtual environment" or "global installation"
    """
    return "virtual environment" if get_virtualenv_path() else "global installation"


def initialize_data_directory(data_dir: Path) -> None:
    """
    Initialize data directory structure on first run.

    Creates:
        - logs/ directory
        - .initialized marker file
        - .env template (if not exists)

    Args:
        data_dir: Path to data directory
    """
    # Create logs directory
    (data_dir / "logs").mkdir(exist_ok=True)

    # Create .env template if it doesn't exist
    env_file = data_dir / ".env"
    if not env_file.exists():
        env_template = """# AIDiscuss Configuration"""
        env_file.write_text(env_template)

    # Create initialization marker
    (data_dir / ".initialized").touch()
