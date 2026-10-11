from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.connection import get_db
from app.schemas.sensor import MedicionRespuesta, SensorMagnitudRespuesta
from app.services.medicion_service import (
    consultar_medicion_por_id,
    consultar_mediciones_de_sensor,
    consultar_mediciones_de_sensor_magnitud,
    consultar_ultima_medicion_de_sensor,
)
from app.services.sensor_service import RecursoNoEncontradoError


router = APIRouter(tags=["Mediciones"])


@router.get(
    "/mediciones/{medicion_id}",
    response_model=MedicionRespuesta,
)
def obtener_medicion_endpoint(
    medicion_id: int,
    db: Session = Depends(get_db),
):
    try:
        return consultar_medicion_por_id(db, medicion_id)
    except RecursoNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error



@router.get(
    "/sensores/{sensor_id}/mediciones",
    response_model=list[MedicionRespuesta],
)
def obtener_mediciones_sensor_endpoint(
    sensor_id: int,
    limit: int = Query(default=100, ge=1, le=1000),
    desde: datetime | None = Query(default=None),
    hasta: datetime | None = Query(default=None),
    magnitud: str | None = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
):
    try:
        return consultar_mediciones_de_sensor(
            db=db,
            sensor_id=sensor_id,
            limit=limit,
            desde=desde,
            hasta=hasta,
            magnitud=magnitud,
        )
    except RecursoNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get(
    "/sensores/{sensor_id}/ultima-medicion",
    response_model=MedicionRespuesta,
)
def obtener_ultima_medicion_endpoint(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    try:
        return consultar_ultima_medicion_de_sensor(db, sensor_id)
    except RecursoNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.get(
    "/sensor-magnitudes/{sensor_magnitud_id}",
)
def obtener_mediciones_sensor_magnitud_endpoint(
    sensor_magnitud_id: int,
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    try:
        configuracion, mediciones = consultar_mediciones_de_sensor_magnitud(
            db,
            sensor_magnitud_id,
            limit,
        )
        return {
            "sensor_magnitud": SensorMagnitudRespuesta.model_validate(
                configuracion
            ),
            "mediciones": [
                MedicionRespuesta.model_validate(medicion)
                for medicion in mediciones
            ],
        }
    except RecursoNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
