# Endpoints — STUB

This directory will contain the **FastAPI route handlers** for API v1.

## Planned modules

| File | Purpose |
|------|---------|
| `heatwave.py` | CRUD + query endpoints for heatwave alerts & forecasts |
| `weather.py` | Proxy / cache for upstream weather-data APIs (IMD, OpenMeteo) |
| `zones.py` | Urban heat-island zone CRUD & geospatial queries |
| `users.py` | Auth, profile, notification-preferences |
| `analytics.py` | Aggregated risk scores, time-series analytics |

Each file will expose an `APIRouter` that `main.py` includes.
