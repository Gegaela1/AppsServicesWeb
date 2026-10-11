
from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.models.sensor import Sensor
from app.models.sensor_magnitud import SensorMagnitud
from app.schemas.mqtt import MensajeMQTT
from app.services.mqtt_service import (
    ErrorValidacionMQTT,
    validar_mensaje_mqtt,
)


@pytest.fixture
def mensaje_valido():
    return MensajeMQTT.model_validate({
        "sensor_id": "WQ-003",
        "timestamp": "2026-10-10T20:01:36Z",
        "measurements": {
            "temperature": {
                "value": 24.02,
                "unit": "C",
            },
            "dissolved_oxygen": {
                "value": 10.77,
                "unit": "mg/L",
            },
        },
    })


@pytest.fixture
def configuracion_sensor():
    sensor = Sensor(
        id=11,
        codigo="WQ-003",
        nombre="Sensor de oxígeno disuelto",
        categoria="AGUA",
        ubicacion="Estanque experimental",
        activo=True,
    )

    magnitudes = [
        SensorMagnitud(
            id=29,
            sensor_id=11,
            magnitud="temperature",
            unidad="C",
            valor_minimo=Decimal("0"),
            valor_maximo=Decimal("50"),
        ),
        SensorMagnitud(
            id=30,
            sensor_id=11,
            magnitud="dissolved_oxygen",
            unidad="mg/L",
            valor_minimo=Decimal("0"),
            valor_maximo=Decimal("20"),
        ),
    ]

    return sensor, magnitudes


def preparar_repositorios(monkeypatch, sensor, magnitudes):
    from app.services import mqtt_service

    monkeypatch.setattr(
        mqtt_service,
        "obtener_sensor_por_codigo",
        lambda db, codigo: sensor if codigo == "WQ-003" else None,
    )

    monkeypatch.setattr(
        mqtt_service,
        "obtener_magnitudes_de_sensor",
        lambda db, sensor_id: magnitudes,
    )


def test_acepta_mensaje_valido(
    mensaje_valido,
    configuracion_sensor,
    monkeypatch,
):
    sensor, magnitudes = configuracion_sensor
    preparar_repositorios(monkeypatch, sensor, magnitudes)

    validar_mensaje_mqtt(Mock(), mensaje_valido)


def test_rechaza_sensor_inexistente(
    mensaje_valido,
    configuracion_sensor,
    monkeypatch,
):
    _, magnitudes = configuracion_sensor
    preparar_repositorios(monkeypatch, None, magnitudes)

    with pytest.raises(
        ErrorValidacionMQTT,
        match="no existe",
    ):
        validar_mensaje_mqtt(Mock(), mensaje_valido)


def test_rechaza_unidad_incorrecta(
    configuracion_sensor,
    monkeypatch,
):
    sensor, magnitudes = configuracion_sensor
    preparar_repositorios(monkeypatch, sensor, magnitudes)

    mensaje = MensajeMQTT.model_validate({
        "sensor_id": "WQ-003",
        "timestamp": "2026-10-10T20:01:36Z",
        "measurements": {
            "temperature": {
                "value": 24.02,
                "unit": "F",
            },
        },
    })

    with pytest.raises(
        ErrorValidacionMQTT,
        match="Unidad incorrecta",
    ):
        validar_mensaje_mqtt(Mock(), mensaje)


def test_rechaza_magnitud_no_configurada(
    configuracion_sensor,
    monkeypatch,
):
    sensor, magnitudes = configuracion_sensor
    preparar_repositorios(monkeypatch, sensor, magnitudes)

    mensaje = MensajeMQTT.model_validate({
        "sensor_id": "WQ-003",
        "timestamp": "2026-10-10T20:01:36Z",
        "measurements": {
            "humidity": {
                "value": 70.0,
                "unit": "%",
            },
        },
    })

    with pytest.raises(
        ErrorValidacionMQTT,
        match="no está configurada",
    ):
        validar_mensaje_mqtt(Mock(), mensaje)


def test_rechaza_valor_fuera_de_rango(
    configuracion_sensor,
    monkeypatch,
):
    sensor, magnitudes = configuracion_sensor
    preparar_repositorios(monkeypatch, sensor, magnitudes)

    mensaje = MensajeMQTT.model_validate({
        "sensor_id": "WQ-003",
        "timestamp": "2026-10-10T20:01:36Z",
        "measurements": {
            "temperature": {
                "value": 55.0,
                "unit": "C",
            },
        },
    })

    with pytest.raises(
        ErrorValidacionMQTT,
        match="supera el máximo permitido",
    ):
        validar_mensaje_mqtt(Mock(), mensaje)


def test_rechaza_sensor_inactivo(
    mensaje_valido,
    configuracion_sensor,
    monkeypatch,
):
    sensor, magnitudes = configuracion_sensor
    sensor.activo = False
    preparar_repositorios(monkeypatch, sensor, magnitudes)

    with pytest.raises(
        ErrorValidacionMQTT,
        match="está inactivo",
    ):
        validar_mensaje_mqtt(Mock(), mensaje_valido)
