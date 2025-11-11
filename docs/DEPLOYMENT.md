# Deployment Guide

## Docker Deployment

### Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production

1. **Build production image**
   ```bash
   docker build -t ai-code-reviewer:latest .
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Run with docker-compose**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured
- Helm (optional but recommended)

### Deploy

```bash
# Create namespace
kubectl create namespace ai-reviewer

# Create secrets
kubectl create secret generic ai-reviewer-secrets \
  --from-env-file=.env \
  -n ai-reviewer

# Apply manifests
kubectl apply -f infrastructure/kubernetes/ -n ai-reviewer

# Check status
kubectl get pods -n ai-reviewer
```

## Environment Variables

### Required

- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
- `DATABASE_URL`
- `REDIS_HOST`

### Optional

- `GITHUB_TOKEN`
- `GITLAB_TOKEN`
- `SLACK_BOT_TOKEN`
- `JIRA_API_TOKEN`

## Database Migrations

```bash
# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Monitoring

### Health Checks

- API: `http://localhost:8000/health`
- Readiness: `http://localhost:8000/ready`

### Metrics

Prometheus metrics available at `/metrics`

### Logging

Logs are output to stdout in JSON format.

## Scaling

### Horizontal Scaling

```bash
# Scale backend
docker-compose up -d --scale backend=3

# Or with Kubernetes
kubectl scale deployment ai-reviewer-backend --replicas=3
```

### Performance Tuning

- Adjust `DATABASE_POOL_SIZE`
- Increase Celery workers
- Configure Redis maxmemory

## Security

### Checklist

- [ ] Use HTTPS in production
- [ ] Set strong `SECRET_KEY`
- [ ] Enable webhook signature verification
- [ ] Use secrets management (Vault, AWS Secrets Manager)
- [ ] Limit database permissions
- [ ] Configure CORS appropriately
- [ ] Enable rate limiting

## Backup

### Database

```bash
# Backup
docker-compose exec postgres pg_dump -U postgres ai_code_reviewer > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres ai_code_reviewer < backup.sql
```

### Redis

```bash
# Backup
docker-compose exec redis redis-cli BGSAVE
```

## Troubleshooting

### Common Issues

1. **Database connection failed**
   - Check `DATABASE_URL`
   - Verify PostgreSQL is running
   - Check network connectivity

2. **Redis unavailable**
   - Verify Redis is running
   - Check `REDIS_HOST` and `REDIS_PORT`

3. **LLM API errors**
   - Verify API keys
   - Check rate limits
   - Review error logs

### Debug Mode

Enable debug mode:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

## Updates

```bash
# Pull latest code
git pull

# Rebuild images
docker-compose build

# Restart services
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```
