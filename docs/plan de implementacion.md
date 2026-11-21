# Plan de implementacion - Facturacion Electronica SIFEN

> **Version:** 0.3 (un solo contribuyente)
> **Fecha:** 2026-11-20
> **Fase:** Implementacion. Fase 0 documental cerrada.
> **Base:** [`requesitos de la facturacion electronica.md`](requesitos%20de%20la%20facturacion%20electronica.md), [`puntos de verificacion.md`](puntos%20de%20verificacion.md), [`registro de decisiones.md`](registro%20de%20decisiones.md) y [`checklist.md`](checklist.md).

---

## 1. Resumen ejecutivo

Se construye una aplicacion de facturacion electronica para un solo contribuyente
(el RUC piloto), integrada a los web services del SIFEN. El backend es Python 3.12
con FastAPI, el panel usa Jinja2 y HTMX, la base es PostgreSQL y el despliegue es
on-premise con Docker Compose.

La capa SIFEN se apoya en `sifen` 0.2.0 (kmee), aislada detras de un `SifenGateway`
para poder probar en local y cambiar de implementacion sin tocar el dominio.
La firma es XMLDSig enveloped con `CanonicalizationMethod` inclusiva y
`Reference/Transform` exclusiva.

El MVP se planifica en **10 semanas de desarrollo mas 2 de buffer**. El camino
critico externo sigue siendo el acceso al ambiente de testing, el set de datos y
el certificado cualificado vigente. Sin eso no hay homologacion.

---

## 2. Objetivos

1. Emitir Documentos Electronicos (DE) validos ante el SIFEN.
2. Firmar y transmitir de forma segura con el certificado del contribuyente.
3. Operar en contingencia cuando la DNIT no responde.
4. Dar una experiencia simple: emitir, consultar, descargar y enviar comprobantes.
5. Completar la homologacion y pasar a produccion con el RUC piloto.

---

## 3. Alcance

### 3.1 Incluido en el MVP (10 + 2 semanas)

- Configuracion fiscal: RUC, establecimientos, puntos de expedicion, timbrados,
  tipos de documento y numeracion.
- Factura electronica.
- Nota de credito y nota de debito.
- Consulta de RUC y consulta de DE.
- Eventos: cancelacion, inutilizacion y conformidad del receptor.
- Firma digital y transmision a testing y produccion.
- Maquina de estados del DE con reproceso automatico y correccion manual.
- Contingencia con cola de reintentos y alertas por plazo.
- PDF con KuDE y QR.
- Envio por email y enlace de WhatsApp `wa.me`.
- Reportes basicos y exportacion CSV/Excel.
- Panel de configuracion fiscal, certificados y alertas de vencimiento.
- Logs operativos con retencion de 12 meses.

### 3.2 Fase 2 (post-MVP)

- Autofactura.
- Nota de remision.
- Retencion.
- API publica con webhooks y documentacion.
- WhatsApp via API oficial.
- Onboarding self-service.
- Alta disponibilidad real.
- Multi-pais y multi-moneda.

### 3.3 Fuera de alcance

- Integracion con Marangatu.
- Contabilidad completa.
- Gestion de stock o POS.
- Multi-tenant y licenciamiento a terceros en el MVP.
- XAdES.

---

## 4. Supuestos y restricciones

| Tema | Supuesto |
|---|---|
| Equipo | 1 desarrollador a tiempo completo, con apoyo puntual de abogado y contador. |
| Plazo | 10 semanas de desarrollo mas 2 de buffer. |
| Infraestructura | On-premise, Linux con Docker Compose. |
| Clientes | Un solo contribuyente: el RUC piloto. |
| Certificados | Certificado cualificado tipo F1 vigente, custodiado cifrado en `secrets/`. |
| RUC piloto | Pendiente de habilitacion como facturador electronico. |
| Testing | Solicitar acceso en la semana 1; el Formulario 364 va despues de las pruebas. |
| Presupuesto | Pendiente de confirmacion. |
| Internet | Salida estable hacia la DNIT y enlace de respaldo. |

