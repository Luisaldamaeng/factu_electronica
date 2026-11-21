# Baseline normativo SIFEN

> **Version del baseline:** 1.0
> **Fecha de archivo:** 2026-11-12
> **Estado:** Archivado y verificado
> **Inventario completo con hashes:** [`inventario.csv`](inventario.csv)

---

## 1. Que contiene este baseline

Conjunto congelado de recursos oficiales contra los cuales se implementara y homologara el proyecto:

| Grupo | Cantidad | Ubicacion |
|---|---|---|
| Manual Tecnico V150 | 1 | `Manual_Tecnico_V150.pdf` |
| Notas Tecnicas NT 001 a 027 | 27 | `nt/` |
| Esquemas XSD oficiales | 47 | `xsd/oficial/` |
| XML de ejemplo de DE | 1 | `xml_ejemplo/Extructura xml_DE.xml` |
| Bosquejo de estructura XSD | 1 | `xsd/Estructura_DE xsd.xml` |
| Guia de Mejores Practicas | 1 | `Guia_Mejores_Practicas.pdf` |
| Guia de Pruebas e-kuatia | 1 | `Guia_de_Pruebas_e-kuatia.pdf` |
| Listado Checksum MD5 | 1 | `Checksum_MD5_Manuales.pdf` |
| Contenedores originales | 2 | `Estructura_DE_xsd.rar`, `Estructura_xml_DE.rar` |
| **Total recursos** | **82 archivos** | **15,33 MB** |

> Ademas de los 82 recursos, la carpeta contiene 2 archivos de control: `BASELINE.md` (este documento) e `inventario.csv`.

---

## 2. Fuentes oficiales

| Recurso | Origen | Fecha de descarga |
|---|---|---|
| Manual Tecnico V150 | `https://www.dnit.gov.py/documents/20123/420592/Manual+Tecnico+Version+150.pdf` | 2026-11-12 |
| Notas Tecnicas 001 a 027 | `https://www.dnit.gov.py/web/e-kuatia/documentacion-tecnica` | 2026-11-12 |
| Esquemas XSD | `http://ekuatia.set.gov.py/sifen/xsd` | 2026-11-12 |
| Guia de Mejores Practicas | Documentacion Tecnica DNIT | ya archivada |
| Guia de Pruebas e-kuatia | Documentacion Tecnica DNIT | ya archivada |
| XML de ejemplo y bosquejo XSD | `.rar` publicados por la DNIT | ya archivados |

---

## 3. Documentos principales y hashes

| Archivo | Version | MD5 | SHA-256 |
|---|---|---|---|
| `Manual_Tecnico_V150.pdf` | 150 (10/09/2019) | `F48D7C820A14723EC14E66BFCB02E0DF` | `976CD88C05C31041EE86DB1667E1B426E2D9DDF675D941973D5918CBDC5427C6` |
| `nt/NT_E_KUATIA_027_MT_V150.pdf` | 027 (09/03/2026) | `4431FBE48F761A4CDEABA450BAAF3419` | `3FF6FBBF9F54D938A777C8A98F0B18555AF6B21014E2BC5349C7BFE56E2BB37D` |
| `Guia_Mejores_Practicas.pdf` | octubre 2024 | `3DD69A25F391015B70DB988CD97659C5` | `6AA46DA4AFFDF94AAE56C558537E4FDE0FC3A26A532D6CA7EB633F7E17412313` |
| `Guia_de_Pruebas_e-kuatia.pdf` | 2026 | `173620BDF7B6824072E9ACD89A6E3ED2` | `34A6823F28690CBA8D45F8C7E5D7C7625F219E627A73A83479D9487CA0D722C9` |
| `xml_ejemplo/Extructura xml_DE.xml` | 150 | `C40014FB6AFA05E99D3BB12438ADA72D` | `A08C679EE06142CAF729A00DC5E11F6DD42781FF26DEBEB964D06EE545E0FC17` |
| `xsd/Estructura_DE xsd.xml` | 2018-02-07 | `8EA6A6BBE767AA9DD732867DDC31B130` | `60054E0F6B47DAFA4268506BD25DC6FC8539767CAECD4E6AFA2C1F8BB3762754` |

