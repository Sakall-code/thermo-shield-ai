"""
Convenience re-exports so the rest of the app can do::

    from app.models import Ward, HourlyForecast, HealthSurge, AlertLog
"""

from app.models.ward import Ward
from app.models.hourly_forecast import HourlyForecast
from app.models.health_surge import HealthSurge
from app.models.alert_log import AlertLog

__all__ = ["Ward", "HourlyForecast", "HealthSurge", "AlertLog"]
