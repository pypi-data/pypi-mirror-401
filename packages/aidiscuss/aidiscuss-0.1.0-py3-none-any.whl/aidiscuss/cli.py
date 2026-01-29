"""CLI entry point for AIDiscuss package."""

import asyncio
import sys
from pathlib import Path

from aidiscuss import __version__
from aidiscuss.utils.paths import (
    get_data_directory,
    get_env_type,
    initialize_data_directory,
)
from aidiscuss.utils.logging import setup_logging, get_logger
from aidiscuss.utils.version import check_for_updates, print_update_notification


def main() -> None:
    """
    Main CLI entry point for AIDiscuss.

    Workflow:
    1. Detect environment (virtual env vs global)
    2. Setup data directory
    3. Configure logging
    4. Check for updates (non-blocking)
    5. Initialize on first run
    6. Start the FastAPI server

    Usage:
        $ aidiscuss                    # Start server
        $ AIDISCUSS_DATA_DIR=/custom/path aidiscuss  # Custom data dir
    """
    # Detect environment and setup data directory
    data_dir = get_data_directory()
    env_type = get_env_type()

    # Setup logging before anything else
    logger = setup_logging(data_dir / "logs")

    # Welcome message
    logger.info("=" * 60)
    logger.info(f"AIDiscuss v{__version__}")
    logger.info(f"Running in: {env_type}")
    logger.info(f"Data directory: {data_dir}")
    logger.info("=" * 60)

    # First-run initialization
    if not (data_dir / ".initialized").exists():
        logger.info("First run detected - initializing AIDiscuss...")
        initialize_data_directory(data_dir)
        logger.info("Initialization complete!")
        logger.info(f"Configuration file: {data_dir / '.env'}")
        logger.info("You can edit this file to customize settings.")

    # Check for updates (async, non-blocking)
    try:
        update_info = asyncio.run(check_for_updates())
        if update_info and update_info.get("update_available"):
            print_update_notification(update_info)
    except Exception as e:
        logger.debug(f"Update check skipped: {e}")

    # Import and run the server
    # Import here to ensure logging is configured first
    try:
        from aidiscuss.main import run_server

        logger.info("Starting AIDiscuss server...")
        asyncio.run(run_server())

    except KeyboardInterrupt:
        logger.info("\nShutting down AIDiscuss...")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error starting AIDiscuss: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
