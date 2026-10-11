
import pytest
from pydantic import ValidationError

from app.schemas.mqtt import MensajeMQTT


def mensaje_base():
    return {
        "sensor_id": "WQ-003",
        "timestamp": "2026-10-10T20:01:36Z",
        "measurements": {
            "temperature": {
                "value": 24.02,
                "unit": "C",
            },
        },
    }


def test_acepta_mensaje_correcto():
    mensaje = MensajeMQTT.model_validate(mensaje_base())

    assert mensaje.sensor_id == "WQ-003"
    assert mensaje.timestamp.isoformat() == "2026-10-10T20:01:36+00:00"


def test_rechaza_timestamp_sin_zona_horaria():
    datos = mensaje_base()
    datos["timestamp"] = "2026-10-10T20:01:36"

    with pytest.raises(ValidationError):
        MensajeMQTT.model_validate(datos)


def test_rechaza_timestamp_invalido():
    datos = mensaje_base()
    datos["timestamp"] = "fecha-invalida"

    with pytest.raises(ValidationError):
        MensajeMQTT.model_validate(datos)


def test_rechaza_mensaje_sin_mediciones():
    datos = mensaje_base()
    datos["measurements"] = {}

    with pytest.raises(ValidationError):
        MensajeMQTT.model_validate(datos)


def test_rechaza_campo_adicional():
    datos = mensaje_base()
    datos["campo_no_permitido"] = "valor"

    with pytest.raises(ValidationError):
        MensajeMQTT.model_validate(datos)


def test_rechaza_valor_no_numerico():
    datos = mensaje_base()
    datos["measurements"]["temperature"]["value"] = "veinticuatro"

    with pytest.raises(ValidationError):
        MensajeMQTT.model_validate(datos)
