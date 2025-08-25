from typing import Any


def test_ping(client: Any) -> None:
    resp = client.get("/api/v1/ping")
    assert resp.status_code == 200
    assert resp.json() == {"message": "pong"}