---

## 5. Arquitectura

### 5.1 Vista general

```
[Navegador] -> [Caddy TLS] -> [app FastAPI + Jinja/HTMX] -> [PostgreSQL]
                                      |
                                   [worker] -> [SIFEN]
```

- **app:** panel, autenticacion, configuracion fiscal, documentos y consultas.
- **worker:** cola, firma, transmision, reintentos, PDF y email.
- **PostgreSQL:** una sola base y cola con `SKIP LOCKED`.
- **Sin Vault y sin servicio `signer`:** la firma ocurre en el worker con el
  certificado descifrado solo en memoria.

### 5.2 Decisiones tecnicas

| Componente | Eleccion | Motivo |
|---|---|---|
| Backend | Python 3.12 + FastAPI | Stack elegido; velocidad de desarrollo. |
| Frontend | Jinja2 + HTMX | Menos piezas que una SPA y suficiente para el panel. |
| SIFEN | `sifen` 0.2.0 (kmee) detras de `SifenGateway` | Cubre bindings, firma y transporte; se aisla por ser alpha. |
| Firma | XMLDSig enveloped: RSA-SHA256, SHA-256, `CanonicalizationMethod` inclusiva y `Reference/Transform` exclusiva | MT V150 y Guia de Mejores Practicas. No se usa XAdES. |
| Baseline | Manual Tecnico V150 + NT 001 a 027 | Version oficial vigente. |
| Base de datos | PostgreSQL | Transacciones y cola con `SKIP LOCKED`. |
| Secretos | `.pfx` cifrado y PIN en archivo secreto local | Sin Vault; el secreto nunca entra a git. |
| Despliegue | Docker Compose on-premise | Simple para una persona. |
| TLS | Caddy como reverse proxy | TLS hacia el panel y mTLS hacia la DNIT. |

### 5.3 Modelo de datos

Una sola base, sin `tenant_id`:

- `emisor`
- `establecimiento`
- `punto_expedicion`
- `timbrado`
- `timbrado_tipo_documento`
- `secuencia`
- `documento`
- `documento_transicion`
- `evento`
- `rango_inutilizado`

La numeracion se reserva con bloqueo de fila y no se reutiliza si un DE termina
en error de firma. La inutilizacion se modela por rango, no como estado del DE.

### 5.4 Seguridad

1. `.pfx` cifrado en `secrets/`; PIN en archivo secreto con permisos restringidos.
2. Descifrado solo en memoria al firmar; limpieza de buffers.
3. RBAC simple: administrador, emisor y consulta.
4. TLS en el panel y mTLS hacia la DNIT.
5. Auditoria de accesos, firma y transmision.
6. Respaldos cifrados y fuera del servidor principal.
7. Bloqueo de emision si el certificado esta vencido o el timbrado agotado.

### 5.5 Infraestructura on-premise

- Servidor Linux con Docker.
- UPS y disco de respaldo.
- Respaldos diarios de PostgreSQL y de `secrets/`, con copia externa.
- Monitoreo de salud, cola, errores y vencimientos.
- RPO objetivo: 24 horas. RTO objetivo: 8 horas.
- Alta disponibilidad real queda para fase 2.

### 5.6 Integraciones externas

- Web Services del SIFEN (testing y produccion).
- SMTP para email.
- WhatsApp: enlace `wa.me` en el MVP.
- DNIT: consulta de RUC y consulta de DE.

---

## 6. Fases y cronograma (10 + 2 semanas)

