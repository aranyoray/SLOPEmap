"""
Prepare scraped data for Vercel deployment
Converts CSV data to JSON format optimized for dashboard
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def prepare_data_for_vercel():
    """Prepare scraped data for Vercel deployment"""

    print("="*60)
    print("Preparing Data for Vercel Deployment")
    print("="*60)
    print()

    # Find most recent counties data CSV
    processed_dir = Path("data/processed")

    if not processed_dir.exists():
        print("❌ Error: data/processed directory not found")
        print("Please run the scraper first!")
        return False

    csv_files = sorted(processed_dir.glob("counties_data_*.csv"), reverse=True)

    if not csv_files:
        # Try alternate name
        csv_files = sorted(processed_dir.glob("processed_counties_*.csv"), reverse=True)

    if not csv_files:
        print("❌ Error: No county data CSV files found")
        print("Please run: python scraper/agent_scraper.py")
        return False

    data_file = csv_files[0]
    print(f"✓ Found data file: {data_file}")

    # Load data
    try:
        df = pd.read_csv(data_file)
        print(f"✓ Loaded {len(df)} records")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return False

    # Filter for successful scrapes only
    if 'scrape_status' in df.columns:
        successful_df = df[df['scrape_status'] == 'success']
        print(f"✓ {len(successful_df)} successful scrapes")

        if len(successful_df) == 0:
            print("⚠️ Warning: No successful scrapes found")
            print("Using all data including errors")
            successful_df = df
    else:
        successful_df = df

    # Convert to JSON format
    data_dict = successful_df.to_dict('records')

    # Create dashboard data directory
    dashboard_dir = Path("dashboard/data")
    dashboard_dir.mkdir(exist_ok=True)

    # Save JSON file for dashboard
    output_file = dashboard_dir / "dashboard_data.json"
    with open(output_file, 'w') as f:
        json.dump(data_dict, f, indent=2)

    print(f"✓ Created: {output_file}")
    print(f"  Size: {output_file.stat().st_size / 1024:.2f} KB")

    # Also copy to root for backup
    backup_file = Path("dashboard_data.json")
    with open(backup_file, 'w') as f:
        json.dump(data_dict, f, indent=2)
    print(f"✓ Backup created: {backup_file}")

    # Generate statistics
    print()
    print("="*60)
    print("Data Summary")
    print("="*60)
    print(f"Total records: {len(data_dict)}")

    if 'state_fips' in df.columns:
        print(f"Unique states: {df['state_fips'].nunique()}")

    if 'scrape_status' in df.columns:
        status_counts = df['scrape_status'].value_counts()
        print("\nStatus breakdown:")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")

    print()
    print("="*60)
    print("✓ Data preparation complete!")
    print("="*60)
    print()
    print("Next steps:")
    print("  1. Test locally: python dashboard/vercel_app.py")
    print("  2. Deploy to Vercel: vercel deploy")
    print()

    return True

if __name__ == "__main__":
    success = prepare_data_for_vercel()
    exit(0 if success else 1)
