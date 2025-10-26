"""
Configuration settings for Juicebox AI Backend
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional
import os
import sys


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

    @field_validator('EXA_API_KEY')
    @classmethod
    def validate_exa_api_key(cls, v: str) -> str:
        if not v or v.strip() == "":
            print("\n" + "="*70)
            print("ERROR: EXA_API_KEY is required but not set!")
            print("="*70)
            print("\nPlease set your Exa API key in one of these ways:\n")
            print("1. Create a .env file in the backend directory:")
            print("   EXA_API_KEY=your_key_here\n")
            print("2. Set an environment variable:")
            print("   export EXA_API_KEY=your_key_here\n")
            print("3. Get your API key at: https://dashboard.exa.ai/api-keys\n")
            print("="*70 + "\n")
            sys.exit(1)
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance with helpful error handling
try:
    settings = Settings()
except Exception as e:
    print("\n" + "="*70)
    print("ERROR: Failed to load configuration!")
    print("="*70)
    print(f"\n{str(e)}\n")
    print("Please check your .env file and environment variables.")
    print("="*70 + "\n")
    sys.exit(1)
