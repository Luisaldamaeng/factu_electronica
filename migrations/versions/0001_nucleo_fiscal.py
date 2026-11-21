"""nucleo fiscal

Revision ID: 0001_nucleo_fiscal
Revises:
Create Date: 2026-11-20

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_nucleo_fiscal"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "emisor",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ruc", sa.String(length=8), nullable=False),
        sa.Column("dv", sa.String(length=1), nullable=False),
        sa.Column("razon_social", sa.String(length=255), nullable=False),
        sa.Column("nombre_fantasia", sa.String(length=255), nullable=True),
        sa.Column("direccion", sa.String(length=255), nullable=False),
        sa.Column("telefono", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("actividad_economica", sa.String(length=10), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_emisor"),
        sa.UniqueConstraint("ruc", name="uq_emisor_ruc"),
    )

    op.create_table(
        "establecimiento",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("emisor_id", sa.Integer(), nullable=False),
        sa.Column("codigo", sa.String(length=3), nullable=False),
        sa.Column("nombre", sa.String(length=255), nullable=False),
        sa.Column("direccion", sa.String(length=255), nullable=False),
        sa.Column("telefono", sa.String(length=50), nullable=True),
        sa.Column("ciudad", sa.String(length=100), nullable=True),
        sa.Column("departamento", sa.String(length=100), nullable=True),
        sa.Column("distrito", sa.String(length=100), nullable=True),
        sa.Column(
            "activo",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["emisor_id"],
            ["emisor.id"],
            name="fk_establecimiento_emisor_id_emisor",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_establecimiento"),
        sa.UniqueConstraint(
            "emisor_id",
            "codigo",
            name="uq_establecimiento_emisor_codigo",
        ),
    )

    op.create_table(
        "punto_expedicion",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("establecimiento_id", sa.Integer(), nullable=False),
        sa.Column("codigo", sa.String(length=3), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=False),
        sa.Column(
            "activo",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["establecimiento_id"],
            ["establecimiento.id"],
            name="fk_punto_expedicion_establecimiento_id_establecimiento",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_punto_expedicion"),
        sa.UniqueConstraint(
            "establecimiento_id",
            "codigo",
            name="uq_punto_expedicion_establecimiento_codigo",
        ),
    )

    op.create_table(
        "timbrado",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("emisor_id", sa.Integer(), nullable=False),
        sa.Column("numero", sa.String(length=8), nullable=False),
        sa.Column("fecha_inicio_vigencia", sa.Date(), nullable=False),
        sa.Column("fecha_fin_vigencia", sa.Date(), nullable=False),
        sa.Column(
            "activo",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["emisor_id"],
            ["emisor.id"],
            name="fk_timbrado_emisor_id_emisor",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_timbrado"),
        sa.UniqueConstraint(
            "emisor_id", "numero", name="uq_timbrado_emisor_numero"
        ),
    )

    op.create_table(
        "timbrado_tipo_documento",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timbrado_id", sa.Integer(), nullable=False),
        sa.Column("tipo_documento", sa.String(length=24), nullable=False),
        sa.ForeignKeyConstraint(
            ["timbrado_id"],
            ["timbrado.id"],
            name="fk_timbrado_tipo_documento_timbrado_id_timbrado",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_timbrado_tipo_documento"),
        sa.UniqueConstraint(
            "timbrado_id",
            "tipo_documento",
            name="uq_timbrado_tipo_documento",
        ),
    )

    op.create_table(
        "secuencia",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timbrado_id", sa.Integer(), nullable=False),
        sa.Column("establecimiento_id", sa.Integer(), nullable=False),
        sa.Column("punto_expedicion_id", sa.Integer(), nullable=False),
        sa.Column("tipo_documento", sa.String(length=24), nullable=False),
        sa.Column("serie", sa.String(length=2), nullable=False),
        sa.Column("numero_desde", sa.Integer(), nullable=False),
        sa.Column("numero_hasta", sa.Integer(), nullable=False),
        sa.Column("ultimo_numero", sa.Integer(), nullable=True),
        sa.Column(
            "estado",
            sa.String(length=16),
            server_default="DISPONIBLE",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "numero_desde >= 1", name="ck_secuencia_numero_desde_positivo"
        ),
        sa.CheckConstraint(
            "numero_hasta >= numero_desde", name="ck_secuencia_rango_valido"
        ),
        sa.CheckConstraint(
            "ultimo_numero IS NULL OR "
            "(ultimo_numero >= numero_desde AND ultimo_numero <= numero_hasta)",
            name="ck_secuencia_ultimo_numero_en_rango",
        ),
        sa.CheckConstraint(
            "numero_hasta <= 9999999",
            name="ck_secuencia_numero_hasta_maximo",
        ),
        sa.ForeignKeyConstraint(
            ["establecimiento_id"],
            ["establecimiento.id"],
            name="fk_secuencia_establecimiento_id_establecimiento",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["punto_expedicion_id"],
            ["punto_expedicion.id"],
            name="fk_secuencia_punto_expedicion_id_punto_expedicion",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["timbrado_id"],
            ["timbrado.id"],
            name="fk_secuencia_timbrado_id_timbrado",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_secuencia"),
        sa.UniqueConstraint(
            "timbrado_id",
            "establecimiento_id",
            "punto_expedicion_id",
            "tipo_documento",
            "serie",
            name="uq_secuencia",
        ),
    )

    op.create_table(
        "documento",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tipo_documento", sa.String(length=24), nullable=False),
        sa.Column("cdc", sa.String(length=44), nullable=True),
        sa.Column("numero", sa.Integer(), nullable=False),
        sa.Column("serie", sa.String(length=2), nullable=False),
        sa.Column("timbrado_id", sa.Integer(), nullable=False),
        sa.Column("establecimiento_id", sa.Integer(), nullable=False),
        sa.Column("punto_expedicion_id", sa.Integer(), nullable=False),
        sa.Column(
            "fecha_emision",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "estado",
            sa.String(length=28),
            server_default="GENERADO",
            nullable=False,
        ),
        sa.Column("resultado_sifen", sa.String(length=2), nullable=True),
        sa.Column("codigo_sifen", sa.String(length=4), nullable=True),
        sa.Column(
            "intentos_envio",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "proximo_intento", sa.DateTime(timezone=True), nullable=True
        ),
        sa.Column("fecha_firma", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "fecha_aprobacion", sa.DateTime(timezone=True), nullable=True
        ),
        sa.Column(
            "fecha_ultimo_evento", sa.DateTime(timezone=True), nullable=True
        ),
        sa.Column(
            "moneda",
            sa.String(length=3),
            server_default="PYG",
            nullable=False,
        ),
        sa.Column("monto_total", sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column("receptor_ruc", sa.String(length=8), nullable=True),
        sa.Column("receptor_dv", sa.String(length=1), nullable=True),
        sa.Column("receptor_nombre", sa.String(length=255), nullable=True),
        sa.Column("xml_path", sa.String(length=512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "numero >= 1 AND numero <= 9999999",
            name="ck_documento_numero_valido",
        ),
        sa.ForeignKeyConstraint(
            ["establecimiento_id"],
            ["establecimiento.id"],
            name="fk_documento_establecimiento_id_establecimiento",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["punto_expedicion_id"],
            ["punto_expedicion.id"],
            name="fk_documento_punto_expedicion_id_punto_expedicion",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["timbrado_id"],
            ["timbrado.id"],
            name="fk_documento_timbrado_id_timbrado",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_documento"),
        sa.UniqueConstraint("cdc", name="uq_documento_cdc"),
        sa.UniqueConstraint(
            "timbrado_id",
            "establecimiento_id",
            "punto_expedicion_id",
            "tipo_documento",
            "serie",
            "numero",
            name="uq_documento_numero",
        ),
    )
    op.create_index("ix_documento_estado", "documento", ["estado"])
    op.create_index(
        "ix_documento_proximo_intento", "documento", ["proximo_intento"]
    )

    op.create_table(
        "documento_transicion",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("documento_id", sa.Integer(), nullable=False),
        sa.Column("estado_anterior", sa.String(length=28), nullable=True),
        sa.Column("estado_nuevo", sa.String(length=28), nullable=False),
        sa.Column("codigo_sifen", sa.String(length=4), nullable=True),
        sa.Column(
            "fecha",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "actor",
            sa.String(length=100),
            server_default="sistema",
            nullable=False,
        ),
        sa.Column("detalle", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["documento_id"],
            ["documento.id"],
            name="fk_documento_transicion_documento_id_documento",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_documento_transicion"),
    )
    op.create_index(
        "ix_documento_transicion_documento_id",
        "documento_transicion",
        ["documento_id"],
    )

    op.create_table(
        "evento",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("documento_id", sa.Integer(), nullable=True),
        sa.Column("tipo", sa.String(length=28), nullable=False),
        sa.Column(
            "estado",
            sa.String(length=16),
            server_default="PENDIENTE",
            nullable=False,
        ),
        sa.Column("codigo_sifen", sa.String(length=4), nullable=True),
        sa.Column(
            "fecha",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["documento_id"],
            ["documento.id"],
            name="fk_evento_documento_id_documento",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_evento"),
    )
    op.create_index("ix_evento_documento_id", "evento", ["documento_id"])

    op.create_table(
        "rango_inutilizado",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timbrado_id", sa.Integer(), nullable=False),
        sa.Column("establecimiento_id", sa.Integer(), nullable=False),
        sa.Column("punto_expedicion_id", sa.Integer(), nullable=False),
        sa.Column("tipo_documento", sa.String(length=24), nullable=False),
        sa.Column("serie", sa.String(length=2), nullable=False),
        sa.Column("numero_desde", sa.Integer(), nullable=False),
        sa.Column("numero_hasta", sa.Integer(), nullable=False),
        sa.Column(
            "estado",
            sa.String(length=16),
            server_default="PENDIENTE",
            nullable=False,
        ),
        sa.Column("fecha_envio", sa.DateTime(timezone=True), nullable=True),
        sa.Column("codigo_sifen", sa.String(length=4), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "numero_desde >= 1",
            name="ck_rango_inutilizado_numero_desde_positivo",
        ),
        sa.CheckConstraint(
            "numero_hasta >= numero_desde",
            name="ck_rango_inutilizado_rango_valido",
        ),
        sa.CheckConstraint(
            "numero_hasta <= 9999999",
            name="ck_rango_inutilizado_numero_hasta_maximo",
        ),
        sa.ForeignKeyConstraint(
            ["establecimiento_id"],
            ["establecimiento.id"],
            name="fk_rango_inutilizado_establecimiento_id_establecimiento",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["punto_expedicion_id"],
            ["punto_expedicion.id"],
            name="fk_rango_inutilizado_punto_expedicion_id_punto_expedicion",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["timbrado_id"],
            ["timbrado.id"],
            name="fk_rango_inutilizado_timbrado_id_timbrado",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_rango_inutilizado"),
        sa.UniqueConstraint(
            "timbrado_id",
            "establecimiento_id",
            "punto_expedicion_id",
            "tipo_documento",
            "serie",
            "numero_desde",
            "numero_hasta",
            name="uq_rango_inutilizado",
        ),
    )


def downgrade() -> None:
    op.drop_table("rango_inutilizado")
    op.drop_table("evento")
    op.drop_table("documento_transicion")
    op.drop_table("documento")
    op.drop_table("secuencia")
    op.drop_table("timbrado_tipo_documento")
    op.drop_table("timbrado")
    op.drop_table("punto_expedicion")
    op.drop_table("establecimiento")
    op.drop_table("emisor")
