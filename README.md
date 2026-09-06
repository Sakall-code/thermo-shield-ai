# thermo-shield-ai

> Heatwave early-warning & urban heat-island analytics — **prototype scaffold**

## Repository layout

```
thermo-shield-ai/
├── backend/               # FastAPI + SQLAlchemy (async, SQLite for prototype)
│   ├── main.py            # App entry-point, CORS, health endpoint
│   ├── config.py          # pydantic-settings configuration
│   ├── database.py        # Async engine & session factory
│   └── app/
│       ├── api/v1/endpoints/   # Route handlers (STUB)
│       ├── models/             # ORM models (STUB)
│       ├── schemas/            # Pydantic schemas (STUB)
│       ├── services/           # Business logic (STUB)
│       └── tasks/              # Background tasks (STUB)
│
└── frontend/              # Vite + React + TypeScript + Tailwind CSS v4
    └── src/
        ├── App.tsx         # Landing placeholder
        └── index.css       # Tailwind entry
```

## Quick start

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install   # already done during scaffold
npm run dev
```

## What's intentionally excluded (prototype)

- Docker / docker-compose
- Celery / task queue
- Alembic migrations
- PostGIS / spatial database

Directories marked with a `STUB.md` are placeholders — read those files for
details on what each module will contain in the full build.
