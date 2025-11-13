# Project Structure Documentation

This document explains each directory and key files in the AI Code Reviewer project.

## Root Directory

```
ai-code-reviewer/
├── .github/              # GitHub configuration
├── ai-code-reviewer/     # Main application code
├── .env.example          # Environment variables template
├── docker-compose.yml    # Docker orchestration
├── README.md             # Main documentation
├── GETTING_STARTED.md    # Setup guide
├── API_KEYS.md          # API key instructions
├── CONTRIBUTING.md       # Contribution guidelines
├── ARCHITECTURE.md       # Technical architecture
└── DEMO.md              # Live demo examples
```

---

## `.github/` - GitHub Configuration

**Purpose**: GitHub-specific configuration and automation

### `workflows/`

**`ci.yml`**: Continuous Integration/Continuous Deployment pipeline
- Runs on every push to main/develop
- Tests backend (Python linting, tests)
- Tests frontend (npm build, tests)
- Builds Docker images

**`pages.yml`**: GitHub Pages deployment
- Publishes documentation to GitHub Pages
- Runs on push to main branch
- Creates static documentation site

**Usage**:
- These run automatically on GitHub
- Check Actions tab to see workflow runs
- Configure branch protection to require passing CI

---

## `ai-code-reviewer/` - Main Application

### `backend/` - FastAPI Backend

```
backend/
├── api/                 # API layer
│   ├── routers/        # API endpoints
│   │   └── review.py   # Code review endpoint
│   └── schemas/        # Pydantic models
│       └── review.py   # Request/response schemas
├── services/           # Business logic
│   ├── code_analyzer.py # Static analysis
│   └── llm_service.py   # AI integration
├── config/             # Configuration
│   └── settings.py     # Environment config
├── utils/              # Utilities
│   └── logger.py       # Logging setup
├── Dockerfile          # Backend container
└── requirements.txt    # Python dependencies
```

#### `api/` - API Layer

**Purpose**: HTTP endpoints and request/response handling

**`routers/review.py`**:
- POST `/review` endpoint
- Validates requests
- Orchestrates analysis
- Returns structured responses

**When to modify**:
- Adding new API endpoints
- Changing request/response format
- Adding API middleware

**`schemas/review.py`**:
- `CodeSnippet`: Input validation
- `ReviewResponse`: Output structure
- Uses Pydantic for type safety

**When to modify**:
- Adding new request fields
- Changing response structure
- Adding validation rules

#### `services/` - Business Logic

**Purpose**: Core functionality, independent of API

**`code_analyzer.py`**:
- Language detection (15+ languages)
- Static code analysis
- Security vulnerability scanning
- Quality metrics calculation

**Key Functions**:
- `detect_language(code)`: Auto-detect programming language
- `analyze(code, language)`: Full code analysis
- `_detect_issues(code, language)`: Find problems

**When to modify**:
- Adding new programming languages
- Adding new code quality checks
- Changing quality scoring algorithm

**`llm_service.py`**:
- AI-powered code analysis
- Supports Anthropic Claude & OpenAI GPT
- Mock mode for no-API-key operation

**Key Functions**:
- `analyze_code(code, language, context)`: Get AI review
- `_analyze_with_anthropic(prompt)`: Claude integration
- `_analyze_with_openai(prompt)`: GPT integration
- `_mock_analysis(code)`: Fallback mode

**When to modify**:
- Adding new LLM providers
- Changing prompt engineering
- Improving mock mode responses

#### `config/` - Configuration

**`settings.py`**:
- Loads environment variables
- Provides default values
- Type-safe configuration

**Environment Variables**:
- `ANTHROPIC_API_KEY`: Claude API key
- `OPENAI_API_KEY`: GPT API key
- `LLM_PROVIDER`: Which AI to use
- `LOG_LEVEL`: Logging verbosity

**When to modify**:
- Adding new configuration options
- Changing default values
- Adding environment validation

#### `utils/` - Utilities

**`logger.py`**:
- Structured logging setup
- Console output formatting
- Log level configuration

**When to modify**:
- Changing log format
- Adding new log handlers
- Customizing log levels

---

### `frontend/` - React Frontend

```
frontend/
├── public/             # Static files
│   ├── index.html     # HTML template
│   └── manifest.json  # PWA manifest
├── src/               # Source code
│   ├── components/    # React components
│   │   ├── CodeInputForm.tsx    # Code input
│   │   └── ReviewResult.tsx     # Results display
│   ├── services/      # API client
│   │   └── api.ts     # HTTP requests
│   ├── App.tsx        # Main component
│   ├── App.css        # Styles
│   └── index.tsx      # Entry point
├── Dockerfile         # Frontend container
├── package.json       # Dependencies
└── tailwind.config.js # Tailwind config
```

#### `src/components/` - React Components

**`CodeInputForm.tsx`**:
- Code input textarea
- Submit and clear buttons
- Loading state handling
- Input validation

