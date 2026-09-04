from pathlib import Path
import csv
import json

BASE_DIR = Path(__file__).parent

RUTA_CSV = BASE_DIR / "datos" / "estudiantes.csv"


def transformar_estudiante(estudiante: dict) -> dict:
    return {
        "id": estudiante["codigo"],
        "nombre_completo": f"{estudiante['nombre']} {estudiante['apellido']}",
        "semestre": int(estudiante["semestre"]),
        "promedio": float(estudiante["promedio"]),
        "estado": "Activo" if estudiante["activo"].lower() == "true" else "Inactivo"
    }


def serializar_estudiantes(ruta: Path, estudiantes: list[dict]) -> None:
    """Serializa una lista de estudiantes a JSON."""
    ruta.parent.mkdir(exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(
            estudiantes,
            archivo,
            indent=2,
            ensure_ascii=False
        )


def deserializar_estudiantes(ruta: Path) -> list[dict]:
    """DeserializaJSON a una lista de diccionarios."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


# Leer CSV
estudiantes = []

with open(RUTA_CSV, encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for estudiante in lector:
        estudiantes.append(estudiante)

# Transformar estudiantes
estudiantes_transformados = []

for estudiante in estudiantes:
    estudiantes_transformados.append(
        transformar_estudiante(estudiante)
    )

# Mostrar información
print(f"Estudiantes leídos: {len(estudiantes)}")
print(f"Estudiantes transformados: {len(estudiantes_transformados)}")

print("\nPrimer estudiante transformado:")
print(estudiantes_transformados[0])

# Serializar a JSON
RUTA_JSON = BASE_DIR / "salida" / "estudiantes_resumen.json"

serializar_estudiantes(
    RUTA_JSON,
    estudiantes_transformados
)

print(f"\nArchivo JSON generado: {RUTA_JSON}")

# Deserializar JSON
estudiantes_recuperados = deserializar_estudiantes(RUTA_JSON)

print("\nDatos recuperados desde JSON:")
print(estudiantes_recuperados[0])

print(f"Total recuperado: {len(estudiantes_recuperados)}")