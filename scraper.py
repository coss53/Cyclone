from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from datetime import datetime
from config import BASE_URL

def scrape_active_storms():
    """Scrape NHC GIS page for active storms and shapefile URLs, skip KMZ entries"""
    try:
        r = requests.get(BASE_URL, timeout=30)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table")
        if not table:
            print("⚠️ No table found.")
            return []

        rows = table.find_all("tr")
        if len(rows) < 3:
            print("⚠️ Not enough rows in table.")
            return []

        basins = ["Atlantic", "Eastern Pacific", "Central Pacific"]
        storm_row = rows[2].find_all("td")
        active_storms = []

        for i, basin in enumerate(basins, start=1):
            if i >= len(storm_row):
                continue
            cell = storm_row[i]
            content = cell.decode_contents()
            parts = content.split("<br/>")
            for part in parts:
                part_soup = BeautifulSoup(part, "html.parser")
                text = part_soup.get_text(" ", strip=True)

                if not text or "No current" in text or "Sample" in text:
                    continue

                # cyclone name = before colon
                storm_name = text.split(":")[0].strip() if ":" in text else "UnknownStorm"

                # Skip KMZ entries
                if storm_name.upper() == "KMZ":
                    continue

                # find shapefile link
                link = part_soup.find("a", string=lambda s: s and "shp" in s.lower())
                url = None
                if link:
                    href = link.get("href", "")
                    url = href if href.startswith("http") else urljoin(BASE_URL, href)

                storm_data = {
                    "StormName": storm_name,
                    "Region": basin,
                    "ShapefileURL": url,
                    "Status": "Running",
                    "StartDate": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "EndDate": None
                }
                active_storms.append(storm_data)
        return active_storms

    except Exception as e:
        print(f"❌ Error scraping storms: {e}")
        return []
