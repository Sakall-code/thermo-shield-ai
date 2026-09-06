"""
AlertLog model — issued heat-alert records per ward.

Maps to the ``alert_logs`` table.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AlertLog(Base):
    __tablename__ = "alert_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward_id: Mapped[str] = mapped_column(String(16), ForeignKey("wards.id"), nullable=False, index=True)

    # ── Alert content ────────────────────────────────────────────────────
    alert_level: Mapped[str] = mapped_column(
        String(16), nullable=False,
        comment="yellow | orange | red",
    )
    headline: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # ── Temporal window ──────────────────────────────────────────────────
    issued_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # ── Acknowledgement ──────────────────────────────────────────────────
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relationship ─────────────────────────────────────────────────────
    ward = relationship("Ward", back_populates="alert_logs")

    def __repr__(self) -> str:
        return (f"<AlertLog ward={self.ward_id} level={self.alert_level!r} "
                f"issued={self.issued_at}>")
