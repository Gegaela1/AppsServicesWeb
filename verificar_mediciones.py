
from app.database.connection import SessionLocal
from app.services.sensor_service import consultar_sensor_por_codigo
from app.services.medicion_service import consultar_mediciones_de_sensor


def main():
    with SessionLocal() as db:
        sensor = consultar_sensor_por_codigo(db, "WQ-003")

        if sensor is None:
            print("No se encontró el sensor WQ-003.")
            return

        mediciones = consultar_mediciones_de_sensor(
            db,
            sensor.id,
            limit=10,
        )

        print(f"Sensor: {sensor.codigo}")
        print(f"Mediciones encontradas: {len(mediciones)}")

        for medicion in mediciones:
            print(
                f"ID: {medicion.id} | "
                f"Valor: {medicion.valor} | "
                f"Fecha UTC: {medicion.timestamp_utc}"
            )


if __name__ == "__main__":
    main()