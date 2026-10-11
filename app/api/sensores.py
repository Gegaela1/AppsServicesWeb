from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.sensor import (
    SensorRespuesta,
    SensorMagnitudRespuesta,
)
from app.services.sensor_service import (
    RecursoNoEncontradoError,
    consultar_sensores,
    consultar_sensor_por_id,
    consultar_sensor_por_codigo,
    consultar_magnitudes_de_sensor,
)

router = APIRouter(
    prefix="/sensores",
    tags=["Sensores"],
)


@router.get(
    "",
    response_model=list[SensorRespuesta],
)
def listar_sensores_endpoint(
    db: Session = Depends(get_db),
):
    return consultar_sensores(db)


@router.get(
    "/por-codigo/{codigo}",
    response_model=SensorRespuesta,
)
def obtener_sensor_por_codigo_endpoint(
    codigo: str,
    db: Session = Depends(get_db),
):
    try:
        return consultar_sensor_por_codigo(db, codigo)
    except RecursoNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.get(
    "/{sensor_id}/magnitudes",
    response_model=list[SensorMagnitudRespuesta],
)
def obtener_magnitudes_endpoint(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    try:
        return consultar_magnitudes_de_sensor(db, sensor_id)
    except RecursoNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.get(
    "/{sensor_id}",
    response_model=SensorRespuesta,
)
def obtener_sensor_por_id_endpoint(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    try:
        return consultar_sensor_por_id(db, sensor_id)
    except RecursoNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error