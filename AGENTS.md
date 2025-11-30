# AGENTS.md

> **System Instruction**: This file is the **Source of Truth** for all AI agents working on this repository. You MUST read and follow these guidelines before making any changes.

---

## 1. 🧠 Core Principles

1. **Research First**: Never start coding without understanding the context. Read related files, documentation, and tests first.
2. **Plan Before Action**: Always create or update `implementation_plan.md` before making significant changes.
3. **Test-Driven**: No code is complete without tests. 100% coverage for new logic is mandatory.
4. **Document Everything**: Update documentation (`docs/`) alongside code. If you change behavior, update the docs.
5. **Atomic Changes**: Make small, verifiable changes. Do not break the build.

---

## 2. 🏗️ Project Structure

### Allowed Root Files

Only these files are allowed in the root directory:

- `AGENTS.md` (This file)
- `README.md`
- `Makefile`
- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt` / `requirements-dev.txt`
- `setup.py` / `pyproject.toml`
- `.gitignore` / `.dockerignore`
- `.env.example`

### Directory Layout

- `src/backend/`: FastAPI application (Routers, Services, Schemas).
- `src/frontend/`: React application (Components, Services, Hooks).
- `tests/`: Mirrored structure of `src/` for unit and integration tests.
- `docs/`: All documentation (Architecture, Guides, API).
- `config/`: Configuration files (Logging, Settings).
- `.github/`: CI/CD workflows and templates.

---

## 3. 🔄 Workflows

### Phase 1: Exploration

- **Goal**: Understand the task and codebase.
- **Actions**:
  - Read `task.md` (if exists) or user request.
  - Search for relevant files using `find_by_name` or `grep_search`.
  - Read `ARCHITECTURE.md` or `docs/` to understand the system.

### Phase 2: Planning

- **Goal**: Define *what* to do and *how* to verify it.
- **Actions**:
  - Create/Update `implementation_plan.md`.
  - List affected files.
  - Define verification steps (Automated tests, Manual checks).
  - **Request User Review** via `notify_user`.

### Phase 3: Execution

- **Goal**: Implement the changes.
- **Actions**:
  - **Backend**:
    - Write tests in `tests/backend/`.
    - Implement logic in `src/backend/`.
    - Run `make test` to verify.
  - **Frontend**:
    - Write tests in `src/frontend/**/*.test.tsx`.
    - Implement components in `src/frontend/`.
    - Run `npm test` to verify.

### Phase 4: Verification & Documentation

- **Goal**: Ensure quality and update knowledge base.
- **Actions**:
  - Run full test suite.
  - Update `docs/` if architecture or features changed.
  - Create `walkthrough.md` to demonstrate success.
  - Update `task.md` to mark completion.

---

## 4. 📝 Coding Standards

### General

- **Functions**: Keep under ~30 lines. Single responsibility.
- **Logging**: Use structured logging (JSON). No `print()` statements.
- **Error Handling**: Use custom exceptions. Chain exceptions (`raise ... from ...`).

### Python (Backend)

- **Style**: PEP 8.
- **Typing**: Strict type hints required for all functions and classes.
- **Tools**: `black`, `isort`, `flake8`, `mypy`.
- **Patterns**:
  - Use Pydantic for data validation.
  - Use Dependency Injection for services.

### TypeScript/React (Frontend)

- **Style**: Airbnb style guide.
- **Typing**: No implicit `any`. Define interfaces for all props and state.
- **Components**: Functional components with Hooks.
- **Testing**: React Testing Library.

---

## 5. 🚫 Anti-Patterns (Do NOT Do This)

- **Do NOT** create new files in the root directory (unless explicitly allowed).
- **Do NOT** leave `TODO` or `FIXME` comments without a tracking issue.
- **Do NOT** hardcode secrets. Use environment variables.
- **Do NOT** skip tests "to save time".
- **Do NOT** modify `AGENTS.md` unless instructed to improve agent processes.

---

## 6. 🛠️ Tooling Reference

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make test` | Run backend tests |
| `make lint` | Run code quality checks |
| `npm start` | Start frontend dev server |
| `npm test` | Run frontend tests |

---

> **Final Note**: Your goal is to be a helpful, precise, and safe coding partner. When in doubt, ask the user.
