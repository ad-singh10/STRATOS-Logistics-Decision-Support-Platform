

import os
import time
import requests

# =========================================================
# Configuration
# =========================================================

DATASET_URL = (
    "https://raw.githubusercontent.com/dr5hn/"
    "countries-states-cities-database/master/csv/cities.csv"
)

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SAVE_DIRECTORY = PROJECT_ROOT / "data" / "external" / "cities"
SAVE_FILENAME = "cities_raw.csv"

# =========================================================
# Helper Functions
# =========================================================

def create_directory(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def download_file(url):
    """Download file from URL."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.content


def save_file(content, folder, filename):
    """Save downloaded content."""
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as file:
        file.write(content)

    return file_path


# =========================================================
# Main Function
# =========================================================

def main():

    start_time = time.time()

    print("=" * 60)
    print("STRATOS DATA PIPELINE")
    print("Module : Download Cities Dataset")
    print("=" * 60)

    try:

        print("\nCreating directory...")
        create_directory(SAVE_DIRECTORY)

        print("Downloading dataset...")
        data = download_file(DATASET_URL)

        print("Saving dataset...")
        saved_path = save_file(data, SAVE_DIRECTORY, SAVE_FILENAME)

        elapsed = round(time.time() - start_time, 2)

        print("\nDownload Completed Successfully")
        print("-" * 60)
        print(f"Location      : {saved_path}")
        print(f"File Size     : {round(len(data) / (1024 * 1024), 2)} MB")
        print(f"Execution Time: {elapsed} seconds")
        print("=" * 60)

    except Exception as error:

        print("\nDownload Failed")
        print("-" * 60)
        print(error)
        print("=" * 60)


# =========================================================

if __name__ == "__main__":
    main()