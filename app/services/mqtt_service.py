
from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.sensor_repository import (
    obtener_magnitudes_de_sensor,
    obtener_sensor_por_codigo,
)
from app.repositories.medicion_repository import guardar_mediciones
from app.schemas.mqtt import MensajeMQTT


class ErrorValidacionMQTT(ValueError):
    """Error de negocio al validar un mensaje MQTT."""


def validar_mensaje_mqtt(
    db: Session,
    mensaje: MensajeMQTT,
) -> None:
    """Valida el sensor, las magnitudes, las unidades y los rangos."""

    sensor = obtener_sensor_por_codigo(db, mensaje.sensor_id)

    if sensor is None:
        raise ErrorValidacionMQTT(
            f"El sensor '{mensaje.sensor_id}' no existe"
        )

    if not sensor.activo:
        raise ErrorValidacionMQTT(
            f"El sensor '{mensaje.sensor_id}' está inactivo"
        )

    magnitudes_configuradas = obtener_magnitudes_de_sensor(
        db,
        sensor.id,
    )

    configuracion_por_nombre = {
        magnitud.magnitud: magnitud
        for magnitud in magnitudes_configuradas
    }

    for nombre, medicion in mensaje.measurements.items():
        configuracion = configuracion_por_nombre.get(nombre)

        if configuracion is None:
            raise ErrorValidacionMQTT(
                f"La magnitud '{nombre}' no está configurada "
                f"para el sensor '{mensaje.sensor_id}'"
            )

        if medicion.unit != configuracion.unidad:
            raise ErrorValidacionMQTT(
                f"Unidad incorrecta para '{nombre}': "
                f"se esperaba '{configuracion.unidad}' "
                f"y se recibió '{medicion.unit}'"
            )

        valor = Decimal(str(medicion.value))

        if (
            configuracion.valor_minimo is not None
            and valor < configuracion.valor_minimo
        ):
            raise ErrorValidacionMQTT(
                f"El valor de '{nombre}' está por debajo "
                f"del mínimo permitido "
                f"({configuracion.valor_minimo})"
            )

        if (
            configuracion.valor_maximo is not None
            and valor > configuracion.valor_maximo
        ):
            raise ErrorValidacionMQTT(
                f"El valor de '{nombre}' supera el máximo "
                f"permitido ({configuracion.valor_maximo})"
            )

from app.repositories.medicion_repository import guardar_mediciones

def procesar_mensaje_mqtt(
    db: Session,
    mensaje: MensajeMQTT,
) -> int:
    """Valida y guarda las mediciones de un mensaje MQTT."""

    # Primero validamos todas las reglas de negocio.
    validar_mensaje_mqtt(db, mensaje)

    # Recuperamos el sensor y sus magnitudes configuradas.
    sensor = obtener_sensor_por_codigo(db, mensaje.sensor_id)

    # La validación anterior ya comprobó que el sensor existe.
    if sensor is None:
        raise ErrorValidacionMQTT(
            f"El sensor '{mensaje.sensor_id}' no existe"
        )

    magnitudes_configuradas = obtener_magnitudes_de_sensor(
        db,
        sensor.id,
    )

    configuracion_por_nombre = {
        magnitud.magnitud: magnitud
        for magnitud in magnitudes_configuradas
    }

    mediciones_para_guardar = []

    for nombre, medicion in mensaje.measurements.items():
        configuracion = configuracion_por_nombre[nombre]

        mediciones_para_guardar.append(
            (
                configuracion,
                Decimal(str(medicion.value)),
            )
        )

    registros = guardar_mediciones(
        db=db,
        mediciones=mediciones_para_guardar,
        timestamp_utc=mensaje.timestamp,
    )

    return len(registros)
