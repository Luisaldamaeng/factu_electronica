# Puntos de verificacion

> **Proyecto:** Facturacion Electronica SIFEN (Paraguay)
> **Fase:** Planificacion.
> **Objetivo:** Confirmar contra la fuente oficial de la DNIT los datos que hoy provienen de fuentes secundarias, antes de fijarlos en el plan o en el diseno.
> **Ultima actualizacion:** 2026-11-12
> **Estado:** 11 verificados, 0 parciales, 0 pendientes de inicio.

## Regla de cierre

Un punto se marca como verificado solo si se registro:

1. La fuente oficial consultada (URL o documento y version).
2. La fecha de consulta.
3. La conclusion.
4. El impacto en el plan.

---

## Resumen

| # | Punto | Prioridad | Estado |
|---|---|---|---|
| 1 | Estandar de firma (XMLDSig vs XAdES) | Alta | Verificado |
| 2 | Uso real de mTLS por servicio | Alta | Verificado |
| 3 | Formulario 364 | Media | Verificado con correccion |
| 4 | Tasa de timbrado | Media | Verificado |
| 5 | Costo y proveedores de certificados | Media | Verificado |
| 6 | Ley 6822/21 | Alta | Verificado |
| 7 | Plazos de contingencia | Alta | Verificado |
| 8 | Catalogo de codigos de rechazo | Alta | Verificado |
| 9 | Version del Manual Tecnico y XSD | Alta | Verificado |
| 10 | Set de pruebas de homologacion | Alta | Verificado |
| 11 | Maquina de estados del DE | Alta | Verificado |

---

## Resultados de la verificacion

### 1. Estandar de firma: XMLDSig enveloped, no XAdES

- **Estado:** Verificado.
- **Fuente:** DNIT, Manual Tecnico SIFEN V150 (10/09/2019), secciones 7.6 y 7.7; DNIT, Guia de Mejores Practicas para la Gestion del Envio de DE (octubre 2024).
- **Conclusion:** SIFEN exige **XML Digital Signature (XMLDSig) del W3C, en modalidad enveloped**. No exige XAdES ni una cabecera WS-Security. Parametros confirmados:
  - Canonicalizacion del documento: C14N inclusiva (`http://www.w3.org/TR/2001/REC-xml-c14n-20010315`) en `CanonicalizationMethod`.
  - Transformacion de la referencia: C14N exclusiva (`http://www.w3.org/2001/10/xml-exc-c14n#`) mas enveloped signature.
  - Firma: RSA-SHA256.
  - Digest: SHA-256.
  - Clave: RSA 2048.
  - `KeyInfo` solo con `X509Data`.
  - Codificacion Base64.
  - Ubicacion: dentro de `rDE`, despues de `DE` y antes de `gCamFuFD`. El QR (`gCamFuFD`) queda fuera de la firma.
- **Correccion:** el termino "XAdES" que aparecia en la investigacion inicial es impreciso. XAdES es una familia de extensiones sobre XMLDSig usada en otros paises, pero no es lo que pide el manual paraguayo.
- **Correccion 2026-11-20:** la version anterior decia "C14N exclusiva" para todo el proceso. El MT V150 distingue la canonicalizacion del `SignedInfo` (inclusiva) de la transformacion de la referencia (exclusiva).
- **Impacto:** usar `sifen` (kmee) y forzar el `Transform` exclusivo; validar la firma con una implementacion independiente y contra el XML de ejemplo oficial. No implementar XAdES.

### 2. mTLS: obligatorio en todos los servicios web

- **Estado:** Verificado.
- **Fuente:** DNIT, Guia de Mejores Practicas (octubre 2024); DNIT, Preguntas Frecuentes de e-Kuatia (ambiente de pruebas y produccion); Manual Tecnico V150.
- **Conclusion:** la comunicacion con SIFEN usa TLS 1.2 con **autenticacion mutua** basada en el certificado digital del contribuyente, emitido por un PSC habilitado. Aplica al ingreso y a los servicios web (recepcion, lotes, consultas y eventos).
- **Impacto:** el certificado debe estar disponible en cada conexion mTLS, no solo al firmar. El cliente HTTP necesita un keystore del contribuyente y rotacion controlada.

### 3. Formulario 364: se genera despues de las pruebas

