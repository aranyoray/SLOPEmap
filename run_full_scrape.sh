#!/bin/bash

# Full Scrape Script
# Runs the complete scraping process for all counties

set -e

echo "=============================================="
echo "NREL SLOPE - Full Scrape"
echo "=============================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the scraper
echo "Starting full scrape..."
echo "This may take a while..."
echo ""

python3 scraper/agent_scraper.py --start G0100010 --end G5600450 --agents 5

echo ""
echo "=============================================="
echo "Scraping Complete!"
echo "=============================================="
echo ""

# Process the scraped data
echo "Processing scraped data..."
python3 scraper/data_parser.py

echo ""
echo "=============================================="
echo "Full Scrape Process Complete!"
echo "=============================================="
echo ""
echo "Next step: Run python prepare_for_vercel.py to prepare for deployment"
echo "=============================================="

