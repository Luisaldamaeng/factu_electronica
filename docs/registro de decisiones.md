# Registro de decisiones

> **Proyecto:** Facturacion Electronica SIFEN (Paraguay)
> **Fase:** Planificacion.
> **Proposito:** dejar trazabilidad de cada decision de alcance, arquitectura y operacion, con su estado y justificacion.

## Convenciones

- **ID:** `ADR-###` (Architecture Decision Record).
- **Estado:** `Propuesta`, `Aceptada`, `Rechazada` o `Reemplazada`.
- **Fecha:** formato `DD-MM-AAAA`.
- Toda decision nueva se agrega al final y, si reemplaza a otra, se actualiza el estado de la anterior.

---

## Tabla resumen

| ID | Fecha | Decision | Estado |
|---|---|---|---|
| ADR-001 | 2026-11-01 | El documento se guarda en `docs/` | Aceptada |
| ADR-002 | 2026-11-01 | El documento incluye investigacion y cuestionario | Aceptada |
| ADR-003 | 2026-11-01 | Separar cuestionario, puntos de verificacion y registro de decisiones en archivos propios | Aceptada |
| ADR-004 | 2026-11-01 | Plataforma multi-tenant con doble uso | Reemplazada por ADR-017 |
| ADR-005 | 2026-11-01 | Stack backend y frontend | Reemplazada por ADR-018 |
| ADR-006 | 2026-11-01 | Despliegue on-premise | Aceptada |
| ADR-007 | 2026-11-01 | Microservicios minimos | Reemplazada por ADR-019 |
| ADR-008 | 2026-11-01 | Una base de datos por tenant | Reemplazada por ADR-017 |
| ADR-009 | 2026-11-01 | Cifrado propio con KMS | Reemplazada por ADR-020 |
| ADR-010 | 2026-11-01 | Custodia de certificados y PIN | Reemplazada por ADR-020 |
| ADR-011 | 2026-11-01 | Onboarding y soporte | Aceptada |
| ADR-012 | 2026-11-01 | Panel primero, API despues | Aceptada |
| ADR-013 | 2026-11-01 | Recorte de alcance del MVP | Reemplazada por ADR-021 |
| ADR-014 | 2026-11-12 | Estandar de firma XMLDSig enveloped | Aceptada (corregida 2026-11-20) |
| ADR-015 | 2026-11-12 | Maquina de estados interna del DE | Aceptada |
| ADR-016 | 2026-11-12 | Catalogo de codigos SIFEN versionado en CSV | Aceptada |
| ADR-017 | 2026-11-20 | Un solo contribuyente y una sola base de datos | Aceptada |
| ADR-018 | 2026-11-20 | Jinja2/HTMX y `sifen` (kmee) | Aceptada |
| ADR-019 | 2026-11-20 | Dos procesos: app y worker | Aceptada |
| ADR-020 | 2026-11-20 | Custodia local cifrada de certificado y PIN | Aceptada |
| ADR-021 | 2026-11-20 | Cronograma de 10 semanas mas 2 de buffer | Aceptada |
| ADR-022 | 2026-11-20 | SifenGateway con adaptadores | Aceptada |

---

## ADR-001 - Ubicacion de la documentacion

- **Fecha:** 2026-11-01
- **Estado:** Aceptada
- **Contexto:** El directorio del proyecto estaba vacio y hacia falta un lugar para los artefactos de planificacion.
- **Decision:** Guardar la documentacion en la carpeta `docs/`.
- **Alternativas consideradas:** dejar los archivos en la raiz del proyecto.
- **Consecuencias:** mejor organizacion y separacion entre documentacion y codigo futuro.
- **Justificacion:** convencion habitual y facilita el crecimiento del proyecto.

## ADR-002 - Contenido del documento inicial

- **Fecha:** 2026-11-01
- **Estado:** Aceptada
- **Contexto:** La investigacion aportaba hallazgos pero tambien muchas decisiones abiertas.
- **Decision:** El documento inicial incluye tanto los hallazgos de la investigacion como el cuestionario de decisiones pendientes.
- **Alternativas consideradas:** un documento solo de requisitos y otro solo de preguntas.
- **Consecuencias:** trazabilidad entre lo que se sabe y lo que falta definir.
- **Justificacion:** evitar que las preguntas queden fuera de contexto.

