# Cuestionario de preguntas IA

> **Proyecto:** Facturacion Electronica SIFEN (Paraguay)
> **Fase:** Planificacion. No se escribe codigo todavia.
> **Uso:** Responder cada pregunta para cerrar el alcance antes de redactar el plan definitivo.
> **Estado:** respondido en su mayoria. Pendientes: 2 (volumen) y 29 (aclaracion).
> **Nota 2026-11-20:** las respuestas sobre multi-tenant y 3 meses quedaron reemplazadas por ADR-017 a ADR-022. Este archivo se conserva como historico.

## Instrucciones

- Responde usando el numero de la pregunta.
- Si no tienes una respuesta, escribe `NO SE` o `DEFINIR CON EL EQUIPO`.
- Si una pregunta no aplica, escribe `NO APLICA`.
- Puedes responder en bloque o dentro de este mismo archivo.

---

## A. Alcance del negocio

### 1. Que construimos
SaaS multi-cliente, sistema de uso propio, o producto para licenciar a terceros?

**Respuesta:ambas cosas, uso propio y para licenciar a terceros 

### 2. Volumen y tipo de clientes
Cuantos clientes esperas y de que tipo (unipersonales, PyME, estudios contables que facturan por varios RUC)?

**Respuesta:**unipersonales, pymes y mas adelante estudios contables que facturan por varios RUC.
### 3. Alcance del MVP
Solo factura electronica, o tambien nota de credito/debito, autofactura, nota de remision, retencion, eventos, consulta de RUC y consulta de DE?

**Respuesta:**todas
### 4. Integracion con Marangatu
Solo SIFEN, o tambien integracion con Marangatu (declaraciones, libro de compras y ventas)?

**Respuesta:**sifen, no se contempla Marangatu en principio.

### 5. Modelo comercial
Suscripcion, por documento, freemium? Hay cliente ancla o fecha limite?

**Respuesta:**suscripcion

### 6. Diferenciador
Cual es el diferenciador frente a los sistemas existentes?

**Respuesta:**que sea realmente sencillo de usar.

---

## B. Stack y equipo

### 7. Lenguaje y stack
Lenguaje y stack preferido (Java, Python, Node/TS, .NET, PHP)? Frontend?

**Respuesta:**python y react

### 8. Equipo y experiencia
Cuantas personas desarrollan y que experiencia tienen con SOAP, XML y criptografia?

**Respuesta:**yo solo, con experiencia en php y algo de node,  python , react, si en la logica, formulas, etc, 

### 9. Infraestructura
 on-premise
**Respuesta:**

### 10. Estilo de arquitectura
Monolito modular o microservicios? Estas abierto a un servicio separado solo para firma?

**Respuesta:**micro servicios

---

## C. Arquitectura y seguridad

### 11. Multi-tenancy
Una BD con `tenant_id`, un schema por cliente, o una BD por cliente?

**Respuesta:**una base de datos por cliente

### 12. Gestion de secretos
Donde guardas los `.pfx` y los PIN: AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, o cifrado propio con KMS?

**Respuesta:*cifrado propio con KMS*

### 13. Carga de certificados
El cliente sube su `.pfx` y PIN por panel, o los carga un admin manualmente? Aceptas la responsabilidad de custodiar el PIN?

**Respuesta:*los carga un admin manualmente Aceptas la responsabilidad de custodiar el PIN*

### 14. Auditoria y datos personales
Requisitos de auditoria, logs inmutables y retencion de datos? Te aplica la ley de proteccion de datos personales de Paraguay?

**Respuesta:** Basico: logs operativos con retencion de 12 meses. Sin inmutabilidad estricta. Se revisara el alcance de la ley de proteccion de datos personales en el plan.

### 15. Disponibilidad y respaldo
Necesitas alta disponibilidad, backups y objetivos RPO/RTO definidos?

**Respuesta:*Si Necesito alta disponibilidad, backups y objetivos RPO/RTO definidos*

### 16. Terminos de servicio
Quien redacta los terminos de servicio y las clausulas de responsabilidad sobre certificados vencidos?

**Respuesta:*yo, pero bajo supervision de abogado.  *

---

## D. Flujo funcional

### 17. Canal de emision
Emision manual desde una UI, via API para integracion de terceros, o ambas? Hay POS o e-commerce que deba consumirla?

**Respuesta:*ambas*

### 18. Contingencia
Que pasa si la DNIT esta caida: modo contingencia, cola de reintentos, plazos legales de envio?

**Respuesta:*Si, modo contingencia, cola de reintentos, plazos legales de envio*

