#!/bin/bash

# LOCAL SCRAPING SETUP SCRIPT
# Run this on your local machine with internet access

echo "=============================================="
echo "NREL SLOPE Data Scraper - Local Setup"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    echo "Please run this script from the SLOPEmap directory"
    exit 1
fi

echo "✓ Found SLOPEmap directory"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
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
echo "Installing Python dependencies..."
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers (this may take a few minutes)..."
python -m playwright install chromium
echo "Installing Playwright browsers..."
playwright install chromium
echo "✓ Playwright browsers installed"

# Create data directories
echo ""
echo "Creating data directories..."
mkdir -p data/raw data/processed data/raw/screenshots
mkdir -p data/raw data/processed data/raw/screenshots dashboard/data
echo "✓ Data directories created"

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "Next step: Run ./run_full_scrape.sh to scrape the data"
echo "=============================================="

