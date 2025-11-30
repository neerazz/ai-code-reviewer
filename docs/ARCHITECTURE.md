# AI Code Reviewer – Architecture

This document captures the current architecture, execution flow, and component layout of the AI Code Reviewer project based on the checked-in code.

## System Overview
- **Frontend**: React + TypeScript SPA located at `src/frontend`, built with Create React App.
- **Backend**: FastAPI application under `src/backend` exposing REST endpoints for code review.
- **Composition**: Stateless HTTP API that performs static analysis and optionally augments results with an LLM provider (Anthropic or OpenAI). The UI calls the API directly; there is no database or queue.
- **Docs/Tests**: Documentation lives in `docs/`; API smoke tests live in `tests/`.

## Request/Response Flow
1. **User action**: Code is entered in the UI (`src/frontend/src/App.tsx`) and submitted.
2. **Client call**: `reviewCode` in `src/frontend/src/services/api.ts` issues `POST http://localhost:8000/review` with the code payload.
3. **API gateway**: `src/backend/api/main.py` configures CORS and mounts the review router.
4. **Routing & validation**: `src/backend/api/routers/review.py` validates the request (`CodeSnippet` schema), logs the request, and orchestrates analysis.
5. **Static analysis**: `CodeAnalyzer` (`src/backend/services/code_analyzer.py`) detects language, gathers metrics, identifies issues, computes complexity, and derives a quality score.
6. **LLM analysis**: `LLMService` (`src/backend/services/llm_service.py`) builds a review prompt and calls the configured provider (Anthropic/OpenAI) or returns a mock response when no API key is available.
7. **Aggregation**: The router merges static and AI suggestions, formats a markdown-like review string, and returns a `ReviewResponse` JSON payload.
8. **UI rendering**: `ReviewResult` (`src/frontend/src/components/ReviewResult.tsx`) renders the score, metrics, review text, and suggestions.

## Backend Components (`src/backend`)
- **Entry point**: `api/main.py` creates the FastAPI app, sets CORS, registers routers, and exposes `/` and `/health` endpoints.
- **Routers**: `api/routers/review.py` handles `POST /review`, enforces non-empty code, and joins static + AI outputs.
- **Schemas**: `api/schemas/review.py` defines `CodeSnippet` (input) and `ReviewResponse` (output) Pydantic models.
- **Services**:
  - `services/code_analyzer.py`: Regex-based language detection, metrics (`total_lines`, `comment_lines`, `max_line_length`, etc.), issue detection (security, style, TODO/FIXME), complexity scoring, and overall quality scoring. Exposed via `get_code_analyzer()` singleton.
  - `services/llm_service.py`: Provider selection, prompt construction, Anthropic/OpenAI clients, response parsing, and mock fallback. Exposed via `get_llm_service()` singleton.
- **Config**: `config/settings.py` loads environment via `pydantic-settings` (LLM provider/model, API keys, log level, host/port).
- **Utils**: `utils/logger.py` sets up console logging.
- **Tests**: `tests/test_api.py` (root `tests/`) performs smoke tests against `/` and `/health`.

## Frontend Components (`src/frontend`)
- **Entry point**: `src/index.tsx` bootstraps the app.
- **Stateful shell**: `src/App.tsx` manages code input, loading/error states, invokes `reviewCode`, and conditionally renders results or status banners.
- **Components**:
  - `components/CodeInputForm.tsx`: Controlled textarea, submit/clear actions, disabled states while loading.
  - `components/ReviewResult.tsx`: Displays quality score card, review text, suggestions list, and metrics grid.
- **Services**: `services/api.ts` defines `reviewCode`, calling the backend with JSON payloads.
- **Styling/Tooling**: Create React App with Tailwind CSS classes in component markup; tests scaffolded via React Testing Library (`src/App.test.tsx`).

## Supporting Directories
- `src/ml`, `src/extensions`, `src/infrastructure`: Placeholders with README stubs for future ML models, IDE/browser extensions, and infrastructure artifacts.
- `docs/`: Project documentation (architecture, guides, reports, screenshots). `docs/ARCHITECTURE_AND_FLOW.md` and `docs/HIGHLEVEL_OVERVIEW.md` provide additional execution-flow references.
- `config/` (to be used): Configuration files such as `alembic.ini` are placed here.
- `.github/`: CI workflows (currently point to the legacy layout and should be updated when pipelines are revived).

## Data Contracts
- **Request (`POST /review`)**: `{ "code": string, "language"?: string, "context"?: string }` (code required).
- **Response**: `{ review: string, suggestions: string[], quality_score: int, language: string, metrics: { total_lines, code_lines, comment_lines, blank_lines, max_line_length, avg_line_length }, issues_count: int }`. AI suggestions may be mock data if no API key is configured.

## Technology Stack
- **Backend**: Python 3.11, FastAPI 0.109.0, Uvicorn 0.27.0, Pydantic 2.5.3, Anthropic SDK 0.18.1, OpenAI SDK 1.10.0.
- **Frontend**: React 18.2, TypeScript 4.9, React Scripts 5.0.1, Tailwind CSS 3.3.
- **Tooling/Infra**: Docker/Docker Compose, Makefile helpers, GitHub Actions (CI stubs), pytest (smoke tests), npm scripts for frontend build/test.

## Operational Notes
- **Environment**: `.env.example` at the repo root seeds LLM provider/model/key settings. Without API keys the backend returns mock AI suggestions.
- **Ports**: Backend defaults to `0.0.0.0:8000`; frontend targets `http://localhost:8000`.
- **Extensibility**: Add new endpoints under `src/backend/api/routers`, extend static checks in `CodeAnalyzer`, or support new LLM providers in `LLMService`. Frontend components/hooks live under `src/frontend/src`.
