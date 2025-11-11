# Quick Start Guide

Get AI Code Reviewer running in 5 minutes!

## Option 1: Docker (Recommended)

```bash
# 1. Clone and enter directory
cd ai-code-reviewer

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env and add your API keys
# Required: ANTHROPIC_API_KEY or OPENAI_API_KEY

# 4. Start all services
docker-compose up -d

# 5. Check logs
docker-compose logs -f backend

# 6. Visit API docs
open http://localhost:8000/docs
```

## Option 2: Local Development

```bash
# 1. Run setup script
# On Linux/Mac:
bash scripts/setup.sh

# On Windows:
scripts\setup.bat

# 2. Edit .env with your API keys

# 3. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 4. Start the server
uvicorn backend.main:app --reload
```

## First API Call

Test the API with curl:

```bash
# Health check
curl http://localhost:8000/health

# Analyze code
curl -X POST "http://localhost:8000/api/v1/reviews/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    password = \"secret123\"\n    print(password)",
    "file_path": "example.py",
    "language": "python"
  }'
```

## What's Running?

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Flower (Celery monitoring)**: http://localhost:5555

## Next Steps

1. **Set up GitHub webhook** (Optional)
   - Go to your repo Settings → Webhooks
   - Add webhook: `https://your-domain.com/api/v1/webhooks/github`
   - Select events: Pull requests, Push

2. **Register a repository**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/repositories" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "my-repo",
       "full_name": "owner/my-repo",
       "url": "https://github.com/owner/my-repo",
       "platform": "github"
     }'
   ```

3. **Review a PR**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/reviews/pr" \
     -H "Content-Type: application/json" \
     -d '{
       "repository": "owner/repo",
       "pr_number": 123
     }'
   ```

4. **Try a migration**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/migrations/migrate" \
     -H "Content-Type: application/json" \
     -d '{
       "code": "var x = 1;",
       "migration_type": "jquery_to_vanilla",
       "language": "javascript"
     }'
   ```

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

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yourusername/ai-code-reviewer/issues)
- 💬 [Join Discord](https://discord.gg/example)
