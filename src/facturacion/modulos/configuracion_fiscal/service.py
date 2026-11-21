from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from facturacion.modulos.configuracion_fiscal.models import (
    EstadoSecuencia,
    Secuencia,
    TimbradoTipoDocumento,
)


class NumeracionError(Exception):
    pass


def reservar_siguiente_numero(
    session: Session,
    secuencia_id: int,
    hoy: date | None = None,
) -> int:
    secuencia = session.get(Secuencia, secuencia_id, with_for_update=True)
    if secuencia is None:
        raise NumeracionError("secuencia inexistente")

    fecha = hoy or date.today()
    timbrado = secuencia.timbrado
    vencido = (
        fecha < timbrado.fecha_inicio_vigencia
        or fecha > timbrado.fecha_fin_vigencia
    )
    if not timbrado.activo or vencido:
        secuencia.estado = EstadoSecuencia.VENCIDO
        session.flush()
        raise NumeracionError("timbrado vencido o inactivo")

    if secuencia.estado == EstadoSecuencia.INUTILIZADO:
        raise NumeracionError("secuencia inutilizada")
    if secuencia.estado == EstadoSecuencia.VENCIDO:
        raise NumeracionError("secuencia vencida")
    if secuencia.estado == EstadoSecuencia.AGOTADO:
        raise NumeracionError("secuencia agotada")

    autorizado = session.scalar(
        select(TimbradoTipoDocumento).where(
            TimbradoTipoDocumento.timbrado_id == secuencia.timbrado_id,
            TimbradoTipoDocumento.tipo_documento == secuencia.tipo_documento,
        )
    )
    if autorizado is None:
        raise NumeracionError("tipo de documento no autorizado")

    if not secuencia.establecimiento.activo:
        raise NumeracionError("establecimiento inactivo")
    if not secuencia.punto_expedicion.activo:
        raise NumeracionError("punto de expedicion inactivo")
    if (
        secuencia.punto_expedicion.establecimiento_id
        != secuencia.establecimiento_id
    ):
        raise NumeracionError("punto de expedicion fuera del establecimiento")

    siguiente = (secuencia.ultimo_numero or (secuencia.numero_desde - 1)) + 1
    if siguiente > secuencia.numero_hasta:
        secuencia.estado = EstadoSecuencia.AGOTADO
        session.flush()
        raise NumeracionError("secuencia agotada")

    secuencia.ultimo_numero = siguiente
    if siguiente == secuencia.numero_hasta:
        secuencia.estado = EstadoSecuencia.AGOTADO
    session.flush()
    return siguiente
