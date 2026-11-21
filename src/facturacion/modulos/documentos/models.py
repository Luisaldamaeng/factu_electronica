from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facturacion.db.base import Base, utcnow
from facturacion.modulos.configuracion_fiscal.models import (
    Establecimiento,
    PuntoExpedicion,
    Timbrado,
)
from facturacion.modulos.documentos.estados import EstadoDocumento
from facturacion.modulos.fiscal.codigos import TipoDocumento


class Documento(Base):
    __tablename__ = "documento"
    __table_args__ = (
        UniqueConstraint("cdc", name="uq_documento_cdc"),
        UniqueConstraint(
            "timbrado_id",
            "establecimiento_id",
            "punto_expedicion_id",
            "tipo_documento",
            "serie",
            "numero",
            name="uq_documento_numero",
        ),
        CheckConstraint(
            "numero >= 1 AND numero <= 9999999", name="numero_valido"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo_documento: Mapped[TipoDocumento] = mapped_column(
        SAEnum(TipoDocumento, native_enum=False, length=24)
    )
    cdc: Mapped[str | None] = mapped_column(String(44))
    numero: Mapped[int] = mapped_column(Integer)
    serie: Mapped[str] = mapped_column(String(2))
    timbrado_id: Mapped[int] = mapped_column(
        ForeignKey("timbrado.id", ondelete="RESTRICT")
    )
    establecimiento_id: Mapped[int] = mapped_column(
        ForeignKey("establecimiento.id", ondelete="RESTRICT")
    )
    punto_expedicion_id: Mapped[int] = mapped_column(
        ForeignKey("punto_expedicion.id", ondelete="RESTRICT")
    )
    fecha_emision: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    estado: Mapped[EstadoDocumento] = mapped_column(
        SAEnum(EstadoDocumento, native_enum=False, length=28),
        default=EstadoDocumento.GENERADO,
    )
    resultado_sifen: Mapped[str | None] = mapped_column(String(2))
    codigo_sifen: Mapped[str | None] = mapped_column(String(4))
    intentos_envio: Mapped[int] = mapped_column(Integer, default=0)
    proximo_intento: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    fecha_firma: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    fecha_aprobacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    fecha_ultimo_evento: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    moneda: Mapped[str] = mapped_column(String(3), default="PYG")
    monto_total: Mapped[Decimal | None] = mapped_column(Numeric(15, 2))
    receptor_ruc: Mapped[str | None] = mapped_column(String(8))
    receptor_dv: Mapped[str | None] = mapped_column(String(1))
    receptor_nombre: Mapped[str | None] = mapped_column(String(255))
    xml_path: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    timbrado: Mapped[Timbrado] = relationship()
    establecimiento: Mapped[Establecimiento] = relationship()
    punto_expedicion: Mapped[PuntoExpedicion] = relationship()
    transiciones: Mapped[list[DocumentoTransicion]] = relationship(
        back_populates="documento", cascade="all, delete-orphan"
    )


class DocumentoTransicion(Base):
    __tablename__ = "documento_transicion"

    id: Mapped[int] = mapped_column(primary_key=True)
    documento_id: Mapped[int] = mapped_column(
        ForeignKey("documento.id", ondelete="CASCADE")
    )
    estado_anterior: Mapped[EstadoDocumento | None] = mapped_column(
        SAEnum(EstadoDocumento, native_enum=False, length=28)
    )
    estado_nuevo: Mapped[EstadoDocumento] = mapped_column(
        SAEnum(EstadoDocumento, native_enum=False, length=28)
    )
    codigo_sifen: Mapped[str | None] = mapped_column(String(4))
    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    actor: Mapped[str] = mapped_column(String(100), default="sistema")
    detalle: Mapped[str | None] = mapped_column(Text)

    documento: Mapped[Documento] = relationship(back_populates="transiciones")
