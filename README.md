# SLOPEmap - NREL County Energy Data Scraper & Dashboard

An agent-based geospatial dashboard that scrapes county-wise energy information from the NREL SLOPE (State and Local Planning for Energy) platform.

## Features

- **Multi-Agent Scraping System**: Parallel scraping of county data using multiple agents
- **JavaScript Rendering**: Handles JavaScript-heavy NREL SLOPE website using Playwright
- **Geospatial Visualization**: Interactive dashboard with county-level energy metrics
- **Data Storage**: Structured storage of scraped county energy data
- **Progress Tracking**: Real-time monitoring of scraping progress

## Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Usage

### Scrape County Data

```bash
# Scrape all counties (geoId from G0100010 to G5600450)
python scraper/agent_scraper.py --start G0100010 --end G5600450

# Scrape with custom number of agents
python scraper/agent_scraper.py --agents 10

# Scrape specific range
python scraper/agent_scraper.py --start G0100010 --end G0100050
```

### Launch Dashboard

```bash
python dashboard/app.py
```

Visit `http://localhost:8050` to view the interactive geospatial dashboard.

## Project Structure

```
SLOPEmap/
├── scraper/
│   ├── agent_scraper.py       # Main multi-agent scraping system
│   ├── scraper_agent.py       # Individual scraper agent
│   └── data_parser.py         # Parse and clean scraped data
├── dashboard/
│   ├── app.py                 # Main Dash application
│   ├── components/            # Dashboard components
│   └── assets/                # CSS and static files
├── data/
│   ├── raw/                   # Raw scraped data
│   ├── processed/             # Processed county data
│   └── counties.geojson       # GeoJSON for county boundaries
├── utils/
│   ├── geoid_generator.py     # Generate geoId ranges
│   └── data_storage.py        # Data persistence utilities
├── requirements.txt
└── README.md
```

## GeoID Format

The NREL SLOPE platform uses GeoIDs to identify counties. The format follows the pattern:
- Range: G0100010 to G5600450
- Each GeoID corresponds to a specific U.S. county

## Data Collected

The scraper collects county-level energy data including:
- Energy generation capacity
- Renewable energy potential
- Energy efficiency metrics
- Demographic and geographic information
- Environmental justice indicators

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Acknowledgments

Data source: [NREL SLOPE Platform](https://maps.nrel.gov/slope/)
