"""
Configuration management for the AI Code Reviewer application.
Handles environment variables and application settings.
"""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application Settings
    app_name: str = "AI Code Reviewer"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production"
    access_token_expire_minutes: int = 30

    # LLM Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    llm_provider: str = "anthropic"  # "anthropic" or "openai"
    llm_model: str = "claude-3-5-sonnet-20241022"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 4096

    # GitHub Integration
    github_token: Optional[str] = None
    github_webhook_secret: Optional[str] = None

    # Monitoring
    enable_metrics: bool = True
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.

    Returns:
        Settings: Application configuration
    """
    return Settings()
