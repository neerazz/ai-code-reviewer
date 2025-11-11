# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API is open. Authentication will be added in future versions.

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "services": {
    "redis": "up",
    "llm_provider": "anthropic"
  }
}
```

---

### Code Reviews

#### POST /reviews/analyze

Analyze a single code file or snippet.

**Request Body:**
```json
{
  "code": "def hello():\n    print('Hello')",
  "file_path": "example.py",
  "language": "python",
  "context": {
    "description": "Optional context"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "file_path": "example.py",
    "language": "python",
    "lines_of_code": 2,
    "static_analysis": { ... },
    "llm_review": {
      "overall_score": 85,
      "security_score": 90,
      "performance_score": 80,
      "issues": [
        {
          "line": 2,
          "severity": "info",
          "category": "style",
          "title": "Use f-string",
          "description": "Consider using f-strings for better performance",
          "suggestion": "print(f'Hello')"
        }
      ]
    }
  }
}
```

#### POST /reviews/pr

Review a GitHub pull request.

**Request Body:**
```json
{
  "repository": "owner/repo",
  "pr_number": 123,
  "auto_comment": false
}
```

**Response:**
```json
{
  "success": true,
  "review_id": 1,
  "pr_number": 123,
  "files_analyzed": 5,
  "total_issues": 12,
  "issues": [ ... ]
}
```

#### GET /reviews/{review_id}

Get review details by ID.

**Response:**
```json
{
  "id": 1,
  "status": "completed",
  "created_at": "2024-01-01T12:00:00",
  "total_issues": 12,
  "critical_issues": 2,
  "warnings": 5,
  "files_analyzed": 5,
  "comments": [ ... ]
}
```

---

### Migrations

#### POST /migrations/migrate

Migrate code from one framework/version to another.

**Request Body:**
```json
{
  "code": "class MyComponent extends React.Component { ... }",
  "migration_type": "react_class_to_hooks",
  "language": "javascript"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "migration_complexity": "medium",
    "estimated_effort_hours": 2,
    "transformed_code": "const MyComponent = () => { ... }",
    "breaking_changes": [ ... ],
    "migration_steps": [ ... ]
  }
}
```

#### GET /migrations/templates

List available migration templates.

**Response:**
```json
{
  "templates": [
    {
      "type": "react_class_to_hooks",
      "source": "react_class_components",
      "target": "react_hooks",
      "language": "javascript"
    }
  ]
}
```

---

### Repositories

#### POST /repositories

Register a new repository.

**Request Body:**
```json
{
  "name": "my-repo",
  "full_name": "owner/my-repo",
  "url": "https://github.com/owner/my-repo",
  "platform": "github",
  "auto_review_enabled": true
}
```

#### GET /repositories

List all repositories.

#### GET /repositories/{repo_id}

Get repository details.

---

### Webhooks

#### POST /webhooks/github

GitHub webhook endpoint.

**Headers:**
- `X-GitHub-Event`: Event type
- `X-Hub-Signature-256`: Signature for verification

#### POST /webhooks/gitlab

GitLab webhook endpoint.

**Headers:**
- `X-GitLab-Token`: Token for verification

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

**Status Codes:**
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error
