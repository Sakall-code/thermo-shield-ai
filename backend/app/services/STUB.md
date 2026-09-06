# Services — STUB

This directory will contain **business-logic / service-layer** modules.

## Planned services

| File | Purpose |
|------|---------|
| `forecast.py` | ML inference pipeline — load model, run prediction, return risk |
| `weather_ingest.py` | Fetch & normalise data from external weather APIs |
| `alerting.py` | Threshold evaluation → generate / escalate heatwave alerts |
| `geocoding.py` | Forward/reverse geocoding helpers |
| `notification.py` | Push / SMS / email notification dispatch |

Services are called by endpoint handlers and background tasks; they never import FastAPI directly.
