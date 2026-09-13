# Taller 1 - Integración de datos entre aplicaciones

## Objetivo

Desarrollar un cliente integrador capaz de leer datos meteorológicos desde diferentes fuentes, normalizarlos, validarlos localmente y enviarlos a una API institucional.

## Tecnologías utilizadas

- Python 3
- json
- csv
- requests
- pytest

## Estructura del proyecto

taller-1/
├── datos/
│   ├── proveedor_a.json
│   └── proveedor_b.csv
├── salida/
│   ├── normalizadas.json
│   └── reporte.json
├── tests/
│   └── test_integrador.py
├── ANALISIS.md
└── integrador.py

## Funcionalidades implementadas

- Lectura de archivos JSON y CSV.
- Normalización de datos.
- Conversión de unidades.
- Validación local.
- Generación de reportes.
- Integración con API institucional.
- Consulta de registros mediante GET.
- Pruebas automatizadas con pytest.

## Ejecución

py integrador.py
