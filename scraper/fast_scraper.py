"""
FAST Multi-Agent Scraper for NREL SLOPE
Optimized for maximum speed with 15-20 parallel agents
Can scrape 3300+ counties efficiently
"""

import asyncio
import argparse
import sys
import signal
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.geoid_generator import GeoIDGenerator
from utils.data_storage import DataStorage
from scraper.scraper_agent import ScraperAgent


class FastScraper:
    """Ultra-fast multi-agent scraper optimized for performance"""

    def __init__(self, num_agents=15, start_geoid="G0100010", end_geoid="G5600450"):
        self.num_agents = num_agents
        self.start_geoid = start_geoid
        self.end_geoid = end_geoid
        self.generator = GeoIDGenerator(start_geoid, end_geoid)
        self.storage = DataStorage()
        self.results = []
        self.errors = []
        self.should_stop = False

        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n⚠️  Stopping scraper gracefully...")
        print("Saving collected data...")
        self.should_stop = True

    async def scrape_with_agent(self, agent_id, geoids, pbar=None):
        """Fast scraping with a single agent"""
        agent = ScraperAgent(agent_id=agent_id, headless=True, timeout=15000)
        results = []

        try:
            await agent.initialize()

            for geoid in geoids:
                if self.should_stop:
                    break

                result = await agent.scrape_county(geoid)
                results.append(result)

                # Track errors
                if result.get('status') == 'error':
                    self.errors.append(result)

                # Update progress bar
                if pbar:
                    pbar.update(1)

                # Save every 10 results to prevent data loss
                if len(results) % 10 == 0:
                    for r in results[-10:]:
                        self.storage.save_raw_data(r['geoid'], r)

                # Minimal delay for politeness
                await asyncio.sleep(0.5)

        except Exception as e:
            print(f"\n[Agent {agent_id}] Fatal error: {str(e)}")

        finally:
            await agent.cleanup()

        return results

    async def run(self):
        """Run ultra-fast scraping operation"""
        print(f"\n{'='*70}")
        print(f"NREL SLOPE FAST SCRAPER")
        print(f"{'='*70}")
        print(f"GeoID Range: {self.start_geoid} to {self.end_geoid}")
        print(f"Parallel Agents: {self.num_agents}")
        print(f"Mode: MAXIMUM SPEED")

        # Split work among agents
        agent_ranges = self.generator.split_for_agents(self.num_agents)

        print(f"\nAgent Work Distribution:")
        total_geoids = 0
        for i, (start, end) in enumerate(agent_ranges, 1):
            gen = GeoIDGenerator(start, end)
            count = gen.count_total()
            total_geoids += count
            print(f"  Agent {i:2d}: {start} to {end} ({count:3d} counties)")

        print(f"\nTotal Counties to Scrape: {total_geoids}")
        print(f"Estimated Time: {total_geoids / (self.num_agents * 2):.0f}-{total_geoids / (self.num_agents * 1.5):.0f} seconds")
        print(f"{'='*70}\n")

        # Prepare agent tasks
        tasks = []
        pbar = tqdm(total=total_geoids, desc="Scraping", unit="county",
                   bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')

        for i, (start, end) in enumerate(agent_ranges, 1):
            gen = GeoIDGenerator(start, end)
            geoids = list(gen.generate_range())
            task = self.scrape_with_agent(i, geoids, pbar)
            tasks.append(task)

        # Run all agents in parallel
        start_time = datetime.now()
        print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        all_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results
        for agent_results in all_results:
            if isinstance(agent_results, Exception):
                print(f"\n⚠️  Agent exception: {agent_results}")
            else:
                self.results.extend(agent_results)

        pbar.close()

        # Calculate statistics
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        stats = {
            "total_scraped": len(self.results),
            "successful": sum(1 for r in self.results if r.get('status') == 'success'),
            "errors": len(self.errors),
            "duration_seconds": duration,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "counties_per_second": len(self.results) / duration if duration > 0 else 0
        }

        # Save results
        self.save_results(stats)

        return stats

    def save_results(self, stats):
        """Save scraping results"""
        print(f"\n{'='*70}")
        print("Saving Results...")
        print(f"{'='*70}")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save all results to JSON
        results_file = self.storage.save_batch_data(
            self.results,
            filename=f"fast_scrape_results_{timestamp}.json"
        )
        print(f"✓ Results: {results_file}")

        # Save to CSV
        csv_file = self.storage.save_to_csv(
            self.results,
            filename=f"counties_data_{timestamp}.csv"
        )
        print(f"✓ CSV: {csv_file}")

        # Save errors separately
        if self.errors:
            error_file = self.storage.save_batch_data(
                self.errors,
                filename=f"scrape_errors_{timestamp}.json"
            )
            print(f"✓ Errors: {error_file}")

        # Print statistics
        print(f"\n{'='*70}")
        print("SCRAPING STATISTICS")
        print(f"{'='*70}")
        print(f"Total Scraped:     {stats['total_scraped']}")
        print(f"Successful:        {stats['successful']} ({stats['successful']/stats['total_scraped']*100:.1f}%)")
        print(f"Errors:            {stats['errors']} ({stats['errors']/stats['total_scraped']*100:.1f}%)")
        print(f"Duration:          {stats['duration_seconds']:.1f} seconds ({stats['duration_seconds']/60:.1f} minutes)")
        print(f"Speed:             {stats['counties_per_second']:.2f} counties/second")
        print(f"{'='*70}\n")


async def main():
    """Main entry point for fast scraper"""
    parser = argparse.ArgumentParser(
        description="FAST NREL SLOPE Multi-Agent Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Maximum speed (15 agents, ~3-5 minutes)
  python scraper/fast_scraper.py --agents 15

  # Ultra speed (20 agents, ~2-3 minutes)
  python scraper/fast_scraper.py --agents 20

  # Custom range
  python scraper/fast_scraper.py --start G0100010 --end G0200010 --agents 10
        """
    )

    parser.add_argument(
        "--start",
        default="G0100010",
        help="Starting GeoID (default: G0100010)"
    )
    parser.add_argument(
        "--end",
        default="G5600450",
        help="Ending GeoID (default: G5600450)"
    )
    parser.add_argument(
        "--agents",
        type=int,
        default=15,
        help="Number of parallel agents (default: 15, recommended: 10-20)"
    )

    args = parser.parse_args()

    # Validate agent count
    if args.agents > 25:
        print("⚠️  Warning: More than 25 agents may cause rate limiting")
        print("Recommended: 10-20 agents for optimal speed")

    if args.agents < 5:
        print("⚠️  Warning: Less than 5 agents will be slow")

    scraper = FastScraper(
        num_agents=args.agents,
        start_geoid=args.start,
        end_geoid=args.end
    )

    try:
        stats = await scraper.run()

        if stats['successful'] > 0:
            print("\n✓ Scraping completed successfully!")
            print(f"\nCollected data for {stats['successful']} counties")
            return 0
        else:
            print("\n⚠️  No successful scrapes")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        print(f"Saved {len(scraper.results)} results before stopping")
        return 1

    except Exception as e:
        print(f"\n\n✗ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
