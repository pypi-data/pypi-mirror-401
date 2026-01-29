"""Version checking and update notifications."""

import asyncio
import logging
from typing import Optional

import httpx
from packaging import version

from aidiscuss import __version__

logger = logging.getLogger("aidiscuss.utils.version")


async def check_for_updates() -> Optional[dict]:
    """
    Check PyPI for newer version of AIDiscuss.

    Makes an async HTTP request to PyPI API to fetch latest version information.
    Compares with current version using semantic versioning.

    Returns:
        Dictionary with version information if successful:
        {
            "current": "0.1.0",
            "latest": "0.2.0",
            "update_available": True,
            "update_command": "pip install --upgrade aidiscuss"
        }
        None if check fails (network error, package not found, etc.)

    Example:
        >>> import asyncio
        >>> from aidiscuss.utils.version import check_for_updates
        >>> result = asyncio.run(check_for_updates())
        >>> if result and result["update_available"]:
        ...     print(f"Update available: {result['latest']}")
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("https://pypi.org/pypi/aidiscuss/json")

            if response.status_code == 200:
                data = response.json()
                latest = data["info"]["version"]
                current = __version__

                # Parse versions for comparison
                latest_version = version.parse(latest)
                current_version = version.parse(current)

                return {
                    "current": current,
                    "latest": latest,
                    "update_available": latest_version > current_version,
                    "update_command": "pip install --upgrade aidiscuss",
                    "release_url": f"https://github.com/yourusername/aidiscuss/releases/tag/v{latest}",
                }

    except httpx.HTTPError as e:
        logger.debug(f"Failed to check for updates (network error): {e}")
    except (KeyError, ValueError) as e:
        logger.debug(f"Failed to parse PyPI response: {e}")
    except Exception as e:
        logger.debug(f"Unexpected error checking for updates: {e}")

    return None


def check_for_updates_sync() -> Optional[dict]:
    """
    Synchronous wrapper for check_for_updates().

    Use this in synchronous contexts where async/await is not available.

    Returns:
        Same as check_for_updates()
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If event loop is already running, create a new one in a thread
            # This shouldn't happen in normal CLI usage but handles edge cases
            return None
        return loop.run_until_complete(check_for_updates())
    except Exception as e:
        logger.debug(f"Failed to run synchronous update check: {e}")
        return None


def print_update_notification(update_info: dict) -> None:
    """
    Print user-friendly update notification.

    Args:
        update_info: Dictionary returned from check_for_updates()

    Example:
        >>> update_info = asyncio.run(check_for_updates())
        >>> if update_info and update_info["update_available"]:
        ...     print_update_notification(update_info)
    """
    if update_info and update_info.get("update_available"):
        print("\n" + "=" * 60)
        print(f"  New version available: {update_info['latest']} (current: {update_info['current']})")
        print(f"  Update with: {update_info['update_command']}")
        print("=" * 60 + "\n")
