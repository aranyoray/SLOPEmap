"""
Data Parser
Parse and clean scraped NREL SLOPE county data
"""

import re
import json
from datetime import datetime
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.data_storage import DataStorage


class DataParser:
    """Parse and structure scraped county data"""

    def __init__(self):
        self.storage = DataStorage()

    def parse_geoid(self, geoid):
        """
        Parse GeoID to extract state and county FIPS codes

        Args:
            geoid (str): GeoID string (e.g., 'G0100010')

        Returns:
            dict: Parsed components
        """
        # GeoID format: G + State FIPS (2) + County FIPS (5)
        # Example: G0100010 = State 01 (Alabama), County 00010

        if not geoid.startswith('G') or len(geoid) != 8:
            return {"state_fips": None, "county_fips": None, "valid": False}

        numeric = geoid[1:]  # Remove 'G'
        state_fips = numeric[:2]
        county_fips = numeric[2:]

        return {
            "state_fips": state_fips,
            "county_fips": county_fips,
            "full_fips": numeric,
            "valid": True
        }

    def extract_metrics(self, raw_data):
        """
        Extract energy metrics from raw scraped data

        Args:
            raw_data (dict): Raw scraped data

        Returns:
            dict: Extracted metrics
        """
        metrics = {}

        # Extract from page content if available
        if 'page_content' in raw_data:
            content = raw_data['page_content']

            # Look for common energy metrics patterns
            patterns = {
                'population': r'Population[:\s]+([0-9,]+)',
                'households': r'Households[:\s]+([0-9,]+)',
                'solar_potential': r'Solar[^:]*[:\s]+([0-9,.]+)\s*(MW|GW|kW)',
                'wind_potential': r'Wind[^:]*[:\s]+([0-9,.]+)\s*(MW|GW|kW)',
                'energy_burden': r'Energy\s+Burden[:\s]+([0-9.]+)%?',
                'renewable_percent': r'Renewable[^:]*[:\s]+([0-9.]+)%?',
            }

            for metric_name, pattern in patterns.items():
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    value = match.group(1).replace(',', '')
                    try:
                        metrics[metric_name] = float(value)
                    except:
                        metrics[metric_name] = value

        # Extract from structured stats
        if 'extracted_stats' in raw_data:
            for key, value in raw_data['extracted_stats'].items():
                if value and value.strip():
                    metrics[f'stat_{key}'] = value.strip()

        return metrics

    def parse_raw_data(self, raw_data):
        """
        Parse raw scraped data into structured format

        Args:
            raw_data (dict): Raw data from scraper

        Returns:
            dict: Structured county data
        """
        parsed = {
            "geoid": raw_data.get('geoid'),
            "timestamp": raw_data.get('timestamp'),
            "scrape_status": raw_data.get('status'),
        }

        # Parse GeoID
        geoid_info = self.parse_geoid(raw_data.get('geoid', ''))
        parsed.update(geoid_info)

        # Extract title/name
        if 'page_title' in raw_data:
            parsed['page_title'] = raw_data['page_title']

        # Extract metrics
        metrics = self.extract_metrics(raw_data)
        parsed['metrics'] = metrics

        # Add raw content reference
        if 'page_content' in raw_data:
            # Store first 500 chars as preview
            parsed['content_preview'] = raw_data['page_content'][:500]

        # Error information
        if raw_data.get('status') == 'error':
            parsed['error'] = raw_data.get('error')

        return parsed

    def process_batch(self, raw_data_list):
        """
        Process batch of raw data

        Args:
            raw_data_list (list): List of raw data dictionaries

        Returns:
            pd.DataFrame: Processed data
        """
        parsed_records = []

        for raw_data in raw_data_list:
            parsed = self.parse_raw_data(raw_data)
            parsed_records.append(parsed)

        df = pd.DataFrame(parsed_records)
        return df

    def load_and_process_all(self):
        """
        Load all raw data and process it

        Returns:
            pd.DataFrame: Processed data
        """
        print("Loading raw data...")
        raw_data = self.storage.load_all_data()

        if not raw_data:
            print("No raw data found")
            return pd.DataFrame()

        print(f"Processing {len(raw_data)} records...")
        df = self.process_batch(raw_data)

        # Save processed data
        output_file = self.storage.save_to_csv(
            df,
            filename=f"processed_counties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        print(f"Saved processed data to: {output_file}")

        return df

    def generate_summary(self, df):
        """
        Generate summary statistics

        Args:
            df (pd.DataFrame): Processed data

        Returns:
            dict: Summary statistics
        """
        summary = {
            "total_records": len(df),
            "successful_scrapes": len(df[df['scrape_status'] == 'success']),
            "failed_scrapes": len(df[df['scrape_status'] == 'error']),
            "unique_states": df['state_fips'].nunique() if 'state_fips' in df else 0,
            "date_processed": datetime.now().isoformat()
        }

        return summary


def main():
    """Main entry point for data parsing"""
    parser = DataParser()

    print("\n" + "="*60)
    print("NREL SLOPE Data Parser")
    print("="*60 + "\n")

    df = parser.load_and_process_all()

    if not df.empty:
        summary = parser.generate_summary(df)

        print("\n" + "="*60)
        print("Processing Summary")
        print("="*60)
        for key, value in summary.items():
            print(f"{key}: {value}")
        print("="*60 + "\n")

        # Show sample data
        print("\nSample Data (first 5 records):")
        print(df.head().to_string())
    else:
        print("No data to process")


if __name__ == "__main__":
    main()
