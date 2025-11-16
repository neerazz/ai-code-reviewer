# AI Code Reviewer - User Guide

**Version**: 1.0.0
**Last Updated**: 2025-11-16
**Audience**: End Users, Developers, Team Leads, Code Reviewers

---

## Table of Contents

1. [Introduction](#introduction)
2. [What is AI Code Reviewer?](#what-is-ai-code-reviewer)
3. [Key Features](#key-features)
4. [Prerequisites](#prerequisites)
5. [Installation Guide](#installation-guide)
6. [Getting Started](#getting-started)
7. [Using the Application](#using-the-application)
8. [Supported Languages](#supported-languages)
9. [Understanding Review Results](#understanding-review-results)
10. [Configuration Options](#configuration-options)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#faq)
13. [Best Practices](#best-practices)
14. [Support & Resources](#support--resources)

---

## Introduction

Welcome to the AI Code Reviewer User Guide! This comprehensive document will help you understand, install, configure, and effectively use the AI Code Reviewer application to improve your code quality.

### Who Should Read This Guide?

- **Developers** who want to improve their code quality
- **Code reviewers** looking for automated assistance
- **Team leads** implementing code quality standards
- **Students** learning programming best practices
- **Anyone** who writes code and wants instant feedback

---

## What is AI Code Reviewer?

AI Code Reviewer is an intelligent code analysis tool that combines **AI-powered analysis** with **static code analysis** to provide comprehensive code reviews. It helps you:

- **Find bugs** before they reach production
- **Detect security vulnerabilities** like hardcoded credentials
- **Improve code quality** with actionable suggestions
- **Learn best practices** for multiple programming languages
- **Save time** in code review processes

### How It Works

```
┌─────────────┐
│  Your Code  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  AI Code Reviewer Platform  │
├─────────────────────────────┤
│  1. Language Detection      │
│  2. Static Analysis         │
│  3. AI-Powered Review       │
│  4. Security Scanning       │
│  5. Metrics Calculation     │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Comprehensive Review   │
│  • Quality Score        │
│  • Issues & Suggestions │
│  • Code Metrics         │
│  • Security Alerts      │
└─────────────────────────┘
```

---

## Key Features

### 1. Multi-Language Support
Supports **15+ programming languages** including:
- Python
- JavaScript/TypeScript
- Java
- Go
- C/C++
- Rust
- Ruby
- PHP
- SQL
- HTML/CSS
- And more!

### 2. Dual Analysis Engine

**Static Analysis**:
- Language detection
- Code metrics (lines, complexity, etc.)
- Security vulnerability detection
- Best practice checks

**AI-Powered Analysis** (Optional):
- Deep code understanding
- Context-aware suggestions
- Performance optimization tips
- Architecture recommendations

### 3. Security Scanning

Automatically detects:
- Hardcoded passwords
- API keys and tokens
- SQL injection vulnerabilities
- Unsafe eval() usage
- Common security anti-patterns

### 4. Quality Scoring

Get an instant **quality score (0-100)** based on:
- Code complexity
- Issue severity
- Best practice adherence
- Code documentation
- Line length and formatting

### 5. Real-Time Feedback

- Instant analysis (typically < 2 seconds)
- Interactive web interface
- Clear, actionable suggestions
- Color-coded severity levels

### 6. Mock Mode

Works **without API keys** for basic analysis:
- Language detection
- Static analysis
- Security scanning
- Code metrics

---

## Prerequisites

### System Requirements

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **Operating System** | Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+) | Any modern OS |
| **RAM** | Minimum 4 GB, Recommended 8 GB | For smooth operation |
| **Disk Space** | 2 GB free space | For application and dependencies |
| **Network** | Internet connection | Required for AI features |

### Software Requirements

#### Option 1: Using Docker (Recommended)

- **Docker Desktop**: Version 20.10+ ([Download](https://www.docker.com/products/docker-desktop))
- **Docker Compose**: Version 2.0+ (included with Docker Desktop)

#### Option 2: Manual Installation

**Backend Requirements**:
- **Python**: Version 3.9 or higher ([Download](https://www.python.org/downloads/))
- **pip**: Python package manager (included with Python)

**Frontend Requirements**:
- **Node.js**: Version 16.x or higher ([Download](https://nodejs.org/))
- **npm**: Version 8.x or higher (included with Node.js)

### Optional: AI API Keys

For AI-powered analysis, you'll need **ONE** of the following:

1. **Anthropic Claude API Key** ([Get API Key](https://console.anthropic.com/))
   - Recommended for best results
   - Model: Claude 3.5 Sonnet

2. **OpenAI API Key** ([Get API Key](https://platform.openai.com/api-keys))
   - Alternative option
   - Model: GPT-4 or GPT-3.5 Turbo

**Note**: The application works in **mock mode** without API keys, providing static analysis only.

---

## Installation Guide

### Method 1: Docker Installation (Recommended)

**Step 1: Clone the Repository**

```bash
git clone https://github.com/neerazz/ai-code-reviewer.git
cd ai-code-reviewer
```

**Step 2: Configure Environment (Optional)**

Create a `.env` file for AI features:

```bash
# Create .env file
cp .env.example .env

# Edit .env file and add your API key
# For Anthropic Claude:
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LLM_PROVIDER=anthropic

# OR for OpenAI:
# OPENAI_API_KEY=your_openai_api_key_here
# LLM_PROVIDER=openai
```

**Step 3: Start the Application**

```bash
docker-compose up -d
```

**Step 4: Access the Application**

- **Frontend**: Open http://localhost:3000 in your browser
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Method 2: Manual Installation

**Step 1: Clone the Repository**

```bash
git clone https://github.com/neerazz/ai-code-reviewer.git
cd ai-code-reviewer
```

**Step 2: Install Backend**

```bash
# Navigate to backend directory
cd ai-code-reviewer/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Step 3: Install Frontend**

```bash
# Navigate to frontend directory (from project root)
cd ai-code-reviewer/frontend

# Install dependencies
npm install
```

**Step 4: Configure Environment**

```bash
# In backend directory, create .env file
cd ../backend
cp .env.example .env

# Edit .env and add your API key (optional)
```

**Step 5: Start the Application**

Open **two terminal windows**:

**Terminal 1 - Backend**:
```bash
cd ai-code-reviewer/backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend**:
```bash
cd ai-code-reviewer/frontend
npm start
```

**Step 6: Access the Application**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

---

## Getting Started

### First Time Setup

1. **Verify Installation**: Open http://localhost:3000 - you should see the AI Code Reviewer interface

2. **Test Basic Functionality** (No API key needed):
   - Paste this Python code in the input box:
   ```python
   def calculate_total(items):
       password = "admin123"  # security issue
       total = 0
       for item in items:
           total = total + item
       return total
   ```
   - Click "Review Code"
   - You should receive a review with security warnings

3. **Optional: Enable AI Features**:
   - Stop the application
   - Add your API key to `.env` file
   - Restart the application
   - Test again - you'll get AI-powered suggestions

### Quick Start Example

**Python Example**:
```python
def process_data(data):
    # TODO: Add validation
    result = []
    for item in data:
        if item == "test":  # Use === for comparison
            result.append(item)
    return result
```

**What You'll Get**:
- Quality Score: 75/100
- Language: Python
- Issues: TODO comment detected, loose comparison
- Suggestions: Add input validation, use proper comparisons

---

## Using the Application

### Web Interface Overview

The web interface has **two main panels**:

#### Left Panel: Code Input
- **Code Editor**: Paste or type your code here
- **Review Code Button**: Click to analyze your code
- **Clear Button**: Clear the input area

#### Right Panel: Results Display
- **Quality Score**: Overall code quality (0-100)
- **Review Summary**: Comprehensive analysis
- **Suggestions**: Actionable improvements
- **Metrics**: Code statistics and measurements
- **Issues**: Security and quality problems found

### Step-by-Step Usage

**Step 1: Paste Your Code**

Copy your code from your IDE or text editor and paste it into the left panel.

**Step 2: Click "Review Code"**

The application will:
- Auto-detect the programming language
- Analyze the code structure
- Check for security issues
- Calculate quality metrics
- Generate suggestions

**Step 3: Review the Results**

The right panel displays:

1. **Quality Score Card** (Color-coded):
   - 🟢 Green (80-100): Excellent
   - 🟡 Yellow (60-79): Good
   - 🔴 Red (0-59): Needs Improvement

2. **Detailed Review**:
   - Language information
   - Code metrics
   - AI analysis (if enabled)
   - Issue summary

3. **Suggestions List**:
   - Severity indicators (🔴 High, 🟡 Medium, 🟢 Low)
   - Specific line numbers
   - Actionable recommendations

4. **Metrics Cards**:
   - Total Lines
   - Code Lines
   - Comments
   - Issues Found

**Step 4: Apply Improvements**

- Review each suggestion
- Update your code accordingly
- Re-run the review to verify improvements

**Step 5: Iterate**

Keep refining your code until you achieve the desired quality score.

### Using the API Directly

You can also use the API programmatically:

```bash
# Using curl
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    password=\"123\"\n    print(\"Hello\")",
    "language": "python"
  }'
```

```python
# Using Python
import requests

code = """
def calculate(a, b):
    password = "secret"
    return a + b
"""

response = requests.post(
    'http://localhost:8000/review',
    json={'code': code}
)

print(response.json())
```

```javascript
// Using JavaScript
const reviewCode = async (code) => {
  const response = await fetch('http://localhost:8000/review', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code })
  });

  const result = await response.json();
  console.log(result);
};
```

---

## Supported Languages

The AI Code Reviewer supports **15+ programming languages** with varying levels of analysis:

| Language | Detection | Static Analysis | Best Practices | Security Scanning |
|----------|-----------|-----------------|----------------|-------------------|
| **Python** | ✅ | ✅ | ✅ | ✅ |
| **JavaScript** | ✅ | ✅ | ✅ | ✅ |
| **TypeScript** | ✅ | ✅ | ✅ | ✅ |
| **Java** | ✅ | ✅ | ✅ | ✅ |
| **Go** | ✅ | ✅ | ✅ | ✅ |
| **Rust** | ✅ | ✅ | ✅ | ✅ |
| **C/C++** | ✅ | ✅ | ✅ | ✅ |
| **C#** | ✅ | ✅ | ✅ | ✅ |
| **Ruby** | ✅ | ✅ | ✅ | ✅ |
| **PHP** | ✅ | ✅ | ✅ | ✅ |
| **Swift** | ✅ | ✅ | ⚠️ | ⚠️ |
| **Kotlin** | ✅ | ✅ | ⚠️ | ⚠️ |
| **SQL** | ✅ | ✅ | ✅ | ✅ |
| **HTML** | ✅ | ✅ | ⚠️ | ⚠️ |
| **CSS** | ✅ | ✅ | ⚠️ | ⚠️ |

✅ = Full Support | ⚠️ = Partial Support

### Language-Specific Features

**Python**:
- Bare except detection
- Mutable default argument checks
- PEP 8 style recommendations
- Import optimization

**JavaScript/TypeScript**:
- var vs let/const recommendations
- === vs == checks
- Arrow function suggestions
- TypeScript type safety

**Java**:
- Access modifier recommendations
- Exception handling checks
- Static method usage

**Go**:
- Goroutine safety
- Error handling patterns
- Package organization

---

## Understanding Review Results

### Quality Score Breakdown

The quality score (0-100) is calculated based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Issue Severity** | 40% | High issues: -15 points each, Medium: -8, Low: -3 |
| **Code Complexity** | 25% | Cyclomatic complexity over 7: -5 points per level |
| **Code Style** | 20% | Line length, formatting, naming conventions |
| **Documentation** | 15% | Comment ratio (optimal: 10-30%) |

**Score Ranges**:
- **90-100**: Excellent - Production-ready code
- **80-89**: Very Good - Minor improvements needed
- **70-79**: Good - Some refactoring recommended
- **60-69**: Fair - Multiple issues to address
- **Below 60**: Poor - Significant improvements required

### Issue Severity Levels

**🔴 High Severity**:
- Security vulnerabilities
- Critical bugs
- Potential data loss
- **Action**: Fix immediately

**🟡 Medium Severity**:
- Best practice violations
- Maintainability issues
- Performance concerns
- **Action**: Address soon

**🟢 Low Severity**:
- Style inconsistencies
- Minor optimizations
- Documentation gaps
- **Action**: Consider fixing

### Common Issues Detected

#### Security Issues
1. **Hardcoded Passwords/Secrets**
   - Pattern: `password = "value"`
   - Severity: 🔴 High
   - Fix: Use environment variables

2. **SQL Injection**
   - Pattern: String concatenation in queries
   - Severity: 🔴 High
   - Fix: Use parameterized queries

3. **Eval Usage**
   - Pattern: `eval(user_input)`
   - Severity: 🔴 High
   - Fix: Use safer alternatives

#### Code Quality Issues
1. **Long Lines**
   - Threshold: > 120 characters
   - Severity: 🟢 Low
   - Fix: Break into multiple lines

2. **TODO/FIXME Comments**
   - Pattern: `# TODO: fix this`
   - Severity: 🟡 Medium
   - Fix: Address before production

3. **High Complexity**
   - Threshold: Cyclomatic complexity > 7
   - Severity: 🟡 Medium
   - Fix: Refactor into smaller functions

#### Language-Specific Issues

**Python**:
- Bare except clauses
- Mutable default arguments

**JavaScript**:
- Using `var` instead of `let`/`const`
- Using `==` instead of `===`

### Metrics Explained

**Total Lines**: All lines including blank lines

**Code Lines**: Lines containing actual code (excluding comments and blanks)

**Comment Lines**: Lines starting with comment markers (#, //, /*)

**Blank Lines**: Empty lines for readability

**Max Line Length**: Longest line in the code

**Average Line Length**: Mean length of all lines

**Complexity Score** (1-10):
- 1-3: Simple, easy to understand
- 4-6: Moderate complexity
- 7-8: Complex, consider refactoring
- 9-10: Very complex, refactor recommended

---

## Configuration Options

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Application Settings
APP_NAME="AI Code Reviewer"
APP_VERSION="1.0.0"
DEBUG=false
ENVIRONMENT=production

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# LLM Provider (anthropic or openai)
LLM_PROVIDER=anthropic

# Anthropic Claude Configuration
ANTHROPIC_API_KEY=your_key_here
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=4096

# OpenAI Configuration (alternative)
# OPENAI_API_KEY=your_key_here
# LLM_MODEL=gpt-4
# LLM_TEMPERATURE=0.2
# LLM_MAX_TOKENS=4096

# Logging
LOG_LEVEL=INFO
```

### Configuration Parameters

| Parameter | Default | Description | Values |
|-----------|---------|-------------|--------|
| `LLM_PROVIDER` | `anthropic` | AI provider to use | `anthropic`, `openai` |
| `LLM_MODEL` | `claude-3-5-sonnet-20241022` | AI model | See provider docs |
| `LLM_TEMPERATURE` | `0.2` | Response randomness | `0.0` to `1.0` |
| `LLM_MAX_TOKENS` | `4096` | Max response length | `1` to `8192` |
| `LOG_LEVEL` | `INFO` | Logging verbosity | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `DEBUG` | `false` | Debug mode | `true`, `false` |

### Recommended Settings

**For Production**:
```bash
DEBUG=false
ENVIRONMENT=production
LOG_LEVEL=WARNING
LLM_TEMPERATURE=0.1
```

**For Development**:
```bash
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=DEBUG
LLM_TEMPERATURE=0.3
```

**For Cost Optimization** (OpenAI):
```bash
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
LLM_MAX_TOKENS=2048
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Application Won't Start

**Symptom**: Error when running `docker-compose up`

**Solutions**:
1. Check Docker is running:
   ```bash
   docker --version
   docker-compose --version
   ```

2. Check port availability:
   ```bash
   # On Linux/Mac
   lsof -i :3000
   lsof -i :8000

   # On Windows
   netstat -ano | findstr :3000
   netstat -ano | findstr :8000
   ```

3. Stop conflicting processes:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

#### Issue 2: Frontend Can't Connect to Backend

**Symptom**: "Network Error" or "Failed to fetch"

**Solutions**:
1. Verify backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check CORS settings in `backend/api/main.py`

3. Verify frontend API URL in `frontend/src/services/api.ts`

#### Issue 3: AI Analysis Not Working

**Symptom**: Only receiving mock responses

**Solutions**:
1. Verify API key is set:
   ```bash
   # In backend directory
   cat .env | grep API_KEY
   ```

2. Check API key format:
   - Anthropic: Starts with `sk-ant-`
   - OpenAI: Starts with `sk-`

3. Verify provider setting:
   ```bash
   cat .env | grep LLM_PROVIDER
   ```

4. Check logs for errors:
   ```bash
   docker-compose logs backend
   ```

#### Issue 4: Slow Performance

**Solutions**:
1. Reduce `LLM_MAX_TOKENS` in `.env`
2. Use faster model (e.g., `gpt-3.5-turbo` instead of `gpt-4`)
3. Increase system resources (RAM)
4. Check network connectivity

#### Issue 5: Installation Fails

**Python Issues**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

**Node.js Issues**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Issue 6: Permission Denied Errors

**Linux/Mac**:
```bash
# Fix permissions
chmod +x script_name.sh
sudo chown -R $USER:$USER /path/to/project
```

**Docker**:
```bash
# Run with sudo or add user to docker group
sudo docker-compose up
# OR
sudo usermod -aG docker $USER
```

### Getting Help

If you encounter issues not covered here:

1. **Check Logs**:
   ```bash
   # Docker logs
   docker-compose logs backend
   docker-compose logs frontend

   # Manual installation logs
   # Backend logs appear in terminal
   # Frontend logs in browser console (F12)
   ```

2. **Verify Setup**:
   ```bash
   # Check all services
   docker-compose ps

   # Health check
   curl http://localhost:8000/health
   ```

3. **Restart Application**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

4. **Clean Restart**:
   ```bash
   docker-compose down -v
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

## FAQ

### General Questions

**Q: Do I need an API key to use the application?**
A: No! The application works in "mock mode" without any API key, providing static analysis, security scanning, and code metrics. API keys are only needed for AI-powered deep analysis.

**Q: Which AI provider should I use - Anthropic or OpenAI?**
A: We recommend Anthropic Claude 3.5 Sonnet for best results, but OpenAI GPT-4 works great too. Claude tends to provide more detailed code reviews.

**Q: How much does it cost to use?**
A: The application itself is free and open-source. AI API costs depend on your usage:
- Anthropic Claude: ~$3 per 1M input tokens, $15 per 1M output tokens
- OpenAI GPT-4: ~$30 per 1M input tokens, $60 per 1M output tokens
- Typical code review: 500-2000 tokens (~$0.01-$0.10 per review)

**Q: Is my code sent to external servers?**
A: Only if you configure an AI API key. In mock mode, all analysis happens locally. When using AI, code is sent to Anthropic or OpenAI servers for analysis.

**Q: Can I use this in a CI/CD pipeline?**
A: Yes! Use the REST API to integrate with your CI/CD workflows. See the Developer Guide for integration examples.

### Technical Questions

**Q: What's the difference between static and AI analysis?**
A:
- **Static Analysis**: Rule-based, pattern matching, fast, deterministic
- **AI Analysis**: Context-aware, understands intent, slower, more comprehensive

**Q: Can I customize the quality scoring algorithm?**
A: Yes! The scoring logic is in `backend/services/code_analyzer.py`. You can modify weights and penalties.

**Q: How accurate is language detection?**
A: Very accurate (>95%) for common languages. For mixed-language files, specify the language manually via API.

**Q: Can I review multiple files at once?**
A: Currently, the web UI supports single-file review. Use the API to review multiple files programmatically.

**Q: Does it store my code?**
A: No. The application doesn't store any code. Each review is stateless and ephemeral.

### Usage Questions

**Q: What's a good quality score target?**
A: Aim for 80+ for production code, 70+ for prototypes, 60+ for learning/experimentation.

**Q: Should I fix all suggestions?**
A: Not necessarily. Use judgment:
- 🔴 High severity: Always fix
- 🟡 Medium severity: Fix for production
- 🟢 Low severity: Nice to have

**Q: Can I ignore certain rules?**
A: Yes, but currently requires code modification. Future versions will support configuration files.

**Q: How do I improve my quality score?**
A:
1. Fix high-severity issues first
2. Add comments (aim for 10-30% comment ratio)
3. Keep functions small (< 50 lines)
4. Keep complexity low (< 7)
5. Follow language best practices

---

## Best Practices

### For Best Results

1. **Paste Complete Functions**
   - Include full context, not snippets
   - Include relevant imports and dependencies
   - Avoid partial code blocks

2. **Use Descriptive Variable Names**
   - Better reviews with meaningful names
   - AI can provide better suggestions

3. **Review Iteratively**
   - Fix issues one at a time
   - Re-run review after changes
   - Track quality score improvement

4. **Prioritize Security Issues**
   - Always fix 🔴 high-severity security issues
   - Never commit hardcoded credentials
   - Use environment variables for secrets

5. **Document Your Code**
   - Add comments for complex logic
   - Maintain 10-30% comment ratio
   - Use docstrings for functions

### Integration Workflows

**Solo Development**:
```
Write Code → Review → Fix → Re-review → Commit
```

**Team Development**:
```
Write Code → Self-review → Fix → Team Review → Commit
```

**CI/CD Integration**:
```
Commit → Auto-review → Quality Gate → Deploy
```

### Cost Optimization

If using AI features with paid APIs:

1. **Use Mock Mode for Development**
   - Test without API for basic checks
   - Enable AI only for final review

2. **Optimize Token Usage**
   - Review smaller code chunks
   - Set lower `LLM_MAX_TOKENS`
   - Use cheaper models for quick checks

3. **Batch Reviews**
   - Collect multiple changes
   - Review once before commit

4. **Set Usage Limits**
   - Configure API rate limits
   - Monitor monthly usage
   - Set budget alerts

---

## Support & Resources

### Documentation

- **User Guide** (this document): How to use the application
- **Developer Guide**: How to contribute and develop
- **System Design**: Architecture and technical details
- **API Documentation**: http://localhost:8000/docs (when running)

### Getting Help

1. **GitHub Issues**: [Report bugs or request features](https://github.com/neerazz/ai-code-reviewer/issues)
2. **Documentation**: Read the comprehensive guides
3. **API Docs**: Interactive API documentation at `/docs`
4. **Logs**: Check application logs for errors

### Contributing

We welcome contributions! See `CONTRIBUTING.md` for:
- Development setup
- Coding standards
- Pull request process
- Testing guidelines

### Community

- **GitHub**: [neerazz/ai-code-reviewer](https://github.com/neerazz/ai-code-reviewer)
- **License**: MIT
- **Version**: 1.0.0

### Updates and Changelog

Check the repository for:
- Latest releases
- Version changelogs
- Migration guides
- Known issues

---

## Appendix

### Quick Reference Commands

**Docker**:
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild
docker-compose build --no-cache
```

**Manual Installation**:
```bash
# Backend (from backend directory)
source venv/bin/activate
uvicorn api.main:app --reload

# Frontend (from frontend directory)
npm start
```

**Health Checks**:
```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000
```

### Keyboard Shortcuts

- **Ctrl/Cmd + Enter**: Submit code for review (when in textarea)
- **Ctrl/Cmd + K**: Clear code input
- **F12**: Open browser dev tools (for troubleshooting)

### Default Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend API | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/docs |

---

**Thank you for using AI Code Reviewer!**
We hope this tool helps you write better, safer, and more maintainable code.

For questions, issues, or contributions, visit our [GitHub repository](https://github.com/neerazz/ai-code-reviewer).

*Last updated: 2025-11-16 | Version 1.0.0*
