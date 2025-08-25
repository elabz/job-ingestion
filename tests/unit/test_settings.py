import os
from importlib import reload
from typing import Any

from job_ingestion.utils import config as cfg


def test_settings_default_values(monkeypatch: Any) -> None:
    # Ensure env vars are not set
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("REDIS_URL", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)

    reload(cfg)
    settings = cfg.get_settings()
    assert settings.database_url.startswith("sqlite")
    assert settings.redis_url.startswith("redis://")
    assert settings.environment == "development"


def test_settings_env_override(monkeypatch: Any) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6380")
    monkeypatch.setenv("ENVIRONMENT", "test")

    # Clear cache
    cfg.get_settings.cache_clear()
    settings = cfg.get_settings()

    assert settings.database_url == os.environ["DATABASE_URL"]
    assert settings.redis_url == os.environ["REDIS_URL"]
    assert settings.environment == "test"
