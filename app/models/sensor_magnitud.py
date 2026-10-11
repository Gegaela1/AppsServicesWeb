
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class SensorMagnitud(Base):
    """Representa una magnitud y unidad asociadas a un sensor."""

    __tablename__ = "sensor_magnitudes"

    __table_args__ = (
        UniqueConstraint(
            "sensor_id",
            "magnitud",
            name="uq_sensor_magnitudes_sensor_magnitud",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    sensor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "sensores.id",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    magnitud: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    unidad: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    valor_minimo: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 4),
        nullable=True,
    )

    valor_maximo: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 4),
        nullable=True,
    )
