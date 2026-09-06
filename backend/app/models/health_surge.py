"""
HealthSurge model — daily health-event counts per ward.

Maps to the ``health_surges`` table.
"""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class HealthSurge(Base):
    __tablename__ = "health_surges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward_id: Mapped[str] = mapped_column(String(16), ForeignKey("wards.id"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # ── Daily event counts ───────────────────────────────────────────────
    heatstroke_cases: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hospital_admits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ambulance_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mortality_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationship ─────────────────────────────────────────────────────
    ward = relationship("Ward", back_populates="health_surges")

    def __repr__(self) -> str:
        return (f"<HealthSurge ward={self.ward_id} date={self.date} "
                f"strokes={self.heatstroke_cases} admits={self.hospital_admits}>")
