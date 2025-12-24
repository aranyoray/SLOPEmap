#!/bin/bash

# NREL SLOPE Scraper - Quick Start Script

echo "=============================================="
echo "NREL SLOPE Scraper - Quick Start"
echo "=============================================="
echo ""

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
playwright install chromium
echo "✓ Playwright browsers installed"

# Create data directories
echo ""
echo "Creating data directories..."
mkdir -p data/raw data/processed data/raw/screenshots
echo "✓ Data directories created"

# Run test scrape
echo ""
echo "=============================================="
echo "Running test scrape (3 sample counties)..."
echo "=============================================="
echo ""
python scraper/agent_scraper.py --test --agents 2

echo ""
echo "=============================================="
echo "Quick Start Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. Run full scrape: python scraper/agent_scraper.py"
echo "  2. Process data: python scraper/data_parser.py"
echo "  3. Launch dashboard: python dashboard/app.py"
echo ""
echo "For more information, see USAGE_GUIDE.md"
echo "=============================================="
