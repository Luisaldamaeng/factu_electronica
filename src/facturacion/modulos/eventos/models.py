from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column

from facturacion.db.base import Base, utcnow
from facturacion.modulos.fiscal.codigos import TipoDocumento


class TipoEvento(StrEnum):
    CANCELACION = "CANCELACION"
    INUTILIZACION = "INUTILIZACION"
    CONFORMIDAD = "CONFORMIDAD"
    DISCONFORMIDAD = "DISCONFORMIDAD"
    DESCONOCIMIENTO = "DESCONOCIMIENTO"
    NOTIFICACION_RECEPCION = "NOTIFICACION_RECEPCION"
    AJUSTE_EVENTO = "AJUSTE_EVENTO"


class EstadoEvento(StrEnum):
    PENDIENTE = "PENDIENTE"
    ENVIADO = "ENVIADO"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"


class Evento(Base):
    __tablename__ = "evento"

    id: Mapped[int] = mapped_column(primary_key=True)
    documento_id: Mapped[int | None] = mapped_column(
        ForeignKey("documento.id", ondelete="SET NULL")
    )
    tipo: Mapped[TipoEvento] = mapped_column(
        SAEnum(TipoEvento, native_enum=False, length=28)
    )
    estado: Mapped[EstadoEvento] = mapped_column(
        SAEnum(EstadoEvento, native_enum=False, length=16),
        default=EstadoEvento.PENDIENTE,
    )
    codigo_sifen: Mapped[str | None] = mapped_column(String(4))
    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    payload: Mapped[dict[str, object] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )


class RangoInutilizado(Base):
    __tablename__ = "rango_inutilizado"
    __table_args__ = (
        UniqueConstraint(
            "timbrado_id",
            "establecimiento_id",
            "punto_expedicion_id",
            "tipo_documento",
            "serie",
            "numero_desde",
            "numero_hasta",
            name="uq_rango_inutilizado",
        ),
        CheckConstraint("numero_desde >= 1", name="numero_desde_positivo"),
        CheckConstraint("numero_hasta >= numero_desde", name="rango_valido"),
        CheckConstraint("numero_hasta <= 9999999", name="numero_hasta_maximo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    timbrado_id: Mapped[int] = mapped_column(
        ForeignKey("timbrado.id", ondelete="RESTRICT")
    )
    establecimiento_id: Mapped[int] = mapped_column(
        ForeignKey("establecimiento.id", ondelete="RESTRICT")
    )
    punto_expedicion_id: Mapped[int] = mapped_column(
        ForeignKey("punto_expedicion.id", ondelete="RESTRICT")
    )
    tipo_documento: Mapped[TipoDocumento] = mapped_column(
        SAEnum(TipoDocumento, native_enum=False, length=24)
    )
    serie: Mapped[str] = mapped_column(String(2))
    numero_desde: Mapped[int] = mapped_column(Integer)
    numero_hasta: Mapped[int] = mapped_column(Integer)
    estado: Mapped[EstadoEvento] = mapped_column(
        SAEnum(EstadoEvento, native_enum=False, length=16),
        default=EstadoEvento.PENDIENTE,
    )
    fecha_envio: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    codigo_sifen: Mapped[str | None] = mapped_column(String(4))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
