# Instrucciones para agentes

## Proyecto

Facturacion electronica SIFEN para un solo contribuyente. Backend Python 3.12,
FastAPI, Jinja2/HTMX, PostgreSQL y worker separado.

## Comandos

```bash
uv sync --all-groups
uv run ruff check .
uv run pytest
uv run mypy src
```

## Reglas

- Nunca escribir acentos en texto en espanol.
- Usar coma decimal y punto de miles en la interfaz y la documentacion.
- No incluir `.pfx`, PIN, CSC ni secretos en el repositorio.
- Los secretos van en `secrets/` y los datos de ejecucion en `var/`.
- La autoridad normativa es `docs/baseline/`; ante conflicto, prevalece el PDF.
- No implementar XAdES: el SIFEN exige XMLDSig enveloped.
- No instalar `pysifen` y `sifen` en el mismo entorno: ambas exponen el paquete
  `pysifen`.
- Mantener la logica fiscal fuera de `web/`.
