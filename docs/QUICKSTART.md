# Quick Start Guide

Get AI Code Reviewer running in minutes.

## Option 1: Docker (Recommended)

```bash
# 1) Clone and enter directory
git clone https://github.com/neerazz/ai-code-reviewer.git
cd ai-code-reviewer

# 2) Copy environment file (keys optional; mock mode works)
cp .env.example .env

# 3) Start backend + frontend
docker-compose up -d

# 4) Check logs
docker-compose logs -f

# 5) Visit
# API docs: http://localhost:8000/docs
# Frontend: http://localhost:3000
```

## Option 2: Local Development

```bash
# Backend
cd src/backend
python -m venv .venv && source .venv/bin/activate  # use Scripts\\activate on Windows
pip install -r requirements.txt
PYTHONPATH=. uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (new shell)
cd src/frontend
npm install
npm start
```

## First API Call

```bash
# Health check
curl http://localhost:8000/health

# Analyze code
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"hello\")", "language": "python"}'
```

## What's Running?

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

## Next Steps

1. Try the frontend UI at `http://localhost:3000`.
2. Experiment with different languages in the `/review` payload.
3. Add API keys to `.env` to switch from mock to AI-powered analysis.

## Troubleshooting

### API won't start
- Check .env has valid API keys
- Ensure ports 8000, 5432, 6379 are available
- Check logs: `docker-compose logs backend`

### Database connection failed
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env

### Redis connection failed
- Ensure Redis is running
- Check REDIS_HOST and REDIS_PORT

## Getting Help

- 📖 Full docs: `docs/`
- 🐛 Report issues: https://github.com/neerazz/ai-code-reviewer/issues
