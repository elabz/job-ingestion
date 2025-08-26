#!/usr/bin/env bash
set -euo pipefail

# Simple wait script for local dev to ensure Postgres and Redis are ready
# Checks readiness inside running Docker containers (db, redis)
# Usage: ./scripts/wait_for_services.sh

echo "Waiting for Postgres container (service: db)..."
for i in {1..30}; do
  if docker compose exec -T db pg_isready >/dev/null 2>&1; then
    echo "Postgres is ready."
    break
  fi
  if [[ $i -eq 30 ]]; then
    echo "Timed out waiting for Postgres" >&2
    exit 1
  fi
  sleep 2
done

echo "Waiting for Redis container (service: redis)..."
for i in {1..30}; do
  if docker compose exec -T redis redis-cli ping | grep -q PONG; then
    echo "Redis is ready."
    break
  fi
  if [[ $i -eq 30 ]]; then
    echo "Timed out waiting for Redis" >&2
    exit 1
  fi
  sleep 2
done

echo "All services are healthy."
