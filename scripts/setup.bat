@echo off
REM Setup script for AI Code Reviewer (Windows)

echo AI Code Reviewer - Setup Script
echo ================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.11+
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file
echo.
echo Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo Created .env file
    echo WARNING: Please edit .env with your API keys and configuration
) else (
    echo .env file already exists
)

REM Create data directories
echo.
echo Creating data directories...
if not exist data\chroma mkdir data\chroma
if not exist logs mkdir logs
echo Data directories created

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Start Docker: docker-compose up -d
echo 3. Start the API: uvicorn backend.main:app --reload
echo 4. Visit http://localhost:8000/docs
echo.
echo For more information, see README.md

pause