| Semana | Fase | Entregable |
|---|---|---|
| 1 | Baseline y fundaciones | Baseline archivado; solicitud de testing enviada; repo, CI y Docker listos. |
| 2 | Dominio fiscal | Modelo de datos, migracion inicial, timbrados, numeracion y autenticacion simple. |
| 3 | Documento Electronico | CDC, constructor XML de factura, validacion XSD y pruebas unitarias. |
| 4 | Firma | XMLDSig enveloped con `sifen`, verificacion independiente y manejo del `.pfx`. |
| 5 | Transmision | Gateway, envio a testing, maquina de estados y cola. |
| 6 | Eventos y contingencia | Reintentos, plazos, cancelacion, inutilizacion y conformidad. |
| 7 | Notas | Nota de credito y nota de debito. |
| 8 | Representacion | KuDE/QR en PDF, email y enlace de WhatsApp. |
| 9 | Panel y reportes | Emision, consulta, estados, descargas y exportacion CSV/Excel. |
| 10 | Calidad | Pruebas E2E, revision de seguridad y set de homologacion. |
| 11-12 | Buffer y cierre | Homologacion, documentacion, manual de operacion y piloto controlado. |

---

## 7. Backlog priorizado

### 7.1 MVP

| Prioridad | Historia | Criterio de aceptacion |
|---|---|---|
| P0 | Autenticacion y roles | Un usuario accede solo con su rol. |
| P0 | Configuracion fiscal | Se registran RUC, establecimientos y puntos de expedicion. |
| P0 | Timbrado y numeracion | Se controla el rango y se alerta el agotamiento. |
| P0 | Carga cifrada de certificado | El `.pfx` y el PIN quedan cifrados y auditados. |
| P0 | Emision de factura | El DE se genera, valida contra XSD y se firma. |
| P0 | Envio al SIFEN | Se obtiene aprobacion o rechazo en testing. |
| P0 | Maquina de estados | Todo DE tiene estado y transiciones validas. |
| P0 | Contingencia | Si la DNIT falla, el DE queda en cola y se reintenta. |
| P1 | Nota de credito y debito | Se emiten y asocian al DE original. |
| P1 | Eventos | Cancelacion, inutilizacion y conformidad funcionan. |
| P1 | PDF KuDE y QR | El PDF incluye los datos legales y el QR correcto. |
| P1 | Envio al receptor | Email con PDF y enlace de WhatsApp. |
| P1 | Reportes | Exportacion CSV/Excel y resumen mensual. |
| P2 | Alertas de vencimiento | Avisos a 30 y 15 dias. |

### 7.2 Fase 2

Autofactura, nota de remision, retencion, API publica, webhooks, WhatsApp API,
self-service, alta disponibilidad y multi-pais. El multi-tenant se evalua solo si
aparece un caso de licenciamiento.

---

## 8. Requisitos no funcionales

| Categoria | Requisito |
|---|---|
| Rendimiento | Emision de un DE en menos de 5 segundos en condiciones normales. |
| Disponibilidad | 99% mensual en el MVP; alta disponibilidad en fase 2. |
| Seguridad | Cifrado en transito y en reposo; secretos fuera del codigo. |
| Auditoria | Log de operaciones con 12 meses de retencion. |
| Respaldos | Diarios, cifrados y con copia externa. |
| Observabilidad | Salud de servicios, cola, errores y vencimientos. |
| Usabilidad | Un usuario nuevo emite su primera factura sin capacitacion extensa. |

---

## 9. Riesgos y mitigaciones

