# Deploying NREL SLOPE Dashboard to Vercel

Complete guide to scrape data locally and deploy to Vercel.

## Prerequisites

- Python 3.8+ installed
- Node.js and npm installed
- Vercel CLI installed (`npm i -g vercel`)
- Git installed
- Internet connection

---

## Part 1: Scrape Data Locally

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/aranyoray/SLOPEmap.git
cd SLOPEmap

# Run setup script
chmod +x local_scrape_setup.sh
./local_scrape_setup.sh
```

This will:
- Create a virtual environment
- Install all Python dependencies
- Install Playwright browsers
- Create necessary directories

### Step 2: Run the Scraper

**Option A: Full automated scrape**
```bash
chmod +x run_full_scrape.sh
./run_full_scrape.sh
```

**Option B: Manual scrape**
```bash
# Activate virtual environment
source venv/bin/activate

# Quick test (5 counties, 10 seconds)
python scraper/agent_scraper.py --test --agents 2

# Small sample (50 counties, 30 seconds)
python scraper/agent_scraper.py --start G0100010 --end G0100500 --agents 5

# Full scrape (ALL counties, 2-3 minutes)
python scraper/agent_scraper.py --agents 10
```

**What happens during scraping:**
- Browser agents will scrape county data from NREL SLOPE
- Progress bar shows real-time status
- Data saved to `data/raw/` and `data/processed/`
- Estimated time: 2-3 minutes for full scrape with 10 agents

### Step 3: Process the Data

```bash
# Parse and structure the scraped data
python scraper/data_parser.py

# Prepare data for Vercel deployment
python prepare_for_vercel.py
```

This creates:
- `dashboard/data/dashboard_data.json` - Optimized data for dashboard
- `dashboard_data.json` - Backup copy

### Step 4: Test Locally (Optional)

```bash
# Test the Vercel version locally
python dashboard/vercel_app.py
```

Open `http://localhost:8050` to verify the dashboard works.

---

## Part 2: Deploy to Vercel

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

Follow the prompts to authenticate.

### Step 3: Deploy

```bash
# Deploy to Vercel
vercel deploy

# Or deploy to production immediately
vercel deploy --prod
```

**During deployment:**
1. Vercel will ask for project settings:
   - **Set up and deploy**: Yes
   - **Project name**: slopemap (or your choice)
   - **Directory**: ./ (current directory)
   - **Override settings**: No

2. Vercel will:
   - Upload your code
   - Upload the scraped data JSON
   - Install Python dependencies
   - Build the dashboard
   - Deploy to a URL

3. You'll get a URL like: `https://slopemap.vercel.app`

### Step 4: Configure Custom Domain (Optional)

In Vercel dashboard:
1. Go to your project
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

---

## Updating Data

When you want to update the dashboard with fresh data:

```bash
# 1. Scrape new data
python scraper/agent_scraper.py --agents 10

# 2. Prepare for Vercel
python prepare_for_vercel.py

# 3. Redeploy to Vercel
vercel deploy --prod
```

---

## Project Structure for Deployment

```
SLOPEmap/
├── vercel.json                    # Vercel configuration
├── requirements-vercel.txt        # Vercel Python dependencies
├── dashboard/
│   ├── vercel_app.py             # Dashboard app for Vercel
│   └── data/
│       └── dashboard_data.json   # Scraped data (created by you)
├── dashboard_data.json           # Backup data file
└── data/                         # Local data (not deployed)
```

**Files deployed to Vercel:**
- `vercel.json`
- `requirements-vercel.txt`
- `dashboard/vercel_app.py`
- `dashboard/data/dashboard_data.json`
- `dashboard/assets/style.css`

**Files NOT deployed (too large or unnecessary):**
- `data/raw/*` (raw scrape files)
- `scraper/*` (scraping code)
- `venv/*` (virtual environment)
- `.git/*` (git history)

---

## Troubleshooting

### "No data file found" on Vercel

**Solution:**
```bash
# Make sure you ran data preparation
python prepare_for_vercel.py

# Check file was created
ls -lh dashboard/data/dashboard_data.json

# Redeploy
vercel deploy --prod
```

### Build fails on Vercel

**Solution:**
- Check `vercel.json` is in root directory
- Verify `requirements-vercel.txt` exists
- Make sure `dashboard/vercel_app.py` exists

### Dashboard shows sample data

**Cause:** No real scraped data uploaded

**Solution:**
```bash
# Scrape data first
python scraper/agent_scraper.py --agents 10

# Prepare for Vercel
python prepare_for_vercel.py

# Verify file created
cat dashboard/data/dashboard_data.json | head -20

# Redeploy
vercel deploy --prod
```

### Scraping fails locally

**Common issues:**
1. **Playwright not installed:** Run `playwright install chromium`
2. **No internet:** Check your connection
3. **Firewall blocking:** Disable VPN/firewall temporarily

---

## Environment Variables (if needed)

If you want to add environment variables:

```bash
# In Vercel dashboard
vercel env add VARIABLE_NAME

# Or in command line
vercel env add VARIABLE_NAME production
```

---

## Performance Tips

1. **Optimize data file size:**
   - Only include necessary columns
   - Remove debugging information
   - Compress JSON if very large

2. **Caching:**
   - Vercel automatically caches static files
   - Dashboard loads faster after first visit

3. **Monitoring:**
   - Check Vercel dashboard for usage
   - Monitor function execution time

---

## Cost Estimate

**Vercel Hobby (Free) Tier:**
- ✓ Unlimited deployments
- ✓ 100 GB bandwidth/month
- ✓ Serverless function executions
- ✓ Custom domains (with restrictions)

**For this dashboard:**
- Data size: ~1-5 MB
- Should work fine on free tier
- Upgrade to Pro if you exceed limits

---

## Quick Reference Commands

```bash
# Setup
./local_scrape_setup.sh

# Scrape
./run_full_scrape.sh

# Prepare for deployment
python prepare_for_vercel.py

# Deploy
vercel deploy --prod

# Check logs
vercel logs

# Remove deployment
vercel remove slopemap
```

---

## Support

- Vercel Docs: https://vercel.com/docs
- Dash Docs: https://dash.plotly.com/
- Issues: https://github.com/aranyoray/SLOPEmap/issues

---

## What Gets Deployed

✅ **Included in deployment:**
- Dashboard application code
- Scraped data JSON
- CSS styling
- Python dependencies (minimal)

❌ **NOT included:**
- Scraping tools (not needed on server)
- Raw data files (too large)
- Development files

---

## Success Checklist

Before deploying, make sure:

- [ ] Scraped data successfully
- [ ] `dashboard/data/dashboard_data.json` exists
- [ ] Tested locally with `python dashboard/vercel_app.py`
- [ ] Verified data shows correctly
- [ ] Installed Vercel CLI
- [ ] Logged into Vercel
- [ ] Ready to deploy!

---

Your dashboard will be live at: `https://[your-project-name].vercel.app` 🚀
