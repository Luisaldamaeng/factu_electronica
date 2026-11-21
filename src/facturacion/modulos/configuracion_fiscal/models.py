from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facturacion.db.base import Base, utcnow
from facturacion.modulos.fiscal.codigos import TipoDocumento


class EstadoSecuencia(StrEnum):
    DISPONIBLE = "DISPONIBLE"
    AGOTADO = "AGOTADO"
    INUTILIZADO = "INUTILIZADO"
    VENCIDO = "VENCIDO"


class Emisor(Base):
    __tablename__ = "emisor"

    id: Mapped[int] = mapped_column(primary_key=True)
    ruc: Mapped[str] = mapped_column(String(8), unique=True)
    dv: Mapped[str] = mapped_column(String(1))
    razon_social: Mapped[str] = mapped_column(String(255))
    nombre_fantasia: Mapped[str | None] = mapped_column(String(255))
    direccion: Mapped[str] = mapped_column(String(255))
    telefono: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(255))
    actividad_economica: Mapped[str | None] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    establecimientos: Mapped[list[Establecimiento]] = relationship(
        back_populates="emisor", cascade="all, delete-orphan"
    )
    timbrados: Mapped[list[Timbrado]] = relationship(
        back_populates="emisor", cascade="all, delete-orphan"
    )


class Establecimiento(Base):
    __tablename__ = "establecimiento"
    __table_args__ = (
        UniqueConstraint(
            "emisor_id", "codigo", name="uq_establecimiento_emisor_codigo"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    emisor_id: Mapped[int] = mapped_column(
        ForeignKey("emisor.id", ondelete="CASCADE")
    )
    codigo: Mapped[str] = mapped_column(String(3))
    nombre: Mapped[str] = mapped_column(String(255))
    direccion: Mapped[str] = mapped_column(String(255))
    telefono: Mapped[str | None] = mapped_column(String(50))
    ciudad: Mapped[str | None] = mapped_column(String(100))
    departamento: Mapped[str | None] = mapped_column(String(100))
    distrito: Mapped[str | None] = mapped_column(String(100))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    emisor: Mapped[Emisor] = relationship(back_populates="establecimientos")
    puntos_expedicion: Mapped[list[PuntoExpedicion]] = relationship(
        back_populates="establecimiento", cascade="all, delete-orphan"
    )


class PuntoExpedicion(Base):
    __tablename__ = "punto_expedicion"
    __table_args__ = (
        UniqueConstraint(
            "establecimiento_id",
            "codigo",
            name="uq_punto_expedicion_establecimiento_codigo",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    establecimiento_id: Mapped[int] = mapped_column(
        ForeignKey("establecimiento.id", ondelete="CASCADE")
    )
    codigo: Mapped[str] = mapped_column(String(3))
    descripcion: Mapped[str] = mapped_column(String(255))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    establecimiento: Mapped[Establecimiento] = relationship(
        back_populates="puntos_expedicion"
    )


class Timbrado(Base):
    __tablename__ = "timbrado"
    __table_args__ = (
        UniqueConstraint("emisor_id", "numero", name="uq_timbrado_emisor_numero"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    emisor_id: Mapped[int] = mapped_column(
        ForeignKey("emisor.id", ondelete="CASCADE")
    )
    numero: Mapped[str] = mapped_column(String(8))
    fecha_inicio_vigencia: Mapped[date] = mapped_column(Date)
    fecha_fin_vigencia: Mapped[date] = mapped_column(Date)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )

    emisor: Mapped[Emisor] = relationship(back_populates="timbrados")
    tipos_documento: Mapped[list[TimbradoTipoDocumento]] = relationship(
        back_populates="timbrado", cascade="all, delete-orphan"
    )


class TimbradoTipoDocumento(Base):
    __tablename__ = "timbrado_tipo_documento"
    __table_args__ = (
        UniqueConstraint(
            "timbrado_id", "tipo_documento", name="uq_timbrado_tipo_documento"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    timbrado_id: Mapped[int] = mapped_column(
        ForeignKey("timbrado.id", ondelete="CASCADE")
    )
    tipo_documento: Mapped[TipoDocumento] = mapped_column(
        SAEnum(TipoDocumento, native_enum=False, length=24)
    )

    timbrado: Mapped[Timbrado] = relationship(back_populates="tipos_documento")


class Secuencia(Base):
    __tablename__ = "secuencia"
    __table_args__ = (
        UniqueConstraint(
            "timbrado_id",
            "establecimiento_id",
            "punto_expedicion_id",
            "tipo_documento",
            "serie",
            name="uq_secuencia",
        ),
        CheckConstraint("numero_desde >= 1", name="numero_desde_positivo"),
        CheckConstraint("numero_hasta >= numero_desde", name="rango_valido"),
        CheckConstraint(
            "ultimo_numero IS NULL OR "
            "(ultimo_numero >= numero_desde AND ultimo_numero <= numero_hasta)",
            name="ultimo_numero_en_rango",
        ),
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
    ultimo_numero: Mapped[int | None] = mapped_column(Integer)
    estado: Mapped[EstadoSecuencia] = mapped_column(
        SAEnum(EstadoSecuencia, native_enum=False, length=16),
        default=EstadoSecuencia.DISPONIBLE,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    timbrado: Mapped[Timbrado] = relationship()
    establecimiento: Mapped[Establecimiento] = relationship()
    punto_expedicion: Mapped[PuntoExpedicion] = relationship()
