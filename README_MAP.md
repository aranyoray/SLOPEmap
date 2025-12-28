# 🗺️ Interactive Map Dashboard - Quick Start

Scrape county data from **two URL columns** in urls.csv and deploy an interactive map with hover + search!

---

## ⚡ One Command (5-7 minutes)

```bash
git clone https://github.com/aranyoray/SLOPEmap.git
cd SLOPEmap
chmod +x scrape_and_deploy.sh
./scrape_and_deploy.sh
```

This does EVERYTHING:
1. ✅ Generates `urls.csv` with 2 URL columns
2. ✅ Scrapes from **both URL columns** (energy-snapshot + data-viewer)
3. ✅ Merges data from both sources
4. ✅ Creates interactive map dashboard
5. ✅ Prepares for Vercel deployment

**Time:** 5-7 minutes total

---

## 🗺️ What You Get

### **Interactive Map Features:**

✅ **Hover Info**
- County name, population, metrics
- Solar and wind potential
- Energy burden statistics
- All data from both URLs merged

✅ **Search & Auto-Zoom**
- Search by county name or GeoID
- Map automatically zooms to county
- Shows detailed info panel

✅ **Filters**
- Filter by state
- Real-time map updates
- Statistics dashboard

✅ **Visualizations**
- Color-coded by solar potential
- Interactive markers
- Tooltips on hover

---

## 📊 Dashboard Preview

```
┌─────────────────────────────────────────────────────────────┐
│           NREL SLOPE Interactive County Map                 │
│     Hover over counties • Search to zoom                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Search: _____]  [State: All ▼]  [Search & Zoom]         │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                                                       │ │
│  │            [Interactive US Map]                      │ │
│  │         • • • • • •                                  │ │
│  │       • • • • • • • •                                │ │
│  │      • Hover for county info                         │ │
│  │       • • • • • • • •                                │ │
│  │         • • • • • •                                  │ │
│  │                                                       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [560 Counties]  [1.2M MW Solar]  [850K MW Wind]          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 URLs.csv Format

The script generates `urls.csv` with two URL columns:

```csv
geoid,url_energy_snapshot,url_data_viewer
G0100010,https://maps.nrel.gov/slope/energy-snapshot?geoId=G0100010,https://maps.nrel.gov/slope/data-viewer?geoId=G0100010
G0100030,https://maps.nrel.gov/slope/energy-snapshot?geoId=G0100030,https://maps.nrel.gov/slope/data-viewer?geoId=G0100030
...
```

The scraper:
- ✅ Scrapes **url_energy_snapshot** column
- ✅ Scrapes **url_data_viewer** column
- ✅ **Merges** both data sources
- ✅ Saves to dashboard

---

## 🚀 Deploy to Vercel

After scraping:

```bash
# Deploy
vercel deploy --prod
```

Your map will be live at: **https://slopemap.vercel.app**

---

## 🎯 Manual Steps (if needed)

### 1. Generate URLs
```bash
python generate_urls.py
```

Creates `urls.csv` with both URL columns.

### 2. Scrape from URLs
```bash
python scraper/url_scraper.py --agents 15
```

Scrapes from **both URL columns**, merges data.

### 3. Prepare for Vercel
```bash
python prepare_for_vercel.py
```

Creates `dashboard/data/dashboard_data.json`.

### 4. Test Locally
```bash
python dashboard/map_app.py
```

Visit: `http://localhost:8050`

### 5. Deploy
```bash
vercel deploy --prod
```

---

## 🔍 Using the Map

### **Hover on County:**
- See popup with all metrics
- Data from both URL sources merged
- Solar potential, wind potential, etc.

### **Search:**
1. Type county name or GeoID
2. Click "Search & Zoom"
3. Map zooms to county
4. Detail panel shows full info

### **Filter:**
- Select state from dropdown
- Map updates in real-time
- Stats recalculate automatically

---

## 📊 Data Merging

The scraper merges data from **both URL columns**:

```python
# From url_energy_snapshot:
- County name, population
- Energy metrics
- Demographics

# From url_data_viewer:
- Additional statistics
- Renewable potential
- Cost data

# Merged result:
{
  "geoid": "G0100010",
  "energy_snapshot_data": {...},
  "data_viewer_data": {...},
  "sources": [url1, url2]
}
```

---

## 🎨 Customization

### Change URL Columns

Edit `urls.csv` to add more columns:

```csv
geoid,url1,url2,url3
G0100010,https://...,https://...,https://...
```

Then update `scraper/url_scraper.py` to scrape all columns.

### Modify Map Style

Edit `dashboard/map_app.py`:
- Change color scheme
- Adjust zoom levels
- Customize hover tooltips
- Add more layers

---

## ⏱️ Performance

| Step | Time | Details |
|------|------|---------|
| URL generation | 5s | Creates urls.csv |
| Scraping (2 URLs × 560 counties) | 4-5 min | 15 parallel agents |
| Processing | 10s | Merges and cleans data |
| Deployment | 1 min | Uploads to Vercel |
| **Total** | **~6 min** | From zero to deployed |

---

## 🆘 Troubleshooting

### "urls.csv not found"
```bash
python generate_urls.py
```

### "No data in map"
```bash
# Check if data file exists
ls dashboard/data/dashboard_data.json

# If missing:
python prepare_for_vercel.py
```

### "Map not loading"
- Check browser console for errors
- Ensure dashboard_data.json has coordinates
- Try: `python dashboard/map_app.py` locally first

---

## ✅ Features Checklist

- [x] Scrapes from **two URL columns**
- [x] Merges data from both sources
- [x] Interactive map with markers
- [x] Hover tooltips with all county info
- [x] Search with auto-zoom
- [x] State filtering
- [x] Real-time statistics
- [x] One-command deployment
- [x] Vercel-ready

---

## 🎉 You're Ready!

Run the one command and get your interactive map live in 6 minutes:

```bash
./scrape_and_deploy.sh && vercel deploy --prod
```

Your map dashboard with hover + search will be live! 🗺️
