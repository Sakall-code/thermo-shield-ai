"""
Ward model — one row per Ahmedabad municipal ward.

Maps to the ``wards`` table.  Geometry is stored as a GeoJSON TEXT column
for the prototype; the full build will use a native PostGIS column.
"""

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Ward(Base):
    __tablename__ = "wards"

    id: Mapped[str] = mapped_column(String(16), primary_key=True, comment="e.g. AMC-W01")
    ward_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)

    # ── Vulnerability ratios (0-1) ───────────────────────────────────────
    elderly_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    slum_density_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    outdoor_labor_ratio: Mapped[float] = mapped_column(Float, nullable=False)

    # ── Remote-sensing indices ───────────────────────────────────────────
    mean_ndvi: Mapped[float] = mapped_column(Float, nullable=False)
    mean_ndbi: Mapped[float] = mapped_column(Float, nullable=False)

    # ── Composite vulnerability score (pre-computed) ─────────────────────
    wvi_score: Mapped[float] = mapped_column(Float, nullable=False)

    # ── Location ─────────────────────────────────────────────────────────
    centroid_lat: Mapped[float] = mapped_column(Float, nullable=False)
    centroid_lon: Mapped[float] = mapped_column(Float, nullable=False)

    # STUB: swap for GeoAlchemy2 Geometry(MULTIPOLYGON,4326) in full build
    geom_geojson: Mapped[str] = mapped_column(Text, nullable=False,
                                               comment="GeoJSON MultiPolygon as TEXT — prototype only")

    # ── Relationships ────────────────────────────────────────────────────
    hourly_forecasts = relationship("HourlyForecast", back_populates="ward",
                                    cascade="all, delete-orphan")
    health_surges = relationship("HealthSurge", back_populates="ward",
                                 cascade="all, delete-orphan")
    alert_logs = relationship("AlertLog", back_populates="ward",
                              cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Ward {self.id} {self.ward_name!r} wvi={self.wvi_score:.4f}>"
