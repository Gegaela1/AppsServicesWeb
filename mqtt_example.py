
"""Consumidor MQTT con validación y persistencia para el Taller 2."""

import json
import os
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import SessionLocal
from app.schemas.mqtt import MensajeMQTT
from app.services.mqtt_service import (
    ErrorValidacionMQTT,
    procesar_mensaje_mqtt,
)

load_dotenv(override=True)

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "iot/sensors/WQ-003/data")
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")
KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))


def on_connect(client, userdata, flags, reason_code, properties):
    """Se suscribe al tópico cuando la conexión MQTT es exitosa."""
    if reason_code != 0:
        print(f"Error de conexión MQTT: {reason_code}")
        return

    print(f"Conectado al broker {BROKER}:{PORT}")

    resultado, _ = client.subscribe(TOPIC)

    if resultado != mqtt.MQTT_ERR_SUCCESS:
        print(f"No fue posible suscribirse a {TOPIC}: código {resultado}")
        return

    print(f"Suscrito al tópico: {TOPIC}")
    print("Esperando mensajes. Presiona Ctrl+C para finalizar.")


def on_message(client, userdata, message):
    """Valida y persiste los mensajes recibidos por MQTT."""
    received_at = datetime.now(timezone.utc).isoformat()

    try:
        payload = json.loads(message.payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"[{received_at}] JSON inválido: {error}")
        return

    try:
        mensaje = MensajeMQTT.model_validate(payload)
    except ValidationError as error:
        print(f"[{received_at}] Mensaje rechazado por esquema Pydantic.")
        print(error)
        return

    try:
        with SessionLocal() as db:
            cantidad = procesar_mensaje_mqtt(db, mensaje)

        print(
            f"[{received_at}] Mensaje aceptado. "
            f"Sensor: {mensaje.sensor_id}. "
            f"Mediciones guardadas: {cantidad}."
        )

    except ErrorValidacionMQTT as error:
        print(f"[{received_at}] Mensaje rechazado por reglas de negocio: {error}")

    except SQLAlchemyError as error:
        print(f"[{received_at}] Error de base de datos: {error}")

    except Exception as error:
        print(
            f"[{received_at}] Error inesperado al procesar el mensaje: "
            f"{type(error).__name__}: {error}"
        )


def main():
    """Inicia el consumidor MQTT."""
    if not BROKER:
        raise RuntimeError(
            "Falta MQTT_BROKER. Configúralo en el archivo .env."
        )

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD or "")

    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Conectando a {BROKER}:{PORT}...")
    print(f"Tópico configurado: {TOPIC}")

    client.connect(BROKER, PORT, KEEPALIVE)
    client.loop_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nConsumidor detenido por el usuario.")