- **Estado:** Verificado con correccion.
- **Fuente:** DNIT, Guia paso a paso de solicitud y habilitacion de facturadores electronicos.
- **Conclusion:** el **Formulario 364 "Solicitud de Habilitacion como Facturador Electronico"** se genera en Marangatu/SGTM. El orden correcto es:
  1. Solicitar acceso al ambiente de pruebas por la mesa de ayuda.
  2. Recibir el set de datos de prueba (RUC, timbrado y CSC generico).
  3. Ejecutar las pruebas minimas.
  4. Generar el Formulario 364, que queda en estado "Aceptado/Presentado".
- **Correccion:** la investigacion inicial decia que el 364 habilitaba el testing. En realidad se presenta **despues** de completar las pruebas.
- **Impacto:** reordenar el checklist de homologacion del plan.

### 4. Tasa de timbrado

- **Estado:** Verificado.
- **Fuente:** DNIT, portal y asistente de solicitudes de Marangatu; fuentes secundarias de 2026 (ContaFacil, GOEKUA, Enplazo, Vouga), consultadas el 2026-11-12.
- **Conclusion:** el timbrado electronico **no tiene tasa ni costo oficial** si el contribuyente lo gestiona por Marangatu/SIFEN. Los Gs. 150.000 que mencionan varias fuentes corresponden a un **servicio de gestion privado**, no a una tasa de la DNIT. Los costos obligatorios reales son el certificado cualificado de firma electronica y, opcionalmente, el software de emision.
- **Impacto:** no incluir los Gs. 150.000 como costo obligatorio. El presupuesto solo contempla el certificado (ver punto 5) y la infraestructura.

### 5. Costo y proveedores de certificados

- **Estado:** Verificado.
- **Fuente:** AC Raiz / MIC (`https://www.acraiz.gov.py/html/Certif_1PrestaServ.html`); resoluciones de habilitacion de PCSC; ABC Color; fuentes de mercado 2026; consultadas el 2026-11-12.
- **Conclusion:** la autoridad es la Direccion General de Firma Digital y Comercio Electronico del MIC. Los **PCSC habilitados** identificados son VIT S.A. (eFirma, Res. 774/2014 y 1748/2022), CODE 100 S.A. (Res. 187/2015), CONFIRMA S.A. (Res. 510/2023), Documenta S.A., ITTI S.A.E.C.A. y el Ministerio del Interior. Para SIFEN se requiere un **certificado cualificado de firma electronica tipo F1** (`.pfx`), vigencia anual. El precio de mercado ronda **Gs. 350.000 por ano**, con un rango observado de **Gs. 150.000 a Gs. 440.000** segun prestador y canal.
- **Impacto:** la guia de onboarding debe pedir "certificado cualificado de firma electronica vigente tipo F1" y no un proveedor especifico. La Lista de Confianza vigente se verifica al momento de cada alta.

### 6. Ley 6822/2021

- **Estado:** Verificado.
- **Fuente:** BACN, texto oficial de la Ley N. 6822; MIC, Resolucion N. 994/2023; ABC Color (03/08/2026).
- **Conclusion:** la ley se titula **"De los servicios de confianza para las transacciones electronicas, del documento electronico y los documentos transmisibles electronicos"**, de fecha 30/12/2021. El MIC es la autoridad de aplicacion. La ley reemplaza el termino "firma digital" por **"firma electronica cualificada"** y regula a los PCSC.
- **Impacto:** usar la denominacion correcta en los terminos de servicio y en la documentacion. La responsabilidad del cliente sobre su certificado se apoya en esta ley y en el Decreto 7576/2022.

### 7. Plazos de contingencia y transmision

- **Estado:** Verificado.
- **Fuente:** Manual Tecnico V150, seccion 6.2 y capitulo 14; DNIT, Preguntas Frecuentes (cancelacion e inutilizacion); RG 05/2018.
- **Conclusion:**
  - Transmision normal: hasta **72 horas** desde la firma digital del DE.
  - Diferencia entre emision y transmision mayor a **120 horas (5 dias):** tramite administrativo para normalizar el DE rechazado por extemporaneidad.
  - Cancelacion de factura electronica: hasta **48 horas** desde la aprobacion.
  - Cancelacion de otros DTE: hasta **168 horas (7 dias)**.
  - Inutilizacion de numeracion: dentro de los **15 dias** del mes siguiente.
  - La operacion de contingencia como tal figura como **"Futuro"** en el Manual V150: el capitulo 14 esta marcado asi. En la practica se resuelve con cola de pendientes y reintento.
