from datetime import datetime
from sqlalchemy.orm import Session
from app.models.medicion import Medicion
from app.models.sensor_magnitud import SensorMagnitud
from app.repositories.medicion_repository import (
    consultar_mediciones_por_sensor,
    consultar_ultima_medicion,
    obtener_medicion_por_id,
    obtener_mediciones_por_sensor_magnitud,
)
from app.repositories.sensor_repository import (
    obtener_sensor_magnitud_por_id,
)
from app.services.sensor_service import (
    RecursoNoEncontradoError,
    consultar_sensor_por_id,
)



def consultar_mediciones_de_sensor(
    db: Session,
    sensor_id: int,
    limit: int = 100,
    desde: datetime | None = None,
    hasta: datetime | None = None,
    magnitud: str | None = None,
) -> list[Medicion]:
    """Consulta las mediciones recientes de un sensor con filtros."""

    consultar_sensor_por_id(db, sensor_id)

    if desde is not None and hasta is not None and desde > hasta:
        raise ValueError(
            "La fecha inicial 'desde' no puede ser posterior a 'hasta'"
        )

    return consultar_mediciones_por_sensor(
        db=db,
        sensor_id=sensor_id,
        limit=limit,
        desde=desde,
        hasta=hasta,
        magnitud=magnitud,
    )


def consultar_medicion_por_id(
    db: Session,
    medicion_id: int,
) -> Medicion:
    """Consulta una medición por su identificador."""
    medicion = obtener_medicion_por_id(db, medicion_id)

    if medicion is None:
        raise RecursoNoEncontradoError(
            f"No existe una medición con ID {medicion_id}"
        )

    return medicion


def consultar_ultima_medicion_de_sensor(
    db: Session,
    sensor_id: int,
) -> Medicion:
    """Consulta la última medición de un sensor."""
    consultar_sensor_por_id(db, sensor_id)

    medicion = consultar_ultima_medicion(db, sensor_id)

    if medicion is None:
        raise RecursoNoEncontradoError(
            f"El sensor con ID {sensor_id} no tiene mediciones"
        )

    return medicion


def consultar_mediciones_de_sensor_magnitud(
    db: Session,
    sensor_magnitud_id: int,
    limit: int = 100,
) -> tuple[SensorMagnitud, list[Medicion]]:
    """Consulta las mediciones de una configuración de magnitud."""
    configuracion = obtener_sensor_magnitud_por_id(
        db,
        sensor_magnitud_id,
    )

    if configuracion is None:
        raise RecursoNoEncontradoError(
            "No existe una configuración de sensor-magnitud "
            f"con ID {sensor_magnitud_id}"
        )

    mediciones = obtener_mediciones_por_sensor_magnitud(
        db=db,
        sensor_magnitud_id=sensor_magnitud_id,
        limit=limit,
    )

    return configuracion, mediciones