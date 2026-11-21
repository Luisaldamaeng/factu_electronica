from datetime import datetime
from decimal import Decimal

from facturacion.modulos.fiscal.codigos import (
    TipoContribuyente,
    TipoDocumento,
    TipoEmision,
)
from facturacion.modulos.fiscal.xml_builder import (
    ActividadEconomica,
    CamposFE,
    CondicionOperacion,
    Credito,
    DatosFacturaFE,
    EmisorXML,
    IndicadorPresencia,
    Item,
    IVAItem,
    OperacionComercial,
    ReceptorXML,
    Totales,
    ValorItem,
    construir_de_factura,
)

FECHA_FIJA = datetime(2026, 6, 1, 10, 30, 0)


def _datos_minimos() -> DatosFacturaFE:
    emisor = EmisorXML(
        ruc="80000001",
        dv="9",
        tipo_contribuyente=TipoContribuyente.JURIDICA,
        tipo_regimen=3,
        nombre="EMISOR DE PRUEBA SA",
        nombre_fantasia=None,
        direccion="CALLE 1 CASI CALLE 2",
        numero_casa=0,
        complemento_dir1=None,
        complemento_dir2=None,
        codigo_departamento=1,
        descripcion_departamento="CAPITAL",
        codigo_distrito=1,
        descripcion_distrito="ASUNCION (DISTRITO)",
        codigo_ciudad=1,
        descripcion_ciudad="ASUNCION (DISTRITO)",
        telefono="021123456",
        email="emisor@test.com",
        denominacion_sucursal=None,
        actividades_economicas=[
            ActividadEconomica(
                codigo="46510",
                descripcion="COMERCIO AL POR MAYOR DE EQUIPOS INFORMATICOS",
            )
        ],
    )

    receptor = ReceptorXML(
        naturaleza=1,
        tipo_operacion=1,
        codigo_pais="PRY",
        descripcion_pais="Paraguay",
        tipo_contribuyente=2,
        ruc="80000002",
        dv="7",
        tipo_id=None,
        descripcion_tipo_id=None,
        numero_id=None,
        nombre="RECEPTOR DE PRUEBA",
        nombre_fantasia=None,
        direccion="CALLE 2 ENTRE CALLE 3 Y 4",
        numero_casa=123,
        codigo_departamento=1,
        descripcion_departamento="CAPITAL",
        codigo_distrito=1,
        descripcion_distrito="ASUNCION (DISTRITO)",
        codigo_ciudad=1,
        descripcion_ciudad="ASUNCION (DISTRITO)",
        telefono="021654321",
        celular=None,
        email=None,
        codigo_cliente="AAA",
    )

    operacion = OperacionComercial(
        tipo_transaccion=1,
        descripcion_transaccion="Venta de mercaderia",
        tipo_impuesto=1,
        descripcion_impuesto="IVA",
        codigo_moneda="PYG",
        descripcion_moneda="Guarani",
        condicion_tipo_cambio=None,
        tipo_cambio=None,
        condicion_anticipo=None,
        descripcion_anticipo=None,
    )

    campos_fe = CamposFE(
        indicador_presencia=IndicadorPresencia(
            codigo=1,
            descripcion="Operacion presencial",
        )
    )

    condicion = CondicionOperacion(
        condicion=2,
        descripcion="Credito",
        credito=Credito(
            condicion_credito=1,
            descripcion_condicion="Plazo",
            plazo="28",
        ),
    )

    items = [
        Item(
            codigo_interno="CAC/CTAC",
            descripcion="CUENTAS ACTIVAS",
            codigo_unidad_medida=77,
            descripcion_unidad_medida="UNI",
            cantidad=Decimal("1"),
            informacion_item="21",
            valor=ValorItem(
                precio_unitario=Decimal("1100000"),
                total_bruto_item=Decimal("1100000"),
                total_operacion_item=Decimal("1100000"),
            ),
            iva=IVAItem(
                afectacion=1,
                descripcion_afectacion="Gravado IVA",
                proporcion=Decimal("100"),
                tasa=10,
                base_gravable=Decimal("1000000"),
                liquidacion=Decimal("100000"),
            ),
        ),
    ]

    totales = Totales(
        subTotal10=Decimal("2200000"),
        total_operacion=Decimal("2200000"),
        total_general=Decimal("2200000"),
        iva10=Decimal("200000"),
        total_iva=Decimal("200000"),
        base_grav10=Decimal("2000000"),
        total_base_gra_iva=Decimal("2000000"),
    )

    return DatosFacturaFE(
        cdc="0100000001900100110000502202005071",
        dv_cdc=1,
        fecha_firma=FECHA_FIJA,
        tipo_emision=TipoEmision.NORMAL,
        tipo_documento=TipoDocumento.FACTURA,
        codigo_seguridad="000000023",
        numero_timbrado="12345678",
        establecimiento="001",
        punto_expedicion="001",
        numero_documento=1000050,
        serie="AB",
        fecha_inicio_timbrado="2019-08-13",
        fecha_emision=FECHA_FIJA,
        operacion_comercial=operacion,
        emisor=emisor,
        receptor=receptor,
        campos_fe=campos_fe,
        condicion_operacion=condicion,
        items=items,
        totales=totales,
    )


