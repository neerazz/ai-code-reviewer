# Project Structure Guide

This document describes the repository layout, key directories, and where to find important files.

## Root Layout
```
ai-code-reviewer/
├── AGENTS.md                 # Working agreement for contributors/agents
├── config/                   # Configuration artifacts (e.g., alembic.ini)
├── docs/                     # Documentation (architecture, guides, reports, screenshots)
├── src/
│   ├── backend/              # FastAPI application
│   ├── frontend/             # React application
│   ├── extensions/           # Placeholder for browser/IDE extensions
│   ├── infrastructure/       # Placeholder for infra tooling
│   └── ml/                   # Placeholder for ML assets
├── tests/                    # Root-level tests (mirrors src/)
├── .github/                  # CI/CD workflows
├── Dockerfile                # Backend/tooling image
├── docker-compose.yml        # Local orchestration
├── Makefile                  # Common tasks
├── requirements.txt          # Python runtime dependencies
├── requirements-dev.txt      # Python dev/test dependencies
├── setup.py                  # Package metadata
├── .env.example              # Environment variable template
├── .gitignore / .dockerignore
└── LICENSE
```

## Documentation (`docs/`)
- Architecture and execution flow: `docs/ARCHITECTURE.md`, `docs/ARCHITECTURE_AND_FLOW.md`, `docs/HIGHLEVEL_OVERVIEW.md`
- Guides and references: `docs/GETTING_STARTED.md`, `docs/QUICKSTART.md`, `docs/DEMO.md`, `docs/USER_GUIDE.md`, `docs/DEVELOPER_GUIDE.md`, `docs/CONTRIBUTING.md`, `docs/API_KEYS.md`
- Reports/summaries: `docs/PROJECT_SUMMARY.md`, `docs/COMPLETION_SUMMARY.md`, `docs/FINAL_COMPLETION_REPORT.md`, `docs/TESTING_VERIFICATION_REPORT.md`
- Assets: `docs/screenshots/` holds screenshot guidance and image placeholders.

## Configuration (`config/`)
- `config/alembic.ini`: Placeholder Alembic configuration for future database migrations.

## Backend (`src/backend`)
- **Entrypoint**: `api/main.py` creates the FastAPI app, configures CORS, and exposes `/` and `/health`.
- **Routers**: `api/routers/` currently serves `POST /review` orchestrating static + AI analysis.
- **Schemas**: `api/schemas/` defines request/response Pydantic models (e.g., `CodeSnippet`, `ReviewResponse`).
- **Services**:
  - `services/code_analyzer.py`: Language detection, metrics, issue detection, complexity and quality scoring.
  - `services/llm_service.py`: Prompt building and provider calls (Anthropic/OpenAI) with a mock fallback.
- **Config/Utils**: `config/settings.py` (environment-backed settings), `utils/logger.py` (console logging).
- **Dependencies**: `requirements.txt` lists backend Python packages.

## Frontend (`src/frontend`)
- **Entrypoint**: `src/index.tsx` bootstraps the React app.
- **App shell**: `src/App.tsx` manages form state, API calls, loading/error handling, and renders results.
- **Components**: `src/components/CodeInputForm.tsx`, `src/components/ReviewResult.tsx`.
- **Services**: `src/services/api.ts` calls `POST http://localhost:8000/review`.
- **Styling/Tooling**: CRA with Tailwind classes in JSX, tests scaffolded in `src/App.test.tsx`.

## Other `src` Folders
- `src/extensions/`: Placeholder README for future browser/IDE extensions.
- `src/infrastructure/`: Placeholder README for future infrastructure assets (K8s, Terraform, etc.).
- `src/ml/`: Placeholder README for future ML models and training assets.

## Tests (`tests/`)
- `tests/test_api.py`: Smoke tests for `/` and `/health`, adding `src/backend` to `PYTHONPATH` for imports.

## Tooling & Config Files
- `.env.example`: Copy to `.env` in the repo root to configure LLM provider/model/API keys.
- `docker-compose.yml`: Local stack bringing up backend and frontend containers.
- `Makefile`: Helper targets (`make install`, `make test`, `make lint`, etc.).

## Quick Reference
- **API endpoints**: `src/backend/api/routers/`
- **Business logic**: `src/backend/services/`
- **Frontend components**: `src/frontend/src/components/`
- **Docs**: `docs/`
- **Env config**: `src/backend/config/settings.py`
