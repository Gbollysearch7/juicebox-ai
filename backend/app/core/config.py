"""
Configuration settings for Juicebox AI Backend
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Juicebox AI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Powered Recruiting Platform - Find and rank top talent"

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS Settings
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Exa API Settings
    EXA_API_KEY: str
    EXA_TIMEOUT: int = 3600  # 1 hour
    EXA_MAX_RETRIES: int = 3
    EXA_CHECK_INTERVAL: int = 10

    # Search Settings
    DEFAULT_CANDIDATE_COUNT: int = 10
    MAX_CANDIDATE_COUNT: int = 100

    # Cache Settings (optional)
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
