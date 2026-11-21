from datetime import date

import pytest
from sqlalchemy.orm import Session

from facturacion.modulos.configuracion_fiscal.models import (
    Emisor,
    Establecimiento,
    EstadoSecuencia,
    PuntoExpedicion,
    Secuencia,
    Timbrado,
    TimbradoTipoDocumento,
)
from facturacion.modulos.configuracion_fiscal.service import (
    NumeracionError,
    reservar_siguiente_numero,
)
from facturacion.modulos.fiscal.codigos import TipoDocumento

HOY = date(2026, 6, 1)


def crear_secuencia(
    session: Session,
    *,
    desde: int = 1,
    hasta: int = 3,
    fin: date = date(2026, 12, 31),
) -> Secuencia:
    emisor = Emisor(
        ruc="80000001",
        dv="1",
        razon_social="Emisor de prueba",
        direccion="Asuncion",
    )
    session.add(emisor)
    session.flush()

    establecimiento = Establecimiento(
        emisor_id=emisor.id,
        codigo="001",
        nombre="Casa central",
        direccion="Asuncion",
    )
    session.add(establecimiento)
    session.flush()

    punto = PuntoExpedicion(
        establecimiento_id=establecimiento.id,
        codigo="001",
        descripcion="Punto 1",
    )
    session.add(punto)
    session.flush()

    timbrado = Timbrado(
        emisor_id=emisor.id,
        numero="12345678",
        fecha_inicio_vigencia=date(2026, 1, 1),
        fecha_fin_vigencia=fin,
    )
    session.add(timbrado)
    session.flush()

    session.add(
        TimbradoTipoDocumento(
            timbrado_id=timbrado.id,
            tipo_documento=TipoDocumento.FACTURA,
        )
    )
    secuencia = Secuencia(
        timbrado_id=timbrado.id,
        establecimiento_id=establecimiento.id,
        punto_expedicion_id=punto.id,
        tipo_documento=TipoDocumento.FACTURA,
        serie="AA",
        numero_desde=desde,
        numero_hasta=hasta,
    )
    session.add(secuencia)
    session.flush()
    return secuencia


def test_reserva_numeros_en_orden(session: Session) -> None:
    secuencia = crear_secuencia(session)
    assert reservar_siguiente_numero(session, secuencia.id, hoy=HOY) == 1
    assert reservar_siguiente_numero(session, secuencia.id, hoy=HOY) == 2
    assert reservar_siguiente_numero(session, secuencia.id, hoy=HOY) == 3
    assert secuencia.ultimo_numero == 3
    assert secuencia.estado == EstadoSecuencia.AGOTADO


def test_no_entrega_numero_cuando_agotada(session: Session) -> None:
    secuencia = crear_secuencia(session, hasta=1)
    assert reservar_siguiente_numero(session, secuencia.id, hoy=HOY) == 1
    with pytest.raises(NumeracionError, match="agotada"):
        reservar_siguiente_numero(session, secuencia.id, hoy=HOY)


def test_rechaza_timbrado_vencido(session: Session) -> None:
    secuencia = crear_secuencia(session, fin=date(2026, 5, 31))
    with pytest.raises(NumeracionError, match="vencido"):
        reservar_siguiente_numero(session, secuencia.id, hoy=HOY)
    assert secuencia.estado == EstadoSecuencia.VENCIDO


def test_rechaza_tipo_no_autorizado(session: Session) -> None:
    secuencia = crear_secuencia(session)
    secuencia.tipo_documento = TipoDocumento.NOTA_CREDITO
    session.flush()
    with pytest.raises(NumeracionError, match="no autorizado"):
        reservar_siguiente_numero(session, secuencia.id, hoy=HOY)


def test_rechaza_punto_inactivo(session: Session) -> None:
    secuencia = crear_secuencia(session)
    secuencia.punto_expedicion.activo = False
    session.flush()
    with pytest.raises(NumeracionError, match="punto de expedicion inactivo"):
        reservar_siguiente_numero(session, secuencia.id, hoy=HOY)