**Props**:
- `code`: Current code value
- `setCode`: Update code
- `handleSubmit`: Submit handler
- `handleClear`: Clear handler
- `loading`: Loading state

**When to modify**:
- Changing input UI
- Adding new form fields
- Customizing validation

**`ReviewResult.tsx`**:
- Displays analysis results
- Quality score visualization
- Suggestions list
- Metrics dashboard

**Props**:
- `review`: Analysis results object
  - `review`: Text review
  - `suggestions`: List of suggestions
  - `quality_score`: 0-100 score
  - `metrics`: Code statistics
  - `issues_count`: Number of issues

**When to modify**:
- Changing results display
- Adding new visualizations
- Customizing UI layout

#### `src/services/` - API Client

**`api.ts`**:
- HTTP request handling
- Error management
- API base URL configuration

**Functions**:
- `reviewCode(code)`: Submit code for review

**When to modify**:
- Adding new API calls
- Changing error handling
- Updating base URL

#### `src/App.tsx` - Main Component

**Purpose**: Application entry point and state management

**State**:
- `code`: Current code input
- `review`: Analysis results
- `error`: Error message
- `loading`: Loading state

**When to modify**:
- Adding global state
- Changing app layout
- Adding routing (future)

---

### `ml/` - Machine Learning (Future)

**Purpose**: ML models and training code

**Planned Features**:
- Custom code pattern detection
- Learning from user feedback
- Language-specific models

**Current Status**: Placeholder directory

---

### `extensions/` - Browser/IDE Extensions (Future)

**Purpose**: Browser and IDE integrations

**Planned Features**:
- Chrome/Firefox extension
- VS Code extension
- JetBrains plugin

**Current Status**: Placeholder directory

---

### `infrastructure/` - DevOps Configuration

**Purpose**: Kubernetes, Terraform, deployment configs

**Planned Features**:
- Kubernetes manifests
- Terraform scripts
- Helm charts

**Current Status**: Placeholder directory

---

### `docs/` - Documentation

**Purpose**: Additional documentation files

**Current Files**:
- `PROJECT_STRUCTURE.md`: This file
- Future: API docs, deployment guides, etc.

---

## Configuration Files

### `.env.example`

**Purpose**: Template for environment variables

**Usage**:
```bash
cp .env.example .env
# Edit .env with your values
```

**Key Variables**:
- `ANTHROPIC_API_KEY`: For AI analysis
- `OPENAI_API_KEY`: Alternative AI provider
- `LLM_PROVIDER`: Which AI to use
- `DEBUG`: Enable debug mode

### `docker-compose.yml`

**Purpose**: Local development with Docker

**Services**:
- `backend`: FastAPI server (port 8000)
- `frontend`: React app (port 3000)

**Usage**:
```bash
docker-compose up -d      # Start
docker-compose logs -f    # View logs
docker-compose down       # Stop
```

### `requirements.txt`

**Purpose**: Python dependencies (root level, unused)

**Note**: Actual backend requirements in `ai-code-reviewer/backend/requirements.txt`

### `requirements-dev.txt`

**Purpose**: Development-only Python dependencies

**Includes**:
- Testing tools (pytest)
- Linting (flake8, black)
- Type checking (mypy)

---

## Documentation Files

### `README.md`

**Purpose**: Main project documentation

**Sections**:
- Project overview
- Quick start
- Features
- Installation
- Usage examples

### `GETTING_STARTED.md`

**Purpose**: Detailed setup guide

**Sections**:
- Prerequisites
- Step-by-step installation
- Configuration
- Troubleshooting

### `API_KEYS.md`

**Purpose**: API key setup instructions

**Sections**:
- How to get Anthropic API key
- How to get OpenAI API key
- Configuration steps
- Cost considerations

### `CONTRIBUTING.md`

**Purpose**: Contribution guidelines

**Sections**:
- Development setup
- Coding standards
- Pull request process
- Testing guidelines

### `ARCHITECTURE.md`

**Purpose**: Technical architecture documentation

**Sections**:
- System overview
- Component breakdown
- Data flow
- Design patterns

### `DEMO.md`

**Purpose**: Live demo examples

**Sections**:
- Real code examples
- API request/response samples
- Feature showcase

---

## Quick Reference

### Adding a New Feature

1. **Backend**: Add service to `backend/services/`
2. **API**: Add router to `backend/api/routers/`
3. **Schema**: Update `backend/api/schemas/`
4. **Frontend**: Add component to `frontend/src/components/`
5. **Docs**: Update README and this document

### Common File Locations

- **API endpoints**: `backend/api/routers/`
- **Business logic**: `backend/services/`
- **UI components**: `frontend/src/components/`
- **Configuration**: `backend/config/settings.py`
- **Environment**: `.env` (create from `.env.example`)

### Testing

- **Backend tests**: `backend/tests/`
- **Frontend tests**: `frontend/src/**/*.test.tsx`
- **Run backend tests**: `pytest`
- **Run frontend tests**: `npm test`

---

For questions about specific files or directories, see the corresponding README files or open an issue.
