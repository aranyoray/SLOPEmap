# NREL SLOPE Scraper Usage Guide

This guide provides detailed instructions on how to use the NREL SLOPE multi-agent scraper and dashboard.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Scraping Data](#scraping-data)
4. [Processing Data](#processing-data)
5. [Launching Dashboard](#launching-dashboard)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection

### Step-by-Step Installation

1. **Clone the repository** (if you haven't already)
   ```bash
   git clone https://github.com/aranyoray/SLOPEmap.git
   cd SLOPEmap
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

## Quick Start

### Test the Scraper

Run a quick test with a limited range of counties:

```bash
python scraper/agent_scraper.py --test --agents 2
```

This will scrape a small sample (G0100010 to G0100050) using 2 agents.

### Launch the Dashboard

```bash
python dashboard/app.py
```

Then open your browser to `http://localhost:8050`

## Scraping Data

### Basic Scraping

Scrape all counties from G0100010 to G5600450:

```bash
python scraper/agent_scraper.py
```

### Custom Range

Scrape a specific range of GeoIDs:

```bash
python scraper/agent_scraper.py --start G0100010 --end G0200010
```

### Adjust Number of Agents

Use more agents for faster scraping (recommended: 5-10):

```bash
python scraper/agent_scraper.py --agents 10
```

⚠️ **Warning**: Too many agents may trigger rate limiting. Start with 5 agents.

### Visible Browser Mode

Run browsers in visible mode (useful for debugging):

```bash
python scraper/agent_scraper.py --visible --test
```

### Complete Examples

#### Example 1: Scrape Alabama counties
```bash
# Alabama state FIPS is 01
python scraper/agent_scraper.py --start G0100010 --end G0199999 --agents 3
```

#### Example 2: Scrape with maximum parallelization
```bash
python scraper/agent_scraper.py --agents 10
```

## Processing Data

After scraping, process the raw data:

```bash
python scraper/data_parser.py
```

This will:
- Load all raw JSON files from `data/raw/`
- Parse and structure the data
- Generate a processed CSV file in `data/processed/`
- Display summary statistics

## Launching Dashboard

### Basic Launch

```bash
python dashboard/app.py
```

Access at: `http://localhost:8050`

### Custom Port

```bash
python dashboard/app.py --port 5000
```

### Use Specific Data File

```bash
python dashboard/app.py --data data/processed/counties_data_20250101_120000.csv
```

### Production Mode (disable debug)

```bash
python dashboard/app.py --no-debug --port 80
```

## Advanced Usage

### Programmatic Usage

You can use the scraper programmatically in your own Python scripts:

```python
import asyncio
from scraper.agent_scraper import AgentOrchestrator

async def main():
    orchestrator = AgentOrchestrator(
        num_agents=5,
        start_geoid="G0100010",
        end_geoid="G0100050",
        headless=True
    )

    stats = await orchestrator.run()
    print(f"Scraped {stats['total_scraped']} counties")

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Data Processing

```python
from scraper.data_parser import DataParser

parser = DataParser()
df = parser.load_and_process_all()

# Your custom analysis here
print(df.describe())
```

### GeoID Generation

```python
from utils.geoid_generator import GeoIDGenerator

generator = GeoIDGenerator("G0100010", "G0100050")

# Get all GeoIDs
geoids = list(generator.generate_range())

# Split for multiple agents
agent_ranges = generator.split_for_agents(5)
```

## Troubleshooting

### Issue: "Playwright not installed"

**Solution**: Install Playwright browsers
```bash
playwright install chromium
```

### Issue: Timeout errors during scraping

**Solutions**:
1. Reduce number of agents
2. Increase timeout in `scraper_agent.py`
3. Check your internet connection

### Issue: No data in dashboard

**Solutions**:
1. Check if data exists in `data/processed/`
2. Run the scraper first: `python scraper/agent_scraper.py --test`
3. Process the data: `python scraper/data_parser.py`

### Issue: Port already in use

**Solution**: Use a different port
```bash
python dashboard/app.py --port 8051
```

### Issue: Memory issues with many agents

**Solution**: Reduce the number of parallel agents
```bash
python scraper/agent_scraper.py --agents 3
```

## Data Files Location

- **Raw scraped data**: `data/raw/*.json`
- **Processed data**: `data/processed/*.csv`
- **Screenshots**: `data/raw/screenshots/*.png`

## Tips for Efficient Scraping

1. **Start small**: Use `--test` mode first to verify everything works
2. **Optimal agents**: 5-10 agents usually provides good balance
3. **Monitor progress**: Watch the progress bar and logs
4. **Save frequently**: Data is saved immediately after each scrape
5. **Resume capability**: You can stop and restart - already scraped data won't be lost

## Performance Benchmarks

Based on testing:
- **Single agent**: ~0.3-0.5 counties/second
- **5 agents**: ~1.5-2.5 counties/second
- **10 agents**: ~3-4 counties/second

For ~560 counties (full range), estimated times:
- 5 agents: ~4-6 minutes
- 10 agents: ~2-3 minutes

## Support

For issues or questions:
- Check the [README.md](README.md)
- Review error logs in console output
- Check the GitHub issues page

## License

MIT License - see LICENSE file for details
