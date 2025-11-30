# High-Level Overview & Screenshots Guide

## Architecture at a Glance
- **Backend** (`src/backend`): FastAPI app with routers under `api/routers/`, core analysis services in `services/`, and configuration in `config/`. Entrypoint: `api.main:app`.
- **Frontend** (`src/frontend`): React + TypeScript app; components in `src/components/`, API helpers in `src/services/`, shared assets under `public/`.
- **Infra & Docs**: Container orchestration via `docker-compose.yml`; additional references in `docs/ARCHITECTURE.md`, `docs/SYSTEM_DESIGN.md`, and `docs/QUICKSTART.md`.

## Running the Stack Locally
```bash
# Backend (from repo root)
cd src/backend
PYTHONPATH=. uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (new shell)
cd src/frontend
npm install
npm start
```
Access: API docs at `http://localhost:8000/docs`; UI at `http://localhost:3000`.

## Testing & Quality Gates
- Python: `make test` runs pytest in `tests/`; add new backend tests under `tests/` or `src/backend/tests/`.
- Lint/format (backend): `make lint` and `make format` after installing dev deps.
- Frontend: `npm test` in `src/frontend`.

## Screenshot Capture Checklist
Create and store images under `docs/screenshots/` and reference them from `DEMO.md` or `README.md`.
- **Home view**: Main UI with empty form.
- **Review results**: After submitting sample code, showing quality score and suggestions.
- **API docs**: `http://localhost:8000/docs` open in Swagger UI.
- **Health check** (optional): `curl http://localhost:8000/health` response.
When saving files, prefer descriptive names, e.g., `ui-home.png`, `ui-review-result.png`, `api-docs.png`. Update captions in `DEMO.md` to match filenames.
