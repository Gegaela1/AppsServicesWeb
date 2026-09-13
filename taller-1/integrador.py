from pathlib import Path
import json
import csv
from datetime import datetime

BASE_DIR = Path(__file__).parent

RUTA_A = BASE_DIR / "datos" / "proveedor_a.json"
RUTA_B = BASE_DIR / "datos" / "proveedor_b.csv"

import requests

URL_BASE = "https://appsweb.quantaiot.co"

EQUIPO = "EQUIPO-13-APPSWEB"

# Funciones para normalizar y validar registros (temperatura, viento, etc.)

def fahrenheit_a_celsius(temperatura_f):
    return round((temperatura_f - 32) * 5 / 9, 2)


def ms_a_kmh(viento_ms):
    return round(viento_ms * 3.6, 2)


def normalizar_proveedor_a(registro):
    return {
        "traza": registro["provider_record_id"],
        "ciudad": registro["station"]["city_name"],
        "pais": registro["station"]["country_code"],
        "latitud": registro["location"]["lat"],
        "longitud": registro["location"]["lon"],
        "temperatura_c": fahrenheit_a_celsius(
            registro["measurements"]["temperature_f"]
        ),
        "humedad": registro["measurements"]["relative_humidity"],
        "viento_kmh": ms_a_kmh(
            registro["measurements"]["wind_speed_ms"]
        ),
        "fecha_hora": registro["observed_at"],
        "origen": "proveedor_a"
    }


def normalizar_proveedor_b(registro):
    return {
        "traza": registro["record_code"],
        "ciudad": registro["municipality"],
        "pais": registro["country"],
        "latitud": float(registro["latitude_deg"]),
        "longitud": float(registro["longitude_deg"]),
        "temperatura_c": float(registro["temp_celsius"]),
        "humedad": float(registro["humidity_pct"]),
        "viento_kmh": float(registro["wind_kmh"]),
        "fecha_hora": registro["measurement_time"],
        "origen": "proveedor_b"
    }


def validar_registro(registro):

    errores = []

    if not registro["ciudad"]:
        errores.append("Ciudad vacia")

    if not registro["pais"]:
        errores.append("Pais vacio")

    if not (-90 <= registro["latitud"] <= 90):
        errores.append("Latitud invalida")

    if not (-180 <= registro["longitud"] <= 180):
        errores.append("Longitud invalida")

    if not (0 <= registro["humedad"] <= 100):
        errores.append("Humedad invalida")

    if registro["viento_kmh"] < 0:
        errores.append("Viento invalido")

    try:
        datetime.fromisoformat(
            registro["fecha_hora"]
        )
    except Exception:
        errores.append("Fecha invalida")

    return errores


def guardar_json(ruta, datos):

    ruta.parent.mkdir(
        exist_ok=True
    )

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=2,
            ensure_ascii=False
        )

def enviar_medicion(registro):

    url = f"{URL_BASE}/api/v1/mediciones"

    headers = {
        "Content-Type": "application/json",
        "X-Equipo": EQUIPO
    }

    respuesta = requests.post(
        url,
        headers=headers,
        json=registro,
        timeout=10
    )

    return respuesta

def generar_reporte():

    return {
    "procesados": 400,
    "normalizados": len(
        todos_normalizados
    ),
    "errores_normalizacion": len(
        errores_normalizacion
    ),
    "validos_localmente": len(
        validos_localmente
    ),
    "rechazados_localmente": len(
        rechazados_localmente
    ),
    "enviados": enviados,
    "aceptados_api": aceptados_api,
    "rechazados_api": rechazados_api,
    "errores_comunicacion": errores_comunicacion
}


# proveedor A

print("=== TALLER 1 ===")

with open(RUTA_A, encoding="utf-8") as archivo:
    proveedor_a = json.load(archivo)

print(f"Proveedor: {proveedor_a['provider']}")
print(f"Fecha generación: {proveedor_a['generated_at']}")

registros = proveedor_a["records"]

print(f"Cantidad de registros: {len(registros)}")

print("\nPrimer registro:")
print(registros[0])

# procesar proveedor B
registros_b = []