### 19. Timbrados y numeracion
Quien administra timbrados, establecimientos, puntos de expedicion y numeracion? Necesitas alertas de agotamiento de rangos?

**Respuesta:**Yo mismo, establecimientos, puntos de expedicion y numeracion. Si necesito alertas de agotamiento de rangos.

### 20. Rechazos
Politica ante rechazos: reproceso automatico, correccion manual, maquina de estados clara?

**Respuesta:**reprocesos automaticos en lo posible, correciones manuales en lo posible, maquina de estados clara.   *

### 21. Eventos del ciclo de vida
Cancelacion, inutilizacion, conformidad del receptor, recordatorios de plazos?

**Respuesta:**SI, cancelacion, inutilizacion, conformidad del receptor, recordatorios de plazos. 

### 22. Representacion grafica
Necesitas PDF con KuDE y QR? Envio por email o WhatsApp al receptor?

**Respuesta:**necesito que tenga KuDE y QR. Envio por email o WhatsApp al receptor.   *

### 23. Reportes
Reportes y exportaciones para el contador (CSV/Excel, resumenes mensuales)?

**Respuesta:* CSV/Excel, resumenes mensuales?   *

### 24. API publica
API publica con webhooks y documentacion, o solo panel web?

**Respuesta:** Panel web en el MVP. API publica con webhooks y documentacion en fase 2.

---

## E. Operacion y datos

### 25. Base de datos e internacionalizacion
Motor de base de datos preferido y necesidad de multi-pais o multi-moneda a futuro?

**Respuesta:**postgres      

### 26. Moneda e impuestos
Solo guaranies? Manejas IVA 10/5, exentas, retenciones y redondeos?

**Respuesta:**guaranies, iva 10 y 5, exentas, retenciones, redondeo.     

### 27. Onboarding
Onboarding self-service o asistido? Que datos minimos pides al cliente?
Es cuando el cliente se registra y completa solo todo el alta en la plataforma, sin que tu intervengas: crea su cuenta, carga sus datos fiscales, sube su .pfx y PIN, configura timbrado y empieza a facturar guiado por el panel y mensajes automaticos.
Lo opuesto es el onboarding asistido, donde tu equipo hace la carga y validacion por el cliente (o lo acompana paso a paso).

**Respuesta:** Asistido en el MVP: el administrador carga los datos fiscales y el certificado. El self-service queda para una fase posterior.

### 28. Soporte
Canal, horario y SLA?
- Canal: por donde te contactan (WhatsApp, email, telefono, chat en el panel, ticket).
- Horario: cuando atiendes (24/7, lun-vie 8:00-18:00, solo dias habiles).
- SLA: el compromiso de tiempo de respuesta y resolucion (ej. respuesta en 4 horas habiles, incidentes criticos en 1 hora).
Ejemplo de respuesta: "Soporte por WhatsApp y email, lunes a viernes de 08:00 a 18:00; SLA de 4 horas para respuesta y 24 horas para incidentes criticos."
**Respuesta:** WhatsApp y email, lunes a viernes de 08:00 a 18:00. SLA de 4 horas habiles para respuesta y 1 hora para incidentes criticos.

### 29. Validacion previa
Como validas antes de produccion: ya tienes RUC piloto, certificado `.pfx` real y acceso al ambiente de testing?

**Respuesta:** todavia ,prueba en forma local.El ruc es el mio propio y el certificado tambien

---

## F. Entregables del plan

### 30. Formato del plan
Documento markdown con fases, estimaciones, riesgos y backlog?

**Respuesta:**Documento markdown con fases, estimaciones, riesgos y backlog

### 31. Horizonte y hitos
Horizonte de tiempo y hitos que tienes en mente (MVP en X semanas)?

**Respuesta:**3 meses

### 32. Presupuesto
Presupuesto para infraestructura, gestor de secretos y certificados de prueba?

**Respuesta:** Sin definir aun. Se estimara en el plan.

---

## Resumen de respuestas (opcional)

| # | Respuesta corta |
|---|---|
| 1 | |
| 2 | |
| 3 | |
| 4 | |cual sera
| 5 | |
| 6 | |
| 7 | |
| 8 | |
| 9 | |
| 10 | |
| 11 | |
| 12 | |
| 13 | |
| 14 | |
| 15 | |
| 16 | |
| 17 | |
| 18 | |
| 19 | |
| 20 | |
| 21 | |
| 22 | |
| 23 | |
| 24 | |
| 25 | |
| 26 | |
| 27 | |
| 28 | |
| 29 | |
| 30 | |
| 31 | |
| 32 | |
