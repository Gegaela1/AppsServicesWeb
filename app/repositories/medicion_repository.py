from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medicion import Medicion
from app.models.sensor_magnitud import SensorMagnitud


def guardar_mediciones(
    db: Session,
    mediciones: list[tuple[SensorMagnitud, Decimal]],
    timestamp_utc: datetime,
) -> list[Medicion]:
    """Guarda las mediciones de un mensaje en una transacción."""

    registros = [
        Medicion(
            sensor_magnitud_id=sensor_magnitud.id,
            valor=valor,
            timestamp_utc=timestamp_utc,
        )
        for sensor_magnitud, valor in mediciones
    ]

    try:
        db.add_all(registros)
        db.flush()
        db.commit()

        for registro in registros:
            db.refresh(registro)

        return registros

    except Exception:
        db.rollback()
        raise



def consultar_mediciones_por_sensor(
    db: Session,
    sensor_id: int,
    limit: int = 100,
    desde: datetime | None = None,
    hasta: datetime | None = None,
    magnitud: str | None = None,
) -> list[Medicion]:
    """Consulta el historial de un sensor con filtros opcionales."""

    consulta = (
        select(Medicion)
        .join(
            SensorMagnitud,
            Medicion.sensor_magnitud_id == SensorMagnitud.id,
        )
        .where(SensorMagnitud.sensor_id == sensor_id)
    )

    if desde is not None:
        consulta = consulta.where(
            Medicion.timestamp_utc >= desde
        )

    if hasta is not None:
        consulta = consulta.where(
            Medicion.timestamp_utc <= hasta
        )

    if magnitud is not None:
        consulta = consulta.where(
            SensorMagnitud.magnitud == magnitud
        )

    consulta = (
        consulta
        .order_by(
            Medicion.timestamp_utc.desc(),
            Medicion.id.desc(),
        )
        .limit(limit)
    )

    return list(db.scalars(consulta).all())


def obtener_medicion_por_id(
    db: Session,
    medicion_id: int,
) -> Medicion | None:
    """Busca una medición por su ID."""
    consulta = select(Medicion).where(Medicion.id == medicion_id)
    return db.scalar(consulta)


def consultar_ultima_medicion(
    db: Session,
    sensor_id: int,
) -> Medicion | None:
    """Obtiene la medición más reciente de un sensor."""
    consulta = (
        select(Medicion)
        .join(
            SensorMagnitud,
            Medicion.sensor_magnitud_id == SensorMagnitud.id,
        )
        .where(SensorMagnitud.sensor_id == sensor_id)
        .order_by(
            Medicion.timestamp_utc.desc(),
            Medicion.id.desc(),
        )
        .limit(1)
    )
    return db.scalar(consulta)


def obtener_mediciones_por_sensor_magnitud(
    db: Session,
    sensor_magnitud_id: int,
    limit: int = 100,
) -> list[Medicion]:
    """Consulta las mediciones asociadas a una configuración de magnitud."""
    consulta = (
        select(Medicion)
        .where(Medicion.sensor_magnitud_id == sensor_magnitud_id)
        .order_by(
            Medicion.timestamp_utc.desc(),
            Medicion.id.desc(),
        )
        .limit(limit)
    )
    return list(db.scalars(consulta).all())