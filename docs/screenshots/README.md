# Screenshots Guide

Use this checklist to capture and store screenshots. Save files in this folder and link them from `DEMO.md` or `README.md` as needed.

Recommended shots
- `ui-home.png`: Frontend landing view with empty form.
- `ui-review-result.png`: After submitting sample code showing score, metrics, and suggestions.
- `ui-error.png` (optional): Validation or error state, if applicable.
- `api-docs.png`: Swagger UI at `http://localhost:8000/docs`.
- `health-check.png` (optional): Terminal output of `curl http://localhost:8000/health`.

Capture steps (local dev)
1) Start backend: `cd src/backend && PYTHONPATH=. uvicorn api.main:app --reload --host 0.0.0.0 --port 8000`.
2) Start frontend: `cd src/frontend && npm start`.
3) Open the browser to `http://localhost:3000` and take `ui-home.png`.
4) Paste a sample snippet (e.g., Python code with a hardcoded password), click **Review**, wait for results, and capture `ui-review-result.png`.
5) Visit `http://localhost:8000/docs` and capture `api-docs.png`.
6) Optional: run `curl http://localhost:8000/health` and screenshot the terminal for `health-check.png`.

Tips
- Use consistent browser zoom (100%) and a neutral theme.
- Keep filenames lowercase with hyphens; avoid spaces.
- If updating images, replace the existing files to keep links stable.
