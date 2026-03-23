# Ignyt

Gamified learning (Phase 1). Architecture and APIs: [docs/SPEC.md](docs/SPEC.md).

## Quick start (Podman)

```bash
podman-compose up -d
podman exec -it ignyt-api alembic upgrade head
podman exec -it ignyt-api python -m app.seed.chapter1
```

- API: http://localhost:8001  
- Frontend: http://localhost:5173  
- Postgres: localhost:5433  

## Local dev (without Podman)

Backend (Python 3.12 recommended):

```bash
cd backend && python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://...
alembic upgrade head
python -m app.seed.chapter1
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend && npm install && npm run dev
```

Point `vite.config.ts` proxy at your API port.

## Tests

```bash
cd backend && source .venv/bin/activate && pytest
```

SQLite is used by default; set `TEST_DATABASE_URL` for PostgreSQL.
