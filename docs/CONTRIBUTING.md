# Contributing to AI Code Reviewer

First off, thank you for considering contributing to AI Code Reviewer! It's people like you that make this tool better for everyone.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Project Structure](#project-structure)
5. [Coding Standards](#coding-standards)
6. [Commit Messages](#commit-messages)
7. [Pull Request Process](#pull-request-process)
8. [Testing Guidelines](#testing-guidelines)
9. [Documentation](#documentation)

---

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

**Our Standards:**
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
A clear description of what you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g., macOS, Windows, Linux]
 - Python version: [e.g., 3.11.0]
 - Node.js version: [e.g., 18.0.0]
 - Browser: [e.g., Chrome, Firefox]

**Additional context**
Add any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List some examples** of how it would be used

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Simple issues perfect for newcomers
- `help wanted` - Issues where we need community help
- `documentation` - Documentation improvements

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/ai-code-reviewer.git
cd ai-code-reviewer

# Add upstream remote
git remote add upstream https://github.com/neerazz/ai-code-reviewer.git
```

### 2. Create a Branch

```bash
# Update your local main
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

### 3. Set Up Development Environment

**Backend:**

```bash
cd src/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r ../requirements-dev.txt

# Run the backend
PYTHONPATH=. uvicorn api.main:app --reload
```

**Frontend:**

```bash
cd src/frontend

# Install dependencies
npm install

# Run the frontend
npm start
```

### 4. Make Your Changes

- Write your code
- Add tests if applicable
- Update documentation
- Ensure your code follows our coding standards

---

## Project Structure

```
ai-code-reviewer/
├── AGENTS.md                 # Working agreement
├── config/                   # Shared config artifacts
├── docs/                     # Architecture, guides, reports, screenshots
├── src/
│   ├── backend/              # FastAPI backend (api, services, config, utils)
│   ├── frontend/             # React frontend (components, services)
│   ├── ml/                   # ML models (future)
│   ├── extensions/           # Browser/IDE extensions (future)
│   └── infrastructure/       # K8s, Terraform (future)
├── tests/                    # Root-level tests
├── .github/workflows/        # CI/CD pipelines
├── Dockerfile                # Backend/tooling image
├── docker-compose.yml        # Local orchestration
├── requirements.txt          # Python dependencies
├── requirements-dev.txt      # Dev/test dependencies
├── Makefile                  # Helper tasks
├── setup.py                  # Package metadata
├── .env.example              # Environment template
└── README.md                 # Main documentation
```

### Key Directories Explained

**`backend/api/routers/`**: API endpoint definitions
- Add new routes here for new features
- Follow RESTful conventions

**`backend/services/`**: Core business logic
- `code_analyzer.py`: Language detection, static analysis
- `llm_service.py`: AI/LLM integration

**`frontend/src/components/`**: React UI components
- Keep components small and focused
- Use TypeScript for type safety

---

## Coding Standards

### Python (Backend)

**Style Guide:** Follow [PEP 8](https://pep8.org/)

```python
# Good: Clear function with type hints and docstring
def analyze_code(code: str, language: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze code for quality and security issues.

    Args:
        code: The code snippet to analyze
        language: Programming language (auto-detected if None)

    Returns:
        Dictionary containing analysis results
    """
    # Implementation
    pass

# Use type hints
from typing import Dict, List, Optional, Any

# Use descriptive variable names
quality_score = calculate_quality(metrics)  # Good
qs = calc(m)  # Bad
```

**Tools:**
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

### JavaScript/TypeScript (Frontend)

**Style Guide:** Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

```typescript
// Good: Typed interface and functional component
interface Props {
  code: string;
  onSubmit: (code: string) => void;
}

const CodeInput: React.FC<Props> = ({ code, onSubmit }) => {
  // Implementation
};

// Use meaningful names
const handleCodeSubmit = () => { /* ... */ };  // Good
const hcs = () => { /* ... */ };  // Bad
```

**Tools:**
```bash
# Format code
npm run format

# Lint code
npm run lint

# Type check
npm run type-check
```

### General Principles

1. **Keep it simple**: Write clear, readable code
2. **DRY (Don't Repeat Yourself)**: Extract common logic
3. **SOLID principles**: Especially Single Responsibility
4. **Error handling**: Always handle errors gracefully
5. **Logging**: Add appropriate logging for debugging
6. **Comments**: Explain "why", not "what"

---

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```bash
feat(backend): add support for Rust language detection

Add Rust to supported languages in code_analyzer.
Includes pattern matching for Rust syntax.

Closes #123

---

fix(frontend): resolve CORS error on code submission

Update API base URL to use environment variable.
Fixes issue where submissions failed in production.

Fixes #456

---

docs(readme): update installation instructions

Add detailed Docker setup steps and troubleshooting
section for common installation issues.
```

---

## Pull Request Process

### Before Submitting

1. **Update your branch:**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Test your changes:**
   ```bash
   # Backend tests
   cd src/backend
   pytest

   # Frontend tests
   cd src/frontend
   npm test

   # Manual testing
   # Start both services and test functionality
   ```

3. **Lint your code:**
   ```bash
   # Backend
   flake8 .
   black . --check

   # Frontend
   npm run lint
   ```

4. **Update documentation** if needed

### Submitting

1. **Push your branch:**
   ```bash
   git push origin your-feature-branch
   ```

2. **Create Pull Request on GitHub:**
   - Use a clear, descriptive title
   - Fill out the PR template
   - Link related issues
   - Add screenshots for UI changes

**PR Template:**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code where necessary
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or my feature works
- [ ] New and existing tests pass locally

## Screenshots (if applicable)
Add screenshots here
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Address feedback** if requested
4. **Approval** from maintainer(s)
5. **Merge** by maintainer

---

## Testing Guidelines

### Backend Tests

```python
# src/backend/tests/test_code_analyzer.py

import pytest
from services.code_analyzer import CodeAnalyzer

def test_detect_python_language():
    """Test Python language detection."""
    analyzer = CodeAnalyzer()
    code = "def hello():\n    print('Hello')"
    result = analyzer.detect_language(code)
    assert result == "python"

def test_detect_security_issue():
    """Test detection of hardcoded password."""
    analyzer = CodeAnalyzer()
    code = 'password = "12345"'
    result = analyzer.analyze(code)
    assert len(result['issues']) > 0
    assert any('password' in issue['issue'].lower()
               for issue in result['issues'])
```

Run tests:
```bash
pytest
pytest --cov=. --cov-report=html  # With coverage
```

### Frontend Tests

```typescript
// src/frontend/src/components/CodeInput.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import CodeInput from './CodeInput';

test('renders code input textarea', () => {
  render(<CodeInput code="" setCode={() => {}} handleSubmit={() => {}} />);
  const textarea = screen.getByPlaceholderText(/paste your code/i);
  expect(textarea).toBeInTheDocument();
});

test('submit button disabled when code is empty', () => {
  render(<CodeInput code="" setCode={() => {}} handleSubmit={() => {}} />);
  const button = screen.getByText(/review code/i);
  expect(button).toBeDisabled();
});
```

Run tests:
```bash
npm test
npm test -- --coverage  # With coverage
```

---

## Documentation

### When to Update Documentation

- Adding a new feature → Update README, add to DEMO.md
- Changing configuration → Update .env.example, GETTING_STARTED.md
- Adding new API endpoint → Update API documentation
- Changing setup process → Update GETTING_STARTED.md

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots for UI features
- Keep formatting consistent
- Test all commands/instructions

### Example Documentation

```markdown
## Adding a New Language

To add support for a new programming language:

1. **Update language patterns** in `backend/services/code_analyzer.py`:

   ```python
   LANGUAGE_PATTERNS = {
       # ... existing languages
       'swift': [
           r'func\s+\w+\(',
           r'var\s+\w+:',
           r'import\s+\w+',
       ],
   }
   ```

2. **Add language-specific checks** (optional):

   ```python
   def _check_swift_issues(self, code: str) -> List[Dict[str, Any]]:
       """Swift-specific issue detection."""
       issues = []
       # Add your checks here
       return issues
   ```

3. **Test your changes**:

   ```bash
   pytest tests/test_code_analyzer.py::test_detect_swift
   ```

4. **Update documentation**:
   - Add Swift to supported languages in README.md
   - Add example to DEMO.md
```

---

## Questions?

- **General questions**: Open a [Discussion](https://github.com/neerazz/ai-code-reviewer/discussions)
- **Bug reports**: Open an [Issue](https://github.com/neerazz/ai-code-reviewer/issues)
- **Security issues**: Email the maintainers directly (see README)

---

Thank you for contributing! 🎉

Your efforts make AI Code Reviewer better for everyone!
