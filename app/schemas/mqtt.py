
from datetime import datetime, timezone
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class MedicionEntrada(BaseModel):
    """Representa el valor y la unidad de una magnitud recibida."""

    model_config = ConfigDict(extra="forbid", strict=True)

    value: Annotated[
        float,
        Field(allow_inf_nan=False),
    ]

    unit: Annotated[
        str,
        Field(min_length=1, max_length=20),
    ]


class MensajeMQTT(BaseModel):
    """Valida la estructura del mensaje recibido por MQTT."""

    model_config = ConfigDict(extra="forbid")

    sensor_id: Annotated[
        str,
        Field(min_length=1, max_length=20),
    ]

    timestamp: datetime

    measurements: Annotated[
        dict[str, MedicionEntrada],
        Field(min_length=1),
    ]

    @field_validator("sensor_id")
    @classmethod
    def validar_sensor_id(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("sensor_id no puede estar vacío")

        return valor

    @field_validator("timestamp")
    @classmethod
    def validar_timestamp_utc(cls, valor: datetime) -> datetime:
        if valor.tzinfo is None or valor.utcoffset() is None:
            raise ValueError(
                "timestamp debe incluir zona horaria"
            )

        return valor.astimezone(timezone.utc)
