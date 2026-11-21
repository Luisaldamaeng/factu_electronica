from enum import StrEnum


class TipoDocumento(StrEnum):
    FACTURA = "1"
    FACTURA_EXPORTACION = "2"
    FACTURA_IMPORTACION = "3"
    AUTOFACTURA = "4"
    NOTA_CREDITO = "5"
    NOTA_DEBITO = "6"
    NOTA_REMISION = "7"


class TipoContribuyente(StrEnum):
    FISICA = "1"
    JURIDICA = "2"


class TipoEmision(StrEnum):
    NORMAL = "1"
    CONTINGENCIA = "2"
