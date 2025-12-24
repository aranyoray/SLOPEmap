"""
Scraper Agent
Individual agent for scraping NREL SLOPE county data
"""

import asyncio
import json
import time
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_storage import DataStorage


class ScraperAgent:
    """Individual scraper agent for NREL SLOPE data"""

    BASE_URL = "https://maps.nrel.gov/slope/energy-snapshot?geoId="

    def __init__(self, agent_id, headless=True, timeout=30000):
        """
        Initialize scraper agent

        Args:
            agent_id (int): Unique agent identifier
            headless (bool): Run browser in headless mode
            timeout (int): Page load timeout in milliseconds
        """
        self.agent_id = agent_id
        self.headless = headless
        self.timeout = timeout
        self.storage = DataStorage()
        self.browser = None
        self.context = None
        self.page = None

    async def initialize(self):
        """Initialize browser and page"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await self.context.new_page()
        print(f"[Agent {self.agent_id}] Initialized")

    async def scrape_county(self, geoid):
        """
        Scrape data for a single county

        Args:
            geoid (str): County GeoID

        Returns:
            dict: Scraped county data
        """
        url = f"{self.BASE_URL}{geoid}"
        print(f"[Agent {self.agent_id}] Scraping {geoid}...")

        try:
            # Navigate to page
            await self.page.goto(url, wait_until='networkidle', timeout=self.timeout)

            # Wait for content to load
            await asyncio.sleep(3)

            # Extract data from the page
            data = await self.extract_data(geoid)

            print(f"[Agent {self.agent_id}] ✓ Scraped {geoid}")
            return data

        except PlaywrightTimeout:
            print(f"[Agent {self.agent_id}] ✗ Timeout for {geoid}")
            return self.create_error_record(geoid, "timeout")

        except Exception as e:
            print(f"[Agent {self.agent_id}] ✗ Error scraping {geoid}: {str(e)}")
            return self.create_error_record(geoid, str(e))

    async def extract_data(self, geoid):
        """
        Extract data from the loaded page

        Args:
            geoid (str): County GeoID

        Returns:
            dict: Extracted data
        """
        data = {
            "geoid": geoid,
            "timestamp": datetime.now().isoformat(),
            "url": f"{self.BASE_URL}{geoid}",
            "agent_id": self.agent_id,
            "status": "success"
        }

        try:
            # Extract page title
            title = await self.page.title()
            data["page_title"] = title

            # Extract main content
            # Wait for main content container
            await self.page.wait_for_selector('body', timeout=5000)

            # Get all text content
            text_content = await self.page.evaluate('''() => {
                return document.body.innerText;
            }''')
            data["page_content"] = text_content

            # Try to extract structured data if available
            # Look for common data patterns
            try:
                # Extract any visible metrics/statistics
                stats = await self.page.evaluate('''() => {
                    const stats = {};

                    // Look for any data attributes or classes that might contain metrics
                    const dataElements = document.querySelectorAll('[class*="metric"], [class*="stat"], [class*="value"]');
                    dataElements.forEach((el, idx) => {
                        stats[`metric_${idx}`] = el.innerText.trim();
                    });

                    return stats;
                }''')
                data["extracted_stats"] = stats
            except:
                data["extracted_stats"] = {}

            # Take screenshot for reference
            screenshot_path = f"data/raw/screenshots/{geoid}.png"
            Path("data/raw/screenshots").mkdir(parents=True, exist_ok=True)
            await self.page.screenshot(path=screenshot_path)
            data["screenshot"] = screenshot_path

        except Exception as e:
            data["extraction_error"] = str(e)

        return data

    def create_error_record(self, geoid, error_msg):
        """
        Create error record for failed scrape

        Args:
            geoid (str): County GeoID
            error_msg (str): Error message

        Returns:
            dict: Error record
        """
        return {
            "geoid": geoid,
            "timestamp": datetime.now().isoformat(),
            "url": f"{self.BASE_URL}{geoid}",
            "agent_id": self.agent_id,
            "status": "error",
            "error": error_msg
        }

    async def scrape_batch(self, geoids):
        """
        Scrape a batch of counties

        Args:
            geoids (list): List of GeoIDs to scrape

        Returns:
            list: List of scraped data dictionaries
        """
        await self.initialize()

        results = []
        for geoid in geoids:
            result = await self.scrape_county(geoid)
            results.append(result)

            # Save immediately
            self.storage.save_raw_data(geoid, result)

            # Small delay between requests
            await asyncio.sleep(1)

        await self.cleanup()
        return results

    async def cleanup(self):
        """Close browser and cleanup resources"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        print(f"[Agent {self.agent_id}] Cleaned up")


async def test_agent():
    """Test scraper agent with sample GeoIDs"""
    agent = ScraperAgent(agent_id=1, headless=True)

    test_geoids = ["G0100010", "G0100030", "G0100050"]

    results = await agent.scrape_batch(test_geoids)

    print("\n=== Results ===")
    for result in results:
        print(f"\nGeoID: {result['geoid']}")
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Title: {result.get('page_title', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(test_agent())
