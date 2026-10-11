from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo
from pydantic import BaseModel, ConfigDict, computed_field


class SensorRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    categoria: str
    ubicacion: str
    activo: bool
    fecha_registro: datetime


class SensorMagnitudRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: int
    magnitud: str
    unidad: str
    valor_minimo: Decimal | None
    valor_maximo: Decimal | None


class MedicionRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_magnitud_id: int
    valor: Decimal
    timestamp_utc: datetime
    fecha_recepcion: datetime

    @computed_field
    @property
    def timestamp_colombia(self) -> datetime:
        """Fecha de la medición en la zona horaria de Colombia."""
        return self.timestamp_utc.astimezone(
            ZoneInfo("America/Bogota")
        )

    @computed_field
    @property
    def fecha_recepcion_colombia(self) -> datetime:
        """Fecha de recepción en la zona horaria de Colombia."""
        return self.fecha_recepcion.astimezone(
            ZoneInfo("America/Bogota")
        )
