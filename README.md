# Taller 2: API para adquisición y consulta de datos IoT

## 1. Información general

-   **Proyecto:** API para adquisición y consulta de datos IoT.
-   **Integrante:** Trabajo individual.
-   **Asignatura:** Aplicaciones y Servicios Web.
-   **Programa:** Tecnología en Desarrollo de Software, ITM.
-   **Fecha:** 10 de octubre de 2026.
-   **Sensor asignado:** `WQ-003`.
-   **Tópico MQTT configurado:** `iot/sensors/WQ-003/data`.
-   **Repositorio:** https://github.com/Gegaela1/AppsServicesWeb
-   **Rama:** `taller-2`.

## 2. Descripción del sistema

El proyecto permite consultar por HTTP la información de sensores y las
mediciones guardadas en PostgreSQL. También incluye código para recibir
mensajes mediante MQTT y validar los datos antes de procesarlos.

La API se desarrolló con FastAPI. Los esquemas Pydantic validan los
datos de entrada, SQLAlchemy se utiliza para trabajar con la base de
datos y los servicios separan la lógica de negocio de las rutas HTTP.

El sensor `WQ-003` tiene configuradas estas magnitudes en el catálogo
consultado:

  Magnitud             Unidad     Rango configurado
  -------------------- -------- -------------------
  `temperature`        `C`                   0 a 50
  `dissolved_oxygen`   `mg/L`                0 a 20

**Payload del sensor:** el siguiente JSON es un ejemplo de estructura;
no debe considerarse un mensaje real recibido. Para completar este
punto, se debe sustituir por un payload capturado durante la prueba
MQTT, sin incluir datos sensibles.

``` json
{
  "sensor_id": "WQ-003",
  "timestamp": "2026-10-07T16:25:30Z",
  "measurements": {
    "temperature": {
      "value": 24.6,
      "unit": "C"
    }
  }
}
```

El campo `sensor_id` corresponde al código del sensor
(`sensores.codigo`), no al ID numérico de la tabla.

## 3. Configuración del entorno

Se requiere Python 3.10 o superior y acceso a la base PostgreSQL y al
broker MQTT configurados para el taller.

Desde PowerShell, en la carpeta del proyecto, se crea y activa el
entorno virtual y se instalan las dependencias:

``` powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Para ejecutar las pruebas automatizadas:

``` powershell
python -m pytest .\tests -v
```

Las pruebas automatizadas ejecutadas durante el desarrollo finalizaron
con 12 pruebas aprobadas.

La aplicación utiliza variables de entorno. Crea un archivo `.env` local
a partir de `.env.example` y completa los valores que correspondan a tu
entorno. No publiques `.env` ni credenciales reales.

Variables MQTT utilizadas como referencia:

``` dotenv
MQTT_BROKER=emqx.coriotlab.co
MQTT_PORT=1883
MQTT_TOPIC=iot/sensors/WQ-003/data
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_KEEPALIVE=60
```

También se deben configurar las variables `POSTGRES_*` que utiliza el
proyecto. Los valores sensibles deben permanecer en el `.env` local.

## 4. Base de datos

La definición del modelo se documenta en
[`data-model.md`](data-model.md). La aplicación utiliza SQLAlchemy ORM
para consultar y relacionar estas tablas:

-   `sensores`: contiene el catálogo de sensores.
-   `sensor_magnitudes`: relaciona cada sensor con las magnitudes que
    puede medir, incluyendo unidad y límites.
-   `mediciones`: guarda los valores medidos, la referencia a
    `sensor_magnitudes`, el timestamp de la medición y la fecha de
    recepción.

Las relaciones se mantienen mediante las claves primarias y foráneas
definidas en el modelo. El catálogo de sensores y magnitudes es
proporcionado por el curso; la aplicación lo consulta y no debe
modificarlo sin autorización.

Los timestamps de medición se conservan como instantes UTC. En las
respuestas de la API se convierten a la zona horaria `America/Bogota`.
La fecha de recepción se mantiene separada de la fecha de medición.

## 5. Organización del código

La estructura del proyecto usa `repositories/` y `services/` en lugar de
una carpeta `crud/` independiente. Las funciones principales son:

-   `schemas/`: define y valida los datos de entrada y salida.
-   `models/`: representa las tablas de PostgreSQL mediante SQLAlchemy.
-   `repositories/`: contiene las consultas y operaciones de acceso a
    datos.
-   `services/`: implementa la lógica de negocio y coordina las
    consultas.
-   `api/`: define las rutas HTTP de sensores y mediciones.
-   `database/`: configura la conexión y las sesiones de PostgreSQL.
-   `mqtt_example.py`: ejemplo de conexión y recepción de mensajes MQTT.
-   `tests/`: contiene las pruebas automatizadas.

La estructura principal es:

``` text
app/
├── main.py
├── api/
│   ├── mediciones.py
│   └── sensores.py
├── database/
│   └── connection.py
├── models/
│   ├── medicion.py
│   ├── sensor.py
│   └── sensor_magnitud.py
├── repositories/
│   ├── medicion_repository.py
│   └── sensor_repository.py
├── schemas/
│   ├── mqtt.py
│   └── sensor.py
└── services/
    ├── medicion_service.py
    ├── mqtt_service.py
    └── sensor_service.py
