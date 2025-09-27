# NHC Active Cyclone Scraper & Buffer Generator

This Python project automatically scrapes active tropical cyclones from the [NHC GIS page](https://www.nhc.noaa.gov/gis/), downloads their shapefiles, creates 50 km buffers for point data, and maintains a metadata JSON for tracking processed storms.

---

## Features

- Scrape **active storms** from Atlantic, Eastern Pacific, and Central Pacific basins.
- Skip non-relevant entries like `KMZ`.
- Download associated **shapefiles** dynamically.
- Extract **point geometry** from shapefiles and create a **50 km buffer**.
- Store processed storms in a **metadata JSON** (`nhc_storm_history.json`) with:
  - Storm name
  - Basin/Region
  - Download URL
  - Status (`Running` or ended)
  - Start and End date
- Automatically **skip already downloaded URLs** to avoid duplicates.
- Save buffered shapefiles in `buffers/` folder.

---

## Folder Structure

