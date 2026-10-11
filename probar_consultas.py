from app.database.connection import SessionLocal
from app.services.sensor_service import (
    consultar_sensores,
    consultar_sensor_por_codigo,
    consultar_magnitudes_de_sensor,
)
from app.services.medicion_service import (
    consultar_mediciones_de_sensor,
)


def main():
    db = SessionLocal()

    try:
        sensores = consultar_sensores(db)
        sensor = consultar_sensor_por_codigo(db, "WQ-003")
        magnitudes = consultar_magnitudes_de_sensor(db, sensor.id)
        mediciones = consultar_mediciones_de_sensor(
            db,
            sensor.id,
            limit=5,
        )

        print("Sensores encontrados:", len(sensores))
        print("Sensor consultado:", sensor.codigo)

        print(
            "Magnitudes configuradas:",
            [magnitud.magnitud for magnitud in magnitudes],
        )

        print("Mediciones consultadas:", len(mediciones))

        for medicion in mediciones:
            print(
                "ID:", medicion.id,
                "| Valor:", medicion.valor,
                "| Fecha UTC:", medicion.timestamp_utc,
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()