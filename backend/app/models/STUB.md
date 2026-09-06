# Models — STUB

This directory will contain **SQLAlchemy ORM models** mapped to the database.

## Planned models

| Model | Description |
|-------|-------------|
| `HeatwaveAlert` | Forecast/alert record with severity, time-window, region |
| `WeatherReading` | Raw or aggregated weather observation (temp, humidity, wind) |
| `Zone` | Geographic zone / ward with metadata (population, land-use) |
| `User` | Application user with role & notification prefs |
| `RiskScore` | Computed composite risk score per zone per time-step |

All models will inherit from `database.Base`.