with open(RUTA_B, encoding="utf-8") as archivo:

    lector = csv.DictReader(
        archivo,
        delimiter=";"
    )

    for fila in lector:
        registros_b.append(fila)

print("\n=== PROVEEDOR B ===")

print(f"Cantidad de registros: {len(registros_b)}")

print("\nPrimer registro:")
print(registros_b[0])


# normalización de un registro (a)

print("\n=== NORMALIZACION A ===")

primer_normalizado = normalizar_proveedor_a(
    registros[0]
)

print(primer_normalizado)

# normalización de un registro (b)

print("\n=== NORMALIZACION B ===")

primer_normalizado_b = normalizar_proveedor_b(
    registros_b[0]
)

print(primer_normalizado_b)


# normalizar todos los registros y capturar errores

errores_normalizacion = []

normalizados_a = []

for registro in registros:

    try:

        normalizado = normalizar_proveedor_a(
            registro
        )

        normalizados_a.append(
            normalizado
        )

    except Exception as error:

        errores_normalizacion.append({
            "origen": "proveedor_a",
            "error": str(error)
        })

normalizados_b = []

for registro in registros_b:

    try:

        normalizado = normalizar_proveedor_b(
            registro
        )

        normalizados_b.append(
            normalizado
        )

    except Exception as error:

        errores_normalizacion.append({
            "origen": "proveedor_b",
            "error": str(error)
        })

todos_normalizados = (
    normalizados_a +
    normalizados_b
)

print("\n=== RESUMEN DE NORMALIZACION ===")

print(f"Normalizados A: {len(normalizados_a)}")
print(f"Normalizados B: {len(normalizados_b)}")
print(f"Total normalizados: {len(todos_normalizados)}")

print(
    f"Errores de normalizacion: "
    f"{len(errores_normalizacion)}"
)


# sirve para realizar la validación

validos_localmente = []
rechazados_localmente = []

for registro in todos_normalizados:

    errores = validar_registro(
        registro
    )

    if errores:

        rechazados_localmente.append({
            "registro": registro,
            "errores": errores
        })

    else:

        validos_localmente.append(
            registro
        )

print("\n=== VALIDACION LOCAL ===")

print(
    f"Validos localmente: "
    f"{len(validos_localmente)}"
)

print(
    f"Rechazados localmente: "
    f"{len(rechazados_localmente)}"
)

# Sirve para generar el archivo JSON


RUTA_NORMALIZADAS = (
    BASE_DIR
    / "salida"
    / "normalizadas.json"
)

guardar_json(
    RUTA_NORMALIZADAS,
    todos_normalizados
)

print(
    f"\nArchivo generado: "
    f"{RUTA_NORMALIZADAS}"
)

RUTA_REPORTE = (
    BASE_DIR
    / "salida"
    / "reporte.json"
)


enviados = 0
aceptados_api = 0
rechazados_api = 0
errores_comunicacion = 0

print("\n=== ENVIO A API ===")

for registro in validos_localmente:

    try:

        respuesta = enviar_medicion(
            registro
        )

        enviados += 1

        if respuesta.status_code == 201:

            aceptados_api += 1

        elif respuesta.status_code in (
            400,
            409,
            422
        ):

            rechazados_api += 1

        else:

            errores_comunicacion += 1

    except Exception:

        errores_comunicacion += 1

        print(
    f"Enviados: {enviados}"
)

print(
    f"Aceptados API: "
    f"{aceptados_api}"
)

print(
    f"Rechazados API: "
    f"{rechazados_api}"
)

print(
    f"Errores comunicacion: "
    f"{errores_comunicacion}"
)

def consultar_mediciones():

    url = (
        f"{URL_BASE}"
        f"/api/v1/mediciones"
    )

    params = {
        "equipo": EQUIPO
    }

    return requests.get(
        url,
        params=params,
        timeout=10
    )

print("\n=== CONSULTA FINAL ===")

try:

    respuesta_get = (
        consultar_mediciones()
    )

    print(
        f"GET: "
        f"{respuesta_get.status_code}"
    )

except Exception as error:

    print(
        f"Error GET: {error}"
    )
reporte = generar_reporte()

guardar_json(
    RUTA_REPORTE,
    reporte
)

print(
    f"Reporte generado: "
    f"{RUTA_REPORTE}"
)