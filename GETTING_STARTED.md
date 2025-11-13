# Getting Started with AI Code Reviewer

This guide will help you set up and run the AI Code Reviewer project on your local machine.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Using the Application](#using-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

- **Git** (version 2.0 or higher)
  - [Download Git](https://git-scm.com/downloads)
  - Verify: `git --version`

- **Docker** (version 20.10 or higher) - *Recommended*
  - [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - Verify: `docker --version`

- **Docker Compose** (version 2.0 or higher) - *Recommended*
  - Usually included with Docker Desktop
  - Verify: `docker-compose --version`

### Alternative: Manual Setup (Without Docker)

If you prefer not to use Docker:

- **Python** (version 3.11 or higher)
  - [Download Python](https://www.python.org/downloads/)
  - Verify: `python --version` or `python3 --version`

- **pip** (Python package manager)
  - Usually included with Python
  - Verify: `pip --version` or `pip3 --version`

- **Node.js** (version 18 or higher)
  - [Download Node.js](https://nodejs.org/)
  - Verify: `node --version`

- **npm** (Node package manager)
  - Included with Node.js
  - Verify: `npm --version`

### Optional: API Keys (For AI-Powered Analysis)

The application works perfectly in **mock mode** without API keys. However, for full AI-powered analysis, you'll need one of:

- **Anthropic Claude API Key** (recommended) - See [How to Get API Keys](#how-to-get-api-keys)
- **OpenAI API Key** (alternative)

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/neerazz/ai-code-reviewer.git
cd ai-code-reviewer
```

### Step 2: Choose Your Installation Method

#### Option A: Docker Installation (Recommended)

This is the easiest way to get started.

```bash
# Start both frontend and backend
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**That's it!** Skip to [Using the Application](#using-the-application).

#### Option B: Manual Installation

If you're not using Docker, follow these steps:

**Backend Setup:**

```bash
# Navigate to backend directory
cd ai-code-reviewer/backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Frontend Setup:**

```bash
# Open a new terminal
# Navigate to frontend directory
cd ai-code-reviewer/frontend

# Install dependencies
npm install
```

---

## Configuration

### Environment Variables

1. **Copy the example environment file:**

```bash
cp .env.example .env
```

2. **Edit `.env` file:**

```bash
# Open in your preferred editor
nano .env
# OR
code .env
# OR
vim .env
```

3. **Basic Configuration (Works without API keys):**

The application works in mock mode by default. No API keys required!

```env
# Application Settings
APP_NAME="AI Code Reviewer"
DEBUG=True
ENVIRONMENT=development

# LLM Configuration (Optional - leave empty for mock mode)
LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=  # Add your key here if you have one
# OPENAI_API_KEY=     # Or use OpenAI instead
```

4. **Advanced Configuration (With AI Integration):**

If you have API keys, add them:

```env
# For Anthropic Claude (recommended)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022

# OR for OpenAI
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
```

See [API_KEYS.md](./API_KEYS.md) for detailed instructions on obtaining API keys.

---

## Running the Application

### Using Docker (Recommended)

```bash
# Start services in background
docker-compose up -d

# Check if services are running
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Manual Setup

**Terminal 1 - Backend:**

```bash
cd ai-code-reviewer/backend

# Activate virtual environment if you created one
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Start the backend server
PYTHONPATH=. uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Terminal 2 - Frontend:**

```bash
cd ai-code-reviewer/frontend

# Start the development server
npm start
```

You should see:
```
Compiled successfully!
You can now view frontend in the browser.
  Local:            http://localhost:3000
```

---

## Using the Application

### 1. Access the Application

- **Frontend UI**: Open your browser and go to [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Try Your First Code Review

**Using the Web Interface:**

1. Open [http://localhost:3000](http://localhost:3000)
2. Paste this sample code:

```python
def calculate_sum(a, b):
    password = "12345"  # This will be detected as a security issue!
    return a + b
```

3. Click **"Review Code"**
4. View the comprehensive analysis!

**Using the API:**

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def calculate_sum(a, b):\n    password = \"12345\"\n    return a + b"
  }'
```

### 3. Explore Features

- **Multi-Language Support**: Try JavaScript, TypeScript, Java, Go, etc.
- **Security Scanning**: The analyzer detects hardcoded secrets and vulnerabilities
- **Quality Metrics**: Get detailed code quality scores and metrics
- **Smart Suggestions**: Receive actionable improvement recommendations

---

## Troubleshooting

### Common Issues

**1. Port Already in Use**

If you see `Port 3000 is already in use` or `Port 8000 is already in use`:

```bash
# Find and kill the process using the port
# On macOS/Linux:
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**2. Docker Issues**

```bash
# Reset Docker containers
docker-compose down
docker-compose up --build

# Check Docker is running
docker ps

# Clean up old images
docker system prune
```

**3. Module Not Found Errors (Backend)**

```bash
# Ensure you're in the backend directory
cd ai-code-reviewer/backend

# Reinstall dependencies
pip install -r requirements.txt

# Make sure PYTHONPATH is set when running
PYTHONPATH=. uvicorn api.main:app --reload
```

**4. npm Install Failures (Frontend)**

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**5. CORS Errors**

If you see CORS errors in the browser console:
- Ensure backend is running on port 8000
- Check that the backend CORS configuration includes `http://localhost:3000`

### Still Having Issues?

1. Check the [FAQ](./docs/FAQ.md)
2. Search [existing issues](https://github.com/neerazz/ai-code-reviewer/issues)
3. Create a [new issue](https://github.com/neerazz/ai-code-reviewer/issues/new) with:
   - Your operating system
   - Python/Node.js versions
   - Error messages
   - Steps to reproduce

---

## Next Steps

### Learn More

- Read the full [README.md](./README.md)
- Explore [API Documentation](http://localhost:8000/docs)
- Check out [Live Demo Examples](./DEMO.md)
- Review [Architecture Overview](./ARCHITECTURE.md)

### Contribute

- Read [Contributing Guidelines](./CONTRIBUTING.md)
- Check [open issues](https://github.com/neerazz/ai-code-reviewer/issues)
- Submit a pull request

### Customize

- Add your own code analysis rules
- Integrate with your CI/CD pipeline
- Deploy to production (see [Deployment Guide](./docs/DEPLOYMENT.md))

---

## Quick Reference

### Useful Commands

```bash
# Docker
docker-compose up -d              # Start services
docker-compose down               # Stop services
docker-compose logs -f            # View logs
docker-compose restart            # Restart services

# Backend (Manual)
cd ai-code-reviewer/backend
PYTHONPATH=. uvicorn api.main:app --reload

# Frontend (Manual)
cd ai-code-reviewer/frontend
npm start

# Health Checks
curl http://localhost:8000/health
curl http://localhost:3000
```

### Default URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc

---

**Welcome to AI Code Reviewer! 🚀**

If you found this helpful, please give us a ⭐ on [GitHub](https://github.com/neerazz/ai-code-reviewer)!
