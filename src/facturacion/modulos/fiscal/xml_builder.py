from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from facturacion.modulos.fiscal.codigos import (
    TipoContribuyente,
    TipoDocumento,
    TipoEmision,
)


@dataclass
class ActividadEconomica:
    codigo: str
    descripcion: str


@dataclass
class EmisorXML:
    ruc: str
    dv: str
    tipo_contribuyente: TipoContribuyente
    tipo_regimen: int
    nombre: str
    nombre_fantasia: str | None
    direccion: str
    numero_casa: int
    complemento_dir1: str | None
    complemento_dir2: str | None
    codigo_departamento: int
    descripcion_departamento: str
    codigo_distrito: int | None
    descripcion_distrito: str | None
    codigo_ciudad: int
    descripcion_ciudad: str
    telefono: str
    email: str
    denominacion_sucursal: str | None
    actividades_economicas: list[ActividadEconomica]
    responsable_de: ResponsableDE | None = None


@dataclass
class ResponsableDE:
    tipo_id: int
    descripcion_tipo_id: str
    numero_id: str
    nombre: str
    cargo: str


@dataclass
class ReceptorXML:
    naturaleza: int
    tipo_operacion: int
    codigo_pais: str
    descripcion_pais: str
    tipo_contribuyente: int | None
    ruc: str | None
    dv: str | None
    tipo_id: int | None
    descripcion_tipo_id: str | None
    numero_id: str | None
    nombre: str
    nombre_fantasia: str | None
    direccion: str | None
    numero_casa: int | None
    codigo_departamento: int | None
    descripcion_departamento: str | None
    codigo_distrito: int | None
    descripcion_distrito: str | None
    codigo_ciudad: int | None
    descripcion_ciudad: str | None
    telefono: str | None
    celular: str | None
    email: str | None
    codigo_cliente: str | None


@dataclass
class OperacionComercial:
    tipo_transaccion: int | None
    descripcion_transaccion: str | None
    tipo_impuesto: int
    descripcion_impuesto: str
    codigo_moneda: str
    descripcion_moneda: str
    condicion_tipo_cambio: int | None
    tipo_cambio: Decimal | None
    condicion_anticipo: int | None
    descripcion_anticipo: str | None
    obligaciones_afectadas: list[ObligacionAfectada] = field(default_factory=list)


@dataclass
class ObligacionAfectada:
    codigo: int
    descripcion: str


@dataclass
class IndicadorPresencia:
    codigo: int
    descripcion: str


@dataclass
class CamposFE:
    indicador_presencia: IndicadorPresencia
    fecha_emision_nr: str | None = None


@dataclass
class CondicionOperacion:
    condicion: int
    descripcion: str
    credito: Credito | None = None


@dataclass
class Credito:
    condicion_credito: int
    descripcion_condicion: str
    plazo: str | None = None
    cantidad_cuotas: int | None = None
    monto_entrada: Decimal | None = None


@dataclass
class ValorItem:
    precio_unitario: Decimal
    total_bruto_item: Decimal
    descuento_item: Decimal | None = None
    porc_descuento_item: Decimal | None = None
    descuento_global_item: Decimal | None = None
    anticipo_preuni_item: Decimal | None = None
    anticipo_global_preuni_item: Decimal | None = None
    total_operacion_item: Decimal = Decimal("0")
    total_operacion_gs: Decimal | None = None


@dataclass
class IVAItem:
    afectacion: int
    descripcion_afectacion: str
    proporcion: Decimal
    tasa: int
    base_gravable: Decimal
    liquidacion: Decimal
    base_exenta: Decimal = Decimal("0")


@dataclass
class Item:
    codigo_interno: str
    descripcion: str
    codigo_unidad_medida: int
    descripcion_unidad_medida: str
    cantidad: Decimal
    informacion_item: str | None
    valor: ValorItem
    iva: IVAItem | None = None


