"""
Multi-Agent Scraper Orchestrator
Coordinates multiple scraper agents to scrape NREL SLOPE county data in parallel
"""

import asyncio
import argparse
import sys
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.geoid_generator import GeoIDGenerator
from utils.data_storage import DataStorage
from scraper.scraper_agent import ScraperAgent


class AgentOrchestrator:
    """Orchestrate multiple scraper agents"""

    def __init__(self, num_agents=5, start_geoid="G0100010", end_geoid="G5600450", headless=True):
        """
        Initialize agent orchestrator

        Args:
            num_agents (int): Number of parallel agents to use
            start_geoid (str): Starting GeoID
            end_geoid (str): Ending GeoID
            headless (bool): Run browsers in headless mode
        """
        self.num_agents = num_agents
        self.start_geoid = start_geoid
        self.end_geoid = end_geoid
        self.headless = headless

        self.generator = GeoIDGenerator(start_geoid, end_geoid)
        self.storage = DataStorage()

        self.results = []
        self.errors = []

    async def scrape_with_agent(self, agent_id, geoids, pbar=None):
        """
        Run scraping task for a single agent

        Args:
            agent_id (int): Agent identifier
            geoids (list): List of GeoIDs for this agent
            pbar (tqdm): Progress bar

        Returns:
            list: Scraped results
        """
        agent = ScraperAgent(agent_id=agent_id, headless=self.headless)
        results = []

        try:
            await agent.initialize()

            for geoid in geoids:
                result = await agent.scrape_county(geoid)
                results.append(result)

                # Track errors
                if result.get('status') == 'error':
                    self.errors.append(result)

                # Update progress bar
                if pbar:
                    pbar.update(1)

                # Small delay between requests
                await asyncio.sleep(1)

        except Exception as e:
            print(f"\n[Agent {agent_id}] Fatal error: {str(e)}")

        finally:
            await agent.cleanup()

        return results

    async def run(self):
        """
        Run multi-agent scraping operation

        Returns:
            dict: Scraping results and statistics
        """
        print(f"\n{'='*60}")
        print(f"NREL SLOPE Multi-Agent Scraper")
        print(f"{'='*60}")
        print(f"GeoID Range: {self.start_geoid} to {self.end_geoid}")
        print(f"Number of Agents: {self.num_agents}")

        # Split work among agents
        agent_ranges = self.generator.split_for_agents(self.num_agents)

        print(f"\nAgent Work Distribution:")
        total_geoids = 0
        for i, (start, end) in enumerate(agent_ranges, 1):
            # Calculate geoids for this range
            gen = GeoIDGenerator(start, end)
            count = gen.count_total()
            total_geoids += count
            print(f"  Agent {i}: {start} to {end} ({count} counties)")

        print(f"\nTotal GeoIDs to scrape: {total_geoids}")
        print(f"{'='*60}\n")

        # Prepare agent tasks
        tasks = []
        pbar = tqdm(total=total_geoids, desc="Scraping progress", unit="county")

        for i, (start, end) in enumerate(agent_ranges, 1):
            gen = GeoIDGenerator(start, end)
            geoids = list(gen.generate_range())
            task = self.scrape_with_agent(i, geoids, pbar)
            tasks.append(task)

        # Run all agents in parallel
        start_time = datetime.now()
        print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        all_results = await asyncio.gather(*tasks)

        # Flatten results
        for agent_results in all_results:
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
            "geoids_per_second": len(self.results) / duration if duration > 0 else 0
        }

        # Save results
        self.save_results(stats)

        return stats

    def save_results(self, stats):
        """
        Save scraping results and statistics

        Args:
            stats (dict): Scraping statistics
        """
        print(f"\n{'='*60}")
        print("Saving Results...")
        print(f"{'='*60}")

        # Save all results to JSON
        results_file = self.storage.save_batch_data(
            self.results,
            filename=f"scrape_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        print(f"✓ Results saved to: {results_file}")

        # Save to CSV
        csv_file = self.storage.save_to_csv(
            self.results,
            filename=f"counties_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        print(f"✓ CSV saved to: {csv_file}")

        # Save errors separately
        if self.errors:
            error_file = self.storage.save_batch_data(
                self.errors,
                filename=f"scrape_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            print(f"✓ Errors saved to: {error_file}")

        # Print statistics
        print(f"\n{'='*60}")
        print("Scraping Statistics")
        print(f"{'='*60}")
        print(f"Total Scraped: {stats['total_scraped']}")
        print(f"Successful: {stats['successful']}")
        print(f"Errors: {stats['errors']}")
        print(f"Duration: {stats['duration_seconds']:.2f} seconds")
        print(f"Speed: {stats['geoids_per_second']:.2f} counties/second")
        print(f"{'='*60}\n")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="NREL SLOPE Multi-Agent Scraper")
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
        default=5,
        help="Number of parallel agents (default: 5)"
    )
    parser.add_argument(
        "--visible",
        action="store_true",
        help="Run browsers in visible mode (default: headless)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode with limited range"
    )

    args = parser.parse_args()

    # Test mode uses smaller range
    if args.test:
        start_geoid = "G0100010"
        end_geoid = "G0100050"
        print("\n⚠️  Running in TEST mode with limited range")
    else:
        start_geoid = args.start
        end_geoid = args.end

    orchestrator = AgentOrchestrator(
        num_agents=args.agents,
        start_geoid=start_geoid,
        end_geoid=end_geoid,
        headless=not args.visible
    )

    try:
        stats = await orchestrator.run()
        print("\n✓ Scraping completed successfully!")
        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        return 1

    except Exception as e:
        print(f"\n\n✗ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
