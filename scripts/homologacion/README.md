# Set de homologacion

Espacio para automatizar la Guia de Pruebas de e-Kuatia.

## Orden

1. Solicitar acceso al ambiente de testing.
2. Cargar el set de datos de prueba: RUC, timbrado y CSC.
3. Ejecutar los escenarios minimos contra `sifen-test.set.gov.py`.
4. Generar el Formulario 364 despues de completar las pruebas.

## Pendiente

- Descargar la Guia de Pruebas vigente desde `docs/baseline/`.
- Implementar el runner de escenarios en `set_pruebas.py`.
- Guardar las respuestas del SIFEN como evidencia.
