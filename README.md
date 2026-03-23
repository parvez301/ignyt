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

## Deploy frontend on Vercel

1. Import this repo in Vercel.
2. Set project root to `frontend`.
3. Build settings:
   - Install command: `npm install`
   - Build command: `npm run build`
   - Output directory: `dist`
4. Add environment variable in Vercel:
   - `VITE_API_BASE_URL=https://<your-backend-domain>/api`

The backend (FastAPI + PostgreSQL) should be deployed separately (Railway/Render/Fly/etc.).
Set backend CORS to include your Vercel domain, for example:

`CORS_ORIGINS=https://<your-project>.vercel.app`

## Deploy backend on Render

This repo includes `render.yaml` for Blueprint deploy.

1. In Render, choose **New +** -> **Blueprint**.
2. Point to this repository (`parvez301/ignyt`).
3. Render will create:
   - PostgreSQL database `ignyt-db`
   - Web service `ignyt-api` from `backend/`
4. After first deploy, set backend env var:
   - `CORS_ORIGINS=https://<your-project>.vercel.app`
5. Open Render Shell for `ignyt-api` and run one-time seed:
   - `python -m app.seed.chapter1`

Backend URL will be like:
`https://ignyt-api.onrender.com`

Then in Vercel set:
`VITE_API_BASE_URL=https://ignyt-api.onrender.com/api`
