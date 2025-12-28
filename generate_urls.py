"""
Generate urls.csv with all county URLs for scraping
Creates two columns: energy-snapshot URL and data-viewer URL
"""

import csv
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))
from utils.geoid_generator import GeoIDGenerator


def generate_urls_csv(output_file="urls.csv", start_geoid="G0100010", end_geoid="G5600450"):
    """Generate CSV with URLs for all counties"""

    print("Generating URLs CSV...")
    generator = GeoIDGenerator(start_geoid, end_geoid)

    rows = []
    for geoid in generator.generate_range():
        row = {
            'geoid': geoid,
            'url_energy_snapshot': f'https://maps.nrel.gov/slope/energy-snapshot?geoId={geoid}',
            'url_data_viewer': f'https://maps.nrel.gov/slope/data-viewer?geoId={geoid}'
        }
        rows.append(row)

    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['geoid', 'url_energy_snapshot', 'url_data_viewer'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Created {output_file} with {len(rows)} counties")
    print(f"  Columns: geoid, url_energy_snapshot, url_data_viewer")

    return output_file


if __name__ == "__main__":
    generate_urls_csv()
