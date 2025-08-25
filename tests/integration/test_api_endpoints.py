from typing import Any


def test_health_endpoint_integration(client: Any) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_docs_available(client: Any) -> None:
    resp = client.get("/docs")
    assert resp.status_code == 200
