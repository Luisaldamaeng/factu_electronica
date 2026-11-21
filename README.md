# Facturacion Electronica SIFEN

Aplicacion de facturacion electronica para un solo contribuyente, integrada a los
web services del SIFEN de la DNIT.

## Stack

- Python 3.12 con `uv`
- FastAPI, Jinja2 y HTMX
- PostgreSQL con SQLAlchemy y Alembic
- `sifen` 0.2.0 como adaptador hacia la DNIT
- Worker en proceso separado

## Requisitos

- Python 3.12
- Docker y Docker Compose
- Certificado cualificado tipo F1 (`.pfx`) y PIN
- CSC del SIFEN

## Puesta en marcha

```bash
cp .env.example .env
uv sync --all-groups
uv run alembic upgrade head
uv run uvicorn facturacion.main:app --reload
```

Con Docker:

```bash
docker compose up --build
```

## Comandos

```bash
uv run ruff check .
uv run pytest
uv run mypy src
```

## Estructura

- `src/facturacion/modulos/`: dominio fiscal, documentos, eventos, sifen y representacion.
- `src/facturacion/worker/`: cola, reintentos y contingencias.
- `src/facturacion/web/`: plantillas y estaticos.
- `tests/`: pruebas unitarias, de integracion y end-to-end.
- `docs/`: baseline normativo y decisiones del proyecto.
- `migrations/`: migraciones de Alembic.
- `secrets/` y `var/`: datos locales fuera de git.

## Estado

Esqueleto inicial. La logica fiscal y la transmision al SIFEN se implementan por
modulos segun el plan del proyecto.