- **Impacto:** el worker debe reintentar y alertar antes de las 72 horas; no prometer un modo contingencia que el manual aun no define.

### 8. Catalogo de codigos de rechazo

- **Estado:** Verificado.
- **Fuente:** Manual Tecnico V150 (secciones 12.2 a 12.4, paginas 148 a 193 del PDF); NT_E_KUATIA_027 (09/03/2026); extraccion y deduplicacion realizadas el 2026-11-12.
- **Conclusion:** se extrajeron **396 codigos unicos**: 42 de servicios web (0001 a 0650), 280 de validacion del DE (1000 a 2650) y 74 de eventos (4000 a 4350). La NT 027 no modifica codigos. Ejemplos clave: `0260` aprobado, `0300` lote recibido, `0301` lote no encolado, `1005` aprobado con observacion por extemporaneidad, `1101`/`1103`/`1104` timbrado invalido o no vigente, `1150` retraso mayor a 720 horas, `0600` evento registrado.
- **Impacto:** la maquina de estados y los mensajes al usuario se construyen sobre [`catalogo de codigos SIFEN.md`](catalogo%20de%20codigos%20SIFEN.md) y su CSV versionado. La maquina interna esta en [`maquina de estados del DE.md`](maquina%20de%20estados%20del%20DE.md).

### 9. Version del Manual Tecnico y XSD

- **Estado:** Verificado.
- **Fuente:** DNIT, pagina de Documentacion Tecnica (`https://www.dnit.gov.py/web/e-kuatia/documentacion-tecnica`), consultada el 2026-11-08.
- **Conclusion:** la version publicada es el **Manual Tecnico V150 (10/09/2019)**, complementado por las **Notas Tecnicas NT_E_KUATIA_001 a 027**. Se publican ademas:
  - `Estructura xml_DE.rar` (ejemplos).
  - `Estructura_DE xsd.rar` (esquemas).
  - `Listado Checksum MD5 de las versiones del Manual Tecnico`.
  - `Guia de Mejores Practicas para la Gestion del Envio de DE`.
  - Los XSD tambien en `http://ekuatia.set.gov.py/sifen/xsd`.
- **Impacto:** baseline archivado en `docs/baseline/` con 82 archivos y hashes en `inventario.csv`; ver `baseline/BASELINE.md`. Incluye el hallazgo de que el MD5 del Manual local no coincide con el listado oficial porque la DNIT reemplazo el PDF publicado.

### 10. Set de pruebas de homologacion

- **Estado:** Verificado.
- **Fuente:** DNIT, Guia de Pruebas para e-kuatia (actualizada en 2026).
- **Conclusion:** existe una guia oficial con el set de datos de prueba (RUC, timbrado y CSC generico) y los escenarios minimos: ingreso con autenticacion mutua, envio sincrono y asincrono, aprobaciones y rechazos, consultas, eventos y validacion de KuDE/QR. Cubre factura, nota de credito, nota de debito, autofactura y nota de remision.
- **Impacto:** automatizar el set como suite de aceptacion antes de la homologacion.

### 11. Maquina de estados del DE

- **Estado:** Verificado.
- **Fuente:** Manual Tecnico V150; DNIT, Preguntas Frecuentes; RG 23/2019; diseno interno documentado el 2026-11-12.
- **Conclusion:** SIFEN define el resultado como **Aprobado (A)**, **Aprobado con Observacion (AO)** o **Rechazado (R)**. Los estados de ciclo de vida documentados son **aprobado, cancelado e inutilizado**; el resto son de implementacion propia. Se definio la maquina interna con los estados `GENERADO`, `ERROR_FIRMA`, `FIRMADO`, `EN_COLA`, `ENVIADO`, `EN_CONTINGENCIA`, `APROBADO`, `APROBADO_CON_OBSERVACION`, `RECHAZADO`, `CANCELADO` y `BLOQUEADO`, mapeados a los codigos del catalogo. La inutilizacion se modela por rango de numeracion y no como estado del DE.
- **Impacto:** modelo de datos con `estado`, `resultado_sifen`, `codigo_sifen`, `intentos_envio`, `proximo_intento` y tabla de transiciones append-only. Ver [`maquina de estados del DE.md`](maquina%20de%20estados%20del%20DE.md).