def test_construir_de_factura_genera_xml():
    datos = _datos_minimos()
    xml = construir_de_factura(datos)

    assert xml.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert "<rDE " in xml
    assert "</rDE>" in xml
    assert "dVerFor" in xml
    assert "<!-- SIGNATURE_PLACEHOLDER -->" in xml
    assert "<!-- QR_PLACEHOLDER -->" in xml


def test_construir_de_factura_incluye_cdc_en_de():
    datos = _datos_minimos()
    xml = construir_de_factura(datos)
    cdc_completo = f"{datos.cdc}{datos.dv_cdc}"
    assert f'<DE Id="{cdc_completo}"' in xml


def test_construir_de_factura_tipo_emision_normal():
    datos = _datos_minimos()
    xml = construir_de_factura(datos)
    assert "<iTipEmi>1</iTipEmi>" in xml
    assert "<dDesTipEmi>Normal</dDesTipEmi>" in xml


def test_construir_de_factura_contiene_g_timb():
    datos = _datos_minimos()
    xml = construir_de_factura(datos)
    assert "<gTimb>" in xml
    assert "<iTiDE>1</iTiDE>" in xml
    assert "<dNumTim>12345678</dNumTim>" in xml
    assert "<dEst>001</dEst>" in xml
    assert "<dPunExp>001</dPunExp>" in xml


def test_construir_de_factura_contiene_emisor():
    datos = _datos_minimos()
    xml = construir_de_factura(datos)
    assert "<gEmis>" in xml
    assert "<dRucEm>80000001</dRucEm>" in xml
    assert "<dDVEmi>9</dDVEmi>" in xml
    assert "<iTipCont>2</iTipCont>" in xml


def test_construir_de_factura_contiene_receptor():
    datos = _datos_minimos()
    xml = construir_de_factura(datos)
    assert "<gDatRec>" in xml
    assert "<dRucRec>80000002</dRucRec>" in xml
    assert "<dNomRec>RECEPTOR DE PRUEBA</dNomRec>" in xml


def test_construir_de_factura_contiene_items():
    datos = _datos_minimos()
    xml = construir_de_factura(datos)
    assert "<gCamItem>" in xml
    assert "<dCodInt>CAC/CTAC</dCodInt>" in xml
    assert "<gValorItem>" in xml
    assert "<gCamIVA>" in xml


def test_construir_de_factura_contiene_totales():
    datos = _datos_minimos()
    xml = construir_de_factura(datos)
    assert "<gTotSub>" in xml
    assert "<dTotGralOpe>2200000</dTotGralOpe>" in xml


def test_construir_de_factura_emision_contingencia():
    datos = _datos_minimos()
    datos.tipo_emision = TipoEmision.CONTINGENCIA
    xml = construir_de_factura(datos)
    assert "<iTipEmi>2</iTipEmi>" in xml
    assert "<dDesTipEmi>Contingencia</dDesTipEmi>" in xml


def test_construir_de_factura_maneja_caracteres_especiales():
    datos = _datos_minimos()
    datos.emisor.nombre = "EMISOR & CIA <TEST>"
    datos.receptor.nombre = "RECEPTOR & CO"
    xml = construir_de_factura(datos)
    assert "&amp;" in xml
    assert "&lt;" in xml
    assert "<" not in xml.split("<dNomEmi>")[1].split("</dNomEmi>")[0]


def test_construir_de_factura_con_dos_items():
    datos = _datos_minimos()
    item2 = Item(
        codigo_interno="TAU/TAUR",
        descripcion="TARJETA URGENTE",
        codigo_unidad_medida=77,
        descripcion_unidad_medida="UNI",
        cantidad=Decimal("1"),
        informacion_item=None,
        valor=ValorItem(
            precio_unitario=Decimal("1100000"),
            total_bruto_item=Decimal("1100000"),
            total_operacion_item=Decimal("1100000"),
        ),
        iva=IVAItem(
            afectacion=1,
            descripcion_afectacion="Gravado IVA",
            proporcion=Decimal("100"),
            tasa=10,
            base_gravable=Decimal("1000000"),
            liquidacion=Decimal("100000"),
        ),
    )
    datos.items.append(item2)
    xml = construir_de_factura(datos)
    assert xml.count("<gCamItem>") == 2
    assert xml.count("<dCodInt>") == 2