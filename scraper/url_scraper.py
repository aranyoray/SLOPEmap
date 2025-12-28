"""
Scraper that reads from urls.csv and scrapes both URL columns
Merges data from energy-snapshot and data-viewer pages
"""

import asyncio
import csv
import sys
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
from playwright.async_api import async_playwright

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_storage import DataStorage


class URLBasedScraper:
    """Scrape counties from urls.csv"""

    def __init__(self, urls_csv="urls.csv", num_agents=15):
        self.urls_csv = urls_csv
        self.num_agents = num_agents
        self.storage = DataStorage()
        self.results = []
        self.errors = []

    def load_urls(self):
        """Load URLs from CSV"""
        print(f"Loading URLs from {self.urls_csv}...")

        urls_data = []
        with open(self.urls_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                urls_data.append(row)

        print(f"✓ Loaded {len(urls_data)} counties to scrape")
        return urls_data

    async def scrape_url(self, browser, url, geoid, source_name):
        """Scrape a single URL"""
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url, wait_until='networkidle', timeout=15000)
            await asyncio.sleep(2)

            # Extract data
            data = {
                'geoid': geoid,
                'url': url,
                'source': source_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }

            # Get page title
            data['page_title'] = await page.title()

            # Get page content
            data['page_content'] = await page.evaluate('() => document.body.innerText')

            # Try to extract metrics
            try:
                stats = await page.evaluate('''() => {
                    const stats = {};
                    const dataElements = document.querySelectorAll('[class*="metric"], [class*="stat"], [class*="value"]');
                    dataElements.forEach((el, idx) => {
                        stats[`metric_${idx}`] = el.innerText.trim();
                    });
                    return stats;
                }''')
                data['extracted_stats'] = stats
            except:
                data['extracted_stats'] = {}

            return data

        except Exception as e:
            return {
                'geoid': geoid,
                'url': url,
                'source': source_name,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }

        finally:
            await page.close()
            await context.close()

    async def scrape_county_urls(self, agent_id, county_data_list, pbar=None):
        """Scrape both URLs for each county"""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        results = []

        try:
            for county_data in county_data_list:
                geoid = county_data['geoid']
                url1 = county_data.get('url_energy_snapshot', '')
                url2 = county_data.get('url_data_viewer', '')

                # Scrape energy snapshot
                if url1:
                    result1 = await self.scrape_url(browser, url1, geoid, 'energy-snapshot')
                    await asyncio.sleep(0.5)
                else:
                    result1 = {'geoid': geoid, 'status': 'skipped', 'source': 'energy-snapshot'}

                # Scrape data viewer
                if url2:
                    result2 = await self.scrape_url(browser, url2, geoid, 'data-viewer')
                    await asyncio.sleep(0.5)
                else:
                    result2 = {'geoid': geoid, 'status': 'skipped', 'source': 'data-viewer'}

                # Merge both results
                merged_result = self.merge_results(geoid, result1, result2)
                results.append(merged_result)

                # Save immediately
                self.storage.save_raw_data(geoid, merged_result)

                if pbar:
                    pbar.update(1)

                await asyncio.sleep(0.5)

        except Exception as e:
            print(f"\n[Agent {agent_id}] Error: {e}")

        finally:
            await browser.close()
            await playwright.stop()

        return results

    def merge_results(self, geoid, result1, result2):
        """Merge data from both URLs"""
        merged = {
            'geoid': geoid,
            'timestamp': datetime.now().isoformat(),
            'status': 'success' if (result1.get('status') == 'success' or result2.get('status') == 'success') else 'error'
        }

        # Add energy snapshot data
        if result1.get('status') == 'success':
            merged['energy_snapshot_title'] = result1.get('page_title', '')
            merged['energy_snapshot_content'] = result1.get('page_content', '')
            merged['energy_snapshot_stats'] = result1.get('extracted_stats', {})

        # Add data viewer data
        if result2.get('status') == 'success':
            merged['data_viewer_title'] = result2.get('page_title', '')
            merged['data_viewer_content'] = result2.get('page_content', '')
            merged['data_viewer_stats'] = result2.get('extracted_stats', {})

        # Add source URLs
        merged['sources'] = {
            'energy_snapshot': result1.get('url', ''),
            'data_viewer': result2.get('url', '')
        }

        # Track errors
        if result1.get('status') == 'error':
            merged['energy_snapshot_error'] = result1.get('error', '')
        if result2.get('status') == 'error':
            merged['data_viewer_error'] = result2.get('error', '')

        return merged

    async def run(self):
        """Run URL-based scraping"""
        print(f"\n{'='*70}")
        print(f"URL-BASED SCRAPER (from urls.csv)")
        print(f"{'='*70}")

        # Load URLs
        urls_data = self.load_urls()
        total = len(urls_data)

        # Split work among agents
        chunk_size = total // self.num_agents
        agent_chunks = []

        for i in range(self.num_agents):
            start_idx = i * chunk_size
            if i == self.num_agents - 1:
                end_idx = total
            else:
                end_idx = start_idx + chunk_size

            agent_chunks.append(urls_data[start_idx:end_idx])

        print(f"\nScraping {total} counties with {self.num_agents} agents")
        print(f"{'='*70}\n")

        # Create tasks
        tasks = []
        pbar = tqdm(total=total, desc="Scraping", unit="county")

        for i, chunk in enumerate(agent_chunks, 1):
            task = self.scrape_county_urls(i, chunk, pbar)
            tasks.append(task)

        # Run all agents
        start_time = datetime.now()
        all_results = await asyncio.gather(*tasks)

        # Flatten results
        for agent_results in all_results:
            self.results.extend(agent_results)

        pbar.close()

        # Stats
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        successful = sum(1 for r in self.results if r.get('status') == 'success')

        print(f"\n{'='*70}")
        print(f"Scraped: {len(self.results)} counties in {duration:.1f}s")
        print(f"Successful: {successful} ({successful/len(self.results)*100:.1f}%)")
        print(f"{'='*70}\n")

        # Save
        self.storage.save_to_csv(self.results, "counties_data_merged.csv")
        self.storage.save_batch_data(self.results, "counties_data_merged.json")

        return self.results


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Scrape from urls.csv")
    parser.add_argument("--urls", default="urls.csv", help="Path to urls.csv")
    parser.add_argument("--agents", type=int, default=15, help="Number of agents")

    args = parser.parse_args()

    if not Path(args.urls).exists():
        print(f"❌ Error: {args.urls} not found")
        print("\nRun this first to generate it:")
        print("  python generate_urls.py")
        return 1

    scraper = URLBasedScraper(urls_csv=args.urls, num_agents=args.agents)
    await scraper.run()

    print("\n✓ Done! Data saved to:")
    print("  - data/processed/counties_data_merged.csv")
    print("  - data/processed/counties_data_merged.json")

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
