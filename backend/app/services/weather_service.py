"""
Weather service — fetch hourly forecasts from the Open-Meteo API.

Open-Meteo is free, requires no API key, and returns JSON directly.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

# Hourly variables we request from Open-Meteo
_HOURLY_VARS = ",".join([
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "direct_normal_irradiance",
])


@dataclass(slots=True)
class HourlyWeatherRow:
    """One hour of forecast data for a single location."""
    timestamp: datetime
    temperature_c: float       # °C
    humidity_pct: float        # 0-100 %
    wind_speed_kmh: float      # km/h
    solar_radiation_wm2: float # W/m² (direct normal irradiance)


async def get_forecast(
    lat: float,
    lon: float,
    *,
    forecast_days: int | None = None,
) -> list[HourlyWeatherRow]:
    """Fetch an hourly weather forecast from Open-Meteo.

    Parameters
    ----------
    lat, lon : float
        Location in decimal degrees (EPSG:4326).
    forecast_days : int, optional
        Number of days to forecast.  Defaults to ``settings.FORECAST_DAYS``.

    Returns
    -------
    list[HourlyWeatherRow]
        One entry per forecast hour.

    Raises
    ------
    httpx.HTTPStatusError
        If the upstream API returns a non-2xx status.
    """
    days = forecast_days or settings.FORECAST_DAYS

    params: dict[str, str | int | float] = {
        "latitude": lat,
        "longitude": lon,
        "hourly": _HOURLY_VARS,
        "forecast_days": days,
        "timezone": "auto",
        "wind_speed_unit": "kmh",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(settings.OPEN_METEO_BASE_URL, params=params)
        resp.raise_for_status()

    data = resp.json()
    hourly = data["hourly"]

    times = hourly["time"]                         # ISO-8601 strings
    temps = hourly["temperature_2m"]               # °C
    rhs   = hourly["relative_humidity_2m"]          # %
    winds = hourly["wind_speed_10m"]                # km/h
    dnis  = hourly["direct_normal_irradiance"]      # W/m²

    rows: list[HourlyWeatherRow] = []
    for i, ts_str in enumerate(times):
        rows.append(HourlyWeatherRow(
            timestamp=datetime.fromisoformat(ts_str),
            temperature_c=temps[i],
            humidity_pct=rhs[i],
            wind_speed_kmh=winds[i],
            solar_radiation_wm2=dnis[i] if dnis[i] is not None else 0.0,
        ))

    logger.info(
        "Fetched %d hourly rows for (%.4f, %.4f) — %d day(s)",
        len(rows), lat, lon, days,
    )
    return rows
