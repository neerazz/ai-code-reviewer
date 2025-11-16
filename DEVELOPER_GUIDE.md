# AI Code Reviewer - Developer Guide

**Version**: 1.0.0
**Last Updated**: 2025-11-16
**Audience**: Contributors, Developers, Maintainers

---

## Table of Contents

1. [Introduction](#introduction)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Architecture Overview](#architecture-overview)
5. [Module Documentation](#module-documentation)
6. [Development Workflow](#development-workflow)
7. [Coding Standards](#coding-standards)
8. [Testing Guidelines](#testing-guidelines)
9. [Adding New Features](#adding-new-features)
10. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
11. [Contributing Guidelines](#contributing-guidelines)
12. [Release Process](#release-process)

---

## Introduction

Welcome to the AI Code Reviewer Developer Guide! This document provides comprehensive information for developers who want to contribute to, extend, or maintain the AI Code Reviewer project.

### Developer Prerequisites

**Required Knowledge**:
- Python 3.9+ (backend development)
- React & TypeScript (frontend development)
- FastAPI framework
- RESTful API design
- Docker and containerization
- Git and version control

**Recommended Knowledge**:
- LLM integration (Anthropic, OpenAI)
- Static code analysis
- Regular expressions
- Pydantic for data validation
- Tailwind CSS
- CI/CD practices

---

## Development Environment Setup

### Step 1: Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/ai-code-reviewer.git
cd ai-code-reviewer

# Add upstream remote
git remote add upstream https://github.com/neerazz/ai-code-reviewer.git
```

### Step 2: Backend Development Setup

```bash
# Navigate to backend directory
cd ai-code-reviewer/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install pytest pytest-cov black flake8 mypy

# Create .env file
cp .env.example .env
```

**Edit `.env` file**:
```bash
# Development settings
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# Optional: Add your API keys for testing
ANTHROPIC_API_KEY=your_test_key_here
LLM_PROVIDER=anthropic
```

### Step 3: Frontend Development Setup

```bash
# Navigate to frontend directory (from project root)
cd ai-code-reviewer/frontend

# Install dependencies
npm install

# For development, frontend expects backend at localhost:8000
# No additional configuration needed
```

### Step 4: Verify Installation

**Terminal 1 - Start Backend**:
```bash
cd ai-code-reviewer/backend
source venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Start Frontend**:
```bash
cd ai-code-reviewer/frontend
npm start
```

**Terminal 3 - Test API**:
```bash
# Health check
curl http://localhost:8000/health

# Test review endpoint
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def test(): pass"}'
```

### Step 5: IDE Configuration

**VS Code** (Recommended):

Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true,
  "typescript.tsdk": "node_modules/typescript/lib",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

**PyCharm**:
1. Open project root
2. Configure Python interpreter → Select venv
3. Enable Black formatter
4. Enable Flake8 linter
5. Set TypeScript version to project's version

---

## Project Structure

### Complete Directory Tree

```
ai-code-reviewer/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI/CD pipeline
│       └── pages.yml           # GitHub Pages deployment
│
├── ai-code-reviewer/
│   ├── backend/                # Python FastAPI backend
│   │   ├── api/
│   │   │   ├── main.py         # FastAPI application entry
│   │   │   ├── routers/
│   │   │   │   └── review.py   # Code review endpoints
│   │   │   └── schemas/
│   │   │       └── review.py   # Pydantic models
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py     # Configuration management
│   │   ├── services/
│   │   │   ├── code_analyzer.py      # Static analysis engine
│   │   │   ├── llm_service.py        # AI integration layer
│   │   │   └── migration_engine.py   # [Future] Code migration
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── logger.py       # Logging utilities
│   │   ├── Dockerfile          # Backend container config
│   │   ├── requirements.txt    # Python dependencies
│   │   └── __init__.py
│   │
│   ├── frontend/               # React TypeScript frontend
│   │   ├── public/
│   │   │   ├── index.html      # HTML template
│   │   │   └── manifest.json   # PWA manifest
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── CodeInputForm.tsx   # Code input component
│   │   │   │   └── ReviewResult.tsx    # Results display component
│   │   │   ├── services/
│   │   │   │   └── api.ts      # API client
│   │   │   ├── App.tsx         # Main application component
│   │   │   ├── App.css         # Application styles
│   │   │   ├── index.tsx       # React entry point
│   │   │   ├── index.css       # Global styles
│   │   │   └── App.test.tsx    # Application tests
│   │   ├── Dockerfile          # Frontend container config
│   │   ├── package.json        # Node dependencies
│   │   ├── tsconfig.json       # TypeScript configuration
│   │   ├── tailwind.config.js  # Tailwind CSS config
│   │   └── postcss.config.js   # PostCSS config
│   │
│   ├── docs/                   # Documentation
│   │   ├── PROJECT_STRUCTURE.md
│   │   └── README.md
│   │
│   ├── extensions/             # [Future] IDE extensions
│   ├── infrastructure/         # [Future] K8s configs
│   └── ml/                     # [Future] ML models
│
├── docker-compose.yml          # Multi-container orchestration
├── README.md                   # Project overview
├── USER_GUIDE.md              # User documentation
├── DEVELOPER_GUIDE.md         # This file
├── SYSTEM_DESIGN.md           # Architecture documentation
├── CONTRIBUTING.md            # Contribution guidelines
├── API_KEYS.md                # API key setup guide
├── ARCHITECTURE.md            # System architecture
└── GETTING_STARTED.md         # Quick start guide
```

### Module Responsibilities

#### Backend Modules

**`api/main.py`**:
- FastAPI application initialization
- CORS middleware configuration
- Router inclusion
- Health check endpoints

**`api/routers/review.py`**:
- Code review endpoint (`/review`)
- Request validation
- Orchestrates static + AI analysis
- Response formatting

**`api/schemas/review.py`**:
- Pydantic models for request/response
- Input validation rules
- API contract definitions

**`config/settings.py`**:
- Environment variable management
- Configuration loading
- Settings validation
- Singleton pattern for config access

**`services/code_analyzer.py`**:
- Language detection (15+ languages)
- Static code analysis
- Security vulnerability scanning
- Code metrics calculation
- Quality score computation

**`services/llm_service.py`**:
- LLM provider abstraction
- Anthropic Claude integration
- OpenAI GPT integration
- Mock mode for testing
- Response parsing

**`utils/logger.py`**:
- Structured logging setup
- Log formatting
- Log level configuration

#### Frontend Modules

**`App.tsx`**:
- Main application component
- State management
- Layout orchestration
- Error handling

**`components/CodeInputForm.tsx`**:
- Code input textarea
- Form validation
- Submit/Clear actions
- Loading states

**`components/ReviewResult.tsx`**:
- Review results display
- Quality score visualization
- Suggestions rendering
- Metrics cards

**`services/api.ts`**:
- HTTP client for backend
- API request formatting
- Error handling

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌─────────────────┐  ┌──────────────────────────────────┐ │
│  │  CodeInputForm  │  │      ReviewResult                │ │
│  │                 │  │  - Quality Score                 │ │
│  │  - Textarea     │  │  - Suggestions                   │ │
│  │  - Submit       │──▶│  - Metrics                       │ │
│  │  - Clear        │  │  - Issues                        │ │
│  └────────┬────────┘  └──────────────────────────────────┘ │
│           │                                                  │
│           │ HTTP POST /review                                │
└───────────┼──────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Layer (main.py)                      │  │
│  │  - CORS Middleware                                    │  │
│  │  - Request Validation (Pydantic)                      │  │
│  │  - Router: /review                                    │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                            │
│                 ▼                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Review Router (routers/review.py)            │  │
│  │  1. Validate input                                   │  │
│  │  2. Call CodeAnalyzer                                │  │
│  │  3. Call LLMService                                  │  │
│  │  4. Combine results                                  │  │
│  │  5. Format response                                  │  │
│  └────┬──────────────────────────┬────────────────────┘  │
│       │                          │                         │
│       ▼                          ▼                         │
│  ┌─────────────────┐   ┌────────────────────────┐         │
│  │  CodeAnalyzer   │   │    LLMService          │         │
│  │                 │   │                        │         │
│  │ - Detect Lang   │   │ - Anthropic Claude     │         │
│  │ - Static Scan   │   │ - OpenAI GPT           │         │
│  │ - Security      │   │ - Mock Mode            │         │
│  │ - Metrics       │   │ - Response Parsing     │         │
│  │ - Quality Score │   │                        │         │
│  └─────────────────┘   └────────┬───────────────┘         │
│                                  │                          │
│                                  │ External API Call        │
└──────────────────────────────────┼──────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │  External AI Providers   │
                    │  - Anthropic Claude API  │
                    │  - OpenAI GPT API        │
                    └──────────────────────────┘
```

### Request Flow

1. **User Action**: User pastes code and clicks "Review Code"
2. **Frontend Processing**:
   - Validates input (non-empty)
   - Shows loading state
   - Sends POST request to `/review`
3. **Backend Reception**:
   - FastAPI receives request
   - Pydantic validates schema
   - Router method called
4. **Static Analysis**:
   - Language detection
   - Code metrics calculation
   - Security scanning
   - Issue detection
5. **AI Analysis** (if configured):
   - Prompt construction
   - API call to LLM provider
   - Response parsing
6. **Result Combination**:
   - Merge static + AI results
   - Format suggestions
   - Calculate quality score
7. **Response Return**:
   - Send JSON response
   - Frontend parses response
   - Display results to user

### Data Flow

```
Code Input
    ↓
[Language Detection]
    ↓
[Static Analysis] ──┬──→ Metrics (lines, complexity, etc.)
    ↓               ├──→ Issues (security, style, etc.)
    ↓               └──→ Quality Score
    ↓
[AI Analysis] ──┬──→ Deep Review
    ↓           └──→ AI Suggestions
    ↓
[Combine Results]
    ↓
[Format Response]
    ↓
Display to User
```

---

## Module Documentation

### Backend: `code_analyzer.py`

**Purpose**: Performs static code analysis including language detection, security scanning, and quality metrics.

**Key Classes**:

```python
class CodeAnalyzer:
    """Service for performing static code analysis."""

    LANGUAGE_PATTERNS: Dict[str, List[str]]
    # Regex patterns for detecting 15+ languages

    def detect_language(self, code: str) -> str:
        """Detect programming language from code."""
        # Returns language name or 'unknown'

    def analyze(self, code: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Perform comprehensive static analysis."""
        # Returns: language, metrics, issues, complexity_score, quality_score

    def _calculate_metrics(self, code: str) -> Dict[str, int]:
        """Calculate code metrics like lines, complexity."""

    def _detect_issues(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Detect security and quality issues."""

    def _calculate_complexity(self, code: str, language: str) -> int:
        """Calculate cyclomatic complexity (1-10)."""

    def _calculate_quality_score(self, metrics, issues, complexity) -> int:
        """Calculate overall quality score (0-100)."""
```

**How to Add a New Language**:

1. Add language pattern to `LANGUAGE_PATTERNS`:
```python
'scala': [
    r'object\s+\w+',
    r'def\s+\w+\s*\(',
    r'val\s+\w+\s*=',
    r'case\s+class'
]
```

2. Add language-specific checks (optional):
```python
def _check_scala_issues(self, code: str) -> List[Dict[str, Any]]:
    """Scala-specific issue detection."""
    issues = []
    # Add scala-specific checks
    return issues
```

3. Update detection in `_detect_issues`:
```python
if language == 'scala':
    issues.extend(self._check_scala_issues(code))
```

**How to Add New Security Pattern**:

```python
# In _detect_issues method
security_patterns = {
    'hardcoded_password': r'password\s*=\s*["\'].*["\']',
    'hardcoded_secret': r'(secret|api_key|token)\s*=\s*["\'].*["\']',
    'sql_injection': r'(execute|query)\s*\(\s*["\'].*\+.*["\']',
    'eval_usage': r'eval\s*\(',
    # Add new pattern here:
    'weak_crypto': r'(md5|sha1)\s*\(',
}
```

### Backend: `llm_service.py`

**Purpose**: Abstracts LLM provider integrations (Anthropic, OpenAI) with fallback to mock mode.

**Key Classes**:

```python
class LLMService:
    """Service for interacting with Large Language Models."""

    def __init__(self):
        """Initialize with configured provider."""
        # Sets up Anthropic or OpenAI client

    def analyze_code(self, code: str, language: Optional[str] = None,
                     context: Optional[str] = None) -> Dict[str, Any]:
        """Analyze code using LLM or mock mode."""
        # Returns: review, suggestions, error flag

    def _build_analysis_prompt(self, code, language, context) -> str:
        """Construct prompt for LLM."""

    def _analyze_with_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Call Anthropic Claude API."""

    def _analyze_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Call OpenAI GPT API."""

    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response into structured format."""

    def _mock_analysis(self, code: str) -> Dict[str, Any]:
        """Provide mock analysis when LLM unavailable."""
```

**How to Add a New LLM Provider** (e.g., Cohere):

1. Add configuration in `settings.py`:
```python
cohere_api_key: Optional[str] = None
```

2. Initialize client in `__init__`:
```python
elif self.provider == "cohere":
    if not settings.cohere_api_key:
        self.client = None
    else:
        import cohere
        self.client = cohere.Client(settings.cohere_api_key)
```

3. Add analysis method:
```python
def _analyze_with_cohere(self, prompt: str) -> Dict[str, Any]:
    """Analyze code using Cohere."""
    try:
        response = self.client.generate(
            model='command',
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        response_text = response.generations[0].text
        return self._parse_llm_response(response_text)
    except Exception as e:
        logger.error(f"Cohere API error: {str(e)}")
        raise
```

4. Update `analyze_code` method:
```python
if self.provider == "anthropic":
    return self._analyze_with_anthropic(prompt)
elif self.provider == "openai":
    return self._analyze_with_openai(prompt)
elif self.provider == "cohere":
    return self._analyze_with_cohere(prompt)
```

### Frontend: `App.tsx`

**Purpose**: Main application component managing state and layout.

**Key State**:
```typescript
const [code, setCode] = useState('');           // User's code input
const [review, setReview] = useState<any>(null); // Review results
const [error, setError] = useState<string | null>(null); // Error messages
const [loading, setLoading] = useState(false);   // Loading state
```

**Key Functions**:
```typescript
const handleSubmit = async (e: React.FormEvent) => {
    // 1. Prevent default form submission
    // 2. Clear previous state
    // 3. Set loading true
    // 4. Call API
    // 5. Set review or error
    // 6. Set loading false
};

const handleClear = () => {
    // Reset all state
};
```

**How to Add a New Feature to UI**:

1. Add state:
```typescript
const [darkMode, setDarkMode] = useState(false);
```

2. Add handler:
```typescript
const toggleDarkMode = () => {
    setDarkMode(!darkMode);
};
```

3. Update JSX:
```tsx
<button onClick={toggleDarkMode}>
  {darkMode ? '☀️ Light' : '🌙 Dark'}
</button>
```

### Frontend: `api.ts`

**Purpose**: HTTP client for backend API.

```typescript
const API_BASE_URL = 'http://localhost:8000';

export const reviewCode = async (code: string) => {
  const response = await fetch(`${API_BASE_URL}/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code }),
  });

  if (!response.ok) {
    throw new Error('Something went wrong with the review request.');
  }

  return response.json();
};
```

**How to Add a New API Endpoint**:

```typescript
export const getReviewHistory = async () => {
  const response = await fetch(`${API_BASE_URL}/history`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch review history.');
  }

  return response.json();
};
```

---

## Development Workflow

### Branch Strategy

```
main (production)
  ↓
develop (integration)
  ↓
feature/add-new-language
feature/improve-ui
bugfix/fix-security-scan
hotfix/critical-issue
```

**Branch Naming**:
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring

### Development Process

1. **Create Branch**:
```bash
git checkout develop
git pull upstream develop
git checkout -b feature/add-rust-support
```

2. **Make Changes**:
   - Write code
   - Add tests
   - Update documentation

3. **Commit Changes**:
```bash
git add .
git commit -m "feat: Add Rust language support

- Add Rust detection patterns
- Add Rust-specific issue checks
- Update language list in docs
- Add unit tests for Rust detection"
```

4. **Push Changes**:
```bash
git push origin feature/add-rust-support
```

5. **Create Pull Request**:
   - Go to GitHub
   - Create PR from your branch to `develop`
   - Fill out PR template
   - Request reviews

6. **Address Reviews**:
   - Make requested changes
   - Push updates
   - Respond to comments

7. **Merge**:
   - Once approved, merge PR
   - Delete feature branch

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:
```bash
feat(analyzer): Add TypeScript support
fix(api): Handle empty code input correctly
docs(readme): Update installation instructions
refactor(llm): Extract prompt building logic
test(analyzer): Add tests for Python detection
chore(deps): Update FastAPI to 0.109.0
```

---

## Coding Standards

### Python Standards

Follow **PEP 8** with some modifications:

**Line Length**: 100 characters (vs PEP 8's 79)

**Imports**:
```python
# Standard library
import os
import sys
from typing import Dict, List, Optional

# Third-party
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Local
from config.settings import get_settings
from utils.logger import setup_logger
```

**Naming Conventions**:
```python
# Classes: PascalCase
class CodeAnalyzer:
    pass

# Functions/Methods: snake_case
def analyze_code():
    pass

# Constants: UPPER_CASE
MAX_TOKEN_LENGTH = 8192

# Private methods: _snake_case
def _internal_helper():
    pass
```

**Type Hints**:
```python
def analyze(self, code: str, language: Optional[str] = None) -> Dict[str, Any]:
    """Always include type hints for function parameters and return values."""
    pass
```

**Docstrings**:
```python
def analyze_code(code: str) -> Dict[str, Any]:
    """
    Analyze code snippet for issues and quality.

    Args:
        code: Source code to analyze

    Returns:
        Dictionary containing analysis results with keys:
        - issues: List of detected issues
        - quality_score: Score from 0-100
        - language: Detected language

    Raises:
        ValueError: If code is empty or invalid
    """
    pass
```

**Error Handling**:
```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {str(e)}")
    raise HTTPException(status_code=500, detail="Operation failed")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    raise
```

### TypeScript/React Standards

Follow **Airbnb JavaScript Style Guide** with TypeScript:

**Component Structure**:
```typescript
import React, { useState, useEffect } from 'react';

interface Props {
  code: string;
  onSubmit: (code: string) => void;
}

const CodeEditor: React.FC<Props> = ({ code, onSubmit }) => {
  const [localCode, setLocalCode] = useState(code);

  useEffect(() => {
    setLocalCode(code);
  }, [code]);

  return (
    <div className="code-editor">
      {/* Component JSX */}
    </div>
  );
};

export default CodeEditor;
```

**Naming Conventions**:
```typescript
// Components: PascalCase
const CodeInputForm: React.FC = () => { };

// Functions: camelCase
const handleSubmit = () => { };

// Constants: UPPER_CASE
const API_BASE_URL = 'http://localhost:8000';

// Interfaces: PascalCase with 'I' prefix (optional)
interface ReviewResponse {
  review: string;
  quality_score: number;
}
```

**Type Definitions**:
```typescript
// Always define types/interfaces
interface Review {
  review: string;
  suggestions: string[];
  quality_score: number;
  language: string;
  metrics: {
    total_lines: number;
    code_lines: number;
  };
}

// Use type for unions
type Status = 'idle' | 'loading' | 'success' | 'error';
```

### Code Formatting

**Python**: Use `black`
```bash
black --line-length 100 backend/
```

**TypeScript/React**: Use `prettier`
```bash
npx prettier --write "frontend/src/**/*.{ts,tsx}"
```

### Linting

**Python**: Use `flake8`
```bash
flake8 backend/ --max-line-length=100
```

**TypeScript**: Use `eslint`
```bash
npm run lint
```

---

## Testing Guidelines

### Backend Testing

**Framework**: pytest

**Test Structure**:
```
backend/
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_code_analyzer.py
    ├── test_llm_service.py
    └── test_api.py
```

**Example Test**:
```python
# tests/test_code_analyzer.py
import pytest
from services.code_analyzer import CodeAnalyzer

class TestCodeAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return CodeAnalyzer()

    def test_detect_python(self, analyzer):
        code = "def hello():\n    print('Hello')"
        language = analyzer.detect_language(code)
        assert language == 'python'

    def test_detect_hardcoded_password(self, analyzer):
        code = 'password = "admin123"'
        result = analyzer.analyze(code)
        assert len(result['issues']) > 0
        assert any('password' in issue['issue'].lower()
                   for issue in result['issues'])

    def test_quality_score_range(self, analyzer):
        code = "def test(): pass"
        result = analyzer.analyze(code)
        assert 0 <= result['quality_score'] <= 100
```

**Run Tests**:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_code_analyzer.py

# Run specific test
pytest tests/test_code_analyzer.py::TestCodeAnalyzer::test_detect_python
```

### Frontend Testing

**Framework**: Jest + React Testing Library

**Example Test**:
```typescript
// src/App.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

test('renders code input form', () => {
  render(<App />);
  const textarea = screen.getByPlaceholderText(/Paste your code here/i);
  expect(textarea).toBeInTheDocument();
});

test('shows loading state when reviewing code', async () => {
  render(<App />);

  const textarea = screen.getByTestId('code-input');
  const submitButton = screen.getByText(/Review Code/i);

  fireEvent.change(textarea, { target: { value: 'def test(): pass' } });
  fireEvent.click(submitButton);

  expect(screen.getByText(/Analyzing your code/i)).toBeInTheDocument();
});
```

**Run Tests**:
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Integration Testing

**Test API Integration**:
```python
# tests/test_api.py
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_review_endpoint():
    code = "def test(): password='123'"
    response = client.post("/review", json={"code": code})

    assert response.status_code == 200
    data = response.json()
    assert "review" in data
    assert "quality_score" in data
    assert "language" in data

def test_empty_code_rejected():
    response = client.post("/review", json={"code": ""})
    assert response.status_code == 400
```

---

## Adding New Features

### Example: Adding Language Support

**Step 1**: Update `code_analyzer.py`
```python
LANGUAGE_PATTERNS = {
    # ... existing patterns ...
    'kotlin': [
        r'fun\s+\w+\(',
        r'val\s+\w+\s*=',
        r'var\s+\w+\s*=',
        r'class\s+\w+',
        r'package\s+\w+'
    ]
}
```

**Step 2**: Add language-specific checks (optional)
```python
def _check_kotlin_issues(self, code: str) -> List[Dict[str, Any]]:
    issues = []

    # Check for var usage (should use val when possible)
    if re.search(r'\bvar\s+\w+', code):
        issues.append({
            "type": "best_practice",
            "severity": "low",
            "issue": "Var Usage",
            "message": "Consider using 'val' for immutable variables"
        })

    return issues
```

**Step 3**: Wire up in `_detect_issues`
```python
if language == 'kotlin':
    issues.extend(self._check_kotlin_issues(code))
```

**Step 4**: Add tests
```python
def test_detect_kotlin(analyzer):
    code = "fun main() { val x = 5 }"
    assert analyzer.detect_language(code) == 'kotlin'

def test_kotlin_var_detection(analyzer):
    code = "var mutableValue = 10"
    result = analyzer.analyze(code, 'kotlin')
    assert any('var' in issue['issue'].lower() for issue in result['issues'])
```

**Step 5**: Update documentation
- Add Kotlin to supported languages list in README
- Update USER_GUIDE.md
- Update API documentation

### Example: Adding New API Endpoint

**Step 1**: Define schema in `api/schemas/`
```python
# api/schemas/batch.py
from pydantic import BaseModel
from typing import List

class BatchReviewRequest(BaseModel):
    files: List[Dict[str, str]]  # filename -> code mapping

class BatchReviewResponse(BaseModel):
    results: List[ReviewResponse]
```

**Step 2**: Create router
```python
# api/routers/batch.py
from fastapi import APIRouter
from api.schemas.batch import BatchReviewRequest, BatchReviewResponse

router = APIRouter()

@router.post("/batch-review", response_model=BatchReviewResponse)
async def batch_review(request: BatchReviewRequest):
    results = []
    for filename, code in request.files.items():
        # Reuse existing review logic
        result = await review_code(CodeSnippet(code=code))
        results.append(result)

    return {"results": results}
```

**Step 3**: Register router in `main.py`
```python
from api.routers import review, batch

app.include_router(batch.router, tags=["Batch Review"])
```

**Step 4**: Add frontend support
```typescript
// services/api.ts
export const batchReviewCode = async (files: Record<string, string>) => {
  const response = await fetch(`${API_BASE_URL}/batch-review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ files }),
  });

  if (!response.ok) {
    throw new Error('Batch review failed');
  }

  return response.json();
};
```

**Step 5**: Add tests
```python
def test_batch_review():
    files = {
        "file1.py": "def test(): pass",
        "file2.js": "function test() {}"
    }
    response = client.post("/batch-review", json={"files": files})
    assert response.status_code == 200
    assert len(response.json()["results"]) == 2
```

---

## Debugging and Troubleshooting

### Backend Debugging

**Enable Debug Logging**:
```python
# config/settings.py
log_level: str = "DEBUG"
```

**Add Debug Statements**:
```python
logger.debug(f"Analyzing code: {code[:100]}...")
logger.debug(f"Detected language: {language}")
logger.debug(f"Found {len(issues)} issues")
```

**Use Python Debugger**:
```python
import pdb; pdb.set_trace()  # Breakpoint
```

**Check Logs**:
```bash
# Docker
docker-compose logs -f backend

# Manual
# Logs appear in terminal where uvicorn is running
```

### Frontend Debugging

**Browser DevTools**:
- F12 → Console tab
- Check Network tab for API requests
- Use React DevTools extension

**Add Console Logs**:
```typescript
console.log('Submitting code:', code);
console.log('API response:', response);
```

**React Strict Mode**:
Already enabled in `index.tsx` - helps catch issues during development

### Common Issues

**Issue**: Import errors in Python
```bash
# Solution: Ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
```

**Issue**: Port already in use
```bash
# Solution: Kill process or use different port
lsof -ti:8000 | xargs kill -9
# Or change port in .env
```

**Issue**: CORS errors
```python
# Solution: Add origin to CORS middleware in main.py
origins = [
    "http://localhost:3000",
    "http://localhost:3001",  # Add your origin
]
```

---

## Contributing Guidelines

### Code Review Checklist

Before submitting PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No hardcoded secrets or API keys
- [ ] Code is well-commented
- [ ] Type hints added (Python)
- [ ] No console.log in production code (TypeScript)
- [ ] Error handling implemented
- [ ] Backwards compatible (if applicable)

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests passing

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

### Review Process

1. **Automated Checks**: CI runs tests, linting
2. **Code Review**: Maintainer reviews code
3. **Address Feedback**: Make requested changes
4. **Approval**: Once approved, ready to merge
5. **Merge**: Squash and merge to develop

---

## Release Process

### Version Numbers

Follow Semantic Versioning (SemVer):
- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

### Release Steps

1. **Update Version**:
```bash
# backend/api/main.py
app = FastAPI(version="1.1.0")

# frontend/package.json
"version": "1.1.0"
```

2. **Update CHANGELOG.md**:
```markdown
## [1.1.0] - 2025-11-20

### Added
- Kotlin language support
- Batch review endpoint

### Fixed
- Security scan false positives

### Changed
- Improved quality score algorithm
```

3. **Create Release Branch**:
```bash
git checkout develop
git checkout -b release/1.1.0
```

4. **Tag Release**:
```bash
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0
```

5. **Create GitHub Release**:
- Go to GitHub → Releases → New Release
- Select tag v1.1.0
- Add release notes from CHANGELOG
- Publish release

---

## Additional Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Pydantic: https://docs.pydantic.dev/
- Anthropic: https://docs.anthropic.com/

### Tools
- Black: https://black.readthedocs.io/
- Pytest: https://docs.pytest.org/
- Jest: https://jestjs.io/

### Community
- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share ideas

---

**Thank you for contributing to AI Code Reviewer!**

Your contributions help make code review better for everyone.

*Last updated: 2025-11-16 | Version 1.0.0*