## ADR-003 - Separacion de artefactos de planificacion

- **Fecha:** 2026-11-01
- **Estado:** Aceptada
- **Contexto:** El documento unico crecia y mezclaba requisitos, verificaciones y decisiones.
- **Decision:** Separar en tres archivos: `cuestionario de preguntas IA.md`, `puntos de verificacion.md` y `registro de decisiones.md`. El documento principal los referencia.
- **Alternativas consideradas:** mantener todo en un solo archivo.
- **Consecuencias:** cada artefacto se edita y revisa por separado; el documento principal queda como indice de requisitos.
- **Justificacion:** facilita el trabajo paralelo y el seguimiento del estado de cada pendiente.

---

## ADR-004 - Plataforma multi-tenant con doble uso

- **Fecha:** 2026-11-01
- **Estado:** Reemplazada
- **Contexto:** El sistema se usara para facturacion propia y para licenciar a terceros.
- **Decision:** Construir una plataforma multi-tenant con aislamiento por cliente.
- **Consecuencias:** se necesita gestion de tenants, roles y credenciales separadas desde el MVP.
- **Reemplazada por:** ADR-017 (2026-11-20).

## ADR-005 - Stack backend y frontend

- **Fecha:** 2026-11-01
- **Estado:** Reemplazada
- **Contexto:** El equipo es una sola persona con experiencia en PHP, Node, Python y React.
- **Decision:** Backend Python y frontend React.
- **Consecuencias:** se usara `pysifen` para la capa SIFEN.
- **Reemplazada por:** ADR-018 (2026-11-20).

## ADR-006 - Despliegue on-premise

- **Fecha:** 2026-11-01
- **Estado:** Aceptada
- **Contexto:** No hay presupuesto de nube definido.
- **Decision:** Desplegar on-premise con Docker Compose sobre Linux.
- **Consecuencias:** la alta disponibilidad real requiere inversion adicional y queda para fase 2.

## ADR-007 - Microservicios minimos

- **Fecha:** 2026-11-01
- **Estado:** Reemplazada
- **Contexto:** Se eligio microservicios, pero hay una sola persona.
- **Decision:** Implementar solo 3 servicios desplegables: `api`, `signer` y `worker`.
- **Alternativas consideradas:** monolito modular.
- **Consecuencias:** se gana aislamiento de la firma sin multiplicar la operacion. No se agregan servicios sin necesidad justificada.
- **Reemplazada por:** ADR-019 (2026-11-20).

## ADR-008 - Una base de datos por tenant

- **Fecha:** 2026-11-01
- **Estado:** Reemplazada
- **Contexto:** Se prioriza el aislamiento de datos.
- **Decision:** Una base PostgreSQL por cliente y una base de administracion.
- **Consecuencias:** las migraciones y los respaldos se ejecutan por cliente. Se revisara en fase 2 si conviene pasar a schema por tenant.
- **Reemplazada por:** ADR-017 (2026-11-20).

## ADR-009 - Cifrado propio con KMS

- **Fecha:** 2026-11-01
- **Estado:** Reemplazada
- **Contexto:** El `.pfx` y el PIN nunca deben guardarse en texto plano.
- **Decision:** Usar HashiCorp Vault self-hosted como KMS y cifrado por tenant.
- **Consecuencias:** el servicio `signer` depende de Vault y debe aislarse por red.
- **Reemplazada por:** ADR-020 (2026-11-20).

## ADR-010 - Custodia de certificados y PIN

- **Fecha:** 2026-11-01
- **Estado:** Reemplazada
- **Contexto:** El cliente no carga sus credenciales en el MVP.
- **Decision:** El administrador carga el `.pfx` y el PIN; la plataforma los custodia cifrados.
- **Consecuencias:** se requieren 2FA, auditoria de accesos y clausulas de responsabilidad en los terminos de servicio.
- **Reemplazada por:** ADR-020 (2026-11-20).

## ADR-011 - Onboarding y soporte

