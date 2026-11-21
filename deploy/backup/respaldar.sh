#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_URL:?Falta DATABASE_URL}"
DESTINO="${1:-./var/respaldos}"
FECHA="$(date +%Y%m%d-%H%M%S)"
ARCHIVO="${DESTINO}/facturacion-${FECHA}.dump"

mkdir -p "${DESTINO}"
pg_dump "${DATABASE_URL}" -Fc -f "${ARCHIVO}"
echo "Respaldo creado en ${ARCHIVO}"
