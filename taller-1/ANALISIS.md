# ANÁLISIS DEL TALLER 1

## 1. ¿Qué diferencias encontró entre los contratos de los proveedores?

Una de las diferencias más notables, es cómo cada proveedor entregaba la información. El proveedor A entrega los datos en formato JSON y utiliza una estructura anidada, mientras que el proveedor B trabaja con un archivo CSV y almacena toda la información en filas y columnas.

También se encontraron diferencias en los nombres de los campos y en las unidades de medida. Por ejemplo, el proveedor A maneja la temperatura en grados Fahrenheit y la velocidad del viento en metros por segundo, mientras que el proveedor B utilizaba grados Celsius y kilómetros por hora.

## 2. ¿Qué transformaciones fueron necesarias?

Para poder adaptar todos los datos al contrato institucional, fue necesario realizar alguno cambios y conversiones:

- Convertir temperaturas de Fahrenheit a Celsius.
- Convertir velocidades del viento de metros por segundo a kilómetros por hora.
- Unificar los nombres de los campos de ambos proveedores.
- Transformar las estructuras de entrada al formato solicitado por la API.
- Normalizar el campo origen.
- Ajustar los formatos de fecha para cumplir con el contrato institucional.

## 3. ¿Qué tipos de errores encontró antes de enviar información?

Durante el procesamiento de los datos se encontraron varios errores, entre ellos:

- Fechas inválidas.
- Valores nulos.
- Temperaturas con datos incorrectos.
- Humedad fuera del rango permitido.
- Coordenadas geográficas inválidas.
- Campos obligatorios vacíos.
- Velocidades de viento negativas.

Estos registros fueron identificados antes de realizar el envío y tratados de acuerdo con las reglas del taller.

## 4. ¿Qué diferencias encontró entre validación local y validación del servidor?

La validación local permitió detectar errores antes de enviar la información a la API. Esto ayudó a evitar el envío de registros que no cumplían con las reglas definidas en el contrato.

La validación del servidor se realizó una vez enviados los datos. Aunque un registro puede ser válido localmente, el servidor puede aplicar validaciones adicionales y rechazarlo si encuentra alguna inconsistencia.

## 5. ¿Qué decisión de implementación considera más importante y por qué?

La decisión más importante fue separar el desarrollo en etapas independientes: lectura de datos, normalización, validación, envío a la API y generación de reportes.

Esto facilitó la identificación de errores durante el desarrollo y permitió realizar pruebas de cada proceso por separado, haciendo el código más organizado y fácil de mantener.

# Evidencia de ejecución

## Resultados obtenidos

Métrica Resultado:
Registros procesados: 400 
Registros normalizados: 394
Errores de normalización: 6
Registros válidos localmente: 190
Registros rechazados localmente: 204
Registros enviados a la API: 190 
Registros aceptados por la API: 0
Registros rechazados por la API: 190
Errores de comunicación: 0
Consulta final GET HTTP: 200

## Ejemplos de errores encontrados

### Error de normalización

- Temperaturas con valores no numéricos.
- Fechas con formato inválido.
- Campos requeridos inexistentes.

### Error de validación local

- Humedad superior al rango permitido.
- Coordenadas fuera de los límites válidos.
- Campos que eran obligatorios vacíos.

## Resultado de integración

Se realizó el envío de los registros válidos utilizando el identificador de equipo **EQUIPO-13-APPSWEB**. Posteriormente se ejecutó la consulta mediante GET a la API institucional y se obtuvo una respuesta HTTP 200, lo que confirmó la comunicación correcta con el servicio.

# Conclusión

Este taller permitió aplicar los conceptos de integración de datos, procesamiento de archivos JSON y CSV, validación de información, consumo de APIs y pruebas automatizadas. Además, permitió comprender la importancia de normalizar datos provenientes de diferentes fuentes antes de compartirlos con otros sistemas, para formar una simetría.