@dataclass
class Totales:
    subtotal_exento: Decimal = Decimal("0")
    subtotal_exonerado: Decimal = Decimal("0")
    subTotal5: Decimal = Decimal("0")
    subTotal10: Decimal = Decimal("0")
    total_operacion: Decimal = Decimal("0")
    total_descuento: Decimal = Decimal("0")
    total_descuento_global: Decimal = Decimal("0")
    total_anticipo_item: Decimal = Decimal("0")
    total_anticipo: Decimal = Decimal("0")
    porcentaje_descuento_total: Decimal = Decimal("0")
    descuento_total: Decimal = Decimal("0")
    anticipo: Decimal = Decimal("0")
    redondeo: Decimal = Decimal("0")
    comision: Decimal | None = None
    total_general: Decimal = Decimal("0")
    iva5: Decimal | None = None
    iva10: Decimal | None = None
    liq_total_iva5: Decimal | None = None
    liq_total_iva10: Decimal | None = None
    iva_comision: Decimal | None = None
    total_iva: Decimal | None = None
    base_grav5: Decimal | None = None
    base_grav10: Decimal | None = None
    total_base_gra_iva: Decimal | None = None
    total_gs: Decimal | None = None


class XMLBuilderError(Exception):
    pass


def _xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _element(tag: str, value: object, attrs: str | None = None) -> str:
    val = str(value) if value is not None else ""
    if val == "":
        return f"<{tag}/>"
    if attrs:
        return f"<{tag} {attrs}>{_xml_escape(val)}</{tag}>"
    return f"<{tag}>{_xml_escape(val)}</{tag}>"


def _build_g_act_eco(actividades: list[ActividadEconomica], indent: str) -> str:
    xml = ""
    for act in actividades:
        xml += f"{indent}  <gActEco>\n"
        xml += f"{indent}    {_element('cActEco', act.codigo)}\n"
        xml += f"{indent}    {_element('dDesActEco', act.descripcion)}\n"
        xml += f"{indent}  </gActEco>\n"
    return xml


def _build_emisor(emisor: EmisorXML, indent: str) -> str:
    xml = f"{indent}<gEmis>\n"
    xml += f"{indent}  {_element('dRucEm', emisor.ruc)}\n"
    xml += f"{indent}  {_element('dDVEmi', emisor.dv)}\n"
    xml += f"{indent}  {_element('iTipCont', emisor.tipo_contribuyente.value)}\n"
    xml += f"{indent}  {_element('cTipReg', emisor.tipo_regimen)}\n"
    xml += f"{indent}  {_element('dNomEmi', emisor.nombre)}\n"
    if emisor.nombre_fantasia:
        xml += f"{indent}  {_element('dNomFanEmi', emisor.nombre_fantasia)}\n"
    xml += f"{indent}  {_element('dDirEmi', emisor.direccion)}\n"
    xml += f"{indent}  {_element('dNumCas', emisor.numero_casa)}\n"
    if emisor.complemento_dir1:
        xml += f"{indent}  {_element('dCompDir1', emisor.complemento_dir1)}\n"
    if emisor.complemento_dir2:
        xml += f"{indent}  {_element('dCompDir2', emisor.complemento_dir2)}\n"
    xml += f"{indent}  {_element('cDepEmi', emisor.codigo_departamento)}\n"
    xml += f"{indent}  {_element('dDesDepEmi', emisor.descripcion_departamento)}\n"
    if emisor.codigo_distrito is not None:
        xml += f"{indent}  {_element('cDisEmi', emisor.codigo_distrito)}\n"
    if emisor.descripcion_distrito is not None:
        xml += f"{indent}  {_element('dDesDisEmi', emisor.descripcion_distrito)}\n"
    xml += f"{indent}  {_element('cCiuEmi', emisor.codigo_ciudad)}\n"
    xml += f"{indent}  {_element('dDesCiuEmi', emisor.descripcion_ciudad)}\n"
    xml += f"{indent}  {_element('dTelEmi', emisor.telefono)}\n"
    xml += f"{indent}  {_element('dEmailE', emisor.email)}\n"
    if emisor.denominacion_sucursal:
        xml += f"{indent}  {_element('dDenSuc', emisor.denominacion_sucursal)}\n"
    xml += _build_g_act_eco(emisor.actividades_economicas, indent)
    if emisor.responsable_de:
        r = emisor.responsable_de
        xml += f"{indent}  <gRespDE>\n"
        xml += f"{indent}    {_element('iTipIDRespDE', r.tipo_id)}\n"
        xml += f"{indent}    {_element('dDTipIDRespDE', r.descripcion_tipo_id)}\n"
        xml += f"{indent}    {_element('dNumIDRespDE', r.numero_id)}\n"
        xml += f"{indent}    {_element('dNomRespDE', r.nombre)}\n"
        xml += f"{indent}    {_element('dCarRespDE', r.cargo)}\n"
        xml += f"{indent}  </gRespDE>\n"
    xml += f"{indent}</gEmis>\n"
    return xml


