# Contributing to AI Code Reviewer

Thank you for your interest in contributing to AI Code Reviewer! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ai-code-reviewer.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `make test`
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Install development dependencies
make dev-install

# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# Run tests
make test
```

## Code Style

We follow PEP 8 for Python code. Please ensure your code:

- Is formatted with `black`
- Has imports sorted with `isort`
- Passes `flake8` linting
- Includes type hints (checked with `mypy`)

Run formatting:
```bash
make format
make lint
```

## Testing

- Write tests for all new features
- Maintain >80% code coverage
- Use pytest for testing

```bash
# Run tests
make test

# Run with coverage
make test-cov
```

## Commit Messages

Follow conventional commits:

- `feat: Add new feature`
- `fix: Fix bug`
- `docs: Update documentation`
- `test: Add tests`
- `refactor: Refactor code`
- `chore: Update dependencies`

## Pull Request Process

1. Update README.md with details of changes if needed
2. Update documentation
3. Add tests for new functionality
4. Ensure all tests pass
5. Request review from maintainers

## Code Review

- Be respectful and constructive
- Address all review comments
- Keep PRs focused and reasonably sized
- Link related issues

## Questions?

Feel free to open an issue or reach out to the maintainers.
