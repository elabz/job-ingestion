import pytest
from fastapi.testclient import TestClient
from job_ingestion.api.main import app


@pytest.fixture()  # type: ignore[misc]
def client() -> TestClient:
    return TestClient(app)
