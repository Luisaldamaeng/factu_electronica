# Checklist del proyecto - Facturacion Electronica SIFEN

> **Version:** 0.2
> **Fecha:** 2026-11-20
> **Base:** [`plan de implementacion.md`](plan%20de%20implementacion.md), [`requesitos de la facturacion electronica.md`](requesitos%20de%20la%20facturacion%20electronica.md), [`puntos de verificacion.md`](puntos%20de%20verificacion.md) y [`registro de decisiones.md`](registro%20de%20decisiones.md).
> **Uso:** marcar cada casilla a medida que se completa.

---

## Fase 0 - Decisiones y cierre de planificacion

- [x] Aprobar el recorte de alcance del MVP (ADR-013, reemplazada por ADR-021)
- [ ] Confirmar presupuesto y servidor on-premise
- [x] Cerrar los 4 puntos parciales de verificacion (2026-11-12):
  - [x] #4 Tasa de timbrado (sin costo oficial por Marangatu)
  - [x] #5 Lista de Confianza y precios de PCSC
  - [x] #8 Tabla completa de codigos de rechazo (396 codigos en CSV)
  - [x] #11 Disenar la maquina de estados interna del DE
- [x] Registrar las decisiones vigentes (ADR-017 a ADR-022):
  - [x] Un solo contribuyente y una sola base de datos
  - [x] Jinja2/HTMX y `sifen` (kmee)
  - [x] Dos procesos: app y worker
  - [x] Custodia local cifrada de certificado y PIN
  - [x] Cronograma de 10 semanas mas 2 de buffer
  - [x] `SifenGateway` con adaptadores
- [x] Corregir la canonicalizacion en ADR-014 y en el punto #1 de verificaciones
- [x] Archivar el baseline (MT V150, NT 001-027, XSD, XML ejemplo, Guia de Pruebas) con checksum
- [x] Iniciar el codigo con el esqueleto del proyecto

---

## Fase 1 - Tramites externos (iniciar en semana 1)

- [x] Preparar la solicitud y el checklist de datos (`solicitud de acceso a testing.md`)
- [ ] Enviar la solicitud de acceso al ambiente de testing por la mesa de ayuda
- [ ] Recibir set de datos de prueba (RUC, timbrado, CSC)
- [ ] Confirmar RUC piloto y certificado cualificado vigente
- [ ] Completar y superar el set de pruebas minimo
- [ ] Generar el Formulario 364 (va **despues** de las pruebas)
- [ ] Contratar dominio, TLS y proveedor de email
- [ ] Encargar TOS y politica de datos al abogado

---

## Fase 2 - MVP (10 + 2 semanas)

- [x] **Semana 1:** baseline, repo, CI, Docker Compose y esqueleto
- [ ] **Semana 2:** modelo fiscal, migracion inicial, timbrados, numeracion y autenticacion
- [ ] **Semana 3:** CDC, constructor XML de factura, validacion XSD y pruebas unitarias
- [ ] **Semana 4:** firma XMLDSig con `sifen`, verificacion independiente y `.pfx`
- [ ] **Semana 5:** gateway, envio a testing, maquina de estados y cola
- [ ] **Semana 6:** contingencias, reintentos, plazos, cancelacion, inutilizacion y conformidad
- [ ] **Semana 7:** nota de credito y nota de debito
- [ ] **Semana 8:** PDF con KuDE y QR, email y enlace WhatsApp `wa.me`
- [ ] **Semana 9:** panel de emision, consulta, estados, descargas y reportes
- [ ] **Semana 10:** pruebas E2E, revision de seguridad y set de homologacion
- [ ] **Semanas 11-12:** buffer, documentacion, manual de operacion, homologacion y piloto

---

## Fase 3 - Homologacion y produccion

- [ ] Correr la suite del set de pruebas sin errores
- [ ] Emitir factura real en produccion con el RUC piloto
- [ ] Aprobar, descargar PDF con KuDE/QR y enviar por email
- [ ] Procesar cancelacion e inutilizacion reales
- [ ] Validar bloqueo por certificado vencido y por timbrado agotado
- [ ] Probar restauracion de respaldo en entorno limpio (menos de 8 horas)
- [ ] Verificar firma XMLDSig y transform exclusivo con un verificador independiente

---

## Fase 4 - Operacion

- [ ] Monitoreo de salud, cola, errores y vencimientos
- [ ] Respaldos diarios cifrados con copia externa
- [ ] Alertas a 30 y 15 dias de vencimiento de certificados
- [ ] Onboarding asistido del contribuyente
- [ ] Revision mensual de nuevas Notas Tecnicas de la DNIT

---

## Criterios de aceptacion del MVP

- [ ] Set de pruebas DNIT completo
- [ ] Un DE se emite en menos de 5 segundos
- [ ] Corte simulado de la DNIT deja DE en cola y se recupera
- [ ] Firma y XML validados localmente antes de transmitir
- [ ] Restauracion de respaldo en menos de 8 horas
