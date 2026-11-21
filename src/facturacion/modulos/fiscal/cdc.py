from dataclasses import dataclass
from datetime import date

from facturacion.modulos.fiscal.codigos import (
    TipoContribuyente,
    TipoDocumento,
    TipoEmision,
)

LONGITUD_CDC = 44


class CdcError(ValueError):
    pass


def calcular_dv_modulo_11(numero: str) -> int:
    if not numero.isdigit():
        raise CdcError("el numero debe contener solo digitos")
    total = 0
    peso = 2
    for caracter in reversed(numero):
        total += int(caracter) * peso
        peso += 1
        if peso > 11:
            peso = 2
    resto = total % 11
    return 11 - resto if resto > 1 else 0


def _campo_numerico(valor: str, largo: int, nombre: str) -> str:
    if not valor.isdigit():
        raise CdcError(f"{nombre} debe contener solo digitos")
    if len(valor) > largo:
        raise CdcError(f"{nombre} no puede superar {largo} digitos")
    return valor.zfill(largo)


@dataclass(frozen=True, slots=True)
class DatosCdc:
    tipo_documento: TipoDocumento
    ruc: str
    dv_ruc: str
    establecimiento: str
    punto_expedicion: str
    numero_documento: int
    tipo_contribuyente: TipoContribuyente
    fecha_emision: date
    tipo_emision: TipoEmision
    codigo_seguridad: str


def generar_cdc(datos: DatosCdc) -> str:
    if datos.numero_documento < 1 or datos.numero_documento > 9_999_999:
        raise CdcError("el numero de documento debe estar entre 1 y 9999999")

    base = "".join(
        (
            datos.tipo_documento.value.zfill(2),
            _campo_numerico(datos.ruc, 8, "RUC"),
            _campo_numerico(datos.dv_ruc, 1, "DV del RUC"),
            _campo_numerico(datos.establecimiento, 3, "establecimiento"),
            _campo_numerico(
                datos.punto_expedicion, 3, "punto de expedicion"
            ),
            str(datos.numero_documento).zfill(7),
            datos.tipo_contribuyente.value,
            datos.fecha_emision.strftime("%Y%m%d"),
            datos.tipo_emision.value,
            _campo_numerico(
                datos.codigo_seguridad, 9, "codigo de seguridad"
            ),
        )
    )
    if len(base) != LONGITUD_CDC - 1:
        raise CdcError("la base del CDC debe tener 43 digitos")
    return f"{base}{calcular_dv_modulo_11(base)}"


def validar_cdc(cdc: str) -> bool:
    return (
        len(cdc) == LONGITUD_CDC
        and cdc.isdigit()
        and calcular_dv_modulo_11(cdc[:-1]) == int(cdc[-1])
    )


def formatear_cdc(cdc: str) -> str:
    if not validar_cdc(cdc):
        raise CdcError("el CDC debe tener 44 digitos y un DV valido")
    return " ".join(cdc[i : i + 4] for i in range(0, LONGITUD_CDC, 4))
