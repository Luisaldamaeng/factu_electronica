import logging
import time

from facturacion.logging import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    logger.info("worker iniciado; cola pendiente de implementar")
    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
