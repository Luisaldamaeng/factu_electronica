# Catalogo de codigos de respuesta SIFEN

> **Version:** 1.0
> **Fecha:** 2026-11-12
> **Estado:** Verificado (punto #8 de `puntos de verificacion.md`)
> **Fuente primaria:** DNIT, Manual Tecnico SIFEN V150 (10/09/2019), paginas 148 a 193 del PDF; DNIT, Nota Tecnica NT_E_KUATIA_027 (09/03/2026).
> **Archivo de datos:** [`catalogo de codigos SIFEN.csv`](catalogo%20de%20codigos%20SIFEN.csv) (396 codigos unicos).

---

## 1. Proposito

Servir como referencia versionada para:

- Construir la maquina de estados del DE.
- Definir los mensajes al usuario ante aprobaciones, observaciones y rechazos.
- Automatizar la suite de pruebas de homologacion con los codigos esperados.

El CSV es una extraccion asistida del Manual V150. **El PDF oficial sigue siendo la autoridad**; ante cualquier diferencia, prevalece el manual.

---

## 2. Como se genero

1. Se extrajo el texto de `docs/baseline/Manual_Tecnico_V150.pdf` con `pypdf`.
2. Se parsearon las tablas de las secciones 12.2, 12.3 y 12.4.
3. Se deduplico por codigo y se conservo el registro con estado y observacion mas completos.
4. Se excluyeron las filas de rango de la seccion 12.1 (por ejemplo `0100 AB20`), que no son codigos de respuesta.

Limitaciones conocidas:

- Los mensajes y observaciones pueden conservar espacios o cortes de linea propios de la extraccion del PDF.
- Algunos codigos no traen el estado en la misma fila del PDF y quedan con la columna `estado` vacia.
- La NT 027 **no modifica codigos**: solo ajusta campos del evento de nominacion de factura electronica.

---

## 3. Cobertura

| Grupo | Rango | Cantidad | Seccion del manual |
|---|---|---|---|
| Servicios web (WS) | 0001 a 0650 | 42 | 12.2 y 12.3 |
| Documento Electronico (DE) | 1000 a 2650 | 280 | 12.4 |
| Eventos | 4000 a 4350 | 74 | 12.1.3 y 12.4 |
| **Total** | | **396** | |
---

## 4. Codigos clave para la implementacion

### 4.1 Resultado de recepcion

| Codigo | Validacion | Significado | Estado |
|---|---|---|---|
| 0260 | BC01 | Autorizacion del DE satisfactoria | N (aprobado sincrono) |
| 0300 | BF01 | Lote recibido con exito | A |
| 0301 | BF02 | Lote no encolado para procesamiento | R |
| 0361 | BI02 | Lote en procesamiento | R (reintentar consulta) |
| 0362 | BI03 | Procesamiento de lote concluido | A |
| 0420 | BL01 | CDC inexistente | |
| 0421 | BL02 | CDC encontrado | |
| 0500 | BO01 | RUC inexistente | |
| 0502 | BO03 | Exito en la consulta de RUC | |
| 0600 | BU01 | Evento registrado correctamente | A |

### 4.2 Transporte y disponibilidad (reintentables)

| Codigo | Validacion | Significado | Accion |
|---|---|---|---|
| 0001 | AA01 | Certificado de transmisor invalido | Bloquear y alertar |
| 0002 | AA02 | Plazo de validez del certificado | Renovar certificado |
| 0160 | AE01 | XML malformado | No reintentar; corregir XML |
| 0161 | AE02 | Servidor momentaneamente sin respuesta | Reintentar con backoff |
| 0162 | AE03 | Servidor paralizado sin tiempo de regreso | Reintentar con backoff |
| 0163 | AE04 | Version del formato del WS no soportada | Revisar version del cliente |

### 4.3 Timbrado y numeracion

| Codigo | Validacion | Significado | Accion |
|---|---|---|---|
| 1101 | C004 | Numero de timbrado invalido | Bloquear emision |
| 1103 | C004b | Timbrado no vigente a la fecha de emision | Bloquear emision |
| 1104 | C004c | Timbrado no activo | Bloquear emision |
| 1105 | C005 | Establecimiento incorrecto | Corregir configuracion |
| 1106 | C006 | Punto de expedicion incorrecto | Corregir configuracion |
| 1109 | C007 | Numero de documento ya inutilizado | Reasignar numeracion |
| 1110 | C010 | Serie informada incorrecta | Corregir serie |

### 4.4 Fechas y extemporaneidad

| Codigo | Validacion | Significado | Accion |
|---|---|---|---|
| 1005 | A004b | Transmision extemporanea del DE | Aprobado con observacion (AO); evaluar sancion |
| 1150 | D002 | Emision invalida por retraso (mas de 720 horas) | Rechazo |
| 1151 | D002f | Emision invalida por envio adelantado (mas de 120 horas) | Rechazo |

### 4.5 Eventos

| Codigo | Validacion | Significado |
|---|---|---|
| 4000 | GDE005 | Version del evento no corresponde |
| 4002 | GEC002a | CDC no existente en el SIFEN |
| 4003 | GEC002b | CDC ya tiene el mismo evento solicitado |
| 4006 | GDE008 | Firmador no autorizado para el evento |
| 4051 | GEI002 | Timbrado invalido para ambiente de pruebas |
| 4065 | GEI005 | Existe DTE en el rango informado |
| 4066 | GEI005a | Existe numero inutilizado en el rango |
| 4067 | GEI006 | Cantidad de numeros del rango invalida (maximo 1.000) |
| 4150 | GCO002 | CDC ya cuenta con dos eventos de conformidad |
| 4200 | GDI002 | CDC ya cuenta con un evento de disconformidad |

---

## 5. Columnas del CSV

| Columna | Descripcion |
|---|---|
| `codigo` | Codigo de respuesta de 4 digitos |
| `estado` | Resultado: A (aprobado), AO (aprobado con observacion), R (rechazo), N (no aplica o informativo) |
| `validacion` | ID de la regla de validacion del manual (por ejemplo `C004b`) |
| `mensaje` | Mensaje de la validacion |
| `observacion` | Detalle o condicion de la regla |
| `version` | Version del formato cuando el manual la informa |
| `pagina_pdf` | Pagina del PDF de origen |

---

## 6. Mantenimiento

- Revisar en cada nueva Nota Tecnica si agrega, quita o cambia codigos.
- Registrar la version del manual y de las notas tecnicas usadas.
- Si se regenera el CSV, comparar el total (396) y los codigos clave de la seccion 4.

---

## 7. Trazabilidad del baseline

| Documento | SHA-256 |
|---|---|
| `Manual_Tecnico_V150.pdf` | `976CD88C05C31041EE86DB1667E1B426E2D9DDF675D941973D5918CBDC5427C6` |
| `NT_E_KUATIA_027_MT_V150.pdf` | `3FF6FBBF9F54D938A777C8A98F0B18555AF6B21014E2BC5349C7BFE56E2BB37D` |
