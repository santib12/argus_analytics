#!/usr/bin/env bash
# =============================================================================
# Argus Phase 2 — scripts/init_db.sh
# =============================================================================
# Creates the local argus database (if missing) and applies:
#   sql/schema.sql
#   sql/indexes.sql
#   sql/views.sql
#
# Usage:
#   ./scripts/init_db.sh
#
# Optional env overrides:
#   DB_NAME=argus
#   DB_USER=argus
#   DB_HOST=localhost
#   DB_PORT=5432
#   PGPASSWORD=password
#
# Superuser used only to CREATE DATABASE when needed:
#   DB_ADMIN_USER=postgres
# =============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DB_NAME="${DB_NAME:-argus}"
DB_USER="${DB_USER:-argus}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_ADMIN_USER="${DB_ADMIN_USER:-postgres}"
export PGPASSWORD="${PGPASSWORD:-password}"

echo "[argus] repo root: $ROOT_DIR"
echo "[argus] target db: ${DB_USER}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

echo "[argus] checking PostgreSQL connectivity..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_ADMIN_USER" -d postgres -c "SELECT 1;" >/dev/null

DB_EXISTS="$(
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_ADMIN_USER" -d postgres -tAc \
    "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'"
)"

if [[ "$DB_EXISTS" != "1" ]]; then
  echo "[argus] creating database ${DB_NAME}..."
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_ADMIN_USER" -d postgres \
    -c "CREATE DATABASE ${DB_NAME};"
else
  echo "[argus] database ${DB_NAME} already exists"
fi

echo "[argus] applying sql/schema.sql..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f sql/schema.sql

echo "[argus] applying sql/indexes.sql..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f sql/indexes.sql

echo "[argus] applying sql/views.sql..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f sql/views.sql

echo "[argus] listing tables..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\dt'

echo "[argus] init_db.sh complete"