- **Fecha:** 2026-11-01
- **Estado:** Aceptada
- **Contexto:** Una sola persona opera la plataforma.
- **Decision:** Onboarding asistido en el MVP. Soporte por WhatsApp y email, lunes a viernes de 08:00 a 18:00, con SLA de 4 horas habiles y 1 hora para incidentes criticos.
- **Consecuencias:** el self-service queda para fase 2.

## ADR-012 - Panel primero, API despues

- **Fecha:** 2026-11-01
- **Estado:** Aceptada
- **Contexto:** El alcance de 3 meses no permite todo.
- **Decision:** Panel web en el MVP; API publica con webhooks en fase 2.
- **Consecuencias:** se posterga la integracion de terceros.

## ADR-013 - Recorte de alcance del MVP

- **Fecha:** 2026-11-01
- **Estado:** Reemplazada
- **Fecha de aprobacion:** 2026-11-12
- **Contexto:** El alcance "todas" no cabe en 13 semanas con una sola persona.
- **Decision:** MVP con factura, NC/ND, eventos, contingencias, KuDE/QR y reportes; fase 2 para autofactura, remision, retencion y API.
- **Consecuencias:** el MVP queda fijado en 13 semanas; cualquier alta de alcance mueve la fecha.
- **Reemplazada por:** ADR-021 (2026-11-20).

---

## ADR-014 - Estandar de firma XMLDSig enveloped

- **Fecha:** 2026-11-12
- **Estado:** Aceptada (corregida 2026-11-20)
- **Contexto:** La investigacion inicial mencionaba XAdES, pero el Manual Tecnico V150 exige XMLDSig.
- **Decision:** Usar XMLDSig enveloped con `CanonicalizationMethod` inclusiva (`http://www.w3.org/TR/2001/REC-xml-c14n-20010315`) y `Reference/Transform` exclusiva (`http://www.w3.org/2001/10/xml-exc-c14n#`) mas enveloped signature, RSA-SHA256, digest SHA-256, clave RSA 2048 y `KeyInfo` solo con `X509Data`. Ubicar la firma dentro de `rDE`, despues de `DE` y antes de `gCamFuFD`. No implementar XAdES.
- **Alternativas consideradas:** XAdES, firma XMLDSig con otros algoritmos.
- **Consecuencias:** se usa `sifen` (kmee) y se fuerza el `Transform` exclusivo; se valida con un verificador independiente y contra el XML de ejemplo oficial.
- **Correccion 2026-11-20:** la version anterior decia "C14N exclusiva" para todo el proceso. El MT V150 distingue la canonicalizacion de `SignedInfo` (inclusiva) de la transformacion de la referencia (exclusiva).

## ADR-015 - Maquina de estados interna del DE

- **Fecha:** 2026-11-12
- **Estado:** Aceptada
- **Contexto:** SIFEN solo define resultado A/AO/R y los estados aprobado, cancelado e inutilizado; falta el ciclo operativo interno.
- **Decision:** Implementar la maquina de 11 estados documentada en [`maquina de estados del DE.md`](maquina%20de%20estados%20del%20DE.md), mapeada a los codigos del catalogo. La inutilizacion se modela por rango de numeracion.
- **Consecuencias:** se persisten `estado`, `resultado_sifen`, `codigo_sifen`, `intentos_envio`, `proximo_intento`, `fecha_firma` y `fecha_aprobacion`, mas una tabla de transiciones append-only.

## ADR-016 - Catalogo de codigos SIFEN versionado en CSV

- **Fecha:** 2026-11-12
- **Estado:** Aceptada
- **Contexto:** El catalogo de codigos vivia solo en el PDF del Manual V150 y cambiaba por Notas Tecnicas.
- **Decision:** Versionar en el repositorio [`catalogo de codigos SIFEN.csv`](catalogo%20de%20codigos%20SIFEN.csv) con 396 codigos extraidos del Manual V150 y la NT 027, y su resumen en [`catalogo de codigos SIFEN.md`](catalogo%20de%20codigos%20SIFEN.md).
- **Consecuencias:** el PDF sigue siendo la autoridad; el CSV se regenera y compara ante cada nueva Nota Tecnica.

---