El resto de los 82 archivos esta en [`inventario.csv`](inventario.csv).

---

## 4. Hallazgo sobre el checksum del Manual

El PDF `Checksum_MD5_Manuales.pdf` publica:

| Archivo oficial | MD5 |
|---|---|
| `MT_E_Kuatia_V141_21_09_2018.pdf` | `3831B120BBDAD67AB032DA80DDED689B` |
| `MT_E_Kuatia_V150_10_09_2019.pdf` | `25EB165A8506EFA3A255B863ABCCAE95` |

El archivo local `Manual_Tecnico_V150.pdf` tiene MD5 `F48D7C820A14723EC14E66BFCB02E0DF`, que **no coincide** con `25EB...`.

Verificacion realizada el 2026-11-12:

- Se descargo nuevamente el PDF desde la URL oficial de la DNIT.
- El archivo descargado tiene el **mismo MD5** `F48D7C...` que el archivo local.
- Conclusion: la DNIT reemplazo el PDF publicado sin cambiar el nombre ni la version. El checksum del listado corresponde a la version original de 2019; el archivo servido hoy es distinto a nivel de bytes.

**Decision:** se conserva el archivo servido actualmente y se registra la discrepancia. No se usa el listado MD5 como unica fuente de verdad. Ante una auditoria, presentar ambos hashes y la fecha de descarga.

---

## 5. Hallazgo sobre el XSD

El contenedor `Estructura_DE_xsd.rar` (2018-02-07) contiene `Estructura_DE xsd.xml`, que es un **bosquejo de estructura** con nombres de elementos que no coinciden con el XML de ejemplo V150 (por ejemplo `gCiODE`, `gDTim`, `gCamOC` en lugar de `gOpeDE`, `gTimb`, `gDatGralOpe`).

Por eso:

- No se usa `xsd/Estructura_DE xsd.xml` para validar.
- Se descargaron los **47 XSD oficiales** desde `http://ekuatia.set.gov.py/sifen/xsd` a `xsd/oficial/`.
- Para V150 se usan `DE_v150.xsd`, `DE_Types_v150.xsd`, `siRecepDE_v150.xsd`, `Evento_v150.xsd`, `Evento_Types_v150.xsd` y los demas `*_v150`.
- El XML de ejemplo referencia `siRecepDE_v150.xsd`, que ya esta archivado.

---

## 6. Notas Tecnicas

Se descargaron las 27 Notas Tecnicas (NT 001 a NT 027) desde la pagina de Documentacion Tecnica. Nombres con espacios o sufijos especiales:

- `NT_E_KUATIA_006_MT_V150 .pdf`
- `NT_E_KUATIA_014_MT_V150X.pdf`
- `NT_E_KUATIA_018_MT_V150- Junio.pdf`
- `NT_E_KUATIA_021_MT_V150 30.12.24.pdf`

Se conservan con el nombre publicado para mantener la trazabilidad.

---

## 7. Como actualizar el baseline

1. Revisar mensualmente `https://www.dnit.gov.py/web/e-kuatia/documentacion-tecnica`.
2. Si aparece una Nota Tecnica nueva, descargarla a `nt/`.
3. Si cambia el Manual, descargar el nuevo PDF, calcular hashes y registrar la version.
4. Si cambian los XSD, volver a descargar `http://ekuatia.set.gov.py/sifen/xsd`.
5. Regenerar `inventario.csv` con MD5 y SHA-256.
6. Registrar el cambio en este documento y en `puntos de verificacion.md`.
7. Comparar el catalogo de codigos (`catalogo de codigos SIFEN.csv`) contra la nueva Nota Tecnica.

---

## 8. Regla de uso

- El PDF del Manual y los XSD oficiales son la autoridad.
- El CSV de codigos y la maquina de estados son documentos derivados; ante conflicto, prevalece el PDF.
- No se valida contra el bosquejo 2018.
- No se homologa contra una version distinta a la registrada en este baseline sin actualizar el documento.