def _build_receptor(receptor: ReceptorXML, indent: str) -> str:
    xml = f"{indent}<gDatRec>\n"
    xml += f"{indent}  {_element('iNatRec', receptor.naturaleza)}\n"
    xml += f"{indent}  {_element('iTiOpe', receptor.tipo_operacion)}\n"
    xml += f"{indent}  {_element('cPaisRec', receptor.codigo_pais)}\n"
    xml += f"{indent}  {_element('dDesPaisRe', receptor.descripcion_pais)}\n"
    if receptor.tipo_contribuyente is not None:
        xml += f"{indent}  {_element('iTiContRec', receptor.tipo_contribuyente)}\n"
    if receptor.ruc is not None:
        xml += f"{indent}  {_element('dRucRec', receptor.ruc)}\n"
    if receptor.dv is not None:
        xml += f"{indent}  {_element('dDVRec', receptor.dv)}\n"
    if receptor.tipo_id is not None:
        xml += f"{indent}  {_element('iTipIDRec', receptor.tipo_id)}\n"
    if receptor.descripcion_tipo_id is not None:
        xml += f"{indent}  {_element('dDTipIDRec', receptor.descripcion_tipo_id)}\n"
    if receptor.numero_id is not None:
        xml += f"{indent}  {_element('dNumIDRec', receptor.numero_id)}\n"
    xml += f"{indent}  {_element('dNomRec', receptor.nombre)}\n"
    if receptor.nombre_fantasia:
        xml += f"{indent}  {_element('dNomFanRec', receptor.nombre_fantasia)}\n"
    if receptor.direccion is not None:
        xml += f"{indent}  {_element('dDirRec', receptor.direccion)}\n"
    if receptor.numero_casa is not None:
        xml += f"{indent}  {_element('dNumCasRec', receptor.numero_casa)}\n"
    if receptor.codigo_departamento is not None:
        xml += f"{indent}  {_element('cDepRec', receptor.codigo_departamento)}\n"
    if receptor.descripcion_departamento is not None:
        xml += f"{indent}  {_element('dDesDepRec', receptor.descripcion_departamento)}\n"
    if receptor.codigo_distrito is not None:
        xml += f"{indent}  {_element('cDisRec', receptor.codigo_distrito)}\n"
    if receptor.descripcion_distrito is not None:
        xml += f"{indent}  {_element('dDesDisRec', receptor.descripcion_distrito)}\n"
    if receptor.codigo_ciudad is not None:
        xml += f"{indent}  {_element('cCiuRec', receptor.codigo_ciudad)}\n"
    if receptor.descripcion_ciudad is not None:
        xml += f"{indent}  {_element('dDesCiuRec', receptor.descripcion_ciudad)}\n"
    if receptor.telefono is not None:
        xml += f"{indent}  {_element('dTelRec', receptor.telefono)}\n"
    if receptor.celular is not None:
        xml += f"{indent}  {_element('dCelRec', receptor.celular)}\n"
    if receptor.email is not None:
        xml += f"{indent}  {_element('dEmailRec', receptor.email)}\n"
    if receptor.codigo_cliente is not None:
        xml += f"{indent}  {_element('dCodCliente', receptor.codigo_cliente)}\n"
    xml += f"{indent}</gDatRec>\n"
    return xml


