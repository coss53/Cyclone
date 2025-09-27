import os
import zipfile
import tempfile
import geopandas as gpd
from downloader import download_file
from config import BUFFER_DIR, BUFFER_DISTANCE_M

def buffer_first_point(zip_path, buffer_dir, storm_name, basin_name, buffer_distance_m=BUFFER_DISTANCE_M):
    """Extract *_pts.shp from ZIP, buffer first point, save to buffer_dir"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(zip_path) as z:
                z.extractall(tmpdir)
            # find point shapefile
            shp_files = [f for f in os.listdir(tmpdir) if f.endswith("_pts.shp")]
            if not shp_files:
                print(f"❌ No Point shapefile in {zip_path}")
                return None
            shp_path = os.path.join(tmpdir, shp_files[0])
            gdf = gpd.read_file(shp_path)
            if gdf.empty:
                print(f"❌ Empty Point shapefile in {zip_path}")
                return None
            first_point = gdf.iloc[0:1].copy()
            if first_point.crs is None:
                first_point.set_crs("EPSG:4326", inplace=True)

            # buffer
            first_point = first_point.to_crs(epsg=3857)
            first_point["geometry"] = first_point.geometry.buffer(buffer_distance_m)
            first_point = first_point.to_crs(epsg=4326)
            first_point["StormName"] = storm_name
            first_point["Region"] = basin_name

            out_path = os.path.join(buffer_dir, f"{basin_name}_{storm_name}_buffer.shp")
            first_point.to_file(out_path, driver="ESRI Shapefile")
            print(f"🌍 Saved buffer shapefile: {out_path}")
            return out_path
    except Exception as e:
        print(f"❌ Error buffering {storm_name}: {e}")
        return None

def process_storm(storm, shapefile_dir, buffer_dir=BUFFER_DIR):
    """Download ZIP and buffer first point"""
    if not storm.get("ShapefileURL"):
        print(f"⚠️ No Shapefile URL for {storm['StormName']}")
        return None

    storm_name_clean = storm["StormName"].replace(" ", "_")
    basin_clean = storm["Region"].replace(" ", "_")
    zip_filename = f"{basin_clean}_{storm_name_clean}.zip"
    zip_path = os.path.join(shapefile_dir, zip_filename)

    # download
    downloaded = download_file(storm["ShapefileURL"], zip_path)
    if not downloaded:
        return None

    # buffer first point
    buffer_path = buffer_first_point(downloaded, buffer_dir, storm_name_clean, basin_clean)
    if buffer_path:
        storm["BufferShapefile"] = buffer_path
    return storm
