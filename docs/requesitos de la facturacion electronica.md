# Requisitos de la Facturacion Electronica (SIFEN - Paraguay)

> **Estado:** borrador de la fase de planificacion. No se ha escrito codigo.
> **Objetivo de esta fase:** pulir el plan y cerrar decisiones antes de disenar o implementar.
> **Fecha:** 2026-11-01
> **Nota 2026-11-20:** las decisiones vigentes estan en `registro de decisiones.md` (ADR-017 a ADR-022). Las menciones a `pysifen`, Vault y multi-tenant son historicas.

---

## 1. Proposito del documento

Servir como base de requisitos para construir una solucion de facturacion electronica integrada al SIFEN de la DNIT (Paraguay). El documento recopila los hallazgos de la investigacion inicial, separa lo que son **supuestos a verificar** de lo que ya esta **confirmado**, y deja registradas las **decisiones pendientes** que deben resolverse antes de redactar el plan definitivo.

La informacion proviene de fuentes secundarias y de repositorios comunitarios. Nada de lo aqui escrito debe tomarse como normativo hasta contrastarlo con el Manual Tecnico vigente y el portal oficial de la DNIT.

---

## 2. Contexto

- El SIFEN (Sistema Integrado de Facturacion Electronica Nacional) es el sistema de la DNIT para la emision de comprobantes electronicos en Paraguay.
- La documentacion oficial (Manual Tecnico, esquemas XSD, ejemplos y set de pruebas) se publica en el portal e-Kuatia.
- El integrador construye el software; el contribuyente sigue siendo el responsable legal y tributario de su habilitacion, su certificado y su timbrado.
- La complejidad tecnica se concentra en tres capas: construccion del XML segun esquema, firmado criptografico y comunicacion SOAP con la DNIT.

---

## 3. Hallazgos de la investigacion

### 3.1 Librerias y herramientas

| Herramienta | Lenguaje | Uso | Notas |
|---|---|---|---|
| `rshk-jsifenlib` (roshkadev) | Java | Consulta de RUC, envio de comprobantes (sincrono y asincrono), manejo de lotes, lectura de certificados `.pfx` | La mas usada en produccion segun las fuentes |
| `pysifen` (roshkadev) | Python | Interaccion con los servicios web del SIFEN | Libreria ligera |
| `factpy-json` (sfabianl) | Python | Transformacion de JSON a XML de factura | Proyecto comunitario |
| `sifen` (Juan804041) | PHP | Adaptador comunitario | Verificar madurez y mantenimiento |

Recursos oficiales:
- Manual Tecnico del SIFEN.
- Esquemas XSD oficiales.
- Ejemplos de referencia publicados por la DNIT.

### 3.2 Capa tecnica de integracion

1. **Construccion del XML:** armar la estructura del Documento Electronico (DE) conforme al esquema oficial vigente.
2. **Firmado digital:** aplicar la firma criptografica sobre el XML. Las librerias abstraen este paso.
3. **Comunicacion:** construir y enviar mensajes SOAP al Web Service del SIFEN.
4. **Autenticacion:** uso del certificado `.pfx` y su PIN. Las fuentes indican autenticacion mutua (mTLS); **verificar por servicio**.
5. **Lotes:** el envio de comprobantes puede ser sincrono o asincrono segun el volumen.

### 3.3 Gestion de certificados `.pfx`

- El certificado nunca debe guardarse en texto plano ni en carpetas publicas.
- Se recomienda almacenarlo en un gestor de secretos (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) o cifrado con una clave maestra.
- El PIN debe cifrarse de forma independiente (ej. AES-256) y no viajar junto al archivo.
- Extraer y persistir la fecha de vencimiento al momento de la carga para disparar alertas.

### 3.4 Firmado aislado en un SaaS

Flujo recomendado por las fuentes:

1. Almacenamiento cifrado previo del `.pfx` en el gestor de secretos y del PIN cifrado con clave maestra.
2. Al emitir un comprobante, descargar el certificado y descifrar el PIN solo en memoria RAM.
3. Generar el XML y firmarlo en memoria.
4. Enviar el XML firmado a la DNIT.
5. Destruir el certificado y el PIN de la memoria de inmediato.
6. Aislar todo por `Tenant ID` para impedir acceso cruzado entre clientes.

### 3.5 Homologacion ante la DNIT (segun las fuentes)

1. Contar con un RUC piloto y un certificado digital real tipo F1 (`.pfx`).
2. Completar el Formulario 364 en Marangatu con el RUC piloto para habilitar el ambiente de testing.
3. Configurar el sistema contra el ambiente de pruebas y transmitir comprobantes por Web Services.
4. Completar y superar el set de pruebas obligatorio (estructura, firmado y comunicacion).
5. Recien despues, cada cliente habilita su propia cuenta en produccion.

### 3.6 Requisitos del cliente final

Cada contribuyente, de forma independiente:

1. Adquiere su certificado digital tipo F1 (`.pfx`) con un proveedor acreditado por el MIC.
2. Gestiona su adhesion al SIFEN en Marangatu.
3. Paga la tasa de timbrado electronico.
4. Carga su `.pfx` y PIN en la plataforma.
5. Mantiene la custodia y responsabilidad legal de sus credenciales.

### 3.7 Ciclo de vida del certificado

- **Vencimiento:** bloquea el firmado y la transmision; el cliente debe renovar y cargar el nuevo archivo.
- **Perdida o compromiso:** el cliente debe solicitar la revocacion ante la entidad emisora y luego cargar un certificado nuevo.
- **Buenas practicas:** alertas a 30 y 15 dias del vencimiento; clausulas de responsabilidad en los terminos de servicio; bloqueo preventivo si el certificado ya vencio.

---

## 4. Puntos a verificar antes de fijarlos en el plan

Los 11 puntos, su prioridad, criterio de cierre e impacto estan detallados en:

- [puntos de verificacion.md](puntos%20de%20verificacion.md)

---

Las 32 preguntas estan separadas para responder de forma individual:

- [cuestionario de preguntas IA.md](cuestionario%20de%20preguntas%20IA.md)

---

## 6. Siguientes pasos

1. Responder el cuestionario de la seccion 5.
2. Verificar los puntos de la seccion 4 contra el portal oficial de la DNIT.
3. Redactar el plan por fases:
   - Descubrimiento y verificacion normativa.
   - Arquitectura y seguridad.
   - MVP funcional.
   - Homologacion en testing.
   - Puesta en produccion.
   - Onboarding de clientes.
   - Operacion y soporte.
4. Aprobar el plan antes de iniciar cualquier desarrollo.

---

## 7. Registro de decisiones

El historial completo de decisiones (ADR) esta separado en:

- [registro de decisiones.md](registro%20de%20decisiones.md)
