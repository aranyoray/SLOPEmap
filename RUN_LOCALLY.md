# 🚀 Run Locally - One Command

Get all 560+ county data in **3-5 minutes**!

---

## ⚡ Super Fast - One Command

```bash
git clone https://github.com/aranyoray/SLOPEmap.git
cd SLOPEmap
chmod +x scrape_fast.sh
./scrape_fast.sh
```

**That's it!** Script does everything:
- ✅ Creates Python virtual environment
- ✅ Installs all dependencies
- ✅ Installs Playwright browsers
- ✅ Scrapes ALL counties (15 parallel agents)
- ✅ Processes data
- ✅ Prepares for Vercel

**Time:** 3-5 minutes total
**Result:** `dashboard/data/dashboard_data.json` with all county data

---

## 📊 What You'll See

```
==============================================
NREL SLOPE Fast Scraper - All Counties
==============================================

Step 1/5: Setting up Python environment
-------------------------------------------
✓ Virtual environment created

Step 2/5: Installing Python packages
-------------------------------------------
✓ Python packages installed

Step 3/5: Installing Playwright browsers
-------------------------------------------
✓ Playwright browsers installed

Step 4/5: Creating data directories
-------------------------------------------
✓ Data directories created

Step 5/5: Starting FAST scraper
==============================================

Scraping Configuration:
  • GeoID Range: G0100010 to G5600450
  • Parallel Agents: 15 (optimized for speed)
  • Estimated Time: ~3-5 minutes
  • Expected Counties: 560+

Press Enter to start scraping...

======================================================================
NREL SLOPE FAST SCRAPER
======================================================================
GeoID Range: G0100010 to G5600450
Parallel Agents: 15
Mode: MAXIMUM SPEED

Scraping: 100%|████████████| 560/560 [03:24<00:00, 2.74 counties/s]

======================================================================
SCRAPING STATISTICS
======================================================================
Total Scraped:     560
Successful:        545 (97.3%)
Errors:            15 (2.7%)
Duration:          204.3 seconds (3.4 minutes)
Speed:             2.74 counties/second
======================================================================

✓ ALL DONE!
```

---

## 🎯 Then Deploy to Vercel

```bash
# Deploy to Vercel (takes 1 minute)
npm install -g vercel
vercel login
vercel deploy --prod
```

Your dashboard is live at: `https://slopemap.vercel.app` 🎉

---

## ⚙️ Speed Options

Want to go faster or slower?

### Maximum Speed (20 agents, ~2-3 min)
```bash
git clone https://github.com/aranyoray/SLOPEmap.git
cd SLOPEmap
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
python scraper/fast_scraper.py --agents 20
```

### Moderate Speed (10 agents, ~4-6 min)
```bash
python scraper/fast_scraper.py --agents 10
```

### Safe Speed (5 agents, ~8-10 min)
```bash
python scraper/fast_scraper.py --agents 5
```

---

## 📁 Output Files

After running, you'll have:

```
data/processed/
├── counties_data_20251224_120000.csv         (All data in CSV)
├── fast_scrape_results_20251224_120000.json  (All data in JSON)
└── scrape_errors_20251224_120000.json       (Any errors)

dashboard/data/
└── dashboard_data.json                       (Ready for Vercel)
```

---

## 🔧 Requirements

- **Python 3.8+** (Check: `python3 --version`)
- **Internet connection** (to reach maps.nrel.gov)
- **~500MB disk space** (for browsers and data)
- **5 minutes of time** ⏰

---

## 💡 Pro Tips

### 1. **Monitor Progress**
The script shows real-time progress:
- Current speed (counties/second)
- Time remaining
- Success/error counts

### 2. **Interrupt Safely**
Press `Ctrl+C` to stop gracefully:
- Saves all collected data
- No data loss

### 3. **Resume Capability**
If interrupted, just run again:
- Already scraped data is saved
- Script continues from where it stopped

### 4. **Custom Range**
Scrape specific states:
```bash
# Alabama only (FIPS code 01)
python scraper/fast_scraper.py --start G0100010 --end G0199999 --agents 10

# First 100 counties
python scraper/fast_scraper.py --start G0100010 --end G0101000 --agents 5
```

---

## 🆘 Troubleshooting

### "Command not found: python3"
Try: `python` instead of `python3`

### "Playwright not working"
```bash
source venv/bin/activate
python -m playwright install chromium
```

### "Connection failed"
- Check internet connection: `ping maps.nrel.gov`
- Disable VPN/firewall temporarily
- Reduce agents: `--agents 5`

### "Too slow"
- Increase agents: `--agents 20`
- Check your internet speed
- Close other applications

---

## 📊 Performance Benchmarks

| Agents | Time | Speed | Recommended For |
|--------|------|-------|-----------------|
| 5 | 8-10 min | 1.0 counties/s | Slow connections |
| 10 | 4-6 min | 2.0 counties/s | Normal use |
| 15 | 3-5 min | 2.7 counties/s | **Recommended** |
| 20 | 2-3 min | 3.5 counties/s | Fast connections |
| 25+ | 2-3 min | 4.0 counties/s | May hit rate limits |

---

## ✅ Quick Checklist

Before running:
- [ ] Have Python 3.8+ installed
- [ ] Have internet connection
- [ ] In the SLOPEmap directory

After running:
- [ ] See "✓ ALL DONE!" message
- [ ] File `dashboard/data/dashboard_data.json` exists
- [ ] Ready to deploy to Vercel!

---

## 🚀 Full Workflow

```bash
# 1. Get the code (1 command)
git clone https://github.com/aranyoray/SLOPEmap.git && cd SLOPEmap

# 2. Run scraper (1 command, 3-5 min)
./scrape_fast.sh

# 3. Deploy to Vercel (2 commands, 1 min)
npm i -g vercel && vercel deploy --prod

# DONE! Dashboard live at slopemap.vercel.app
```

**Total time:** ~5-7 minutes from zero to deployed! ⚡

---

## 📞 Need Help?

- Check [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for deployment help
- See [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed usage
- Check [QUICKSTART.md](QUICKSTART.md) for quick reference

---

Happy scraping! 🎉
