# T23: Dockerize Application Container with Live Reload

## Summary
Dockerize the FastAPI application for local development. Add an `app` service to `docker-compose.yml` that runs Uvicorn with `--reload` and bind-mounts the source tree for active development.

## Affected Paths
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `.env.example`
- `requirements.txt`
- `docs/QUICKSTART.md`, `README.md` (docs updates)

## Requirements
1) Dockerfile based on `python:3.10-slim`:
   - Install dependencies from `requirements.txt`.
   - Set `PYTHONPATH=/app/src`.
   - Default command: `uvicorn src.job_ingestion.api.main:app --host 0.0.0.0 --port 8000 --reload`.
2) Compose `app` service:
   - Build from the Dockerfile.
   - Expose `${APP_HOST_PORT:-8000}:8000`.
   - Bind mount `./src:/app/src` for live reload.
   - Environment:
     - `DATABASE_URL` defaults to `postgresql://postgres:password@db:5432/job_ingestion`.
     - `REDIS_URL` defaults to `redis://redis:6379`.
     - `ENVIRONMENT=development`.
     - `PYTHONPATH=/app/src`.
   - `depends_on`: `db`, `redis`.
   - Healthcheck: HTTP GET `/health` with curl.
3) `.env.example`: add `APP_HOST_PORT` with default `8000`.
4) `.dockerignore`: ignore VCS, caches, venvs, editor files, dist/build, `.env`.
5) Docs updates:
   - Add a section to `README.md` and `docs/QUICKSTART.md` describing how to run the app via compose with Postgres + Redis.
   - Include curl verification commands.

## Implementation Steps
1) Add `requirements.txt` for runtime dependencies.
2) Create `Dockerfile` per spec.
3) Update `docker-compose.yml` with `app` service and healthcheck.
4) Add `.dockerignore` and `APP_HOST_PORT` to `.env.example`.
5) Update docs with start/stop, verification, and troubleshooting.
6) Run `pre-commit run --all-files` and `make quality-check`.

## Verification
- Build configuration: `docker compose config -q` outputs nothing (success).
- Start services: `docker compose up -d db redis app`.
- Check status: `docker compose ps` shows app, db, and redis running (app may be starting until reload watchers are ready).
- Verify health:
  ```sh
  curl -sSf http://127.0.0.1:${APP_HOST_PORT:-8000}/health
  # Expect: {"status":"ok"}
  ```
- Live reload: Make a small change in `src/job_ingestion/api/main.py` (e.g., title) and see it reflected without restarting the container.

## Acceptance Criteria
- Dockerfile and compose `app` service exist and work on macOS.
- Source changes trigger automatic reload in the running container.
- Docs include clear instructions and curl verification.
- Pre-commit and `make quality-check` pass.