---

## Puntos que siguen abiertos

Ninguno. Los 11 puntos quedaron verificados al 2026-11-12. Lo que resta es operativo (descargar la Lista de Confianza al dar de alta cada cliente y pedir acceso al ambiente de testing), no una verificacion normativa pendiente.

---

## Registro de verificaciones

| # | Fecha | Fuente | Conclusion | Impacto |
|---|---|---|---|---|
| 1 | 2026-11-08 | MT V150 seccion 7.6-7.7; Guia de Mejores Practicas | XMLDSig enveloped, RSA-SHA256, SHA-256, C14N mixta (inclusiva en SignedInfo, exclusiva en Reference), X509Data | Usar `sifen` y verificar el Transform; descartar XAdES |
| 2 | 2026-11-08 | Guia de Mejores Practicas; FAQ e-Kuatia | TLS 1.2 con autenticacion mutua en todos los WS | Certificado disponible por conexion |
| 3 | 2026-11-08 | Guia paso a paso de habilitacion | El 364 se genera despues de las pruebas | Reordenar checklist |
| 4 | 2026-11-12 | DNIT Marangatu; fuentes 2026 | Timbrado sin costo oficial por Marangatu; Gs. 150.000 es gestion privada | No contabilizar como obligatorio |
| 5 | 2026-11-12 | AC Raiz; resoluciones PCSC; mercado 2026 | PCSC VIT, CODE 100, CONFIRMA, Documenta, ITTI, Min. Interior; F1 ~Gs. 350.000 (rango 150.000 a 440.000) | Pedir certificado cualificado F1 |
| 6 | 2026-11-08 | BACN; MIC | Ley 6822/2021 vigente; MIC autoridad | Usar "firma electronica cualificada" |
| 7 | 2026-11-08 | MT V150 seccion 6.2; FAQ | 72 h transmision; 48/168 h cancelacion; 15 dias inutilizacion | Cola y alertas por plazo |
| 8 | 2026-11-12 | MT V150 paginas 148-193; NT 027 | 396 codigos unicos extraidos y versionados en CSV | Construir maquina de estados y mensajes |
| 9 | 2026-11-08 | Pagina de Documentacion Tecnica DNIT | MT V150 + NT 001 a 027; XSD publicados | Fijar baseline y archivar XSD |
| 10 | 2026-11-08 | Guia de Pruebas para e-kuatia | Set y escenarios minimos publicados | Automatizar suite |
| 11 | 2026-11-12 | MT V150; FAQ; RG 23/2019; diseno interno | Maquina interna de 11 estados mapeada a codigos | Modelo de datos y reintentos |

---

## Fuentes oficiales consultadas

- Documentacion tecnica DNIT: https://www.dnit.gov.py/web/e-kuatia/documentacion-tecnica
- Manual Tecnico V150: https://www.dnit.gov.py/documents/20123/420592/Manual+T%C3%A9cnico+Versi%C3%B3n+150.pdf
- Guia de Mejores Practicas: https://www.dnit.gov.py/documents/20123/420592/Gu%C3%ADa+de+Mejores+Pr%C3%A1cticas+para+la+Gesti%C3%B3n+del+Env%C3%ADo+de+DE.pdf
- Guia de Pruebas para e-kuatia: https://www.dnit.gov.py/documents/20123/424160/Guia+de+Pruebas+para+e-kuatia.pdf
- Guia paso a paso de habilitacion: https://www.dnit.gov.py/documents/d/global/guia-paso-a-paso-solicitud-y-habilitacion-de-facturadores-electronicos
- Preguntas frecuentes e-Kuatia: https://www.dnit.gov.py/web/e-kuatia/preguntas-frecuentes
- AC Raiz / MIC: https://www.acraiz.gov.py/html/Certif_1PrestaServ.html
- Ley 6822/2021 (BACN): https://www.bacn.gov.py/leyes-paraguayas/10318/
