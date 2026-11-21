# Solicitud de acceso al ambiente de testing

> **Version:** 1.0
> **Fecha:** 2026-11-12
> **Objetivo:** iniciar el tramite ante la DNIT para obtener acceso al ambiente de pruebas del SIFEN, recibir el set de datos de prueba y ejecutar la homologacion.
> **Referencia:** [`puntos de verificacion.md`](puntos%20de%20verificacion.md) puntos 3 y 10; [`plan de implementacion.md`](plan%20de%20implementacion.md) seccion 10.

---

## 1. Orden correcto del tramite

1. Solicitar acceso al ambiente de pruebas por la mesa de ayuda.
2. Recibir el set de datos de prueba (RUC, timbrado y CSC generico).
3. Configurar el sistema contra testing y ejecutar las pruebas minimas.
4. Completar el set de homologacion.
5. Recien entonces generar el **Formulario 364** en Marangatu/SGTM.

> El Formulario 364 **no habilita el testing**: se presenta despues de completar las pruebas. No invertir el orden.

---

## 2. Requisitos previos

- [ ] RUC piloto activo y habilitado para facturacion electronica.
- [ ] Certificado cualificado de firma electronica tipo F1 vigente (`.pfx`) y PIN.
- [ ] Correo electronico institucional para la mesa de ayuda.
- [ ] Datos del contribuyente: razon social, RUC con digito verificador, domicilio fiscal.
- [ ] Persona de contacto tecnico con nombre, telefono y correo.
- [ ] Version del sistema o integrador que se va a homologar.
- [ ] Manual Tecnico V150 y Notas Tecnicas descargados (ya archivados en `docs/baseline/`).

---

## 3. Datos que te van a pedir

| Dato | Ejemplo o formato | Estado |
|---|---|---|
| RUC del contribuyente | con digito verificador | |
| Razon social | como figura en la DNIT | |
| Tipo de contribuyente | persona fisica o juridica | |
| Domicilio fiscal | departamento, distrito, ciudad | |
| Correo de contacto | institucional | |
| Telefono | con codigo de area | |
| Nombre del contacto tecnico | responsable de la integracion | |
| Certificado digital | tipo F1, vigencia | |
| Alcance a homologar | factura, NC/ND, eventos | |

---

## 4. Texto sugerido de la solicitud

Asunto: Solicitud de acceso al ambiente de pruebas del SIFEN - [Razon social] - RUC [RUC]

Estimados:

Me dirijo a ustedes para solicitar el acceso al ambiente de pruebas del SIFEN (e-Kuatia) para el contribuyente [Razon social], RUC [RUC con digito verificador].

El objetivo es homologar una solucion propia de facturacion electronica que emitira, firmara y transmitira Documentos Electronicos (DE) y eventos a traves de los servicios web del SIFEN.

Datos del contribuyente:

- Razon social: [Razon social]
- RUC: [RUC]
- Domicilio fiscal: [Departamento, distrito, ciudad]
- Tipo de contribuyente: [Persona fisica / Persona juridica]

Datos de contacto:

- Contacto tecnico: [Nombre y apellido]
- Correo: [Correo]
- Telefono: [Telefono]

Alcance que se desea homologar:

- Factura electronica
- Nota de credito y nota de debito
- Eventos de cancelacion, inutilizacion y conformidad
- Consulta de RUC y consulta de DE

Solicito el set de datos de prueba (RUC, timbrado y CSC generico) y la indicacion de los pasos para ejecutar el set de pruebas minimo.

Quedo atento a sus indicaciones.

Saludos cordiales,
[Nombre]
[Razon social]
[Correo] | [Telefono]

---

## 5. Canales oficiales de contacto

| Canal | Dato |
|---|---|
| Correo | facturacionelectronica@dnit.gov.py |
| Telefono | (021) 729 7000, opcion 2 |
| Horario | Lunes a viernes de 07:30 a 12:00 y de 13:00 a 16:00 |
| Portal | https://www.dnit.gov.py/web/e-kuatia |
| Presencial | Edificio DNIT, Yegros esq. Mcal. Lopez, Asuncion |

> Verificar estos datos en el portal oficial antes de enviar, ya que pueden cambiar.

---

## 6. Seguimiento

| Fecha | Accion | Canal | Respuesta | Estado |
|---|---|---|---|---|
| | Solicitud enviada | | | |
| | Set de datos recibido | | | |
| | Pruebas minimas ejecutadas | | | |
| | Set de homologacion completo | | | |
| | Formulario 364 generado | | | |

---

## 7. Despues de la solicitud

1. Cargar el set de datos de prueba en el entorno de testing.
2. Ejecutar los escenarios minimos de la Guia de Pruebas.
3. Automatizar el set como suite de aceptacion (ver semana 12 del plan).
4. Documentar aprobaciones y rechazos obtenidos.
5. Generar el Formulario 364 y guardar el comprobante.
