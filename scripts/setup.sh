#!/bin/bash
# Setup script for AI Code Reviewer

set -e

echo "🚀 AI Code Reviewer - Setup Script"
echo "===================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo ""
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file"
    echo "⚠ Please edit .env with your API keys and configuration"
else
    echo "✓ .env file already exists"
fi

# Create data directories
echo ""
echo "Creating data directories..."
mkdir -p data/chroma
mkdir -p logs
echo "✓ Data directories created"

# Start Docker services (optional)
echo ""
read -p "Do you want to start Docker services (PostgreSQL, Redis)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting Docker services..."
    docker-compose up -d postgres redis
    echo "✓ Docker services started"

    # Wait for services to be ready
    echo "Waiting for services to be ready..."
    sleep 5
fi

# Run migrations
echo ""
read -p "Do you want to run database migrations? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running database migrations..."
    alembic upgrade head
    echo "✓ Migrations complete"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start the API: make run"
echo "3. Visit http://localhost:8000/docs"
echo ""
echo "For more information, see README.md"
