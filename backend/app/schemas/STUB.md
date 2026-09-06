# Schemas — STUB

This directory will contain **Pydantic schemas** for request/response validation.

## Planned schemas

| File | Purpose |
|------|---------|
| `heatwave.py` | `HeatwaveAlertCreate`, `HeatwaveAlertRead`, filter params |
| `weather.py` | `WeatherReadingIn`, `WeatherReadingOut` |
| `zone.py` | `ZoneCreate`, `ZoneRead`, GeoJSON helpers |
| `user.py` | `UserCreate`, `UserRead`, `TokenPayload` |
| `analytics.py` | `RiskScoreOut`, time-series response envelopes |

Schemas are kept separate from ORM models to decouple the API contract from storage.
