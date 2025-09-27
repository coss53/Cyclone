import json
import os
from config import SHAPEFILE_DIR, BUFFER_DIR, METADATA_JSON
from scraper import scrape_active_storms
from processor import process_storm

def load_existing_metadata(file_path):
    if os.path.exists(file_path):
        with open(file_path) as f:
            return json.load(f)
    return []

def is_url_processed(url, existing_metadata):
    for storm in existing_metadata:
        if storm.get("ShapefileURL") == url:
            return True
    return False

if __name__ == "__main__":
    # load previous metadata
    existing_meta = load_existing_metadata(METADATA_JSON)

    # scrape new storms
    active_storms = scrape_active_storms()
    processed_storms = existing_meta.copy()

    for storm in active_storms:
        url = storm.get("ShapefileURL")
        if url and is_url_processed(url, existing_meta):
            print(f"ℹ️ Already processed: {storm['StormName']} ({url})")
            continue
        result = process_storm(storm, SHAPEFILE_DIR, BUFFER_DIR)
        if result:
            processed_storms.append(result)

    # save metadata
    with open(METADATA_JSON, "w") as f:
        json.dump(processed_storms, f, indent=4)
    print(f"\n✅ Metadata saved to {METADATA_JSON}")
