"""
Health check and version information router
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from aidiscuss import __version__
from aidiscuss.utils.version import check_for_updates

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str


class VersionInfo(BaseModel):
    """Version information response"""
    current: str
    latest: Optional[str] = None
    update_available: bool = False
    update_command: Optional[str] = None
    release_url: Optional[str] = None


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns current version and status of the application.
    """
    return HealthResponse(status="ok", version=__version__)


@router.get("/api/version", response_model=VersionInfo)
async def get_version_info():
    """
    Get version information and check for updates.

    Checks PyPI for the latest version and returns update information.
    Frontend can use this to display update notifications to users.

    Returns:
        VersionInfo with current version and update availability
    """
    # Check for updates
    update_info = await check_for_updates()

    if update_info:
        return VersionInfo(**update_info)

    # If update check failed, return current version only
    return VersionInfo(current=__version__)
