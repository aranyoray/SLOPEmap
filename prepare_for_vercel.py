"""
Prepare data for Vercel deployment
Converts processed CSV data to JSON format for the dashboard
"""

import json
import pandas as pd
from pathlib import Path
import sys

def prepare_dashboard_data():
    """Prepare dashboard data for Vercel deployment"""
    
    # Find the most recent processed CSV file
    processed_dir = Path("data/processed")
    csv_files = sorted(processed_dir.glob("counties_data_*.csv"), reverse=True)
    
    if not csv_files:
        # Try alternative pattern
        csv_files = sorted(processed_dir.glob("processed_counties_*.csv"), reverse=True)
    
    if not csv_files:
        print("Error: No processed CSV files found in data/processed/")
        print("Please run the scraper first: ./run_full_scrape.sh")
        sys.exit(1)
    
    latest_csv = csv_files[0]
    print(f"Loading data from: {latest_csv}")
    
    # Load CSV data
    df = pd.read_csv(latest_csv)
    
    # Convert DataFrame to JSON-serializable format
    # Handle NaN values and complex types
    data_dict = df.to_dict(orient='records')
    
    # Clean up the data for JSON serialization
    cleaned_data = []
    for record in data_dict:
        cleaned_record = {}
        for key, value in record.items():
            # Convert NaN to None
            if pd.isna(value):
                cleaned_record[key] = None
            # Convert numpy types to Python native types
            elif hasattr(value, 'item'):
                cleaned_record[key] = value.item()
            else:
                cleaned_record[key] = value
        cleaned_data.append(cleaned_record)
    
    # Create output directory if it doesn't exist
    output_dir = Path("dashboard/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as JSON
    output_file = output_dir / "dashboard_data.json"
    with open(output_file, 'w') as f:
        json.dump(cleaned_data, f, indent=2, default=str)
    
    print(f"✓ Dashboard data saved to: {output_file}")
    print(f"✓ Total records: {len(cleaned_data)}")
    
    # Print summary statistics
    if cleaned_data:
        success_count = sum(1 for r in cleaned_data if r.get('scrape_status') == 'success')
        error_count = sum(1 for r in cleaned_data if r.get('scrape_status') == 'error')
        
        print(f"\nSummary:")
        print(f"  - Total counties: {len(cleaned_data)}")
        print(f"  - Successful scrapes: {success_count}")
        print(f"  - Failed scrapes: {error_count}")
    
    return output_file


if __name__ == "__main__":
    print("="*60)
    print("Preparing data for Vercel deployment")
    print("="*60)
    print()
    
    prepare_dashboard_data()
    
    print()
    print("="*60)
    print("Preparation complete!")
    print("="*60)
    print()
    print("Next steps:")
    print("  1. Commit the data: git add dashboard/data/dashboard_data.json")
    print("  2. Push to GitHub: git push origin main")
    print("  3. Deploy to Vercel: vercel deploy --prod")
    print("="*60)