## ADR-017 - Un solo contribuyente y una sola base de datos

- **Fecha:** 2026-11-20
- **Estado:** Aceptada
- **Contexto:** El proyecto se usara para facturacion propia de un unico contribuyente (RUC piloto). El licenciamiento a terceros no esta en el alcance.
- **Decision:** Modelar un solo `emisor`, sin `tenant_id`, con una unica base PostgreSQL. Reemplaza ADR-004 y ADR-008.
- **Alternativas consideradas:** multi-tenant con `tenant_id`; una base por cliente.
- **Consecuencias:** migraciones, respaldos y autenticacion mas simples. Las pruebas de aislamiento entre tenants se eliminan. Un futuro multi-tenant requiere una migracion mayor.

## ADR-018 - Jinja2/HTMX y `sifen` (kmee)

- **Fecha:** 2026-11-20
- **Estado:** Aceptada
- **Contexto:** Una sola persona, despliegue on-premise y UI interna simple. React agrega toolchain y un servicio extra.
- **Decision:** Renderizar el panel con Jinja2 + HTMX sobre FastAPI. Usar `sifen` 0.2.0 (kmee) detras de `SifenGateway`. Reemplaza ADR-005.
- **Alternativas consideradas:** React SPA; `pysifen` (josecuev); implementacion propia.
- **Consecuencias:** menos piezas y despliegue mas simple. `sifen` es alpha: hay que aislarlo, fijar la version y cubrirlo con pruebas. No instalar `pysifen` en el mismo entorno.

## ADR-019 - Dos procesos: app y worker

- **Fecha:** 2026-11-20
- **Estado:** Aceptada
- **Contexto:** La firma y la transmision necesitan una cola y reintentos, pero un servicio `signer` separado agrega operacion sin beneficio para un solo cliente.
- **Decision:** Una imagen Docker con dos comandos: `app` (FastAPI/Jinja) y `worker` (cola, firma, transmision, PDF, email). Reemplaza ADR-007.
- **Consecuencias:** el certificado se descifra solo en memoria en el worker; no hay servicio `signer` ni Vault.

## ADR-020 - Custodia local cifrada de certificado y PIN

- **Fecha:** 2026-11-20
- **Estado:** Aceptada
- **Contexto:** Un solo cliente, on-premise y sin Vault. El `.pfx` y el PIN no pueden quedar en texto plano ni en git.
- **Decision:** Guardar el `.pfx` cifrado en `secrets/` y el PIN en un archivo secreto con permisos restringidos. Descifrar solo en memoria al firmar. Reemplaza ADR-009 y ADR-010.
- **Alternativas consideradas:** Vault; KMS de nube; texto plano.
- **Consecuencias:** el respaldo de `secrets/` es critico; se documenta la rotacion de la clave y el acceso. No hay dependencia de Vault.

## ADR-021 - Cronograma de 10 semanas mas 2 de buffer

- **Fecha:** 2026-11-20
- **Estado:** Aceptada
- **Contexto:** El alcance se redujo a un solo contribuyente y el equipo es una persona.
- **Decision:** 10 semanas de desarrollo y 2 semanas de buffer para homologacion y piloto. Reemplaza ADR-013.
- **Consecuencias:** el alcance del MVP queda fijo; cualquier alta mueve la fecha.

## ADR-022 - SifenGateway con adaptadores

- **Fecha:** 2026-11-20
- **Estado:** Aceptada
- **Contexto:** `sifen` (kmee) es alpha y la integracion real depende del acceso a testing. El dominio no debe depender de la libreria.
- **Decision:** Definir el puerto `SifenGateway` en `src/facturacion/modulos/sifen/gateway.py` con implementaciones `KmeeGateway` (real) y `LocalFakeGateway` (pruebas y desarrollo local).
- **Consecuencias:** pruebas de contrato contra ambos adaptadores; ninguna importacion de `pysifen` fuera del adaptador; se puede cambiar de libreria sin tocar el dominio.

---

## Decisiones pendientes de registrar

- Presupuesto de infraestructura.
- Confirmacion del tramite de RUC piloto y Formulario 364.
- Acceso al ambiente de testing y set de datos.
