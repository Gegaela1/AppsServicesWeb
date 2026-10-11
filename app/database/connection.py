
import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Cargar las variables definidas en el archivo .env
load_dotenv(override=True)


def obtener_url_base_datos() -> URL:
    """Construye la URL de conexión usando las variables de entorno."""
    variables_requeridas = (
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    )

    faltantes = [
        variable
        for variable in variables_requeridas
        if os.getenv(variable) is None
    ]

    if faltantes:
        raise RuntimeError(
            "Faltan variables de configuración: "
            + ", ".join(faltantes)
        )

    return URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
        database=os.environ["POSTGRES_DB"],
    )


class Base(DeclarativeBase):
    """Clase base para los modelos ORM de la aplicación."""


engine = create_engine(
    obtener_url_base_datos(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=5,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Proporciona una sesión y garantiza su cierre."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def comprobar_conexion() -> str:
    """Comprueba la conexión mediante una consulta de solo lectura."""
    with engine.connect() as conexion:
        resultado = conexion.execute(
            text("SELECT current_database()")
        )
        return resultado.scalar_one()
