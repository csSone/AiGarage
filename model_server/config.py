"""Configuration management for the model server proxy."""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API Keys (required)
    openai_api_key: str
    anthropic_api_key: str
    google_api_key: str
    zai_api_key: str

    # Server configuration
    port: int = 8000
    host: str = "0.0.0.0"

    # Optional base URLs for providers
    openai_base_url: Optional[str] = None
    anthropic_base_url: Optional[str] = None
    zai_base_url: Optional[str] = None

    # Logging
    log_level: str = "info"

    @property
    def log_dir(self) -> Path:
        """Get the log directory path."""
        # Parent directory of model_server
        return Path(__file__).parent.parent / "log"

    @property
    def pid_file(self) -> Path:
        """Get the PID file path."""
        return Path(__file__).parent.parent / "model_server.pid"


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