```

## 6. Endpoints implementados

La documentación interactiva se puede consultar en
`http://127.0.0.1:8000/docs` mientras el servidor está ejecutándose.

  -------------------------------------------------------------------------------------------
  Método                  Ruta                                        Descripción
  ----------------------- ------------------------------------------- -----------------------
  GET                     `/`                                         Ruta inicial de la API.

  GET                     `/sensores`                                 Lista los sensores.

  GET                     `/sensores/por-codigo/{codigo}`             Busca un sensor por su
                                                                      código.

  GET                     `/sensores/{sensor_id}`                     Consulta un sensor por
                                                                      ID.

  GET                     `/sensores/{sensor_id}/magnitudes`          Consulta las magnitudes
                                                                      asociadas a un sensor.

  GET                     `/sensores/{sensor_id}/mediciones`          Consulta las mediciones
                                                                      históricas.

  GET                     `/sensores/{sensor_id}/ultima-medicion`     Consulta la última
                                                                      medición.

  GET                     `/mediciones/{medicion_id}`                 Consulta una medición
                                                                      por ID.

  GET                     `/sensor-magnitudes/{sensor_magnitud_id}`   Consulta una relación
                                                                      sensor-magnitud.
  -------------------------------------------------------------------------------------------

La consulta histórica admite los filtros `limit`, `desde`, `hasta` y
`magnitud`, que se pueden combinar. Ejemplos:

``` text
/sensores/11/mediciones?limit=5
/sensores/11/mediciones?magnitud=temperature
/sensores/11/mediciones?desde=2026-10-01T00:00:00Z&hasta=2026-10-10T23:59:59Z
/sensores/11/mediciones?magnitud=temperature&desde=2026-10-01T00:00:00Z&hasta=2026-10-10T23:59:59Z&limit=10
```

El ID `11` corresponde al sensor utilizado durante las pruebas; puede
variar según la base de datos.

Códigos HTTP comprobados en las pruebas de la API:

-   `200`: consulta correcta.
-   `400`: rango de fechas inválido.
-   `404`: recurso inexistente.
-   `422`: parámetro inválido o que no supera la validación.

## 7. Evidencias de funcionamiento

