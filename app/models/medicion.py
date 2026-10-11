
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Medicion(Base):
    """Representa una medición registrada para una magnitud de un sensor."""

    __tablename__ = "mediciones"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    sensor_magnitud_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "sensor_magnitudes.id",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    timestamp_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    fecha_recepcion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("NOW()"),
    )
