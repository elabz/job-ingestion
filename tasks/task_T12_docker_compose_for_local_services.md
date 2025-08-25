# T12: Docker compose for local DB/Redis (dev only)

- [ ] Task complete

## Summary
Add `docker-compose.yml` with Postgres and Redis for local development.

## Implementation details
- `docker-compose.yml` services:
  - `db`: postgres:15, ports `5432:5432`, env from `.env`, healthcheck.
  - `redis`: redis:7, ports `6379:6379`.
- Optional `scripts/wait_for_services.sh` to wait for health.
- Volumes for persistence optional (dev only).

## Checklist
- [ ] Compose file present and valid.
- [ ] Environment variables documented in `.env.example`.
- [ ] Optional wait script added and executable.

## Acceptance criteria
- [ ] `docker compose up -d db redis` succeeds; services healthy.

## Verification
```bash
docker compose up -d db redis
docker compose ps
```

## Docs
- `README.md` dev setup with compose instructions.

## Risks/Notes
- Keep containers dev-only; do not commit secrets.

## Dependencies
- T03 partially (env vars).

## Effort
- S: ~1h.
