
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Sensor(Base):
    """Representa un sensor registrado en la base de datos."""

    __tablename__ = "sensores"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    codigo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    categoria: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    ubicacion: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