Las capturas se encuentran en la carpeta [`evidence/`](evidence/).
Documentan las pruebas automatizadas, consultas de sensores, consulta
por código, magnitudes, última medición, consultas históricas, filtros y
respuestas de error.

  --------------------------------------------------------------------------------------
  Prueba                  Evidencia                           Archivo o función
                                                              relacionada
  ----------------------- ----------------------------------- --------------------------
  Pruebas automatizadas   `02_pruebas_automatizadas.png`      `tests/`

  Consulta de sensores    `13_sensores_lista.png`             `app/api/sensores.py`,
                                                              servicio de sensores

  Consulta de sensor por  `14_sensor_por_id.png`              `app/api/sensores.py`
  ID                                                          

  Sensor inexistente      `15_sensor_no_encontrado_404.png`   `app/api/sensores.py`

  Consulta por código     `16_sensor_por_codigo.png`          `app/api/sensores.py`

  Magnitudes del sensor   `17_magnitudes_sensor.png`          servicio y repositorio de
                                                              sensores

  Última medición         `06_ultima_medicion_200.png`        `app/api/mediciones.py`,
                                                              servicio de mediciones

  Histórico de mediciones `07_ultimas_5_mediciones.png`       `app/api/mediciones.py`

  Filtro por rango de     `09_filtro_rango_fechas.png`        servicio y repositorio de
  fechas                                                      mediciones

  Filtros combinados      `10_filtros_combinados.png`         servicio y repositorio de
                                                              mediciones

  Filtro por magnitud     `8_filtro_por_magnitud.png`         servicio y repositorio de
                                                              mediciones

  Rango de fechas         `04_error_400.png  .png`            validación de parámetros
  inválido                                                    del histórico

  Fecha inválida          `05_error_422_fecha_invalida.png`   validación de parámetros
                                                              del histórico

  Medición inexistente    `11_medicion_inexistente_404.png`   `app/api/mediciones.py`

  Límite inválido         `12_validacion_limit_422.png`       validación del parámetro
                                                              `limit`
  --------------------------------------------------------------------------------------

Las capturas prueban las consultas y respuestas que muestran. Para las
pruebas MQTT, de persistencia y de recolección durante 20 minutos,
registra también la evidencia real correspondiente. No se declara
completada la recolección de 20 minutos sin anotar las horas de inicio y
fin.

## 8. Control de versiones

-   **Repositorio:** https://github.com/Gegaela1/AppsServicesWeb
-   **Rama de entrega:** `taller-2`
-   **Modalidad:** individual.

El historial de Git registra los cambios realizados en el proyecto. Como
el trabajo es individual, no aplica una tabla de aportes por
integrantes. Los commits deben tener mensajes claros que describan cada
cambio.

Antes de subir cambios, verifica que `.env`, `.venv` y las credenciales
no estén incluidos en el commit.

## 9. Conclusiones

Principales aprendizajes

Con este trabajo aprendí a conectar una API desarrollada con FastAPI con una base de datos PostgreSQL y a consultar la información de los sensores. También entendí mejor cómo funciona la comunicación MQTT y cómo se pueden recibir datos de un sensor, en este caso el WQ-003. Además, aprendí a crear endpoints para consultar las mediciones, filtrar los resultados por fechas y magnitud, y validar los datos que recibe la API.

Dificultades encontradas

Una de las dificultades fue organizar el código para que cada parte tuviera una función clara, especialmente la conexión a la base de datos, las consultas y el manejo de las mediciones. También fue necesario revisar las respuestas de la API cuando se enviaban parámetros incorrectos o se consultaban datos que no existían. Otra parte que requirió atención fue configurar las variables de entorno y comprobar que la aplicación pudiera acceder correctamente a la base de datos.

Soluciones aplicadas

Para solucionar estos problemas, organicé el código en módulos separados y revisé las consultas a la base de datos para comprobar que devolvieran la información esperada. También realicé pruebas con diferentes endpoints, incluyendo consultas válidas y casos en los que la API debía responder con errores como 400, 404 o 422. Por último, utilicé pruebas automatizadas para verificar el funcionamiento de varias partes del proyecto y corregir los problemas que fueron apareciendo durante el desarrollo.