def _build_g_valor_item(valor: ValorItem, indent: str) -> str:
    xml = f"{indent}<gValorItem>\n"
    xml += f"{indent}  {_element('dPUniProSer', _fmt_monto(valor.precio_unitario))}\n"
    xml += f"{indent}  {_element('dTotBruOpeItem', _fmt_monto(valor.total_bruto_item))}\n"
    xml += f"{indent}  <gValorRestaItem>\n"
    if valor.descuento_item is not None:
        xml += f"{indent}    {_element('dDescItem', _fmt_monto(valor.descuento_item))}\n"
    if valor.porc_descuento_item is not None:
        xml += f"{indent}    {_element('dPorcDesIt', _fmt_monto(valor.porc_descuento_item))}\n"
    if valor.descuento_global_item is not None:
        xml += f"{indent}    {_element('dDescGloItem', _fmt_monto(valor.descuento_global_item))}\n"
    if valor.anticipo_preuni_item is not None:
        xml += f"{indent}    {_element('dAntPreUniIt', _fmt_monto(valor.anticipo_preuni_item))}\n"
    if valor.anticipo_global_preuni_item is not None:
        xml += (
            f"{indent}    "
            f"{_element('dAntGloPreUniIt', _fmt_monto(valor.anticipo_global_preuni_item))}\n"
        )
    xml += f"{indent}    {_element('dTotOpeItem', _fmt_monto(valor.total_operacion_item))}\n"
    if valor.total_operacion_gs is not None:
        xml += f"{indent}    {_element('dTotOpeGs', _fmt_monto(valor.total_operacion_gs))}\n"
    xml += f"{indent}  </gValorRestaItem>\n"
    xml += f"{indent}</gValorItem>\n"
    return xml


def _build_g_cam_iva(iva: IVAItem, indent: str) -> str:
    xml = f"{indent}<gCamIVA>\n"
    xml += f"{indent}  {_element('iAfecIVA', iva.afectacion)}\n"
    xml += f"{indent}  {_element('dDesAfecIVA', iva.descripcion_afectacion)}\n"
    xml += f"{indent}  {_element('dPropIVA', _fmt_monto(iva.proporcion))}\n"
    xml += f"{indent}  {_element('dTasaIVA', iva.tasa)}\n"
    xml += f"{indent}  {_element('dBasGravIVA', _fmt_monto(iva.base_gravable))}\n"
    xml += f"{indent}  {_element('dLiqIVAItem', _fmt_monto(iva.liquidacion))}\n"
    xml += f"{indent}  {_element('dBasExe', _fmt_monto(iva.base_exenta))}\n"
    xml += f"{indent}</gCamIVA>\n"
    return xml


def _build_g_cam_item(items: list[Item], indent: str) -> str:
    xml = ""
    for item in items:
        xml += f"{indent}<gCamItem>\n"
        xml += f"{indent}  {_element('dCodInt', item.codigo_interno)}\n"
        xml += f"{indent}  {_element('dDesProSer', item.descripcion)}\n"
        xml += f"{indent}  {_element('cUniMed', item.codigo_unidad_medida)}\n"
        xml += f"{indent}  {_element('dDesUniMed', item.descripcion_unidad_medida)}\n"
        xml += f"{indent}  {_element('dCantProSer', _fmt_monto(item.cantidad))}\n"
        if item.informacion_item:
            xml += f"{indent}  {_element('dInfItem', item.informacion_item)}\n"
        if item.valor:
            xml += _build_g_valor_item(item.valor, f"{indent}  ")
        if item.iva:
            xml += _build_g_cam_iva(item.iva, f"{indent}  ")
        xml += f"{indent}</gCamItem>\n"
    return xml


