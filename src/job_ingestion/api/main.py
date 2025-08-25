from fastapi import FastAPI

app = FastAPI(title="Job Ingestion Service API", version="0.1.0")

__all__ = ["app"]


@app.get("/health")  # type: ignore[misc]
def health() -> dict[str, str]:
    return {"status": "ok"}
