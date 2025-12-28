#!/bin/bash

# Complete workflow: Generate URLs -> Scrape -> Prepare -> Deploy
# One command to do everything!

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         NREL SLOPE: Complete Scrape & Deploy Workflow         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Step 1: Setup
echo -e "${GREEN}[1/6] Setting up environment...${NC}"
echo "─────────────────────────────────────────────────────────────────"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q --upgrade pip
pip install -q playwright pandas aiohttp plotly dash requests tqdm
python -m playwright install chromium

echo -e "${GREEN}✓ Environment ready${NC}"
echo ""

# Step 2: Generate URLs
echo -e "${GREEN}[2/6] Generating urls.csv...${NC}"
echo "─────────────────────────────────────────────────────────────────"

if [ ! -f "urls.csv" ] || [ "$1" == "--regenerate" ]; then
    python generate_urls.py
    echo -e "${GREEN}✓ Generated urls.csv${NC}"
else
    echo -e "${YELLOW}✓ urls.csv already exists (use --regenerate to recreate)${NC}"
fi

echo ""

# Step 3: Scrape from URLs
echo -e "${GREEN}[3/6] Scraping data from both URL columns...${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "This will scrape from:"
echo "  • url_energy_snapshot column"
echo "  • url_data_viewer column"
echo ""

python scraper/url_scraper.py --agents 15

echo -e "${GREEN}✓ Scraping complete${NC}"
echo ""

# Step 4: Process data
echo -e "${GREEN}[4/6] Processing scraped data...${NC}"
echo "─────────────────────────────────────────────────────────────────"

python scraper/data_parser.py

echo -e "${GREEN}✓ Data processed${NC}"
echo ""

# Step 5: Prepare for Vercel
echo -e "${GREEN}[5/6] Preparing for Vercel deployment...${NC}"
echo "─────────────────────────────────────────────────────────────────"

python prepare_for_vercel.py

echo -e "${GREEN}✓ Data prepared for Vercel${NC}"
echo ""

# Step 6: Test locally (optional)
echo -e "${GREEN}[6/6] Local testing...${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "You can test the map dashboard locally by running:"
echo "  python dashboard/map_app.py"
echo ""
echo "Then visit: http://localhost:8050"
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                      ✓ ALL DONE!                               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Files created:"
echo "  ✓ urls.csv (county URLs)"
echo "  ✓ data/processed/counties_data_merged.csv (scraped data)"
echo "  ✓ dashboard/data/dashboard_data.json (for Vercel)"
echo ""
echo "Next steps:"
echo ""
echo "1. Test locally (optional):"
echo "   python dashboard/map_app.py"
echo ""
echo "2. Deploy to Vercel:"
echo "   vercel deploy --prod"
echo ""
echo "3. Or push to GitHub:"
echo "   git add dashboard/data/dashboard_data.json urls.csv"
echo "   git commit -m 'Add scraped county data'"
echo "   git push origin main"
echo ""
echo "Your interactive map will show:"
echo "  • County boundaries on hover"
echo "  • Detailed info tooltips"
echo "  • Search with auto-zoom"
echo "  • Energy metrics visualization"
echo ""
echo "Dashboard URL: https://slopemap.vercel.app"
echo ""
