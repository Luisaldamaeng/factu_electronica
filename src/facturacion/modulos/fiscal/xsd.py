from __future__ import annotations

from pathlib import Path
from xml.etree.ElementTree import ParseError

from lxml import etree


class XSDError(Exception):
    pass


class ValidadorXSD:
    def __init__(self, ruta_xsd: Path) -> None:
        self._ruta = ruta_xsd.resolve()
        self._schema: etree.XMLSchema | None = None

    def _cargar(self) -> etree.XMLSchema:
        if self._schema is None:
            with open(self._ruta, "rb") as f:
                doc = etree.parse(f)
            self._schema = etree.XMLSchema(doc)
        return self._schema

    def validar(self, xml: str) -> list[str]:
        try:
            doc = etree.fromstring(xml.encode("utf-8"))
        except ParseError as e:
            raise XSDError(f"Error de parseo del XML: {e}") from e

        schema = self._cargar()
        errores: list[str] = []
        if not schema.validate(doc):
            for err in schema.error_log:
                errores.append(f"L{err.line}: {err.message}")
        return errores


def crear_validador_de_v150(ruta_base: str | Path | None = None) -> ValidadorXSD:
    base = Path(ruta_base) if ruta_base else Path(__file__).resolve().parent.parent.parent.parent
    ruta_xsd = (
        base
        / "docs"
        / "baseline"
        / "xsd"
        / "oficial"
        / "siRecepDE_v150.xsd"
    )
    if not ruta_xsd.exists():
        alt = base / "docs" / "baseline" / "xsd" / "oficial"
        if alt.exists():
            candidates = list(alt.glob("siRecepDE*.xsd"))
            if candidates:
                ruta_xsd = candidates[0]
    return ValidadorXSD(ruta_xsd)