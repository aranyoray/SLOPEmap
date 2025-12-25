#!/bin/bash

# Local Scrape Setup Script
# Sets up the environment for scraping NREL SLOPE data

set -e

echo "=============================================="
echo "NREL SLOPE Scraper - Local Setup"
echo "=============================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
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
mkdir -p data/raw data/processed data/raw/screenshots dashboard/data
echo "✓ Data directories created"

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "Next step: Run ./run_full_scrape.sh to scrape the data"
echo "=============================================="

