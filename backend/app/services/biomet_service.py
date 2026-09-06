"""
Bio-meteorological service — compute WBGT & UTCI from weather variables.

Uses ``pythermalcomfort`` for the ISO 7243 WBGT calculation and the UTCI
polynomial approximation.  Globe temperature is estimated from solar
irradiance so we can work from standard weather-station / forecast data
without dedicated Tg sensors.

Risk-level thresholds are pulled from ``app.config.settings`` so they can
be overridden via ``.env`` or environment variables.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass

from pythermalcomfort.models import utci as _utci_model, wbgt as _wbgt_model
from pythermalcomfort.utilities import wet_bulb_tmp

from app.config import settings

logger = logging.getLogger(__name__)

# ── Risk-level labels ────────────────────────────────────────────────────
NORMAL = "NORMAL"
YELLOW = "YELLOW"
ORANGE = "ORANGE"
RED    = "RED"


@dataclass(slots=True)
class BiometResult:
    """Output of a single WBGT / UTCI computation."""
    wbgt: float          # °C
    utci: float          # °C
    risk_level: str      # NORMAL | YELLOW | ORANGE | RED
    globe_temp: float    # estimated Tg °C (for auditability)
    mean_radiant_temp: float  # estimated Tr °C (for auditability)


# ── Internal helpers ─────────────────────────────────────────────────────

def _estimate_globe_temperature(
    t_air: float,
    solar_radiation: float,
    wind_speed_ms: float,
) -> float:
    """Estimate the black-globe temperature (Tg) from weather data.

    Uses the Liljegren-derived approximation:
        Tg ≈ 0.01498·SR + 1.184·Tdb − 0.0789·Tdb² + 0.000142·Tdb³
             − 0.0073·v¹⁰ + ... (simplified for prototype)

    For a prototype we use the widely-cited simplified Thorsson (2007)
    approximation which is adequate for outdoor urban conditions:
        Tg ≈ Tdb + 0.0175·SR − 0.206·√v10
    """
    v = max(wind_speed_ms, 0.1)  # clamp to avoid division-by-zero edge
    tg = t_air + 0.0175 * solar_radiation - 0.206 * math.sqrt(v)
    return round(tg, 2)


def _estimate_mean_radiant_temp(
    t_air: float,
    solar_radiation: float,
    wind_speed_ms: float,
) -> float:
    """Estimate mean radiant temperature (Tr) for UTCI calculation.

    Approximation from Thorsson et al. (2007) for an outdoor standing
    person under clear sky:
        Tr ≈ Tdb + 0.0420·SR − 0.350·√v10
    """
    v = max(wind_speed_ms, 0.1)
    tr = t_air + 0.0420 * solar_radiation - 0.350 * math.sqrt(v)
    return round(tr, 2)


def _classify_risk(wbgt_value: float) -> str:
    """Map a WBGT value to a risk level using config-driven thresholds."""
    if wbgt_value < settings.WBGT_NORMAL_UPPER:
        return NORMAL
    if wbgt_value < settings.WBGT_YELLOW_UPPER:
        return YELLOW
    if wbgt_value < settings.WBGT_ORANGE_UPPER:
        return ORANGE
    return RED


# ── Public API ───────────────────────────────────────────────────────────

def compute_wbgt_utci(
    t_air: float,
    rh: float,
    wind_speed: float,
    solar_radiation: float,
    *,
    wind_is_kmh: bool = True,
) -> BiometResult:
    """Compute WBGT (Liljegren / ISO 7243) and UTCI from raw weather data.

    Parameters
    ----------
    t_air : float
        Dry-bulb air temperature [°C].
    rh : float
        Relative humidity [%, 0-100].
    wind_speed : float
        Wind speed — km/h by default (set *wind_is_kmh=False* for m/s).
    solar_radiation : float
        Direct normal irradiance [W/m²].
    wind_is_kmh : bool
        If ``True`` (default), *wind_speed* is in km/h and will be
        converted internally to m/s.

    Returns
    -------
    BiometResult
        Dataclass with ``wbgt``, ``utci``, ``risk_level``,
        ``globe_temp``, and ``mean_radiant_temp``.
    """
    # -- Unit conversion ---------------------------------------------------
    v_ms = wind_speed / 3.6 if wind_is_kmh else wind_speed
    v_ms = max(v_ms, 0.1)  # pythermalcomfort UTCI requires v > 0

    # -- Intermediate estimates -------------------------------------------
    tg = _estimate_globe_temperature(t_air, solar_radiation, v_ms)
    tr = _estimate_mean_radiant_temp(t_air, solar_radiation, v_ms)

    # -- Natural wet-bulb temperature (psychrometric) ---------------------
    twb_val = float(wet_bulb_tmp(tdb=t_air, rh=rh))

    # -- WBGT via ISO 7243 (with solar load) ------------------------------
    wbgt_result = _wbgt_model(
        twb=twb_val,
        tg=tg,
        tdb=t_air,
        with_solar_load=True,
        round_output=False,
    )
    wbgt_value = float(wbgt_result.wbgt)

    # -- UTCI --------------------------------------------------------------
    try:
        utci_result = _utci_model(
            tdb=t_air,
            tr=tr,
            v=v_ms,
            rh=rh,
            limit_inputs=False,
            round_output=False,
        )
        utci_value = float(utci_result.utci)
    except Exception:
        # UTCI polynomial can fail for extreme inputs; fall back gracefully
        logger.warning(
            "UTCI computation failed for tdb=%.1f tr=%.1f v=%.1f rh=%.0f; "
            "returning NaN",
            t_air, tr, v_ms, rh,
        )
        utci_value = float("nan")

    # -- Risk classification -----------------------------------------------
    risk = _classify_risk(wbgt_value)

    return BiometResult(
        wbgt=round(wbgt_value, 2),
        utci=round(utci_value, 2),
        risk_level=risk,
        globe_temp=tg,
        mean_radiant_temp=tr,
    )
