"""
Application configuration loaded from environment / .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # ── General ──────────────────────────────────────────────────────────
    APP_NAME: str = "ThermoShield AI"
    DEBUG: bool = True

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./thermoshield_prototype.db"
    POSTGRES_URL: str = "placeholder"
    REDIS_URL: str = "placeholder"

    # ── Prototype Settings ───────────────────────────────────────────────
    PROJECT_NAME: str = "THERMO-SHIELD AI"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"

    # ── External Services ────────────────────────────────────────────────
    TWILIO_SID: str = "placeholder"
    TELEGRAM_BOT_TOKEN: str = "placeholder"

    # ── CORS ─────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # ── Open-Meteo ───────────────────────────────────────────────────────
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    FORECAST_DAYS: int = 5

    # ── WBGT risk-level thresholds (°C, ISO 7243 / Liljegren) ────────────
    WBGT_NORMAL_UPPER: float = 28.0   # < 28 → NORMAL
    WBGT_YELLOW_UPPER: float = 31.0   # 28 – 30.9 → YELLOW
    WBGT_ORANGE_UPPER: float = 34.0   # 31 – 33.9 → ORANGE
    #                                   ≥ 34 → RED
    
    WBGT_ORANGE_THRESHOLD: float = 28.0
    WBGT_RED_THRESHOLD: float = 31.0
    HEALTH_SURGE_RED_THRESHOLD: float = 25.0

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
