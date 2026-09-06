# STUB: replace with real DLNM cross-basis spline fit from ml_pipeline/notebooks/03_dlnm... in full build.
"""
Health impact / surge prediction model (prototype).
"""

import math
from dataclasses import dataclass
from typing import Sequence

@dataclass(slots=True)
class HealthSurgePrediction:
    projected_excess_deaths: int
    projected_er_surge_percent: float
    trigger_red_alert: bool


def mock_surge_prediction(
    wbgt_series_5day: Sequence[float], 
    wvi_score: float
) -> HealthSurgePrediction:
    """
    Mocks a projected health surge based on a 5-day WBGT forecast and the ward's
    vulnerability index (WVI).
    
    Parameters
    ----------
    wbgt_series_5day : Sequence[float]
        A series of hourly WBGT predictions over 5 days (length typically 120).
    wvi_score : float
        The Ward Vulnerability Index [0, 1].
        
    Returns
    -------
    HealthSurgePrediction
        Projected excess deaths, ER surge percent, and an alert trigger boolean.
    """
    # Sum of degrees exceeding 31°C across the 5 days
    exceedance_sum = sum(max(0.0, wbgt - 31.0) for wbgt in wbgt_series_5day)
    
    # Plausible mock formula: scale ER surge by the exceedance heat load and vulnerability
    # E.g. 20 cumulative degree-hours over 31°C * 0.4 WVI * 2.5 factor = 20% surge
    er_surge_factor = 2.5
    projected_er_surge_percent = exceedance_sum * er_surge_factor * wvi_score
    
    # Estimate excess deaths based on the surge and vulnerability
    # E.g. 20% surge * 0.15 * 0.4 WVI = 1.2 deaths (round up or probabilistically)
    expected_deaths_float = projected_er_surge_percent * 0.15 * wvi_score
    projected_excess_deaths = math.ceil(expected_deaths_float) if expected_deaths_float > 0.5 else 0
    
    # Check if ER surge is critical
    trigger_red_alert = projected_er_surge_percent >= 25.0
    
    return HealthSurgePrediction(
        projected_excess_deaths=projected_excess_deaths,
        projected_er_surge_percent=round(projected_er_surge_percent, 1),
        trigger_red_alert=trigger_red_alert,
    )
