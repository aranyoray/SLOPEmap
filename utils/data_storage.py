"""
Data Storage Utility
Handles saving and loading of scraped county data
"""

import json
import csv
import os
from datetime import datetime
from pathlib import Path
import pandas as pd


class DataStorage:
    """Manage storage of scraped county energy data"""

    def __init__(self, base_dir="data"):
        """
        Initialize data storage

        Args:
            base_dir (str): Base directory for data storage
        """
        self.base_dir = Path(base_dir)
        self.raw_dir = self.base_dir / "raw"
        self.processed_dir = self.base_dir / "processed"

        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def save_raw_data(self, geoid, data, format="json"):
        """
        Save raw scraped data for a county

        Args:
            geoid (str): County GeoID
            data (dict): Scraped data
            format (str): Storage format ('json' or 'csv')
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "json":
            filepath = self.raw_dir / f"{geoid}_{timestamp}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif format == "csv":
            filepath = self.raw_dir / f"{geoid}_{timestamp}.csv"
            df = pd.DataFrame([data])
            df.to_csv(filepath, index=False)

        return filepath

    def save_batch_data(self, batch_data, filename="batch_data.json"):
        """
        Save batch of county data

        Args:
            batch_data (list): List of county data dictionaries
            filename (str): Output filename
        """
        filepath = self.processed_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)

        return filepath

    def save_to_csv(self, data, filename="counties_data.csv"):
        """
        Save data to CSV file

        Args:
            data (list or pd.DataFrame): County data
            filename (str): Output filename

        Returns:
            Path: Path to saved file
        """
        filepath = self.processed_dir / filename

        if isinstance(data, pd.DataFrame):
            data.to_csv(filepath, index=False)
        else:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)

        return filepath

    def load_raw_data(self, geoid):
        """
        Load most recent raw data for a GeoID

        Args:
            geoid (str): County GeoID

        Returns:
            dict: Loaded data or None if not found
        """
        # Find most recent file for this GeoID
        pattern = f"{geoid}_*.json"
        files = sorted(self.raw_dir.glob(pattern), reverse=True)

        if not files:
            return None

        with open(files[0], 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_all_data(self):
        """
        Load all processed county data

        Returns:
            list: List of all county data dictionaries
        """
        all_data = []

        # Load from JSON files
        for json_file in self.processed_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)

        return all_data

    def load_csv_data(self, filename="counties_data.csv"):
        """
        Load data from CSV file

        Args:
            filename (str): CSV filename

        Returns:
            pd.DataFrame: Loaded data
        """
        filepath = self.processed_dir / filename
        if filepath.exists():
            return pd.read_csv(filepath)
        return pd.DataFrame()

    def merge_and_deduplicate(self):
        """
        Merge all raw data and remove duplicates

        Returns:
            pd.DataFrame: Merged and deduplicated data
        """
        all_data = []

        for json_file in self.raw_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    all_data.append(data)
                except json.JSONDecodeError:
                    print(f"Error reading {json_file}")
                    continue

        if not all_data:
            return pd.DataFrame()

        df = pd.DataFrame(all_data)

        # Remove duplicates based on GeoID, keeping most recent
        if 'geoid' in df.columns:
            df = df.sort_values('timestamp', ascending=False).drop_duplicates('geoid', keep='first')

        return df

    def get_scraping_progress(self):
        """
        Get scraping progress statistics

        Returns:
            dict: Progress statistics
        """
        raw_files = list(self.raw_dir.glob("*.json"))
        unique_geoids = set()

        for filepath in raw_files:
            geoid = filepath.stem.split('_')[0]
            unique_geoids.add(geoid)

        return {
            "total_files": len(raw_files),
            "unique_counties": len(unique_geoids),
            "geoids_scraped": sorted(unique_geoids)
        }


if __name__ == "__main__":
    # Example usage
    storage = DataStorage()

    # Save sample data
    sample_data = {
        "geoid": "G0100010",
        "county_name": "Sample County",
        "state": "Alabama",
        "energy_data": {
            "solar_potential": 1500,
            "wind_potential": 800
        },
        "timestamp": datetime.now().isoformat()
    }

    filepath = storage.save_raw_data("G0100010", sample_data)
    print(f"Saved to: {filepath}")

    # Get progress
    progress = storage.get_scraping_progress()
    print(f"\nScraping progress: {progress}")
