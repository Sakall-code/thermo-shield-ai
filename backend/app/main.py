"""
thermo-shield-ai — FastAPI application entry point (prototype).
"""

import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.config import settings
from app.database import Base, engine, async_session

# ── Import models so Base.metadata knows about all tables ────────────────
from app.models import Ward, HourlyForecast, HealthSurge, AlertLog  # noqa: F401

logger = logging.getLogger("thermoshield")

# ── Path to seed data ────────────────────────────────────────────────────
PILOT_WARDS_JSON = Path(__file__).resolve().parent / "data" / "pilot_wards.json"


async def _seed_wards() -> None:
    """Load pilot_wards.json into the wards table if it is empty."""
    async with async_session() as session:
        result = await session.execute(select(Ward).limit(1))
        if result.scalars().first() is not None:
            logger.info("Wards table already seeded — skipping.")
            return

        with open(PILOT_WARDS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        wards = []
        for w in data["wards"]:
            wards.append(Ward(
                id=w["id"],
                ward_name=w["ward_name"],
                population=w["population"],
                elderly_ratio=w["elderly_ratio"],
                slum_density_ratio=w["slum_density_ratio"],
                outdoor_labor_ratio=w["outdoor_labor_ratio"],
                mean_ndvi=w["mean_ndvi"],
                mean_ndbi=w["mean_ndbi"],
                wvi_score=w["wvi_score"],
                centroid_lat=w["centroid"]["lat"],
                centroid_lon=w["centroid"]["lon"],
                geom_geojson=json.dumps(w["geometry"]),
            ))

        session.add_all(wards)
        await session.commit()
        logger.info("Seeded %d wards from %s", len(wards), PILOT_WARDS_JSON.name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create tables + seed data.  Shutdown: dispose engine."""
    # -- Startup ----------------------------------------------------------
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created / verified.")

    await _seed_wards()

    yield

    # -- Shutdown ---------------------------------------------------------
    await engine.dispose()


app = FastAPI(
    title="ThermoShield AI",
    version="0.1.0-proto",
    description="Heatwave early-warning & urban heat-island analytics (prototype)",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS – allow the Vite dev-server during local development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": app.version}


# ---------------------------------------------------------------------------
# API Routers
# ---------------------------------------------------------------------------
from app.api.v1.router import api_router
app.include_router(api_router, prefix="/api/v1")

@app.get("/healthz")
async def root_healthz():
    return {"status": "ok"}
