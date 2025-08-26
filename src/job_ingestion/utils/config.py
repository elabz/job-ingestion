import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./db.sqlite3"
    redis_url: str = "redis://localhost:6379"
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True
        fields = {
            "database_url": {"env": "DATABASE_URL"},
            "redis_url": {"env": "REDIS_URL"},
            "environment": {"env": "ENVIRONMENT"},
        }


@lru_cache
def get_settings() -> Settings:
    # Allow tests or callers to disable reading from .env to use pure defaults
    disable_dotenv = os.getenv("DISABLE_DOTENV", "").lower() in {"1", "true", "yes"}
    if disable_dotenv:
        # _env_file is a Pydantic v1 BaseSettings kwarg to override env file handling
        return Settings(_env_file=None)  # type: ignore[call-arg]
    return Settings()
