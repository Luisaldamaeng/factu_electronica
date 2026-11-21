import logging

from facturacion.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    nivel = logging.DEBUG if settings.app_env == "development" else logging.INFO
    logging.basicConfig(
        level=nivel,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
