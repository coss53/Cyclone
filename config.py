import os

OUTPUT_DIR = r"H:\Kam vai"
SHAPEFILE_DIR = os.path.join(OUTPUT_DIR, "shapefiles")
BUFFER_DIR = os.path.join(OUTPUT_DIR, "buffers")
os.makedirs(SHAPEFILE_DIR, exist_ok=True)
os.makedirs(BUFFER_DIR, exist_ok=True)

BASE_URL = "https://www.nhc.noaa.gov/gis/"
BUFFER_DISTANCE_M = 50000  # 50 km
METADATA_JSON = os.path.join(OUTPUT_DIR, "nhc_storm_history.json")
