#!/bin/bash

# FULL SCRAPING SCRIPT
# Run this after local_scrape_setup.sh completes

echo "=============================================="
echo "Starting NREL SLOPE Full Data Scrape"
echo "=============================================="
echo ""
echo "This will scrape county data from:"
echo "  GeoID: G0100010 to G5600450"
echo "  Using: 10 parallel agents"
echo "  Estimated time: 2-3 minutes"
echo ""
read -p "Press Enter to start scraping, or Ctrl+C to cancel..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Run full scrape
echo "Starting scrape..."
python scraper/agent_scraper.py --agents 10

# Check if scraping was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "Scraping Complete! Processing data..."
    echo "=============================================="
    echo ""

    # Process the scraped data
    python scraper/data_parser.py

    echo ""
    echo "=============================================="
    echo "✓ All Done!"
    echo "=============================================="
    echo ""
    echo "Data files created:"
    echo "  - data/processed/counties_data_*.csv"
    echo "  - data/processed/scrape_results_*.json"
    echo ""
    echo "Next steps:"
    echo "  1. Review the data in data/processed/"
    echo "  2. Run: python dashboard/app.py (to test locally)"
    echo "  3. Follow VERCEL_DEPLOYMENT.md to deploy to Vercel"
    echo ""
else
    echo ""
    echo "❌ Scraping failed. Check the error messages above."
    exit 1
fi
