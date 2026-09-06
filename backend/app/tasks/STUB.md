# Tasks — STUB

This directory will contain **background / scheduled tasks**.

> **Note:** Celery is *not* included in the prototype. For the full build,
> this package will house Celery task definitions. During prototyping, use
> FastAPI `BackgroundTasks` or a simple `asyncio` scheduler instead.

## Planned tasks

| File | Purpose |
|------|---------|
| `ingest_weather.py` | Periodic fetch of weather data from upstream APIs |
| `run_forecast.py` | Trigger ML forecast pipeline on new data arrival |
| `send_alerts.py` | Fan-out alert notifications to subscribed users |
| `cleanup.py` | Purge stale / expired data from the database |
