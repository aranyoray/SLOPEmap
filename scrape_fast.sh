#!/bin/bash

# FAST SCRAPER - One Command Setup and Run
# Optimized for maximum speed (3300+ counties)

echo "=============================================="
echo "NREL SLOPE Fast Scraper - All Counties"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Error: requirements.txt not found${NC}"
    echo "Please run this script from the SLOPEmap directory"
    exit 1
fi

echo -e "${GREEN}Step 1/5: Setting up Python environment${NC}"
echo "-------------------------------------------"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || { echo -e "${RED}Failed to create venv${NC}"; exit 1; }
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || { echo -e "${RED}Failed to activate venv${NC}"; exit 1; }
echo -e "${GREEN}✓ Virtual environment activated${NC}"

echo ""
echo -e "${GREEN}Step 2/5: Installing Python packages${NC}"
echo "-------------------------------------------"
pip install -q --upgrade pip
pip install -q playwright beautifulsoup4 pandas aiohttp plotly dash requests lxml tqdm 2>&1 | grep -v "already satisfied" || true
echo -e "${GREEN}✓ Python packages installed${NC}"

echo ""
echo -e "${GREEN}Step 3/5: Installing Playwright browsers${NC}"
echo "-------------------------------------------"
echo "This may take a few minutes on first run..."
python -m playwright install chromium
echo -e "${GREEN}✓ Playwright browsers installed${NC}"

echo ""
echo -e "${GREEN}Step 4/5: Creating data directories${NC}"
echo "-------------------------------------------"
mkdir -p data/raw data/processed data/raw/screenshots dashboard/data
echo -e "${GREEN}✓ Data directories created${NC}"

echo ""
echo -e "${GREEN}Step 5/5: Starting FAST scraper${NC}"
echo "=============================================="
echo ""
echo "Scraping Configuration:"
echo "  • GeoID Range: G0100010 to G5600450"
echo "  • Parallel Agents: 15 (optimized for speed)"
echo "  • Estimated Time: ~3-5 minutes"
echo "  • Expected Counties: 560+"
echo ""
read -p "Press Enter to start scraping, or Ctrl+C to cancel..."
echo ""

# Run the fast scraper
python scraper/fast_scraper.py --agents 15

# Check if scraping was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo -e "${GREEN}✓ Scraping Complete!${NC}"
    echo "=============================================="
    echo ""

    # Process the data
    echo "Processing scraped data..."
    python scraper/data_parser.py

    # Prepare for Vercel
    echo ""
    echo "Preparing data for Vercel deployment..."
    python prepare_for_vercel.py

    echo ""
    echo "=============================================="
    echo -e "${GREEN}✓ ALL DONE!${NC}"
    echo "=============================================="
    echo ""
    echo "Data files created:"
    ls -lh data/processed/*.csv 2>/dev/null | tail -1 || echo "  No CSV files found"
    ls -lh dashboard/data/dashboard_data.json 2>/dev/null || echo "  dashboard_data.json not created"
    echo ""
    echo "Next steps:"
    echo "  1. Test locally: python dashboard/vercel_app.py"
    echo "  2. Deploy to Vercel: vercel deploy --prod"
    echo ""
    echo "To push data to GitHub:"
    echo "  git add dashboard/data/dashboard_data.json"
    echo "  git commit -m 'Add scraped county data'"
    echo "  git push origin main"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Scraping failed. Check the error messages above.${NC}"
    exit 1
fi