| Riesgo | Prob. | Impacto | Mitigacion |
|---|---|---|---|
| Alcance total en 10 semanas con 1 persona | Alta | Alto | Alcance fijo, revision semanal y buffer de 2 semanas. |
| Cambios normativos por nuevas Notas Tecnicas | Media | Medio | Baseline fijo; revision mensual del portal de la DNIT. |
| Demora del RUC piloto o del Formulario 364 | Media | Alto | Iniciar el tramite el primer dia; trabajar con mocks. |
| Perdida o vencimiento del certificado | Media | Alto | Alertas, bloqueo preventivo y respaldo cifrado. |
| Custodia del PIN y responsabilidad legal | Media | Alto | TOS con abogado, 2FA, auditoria y cifrado. |
| Falla del servidor on-premise | Media | Alto | UPS, respaldos externos y restauracion probada. |
| `sifen` alpha con cambios incompatibles | Media | Medio | Version fijada y `SifenGateway` con pruebas de contrato. |
| Mock local distinto del SIFEN real | Media | Medio | Corte vertical temprano contra testing. |
| Rechazos del SIFEN sin catalogo claro | Media | Medio | Catalogo CSV versionado y pruebas automatizadas. |

---

## 10. Dependencias y camino critico

1. RUC piloto habilitado.
2. Formulario 364 completado en Marangatu.
3. Certificado digital real vigente.
4. Set de pruebas obligatorio descargado.
5. Manual Tecnico y XSD de la version vigente.
6. Acceso al ambiente de testing.
7. Proveedor de email y dominio.
8. Abogado para los terminos de servicio.

Sin los puntos 1 a 6 no hay homologacion y, por lo tanto, no hay produccion.

---

## 11. Criterios de aceptacion del MVP

1. El set de pruebas de la DNIT se completa sin errores.
2. Se emite una factura real en produccion con el RUC piloto.
3. La factura se aprueba, se descarga en PDF con KuDE y QR y se envia por email.
4. Un evento de cancelacion y uno de inutilizacion se procesan correctamente.
5. Un corte simulado de la DNIT deja los DE en cola y se envian al restablecerse.
6. Un certificado vencido bloquea la emision y genera alerta.
7. El respaldo se restaura en un entorno limpio en menos de 8 horas.

---

## 12. Presupuesto estimado

| Concepto | Tipo | Estimacion |
|---|---|---|
| Servidor on-premise | Unico | Equipo existente o USD 800 a 1.500. |
| UPS y disco de respaldo | Unico | USD 150 a 300. |
| Internet y electricidad | Mensual | Segun el local. |
| Certificado digital | Anual | Gs. 150.000 a 440.000; referencia Gs. 350.000 para F1. |
| Timbrado electronico | Unica | Sin costo oficial por Marangatu. |
| Dominio y TLS | Anual | `.com.py` Gs. 150.000 a 160.000; `.com` USD 10 a 15; TLS sin costo. |
| Email transaccional | Mensual | USD 0 a 20. |
| WhatsApp API | Mensual | Fase 2, segun proveedor. |

El presupuesto queda pendiente de confirmacion.

---

## 13. Equipo y capacidad

- 1 desarrollador full-time (backend, frontend, infraestructura y pruebas).
- Abogado part-time para terminos de servicio y proteccion de datos.
- Contador o asesor tributario para validar reglas de IVA y redondeos.
- El cliente piloto para pruebas de aceptacion.

Con una sola persona, la capacidad de imprevistos es baja: por eso el plan reserva
2 semanas de buffer.

---

## 14. Proximos pasos

1. ~~Cerrar la Fase 0 documental.~~ Cerrada el 2026-11-20 (ADR-017 a ADR-022).
2. Implementar el modelo fiscal y la migracion inicial (en curso).
3. Solicitar acceso al ambiente de testing y ejecutar el set de pruebas.
4. Confirmar el presupuesto y el servidor on-premise.
5. Homologar y pasar a produccion con el RUC piloto.

---

## 15. Anexos

- Requisitos: [`requesitos de la facturacion electronica.md`](requesitos%20de%20la%20facturacion%20electronica.md)
- Verificaciones: [`puntos de verificacion.md`](puntos%20de%20verificacion.md)
- Decisiones: [`registro de decisiones.md`](registro%20de%20decisiones.md)
- Maquina de estados: [`maquina de estados del DE.md`](maquina%20de%20estados%20del%20DE.md)
- Checklist: [`checklist.md`](checklist.md)
