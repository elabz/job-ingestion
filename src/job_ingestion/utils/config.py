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
    return Settings()