def _build_g_tot_sub(totales: Totales, indent: str) -> str:
    xml = f"{indent}<gTotSub>\n"
    xml += f"{indent}  {_element('dSubExe', _fmt_monto(totales.subtotal_exento))}\n"
    xml += f"{indent}  {_element('dSubExo', _fmt_monto(totales.subtotal_exonerado))}\n"
    xml += f"{indent}  {_element('dSub5', _fmt_monto(totales.subTotal5))}\n"
    xml += f"{indent}  {_element('dSub10', _fmt_monto(totales.subTotal10))}\n"
    xml += f"{indent}  {_element('dTotOpe', _fmt_monto(totales.total_operacion))}\n"
    xml += f"{indent}  {_element('dTotDesc', _fmt_monto(totales.total_descuento))}\n"
    xml += f"{indent}  {_element('dTotDescGlotem', _fmt_monto(totales.total_descuento_global))}\n"
    xml += f"{indent}  {_element('dTotAntItem', _fmt_monto(totales.total_anticipo_item))}\n"
    xml += f"{indent}  {_element('dTotAnt', _fmt_monto(totales.total_anticipo))}\n"
    xml += f"{indent}  {_element('dPorcDescTotal', _fmt_monto(totales.porcentaje_descuento_total))}\n"  # noqa: E501
    xml += f"{indent}  {_element('dDescTotal', _fmt_monto(totales.descuento_total))}\n"
    xml += f"{indent}  {_element('dAnticipo', _fmt_monto(totales.anticipo))}\n"
    xml += f"{indent}  {_element('dRedon', _fmt_monto(totales.redondeo))}\n"
    if totales.comision is not None:
        xml += f"{indent}  {_element('dComi', _fmt_monto(totales.comision))}\n"
    xml += f"{indent}  {_element('dTotGralOpe', _fmt_monto(totales.total_general))}\n"
    if totales.iva5 is not None:
        xml += f"{indent}  {_element('dIVA5', _fmt_monto(totales.iva5))}\n"
    if totales.iva10 is not None:
        xml += f"{indent}  {_element('dIVA10', _fmt_monto(totales.iva10))}\n"
    if totales.liq_total_iva5 is not None:
        xml += f"{indent}  {_element('dLiqTotIVA5', _fmt_monto(totales.liq_total_iva5))}\n"
    if totales.liq_total_iva10 is not None:
        xml += f"{indent}  {_element('dLiqTotIVA10', _fmt_monto(totales.liq_total_iva10))}\n"
    if totales.iva_comision is not None:
        xml += f"{indent}  {_element('dIVAComi', _fmt_monto(totales.iva_comision))}\n"
    if totales.total_iva is not None:
        xml += f"{indent}  {_element('dTotIVA', _fmt_monto(totales.total_iva))}\n"
    if totales.base_grav5 is not None:
        xml += f"{indent}  {_element('dBaseGrav5', _fmt_monto(totales.base_grav5))}\n"
    if totales.base_grav10 is not None:
        xml += f"{indent}  {_element('dBaseGrav10', _fmt_monto(totales.base_grav10))}\n"
    if totales.total_base_gra_iva is not None:
        xml += f"{indent}  {_element('dTBasGraIVA', _fmt_monto(totales.total_base_gra_iva))}\n"
    if totales.total_gs is not None:
        xml += f"{indent}  {_element('dTotalGs', _fmt_monto(totales.total_gs))}\n"
    xml += f"{indent}</gTotSub>\n"
    return xml


def _fmt_monto(valor: Decimal) -> str:
    return f"{valor:f}"


@dataclass
class DatosFacturaFE:
    cdc: str
    dv_cdc: int
    fecha_firma: datetime
    tipo_emision: TipoEmision
    tipo_documento: TipoDocumento
    codigo_seguridad: str
    numero_timbrado: str
    establecimiento: str
    punto_expedicion: str
    numero_documento: int
    serie: str
    fecha_inicio_timbrado: str
    fecha_emision: datetime
    operacion_comercial: OperacionComercial
    emisor: EmisorXML
    receptor: ReceptorXML
    campos_fe: CamposFE
    condicion_operacion: CondicionOperacion | None
    items: list[Item]
    totales: Totales
    informacion_emisor: str | None = None
    informacion_fisco: str | None = None


