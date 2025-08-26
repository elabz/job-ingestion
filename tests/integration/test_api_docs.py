from typing import Any


def test_openapi_includes_jobposting(client: Any) -> None:
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    data = resp.json()
    assert "components" in data and "schemas" in data["components"]
    assert "JobPosting" in data["components"]["schemas"]


def test_jobposting_example_endpoint(client: Any) -> None:
    resp = client.get("/api/v1/jobposting/example")
    assert resp.status_code == 200
    body = resp.json()
    # Minimal shape check
    for key in ("title", "company", "location"):
        assert key in body
