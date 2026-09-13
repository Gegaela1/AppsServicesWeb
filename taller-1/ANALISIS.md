# ANÁLISIS DEL TALLER

## Resumen

En este primer taller de Integración de datos entre aplicaciones, de la materia Aplicaciones y Servicio Web, se trabajó con información meteorológica proveniente de dos proveedores diferentes. Cada proveedor entregó los datos en formatos distintos, por lo que fue necesario realizar un proceso de transformación y normalización para adaptar toda la información al contrato definido por la API institucional.

## Resultados obtenidos

- Registros procesados: 400
- Registros normalizados: 394
- Errores de normalización: 6
- Registros válidos localmente: 190
- Registros rechazados localmente: 204

## Dificultades encontradas

Durante el desarrollo del taller se encontraron varios registros con información incorrecta o incompleta. Por ello, algunos de los problemas más comunes fueron las fechas inválidas, valores nulos, problemas en coordenadas geográficas, humedades fuera del rango permitido y algunos campos obligatorios vacíos.

Estos errores afectaron el proceso de normalización y validación, por lo que fue necesario implementar controles para detectar los registros que no cumplían con las reglas establecidas y así poder tratarlos.

## Desarrollo de la solución

Para resolver el problema se implementaron funciones que permitieron:

- Leer archivos JSON y CSV.
- Convertir temperaturas de Fahrenheit a Celsius.
- Convertir velocidades del viento de metros por segundo a kilómetros por hora.
- Unificar la estructura de los datos de ambos proveedores.
- Validar las reglas del contrato institucional.
- Identificar registros con errores.
- Generar los archivos de salida solicitados.

## Conclusión

El taller permitió aplicar conceptos relacionados con procesamiento de datos, validaciones y manejo de archivos en Python. Además, fue posible identificar cómo pequeñas diferencias en los formatos de entrada pueden generar problemas de integración y la importancia de validar la información antes de almacenarla o enviarla a un servicio externo.