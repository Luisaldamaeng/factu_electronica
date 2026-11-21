#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_URL:?Falta DATABASE_URL}"
ARCHIVO="${1:?Uso: restaurar.sh <archivo.dump>}"

pg_restore --clean --if-exists --no-owner -d "${DATABASE_URL}" "${ARCHIVO}"
echo "Respaldo restaurado desde ${ARCHIVO}"
