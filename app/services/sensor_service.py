
from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.models.sensor_magnitud import SensorMagnitud
from app.repositories.sensor_repository import (
    listar_sensores,
    obtener_magnitudes_de_sensor,
    obtener_sensor_por_codigo,
    obtener_sensor_por_id,
)


class RecursoNoEncontradoError(Exception):
    """Indica que el recurso solicitado no existe."""


def consultar_sensores(db: Session) -> list[Sensor]:
    return listar_sensores(db)


def consultar_sensor_por_id(db: Session, sensor_id: int) -> Sensor:
    sensor = obtener_sensor_por_id(db, sensor_id)

    if sensor is None:
        raise RecursoNoEncontradoError(
            f"No existe un sensor con ID {sensor_id}"
        )

    return sensor


def consultar_sensor_por_codigo(db: Session, codigo: str) -> Sensor:
    sensor = obtener_sensor_por_codigo(db, codigo)

    if sensor is None:
        raise RecursoNoEncontradoError(
            f"No existe un sensor con código '{codigo}'"
        )

    return sensor


def consultar_magnitudes_de_sensor(
    db: Session,
    sensor_id: int,
) -> list[SensorMagnitud]:
    consultar_sensor_por_id(db, sensor_id)
    return obtener_magnitudes_de_sensor(db, sensor_id)
