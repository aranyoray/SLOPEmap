# 🚀 NREL SLOPE Dashboard - Quick Start Guide

Get your dashboard live on Vercel in 3 simple steps!

---

## ⚡ Super Quick Start (5 minutes)

### On Your Local Machine:

```bash
# 1. Clone and setup (1 minute)
git clone https://github.com/aranyoray/SLOPEmap.git
cd SLOPEmap
./local_scrape_setup.sh

# 2. Scrape data (2-3 minutes)
./run_full_scrape.sh

# 3. Deploy to Vercel (1 minute)
npm install -g vercel
vercel login
python prepare_for_vercel.py
vercel deploy --prod
```

**Done!** Your dashboard is now live at `https://[your-project].vercel.app` 🎉

---

## 📋 Detailed Steps

### Step 1: Local Setup (1 minute)

```bash
git clone https://github.com/aranyoray/SLOPEmap.git
cd SLOPEmap
chmod +x local_scrape_setup.sh
./local_scrape_setup.sh
```

**This installs:**
- Python dependencies
- Playwright browsers
- Creates data directories

---

### Step 2: Scrape Data (2-3 minutes)

**Automated (Recommended):**
```bash
chmod +x run_full_scrape.sh
./run_full_scrape.sh
```

**Manual:**
```bash
source venv/bin/activate
python scraper/agent_scraper.py --agents 10
python scraper/data_parser.py
```

**What you'll see:**
```
============================================================
NREL SLOPE Multi-Agent Scraper
============================================================
Scraping progress: 100%|██████████| 560/560 [02:15<00:00, 4.13 counties/s]

✓ Scraping completed successfully!
```

---

### Step 3: Deploy to Vercel (1 minute)

```bash
# Prepare data for deployment
python prepare_for_vercel.py

# Install Vercel CLI (first time only)
npm install -g vercel

# Login to Vercel (first time only)
vercel login

# Deploy!
vercel deploy --prod
```

**Expected output:**
```
🔍 Inspect: https://vercel.com/...
✅ Production: https://slopemap.vercel.app [2s]
```

---

## 🎯 What You Get

### Live Dashboard Features:
- ✅ Interactive county-level energy data
- ✅ Filter by state and status
- ✅ Distribution charts
- ✅ Data table with search
- ✅ Responsive design
- ✅ Fast loading

### Your Dashboard URL:
`https://slopemap.vercel.app` (or your custom domain)

---

## 🔧 Customization

### Change Project Name:
```bash
vercel deploy --prod --name my-energy-dashboard
```

### Add Custom Domain:
1. Go to vercel.com/dashboard
2. Select your project
3. Settings → Domains
4. Add your domain

### Update Data:
```bash
# Re-scrape
python scraper/agent_scraper.py --agents 10

# Re-prepare
python prepare_for_vercel.py

# Re-deploy
vercel deploy --prod
```

---

## 📊 Performance Expectations

| Metric | Value |
|--------|-------|
| Setup Time | 1 minute |
| Scraping Time | 2-3 minutes |
| Deployment Time | 30-60 seconds |
| **Total Time** | **5 minutes** |
| Dashboard Load | <2 seconds |
| Monthly Cost | Free (Hobby tier) |

---

## ⚠️ Prerequisites

Make sure you have:
- [ ] Python 3.8+ installed
- [ ] Node.js installed
- [ ] Git installed
- [ ] Internet connection
- [ ] Vercel account (free at vercel.com)

---

## 🆘 Quick Troubleshooting

### Scraping fails?
```bash
# Check internet connection
ping maps.nrel.gov

# Reinstall Playwright
python -m playwright install chromium
```

### No data in dashboard?
```bash
# Verify data file exists
ls -lh dashboard/data/dashboard_data.json

# If missing, run:
python prepare_for_vercel.py
```

### Vercel deployment fails?
```bash
# Check files exist
ls vercel.json
ls requirements-vercel.txt
ls dashboard/vercel_app.py

# Redeploy
vercel deploy --prod --force
```

---

## 📁 Key Files

After scraping, you should have:
```
SLOPEmap/
├── dashboard/data/dashboard_data.json  ← Your scraped data
├── vercel.json                         ← Vercel config
├── requirements-vercel.txt             ← Python deps
└── dashboard/vercel_app.py            ← Dashboard app
```

---

## 🎓 Learn More

- **Full deployment guide:** [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
- **Usage details:** [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Project README:** [README.md](README.md)

---

## 💡 Pro Tips

1. **Test locally first:**
   ```bash
   python dashboard/vercel_app.py
   # Visit http://localhost:8050
   ```

2. **Scrape specific states:**
   ```bash
   # Alabama only (FIPS 01)
   python scraper/agent_scraper.py --start G0100010 --end G0199999
   ```

3. **Monitor Vercel:**
   ```bash
   vercel logs --follow
   ```

---

## ✅ Success Checklist

- [ ] Ran `./local_scrape_setup.sh`
- [ ] Ran `./run_full_scrape.sh`
- [ ] Saw "Scraping completed successfully!"
- [ ] Ran `python prepare_for_vercel.py`
- [ ] File `dashboard/data/dashboard_data.json` exists
- [ ] Installed Vercel CLI
- [ ] Logged into Vercel
- [ ] Ran `vercel deploy --prod`
- [ ] Dashboard is live! 🎉

---

## 🚀 You're Done!

Your NREL SLOPE County Energy Dashboard is now:
- ✅ Scraped with real data
- ✅ Deployed to Vercel
- ✅ Live and accessible worldwide
- ✅ Free to host

**Share your dashboard:** `https://[your-project].vercel.app`

Need help? Check [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed instructions.
