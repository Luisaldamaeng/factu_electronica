from pathlib import Path

import pytest

from facturacion.modulos.fiscal.xsd import XSDError, crear_validador_de_v150

RUTA_BASE = Path(__file__).resolve().parent.parent.parent


@pytest.fixture
def validador():
    return crear_validador_de_v150(RUTA_BASE)


def test_validador_carga_xsd(validador):
    assert validador._schema is None
    schema = validador._cargar()
    assert schema is not None


def test_validar_xml_valido(validador):
    xml_ejemplo = RUTA_BASE / "docs" / "baseline" / "xml_ejemplo" / "Extructura xml_DE.xml"
    if not xml_ejemplo.exists():
        pytest.skip("Archivo XML de ejemplo no encontrado")
    xml_str = xml_ejemplo.read_text(encoding="utf-8")
    errores = validador.validar(xml_str)
    assert not errores, f"XML de ejemplo deberia ser valido contra XSD, errores: {errores}"


def test_validar_xml_invalido(validador):
    errores = validador.validar("<root/>")
    assert len(errores) > 0


def test_validar_o_error_lanza_excepcion(validador):
    with pytest.raises(XSDError):
        validador.validar_o_error("<root/>")


def test_validar_o_error_pasa_sin_error(validador):
    xml_ejemplo = RUTA_BASE / "docs" / "baseline" / "xml_ejemplo" / "Extructura xml_DE.xml"
    if not xml_ejemplo.exists():
        pytest.skip("Archivo XML de ejemplo no encontrado")
    xml_str = xml_ejemplo.read_text(encoding="utf-8")
    validador.validar_o_error(xml_str)


def test_crear_validador_con_ruta_alternativa(tmp_path):
    """Verifica que crear_validador_de_v150 busca en docs/baseline/xsd/oficial/."""
    xsd_dir = tmp_path / "docs" / "baseline" / "xsd" / "oficial"
    xsd_dir.mkdir(parents=True)
    target = tmp_path / "docs" / "baseline" / "xsd" / "oficial" / "siRecepDE_v150.xsd"
    ruta_real = RUTA_BASE / "docs" / "baseline" / "xsd" / "oficial" / "siRecepDE_v150.xsd"
    if ruta_real.exists():
        target.write_bytes(ruta_real.read_bytes())
        validador = crear_validador_de_v150(tmp_path)
        assert validador is not None
    else:
        pytest.skip("XSD oficial no encontrado")