def construir_de_factura(datos: DatosFacturaFE) -> str:
    ind = "  "
    cdc_completo = f"{datos.cdc}{datos.dv_cdc}"
    fecha_firma_str = datos.fecha_firma.strftime("%Y-%m-%dT%H:%M:%S")
    fecha_emision_str = datos.fecha_emision.strftime("%Y-%m-%dT%H:%M:%S")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<rDE xmlns="http://ekuatia.set.gov.py/sifen/xsd" '
    xml += 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
    xml += 'xsi:schemaLocation="https://ekuatia.set.gov.py/sifen/xsd siRecepDE_v150.xsd">\n'

    # dVerFor
    xml += f"{ind}<dVerFor>150</dVerFor>\n"

    # DE (contenido firmado)
    xml += f'{ind}<DE Id="{cdc_completo}">\n'

    # dDVId
    xml += f'{ind}  {_element("dDVId", datos.dv_cdc)}\n'

    # dFecFirma
    xml += f'{ind}  {_element("dFecFirma", fecha_firma_str)}\n'

    # dSisFact
    xml += f'{ind}  {_element("dSisFact", 1)}\n'

    # gOpeDE
    xml += f"{ind}  <gOpeDE>\n"
    xml += f"{ind}    {_element('iTipEmi', datos.tipo_emision.value)}\n"
    desc_tip_emi = "Normal" if datos.tipo_emision == TipoEmision.NORMAL else "Contingencia"
    xml += f"{ind}    {_element('dDesTipEmi', desc_tip_emi)}\n"
    xml += f"{ind}    {_element('dCodSeg', datos.codigo_seguridad)}\n"
    if datos.informacion_emisor:
        xml += f"{ind}    {_element('dInfoEmi', datos.informacion_emisor)}\n"
    if datos.informacion_fisco:
        xml += f"{ind}    {_element('dInfoFisc', datos.informacion_fisco)}\n"
    xml += f"{ind}  </gOpeDE>\n"

    # gTimb
    xml += f"{ind}  <gTimb>\n"
    xml += f"{ind}    {_element('iTiDE', datos.tipo_documento.value)}\n"
    desc_tipo_de = _desc_tipo_de(datos.tipo_documento)
    xml += f"{ind}    {_element('dDesTiDE', desc_tipo_de)}\n"
    xml += f"{ind}    {_element('dNumTim', datos.numero_timbrado)}\n"
    xml += f"{ind}    {_element('dEst', datos.establecimiento)}\n"
    xml += f"{ind}    {_element('dPunExp', datos.punto_expedicion)}\n"
    xml += f"{ind}    {_element('dNumDoc', str(datos.numero_documento).zfill(7))}\n"
    if datos.serie:
        xml += f"{ind}    {_element('dSerieNum', datos.serie)}\n"
    xml += f"{ind}    {_element('dFeIniT', datos.fecha_inicio_timbrado)}\n"
    xml += f"{ind}  </gTimb>\n"

    # gDatGralOpe
    xml += f"{ind}  <gDatGralOpe>\n"
    xml += f"{ind}    {_element('dFeEmiDE', fecha_emision_str)}\n"

    # gOpeCom
    oc = datos.operacion_comercial
    xml += f"{ind}    <gOpeCom>\n"
    if oc.tipo_transaccion is not None:
        xml += f"{ind}      {_element('iTipTra', oc.tipo_transaccion)}\n"
    if oc.descripcion_transaccion is not None:
        xml += f"{ind}      {_element('dDesTipTra', oc.descripcion_transaccion)}\n"
    xml += f"{ind}      {_element('iTImp', oc.tipo_impuesto)}\n"
    xml += f"{ind}      {_element('dDesTImp', oc.descripcion_impuesto)}\n"
    xml += f"{ind}      {_element('cMoneOpe', oc.codigo_moneda)}\n"
    xml += f"{ind}      {_element('dDesMoneOpe', oc.descripcion_moneda)}\n"
    if oc.condicion_tipo_cambio is not None:
        xml += f"{ind}      {_element('dCondTiCam', oc.condicion_tipo_cambio)}\n"
    if oc.tipo_cambio is not None:
        xml += f"{ind}      {_element('dTiCam', _fmt_monto(oc.tipo_cambio))}\n"
    if oc.condicion_anticipo is not None:
        xml += f"{ind}      {_element('iCondAnt', oc.condicion_anticipo)}\n"
    if oc.descripcion_anticipo is not None:
        xml += f"{ind}      {_element('dDesCondAnt', oc.descripcion_anticipo)}\n"
    for obl in oc.obligaciones_afectadas:
        xml += f"{ind}      <gOblAfe>\n"
        xml += f"{ind}        {_element('cOblAfe', obl.codigo)}\n"
        xml += f"{ind}        {_element('dDesOblAfe', obl.descripcion)}\n"
        xml += f"{ind}      </gOblAfe>\n"
    xml += f"{ind}    </gOpeCom>\n"

    xml += _build_emisor(datos.emisor, f"{ind}    ")
    xml += _build_receptor(datos.receptor, f"{ind}    ")

    xml += f"{ind}  </gDatGralOpe>\n"

    # gDtipDE
    xml += f"{ind}  <gDtipDE>\n"

    # gCamFE
    if datos.campos_fe:
        cf = datos.campos_fe
        xml += f"{ind}    <gCamFE>\n"
        xml += f"{ind}      {_element('iIndPres', cf.indicador_presencia.codigo)}\n"
        xml += f"{ind}      {_element('dDesIndPres', cf.indicador_presencia.descripcion)}\n"
        if cf.fecha_emision_nr:
            xml += f"{ind}      {_element('dFecEmNR', cf.fecha_emision_nr)}\n"
        xml += f"{ind}    </gCamFE>\n"

    # gCamCond
    if datos.condicion_operacion:
        co = datos.condicion_operacion
        xml += f"{ind}    <gCamCond>\n"
        xml += f"{ind}      {_element('iCondOpe', co.condicion)}\n"
        xml += f"{ind}      {_element('dDCondOpe', co.descripcion)}\n"
        if co.credito:
            cr = co.credito
            xml += f"{ind}      <gPagCred>\n"
            xml += f"{ind}        {_element('iCondCred', cr.condicion_credito)}\n"
            xml += f"{ind}        {_element('dDCondCred', cr.descripcion_condicion)}\n"
            if cr.plazo:
                xml += f"{ind}        {_element('dPlazoCre', cr.plazo)}\n"
            if cr.cantidad_cuotas is not None:
                xml += f"{ind}        {_element('dCuotas', cr.cantidad_cuotas)}\n"
            if cr.monto_entrada is not None:
                xml += f"{ind}        {_element('dMonEnt', _fmt_monto(cr.monto_entrada))}\n"
            xml += f"{ind}      </gPagCred>\n"
        xml += f"{ind}    </gCamCond>\n"

    # gCamItem
    xml += _build_g_cam_item(datos.items, f"{ind}    ")

    xml += f"{ind}  </gDtipDE>\n"

    # gTotSub
    xml += _build_g_tot_sub(datos.totales, f"{ind}  ")

    xml += f"{ind}</DE>\n"

    # Espacio para Signature (se inserta despues de firmar)
    xml += f"{ind}<!-- SIGNATURE_PLACEHOLDER -->\n"

    # gCamFuFD
    xml += f"{ind}<gCamFuFD>\n"
    xml += f"{ind}  <!-- QR_PLACEHOLDER -->\n"
    xml += f"{ind}</gCamFuFD>\n"

    xml += "</rDE>\n"
    return xml


def _desc_tipo_de(tipo: TipoDocumento) -> str:
    mapa: dict[TipoDocumento, str] = {
        TipoDocumento.FACTURA: "Factura electr\u00f3nica",
        TipoDocumento.NOTA_CREDITO: "Nota de cr\u00e9dito electr\u00f3nica",
        TipoDocumento.NOTA_DEBITO: "Nota de d\u00e9bito electr\u00f3nica",
    }
    return mapa.get(tipo, tipo.value)