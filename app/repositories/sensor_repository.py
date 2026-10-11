
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.models.sensor_magnitud import SensorMagnitud


def listar_sensores(db: Session) -> list[Sensor]:
    consulta = select(Sensor).order_by(Sensor.id)
    return list(db.scalars(consulta).all())


def obtener_sensor_por_id(db: Session, sensor_id: int) -> Sensor | None:
    consulta = select(Sensor).where(Sensor.id == sensor_id)
    return db.scalar(consulta)


def obtener_sensor_por_codigo(
    db: Session,
    codigo: str,
) -> Sensor | None:
    consulta = select(Sensor).where(Sensor.codigo == codigo)
    return db.scalar(consulta)


def obtener_magnitudes_de_sensor(
    db: Session,
    sensor_id: int,
) -> list[SensorMagnitud]:
    consulta = (
        select(SensorMagnitud)
        .where(SensorMagnitud.sensor_id == sensor_id)
        .order_by(SensorMagnitud.id)
    )
    return list(db.scalars(consulta).all())


def obtener_sensor_magnitud_por_id(
    db: Session,
    sensor_magnitud_id: int,
) -> SensorMagnitud | None:
    consulta = select(SensorMagnitud).where(
        SensorMagnitud.id == sensor_magnitud_id
    )
    return db.scalar(consulta)

