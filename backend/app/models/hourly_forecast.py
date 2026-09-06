"""
HourlyForecast model — one row per ward per forecast hour.

Maps to the ``hourly_forecasts`` table.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class HourlyForecast(Base):
    __tablename__ = "hourly_forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward_id: Mapped[str] = mapped_column(String(16), ForeignKey("wards.id"), nullable=False, index=True)

    # ── Forecast timestamp (the hour being predicted) ────────────────────
    forecast_ts: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    # ── Weather variables ────────────────────────────────────────────────
    temperature_c: Mapped[float] = mapped_column(Float, nullable=False, comment="°C")
    humidity_pct: Mapped[float] = mapped_column(Float, nullable=False, comment="0-100 %")
    wind_speed_kmh: Mapped[float] = mapped_column(Float, nullable=False, comment="km/h")

    # ── Derived heat metrics ─────────────────────────────────────────────
    heat_index: Mapped[float] = mapped_column(Float, nullable=False, comment="Apparent temp °C")
    risk_level: Mapped[str] = mapped_column(
        String(16), nullable=False, default="low",
        comment="low | moderate | high | extreme",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationship ─────────────────────────────────────────────────────
    ward = relationship("Ward", back_populates="hourly_forecasts")

    def __repr__(self) -> str:
        return (f"<HourlyForecast ward={self.ward_id} ts={self.forecast_ts} "
                f"temp={self.temperature_c}°C risk={self.risk_level}>")
