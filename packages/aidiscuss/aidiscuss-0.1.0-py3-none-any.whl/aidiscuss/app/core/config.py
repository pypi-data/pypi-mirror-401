"""
Application configuration with environment-aware data directories.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator

from aidiscuss.utils.paths import get_data_directory


class Settings(BaseSettings):
    """
    Application settings with multi-environment support.

    Data directory is automatically determined based on execution environment:
    - Virtual environment: {venv}/.aidiscuss_data/
    - Global installation: ~/.aidiscuss/
    - Custom: Set AIDISCUSS_DATA_DIR environment variable
    """

    # Data directory (auto-determined based on environment)
    DATA_DIR: Path = Field(default_factory=get_data_directory)

    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Database (dynamically set based on DATA_DIR)
    DATABASE_URL: str = ""

    # CORS - environment-aware, defaults to localhost only
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://127.0.0.1:8000",
            f"http://127.0.0.1:{os.getenv('PORT', '8000')}",
        ]
    )

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def set_database_url(cls, v: str, info) -> str:
        """Set database URL based on DATA_DIR if not explicitly provided."""
        if v:
            return v
        # Get DATA_DIR from the current values
        data_dir = info.data.get("DATA_DIR") or get_data_directory()
        # Use absolute path for SQLite
        db_path = data_dir / "aidiscuss.db"
        return f"sqlite:///{db_path}"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v) -> list[str]:
        """Parse CORS origins from environment variable or use defaults."""
        if isinstance(v, str):
            # Support comma-separated string from env var
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    class Config:
        # Load .env from data directory, not current working directory
        env_file = str(get_data_directory() / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


# Singleton settings instance
settings = Settings()
