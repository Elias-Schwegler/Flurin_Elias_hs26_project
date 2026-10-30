"""Download the archived forecasts used by open_meteo_eda.ipynb into data/ (about 5 MB).

Run once from this folder: python download_data.py
Source: Open-Meteo Previous Runs API, https://open-meteo.com/en/docs/previous-runs-api, CC BY 4.0
"""
import time
from pathlib import Path

import requests

URL = "https://previous-runs-api.open-meteo.com/v1/forecast"
START, END = "2024-01-01", "2025-12-31"
LOCATIONS = {"LUZ": (47.036439, 8.301022), "EGO": (47.179428, 8.004758),      # coordinates of the
             "MOA": (47.243847, 8.232831), "SPF": (46.947042, 8.012442)}      # MeteoSwiss stations
VARIABLES = ["shortwave_radiation", "direct_radiation", "diffuse_radiation", "temperature_2m", "cloud_cover"]
DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

for location, (latitude, longitude) in LOCATIONS.items():
    target = DATA / f"previous_day1_{location}_{START}_{END}.json"
    if not target.exists():
        params = {"latitude": latitude, "longitude": longitude,
                  "hourly": ",".join(f"{v}_previous_day1" for v in VARIABLES),
                  "models": "icon_d2,meteoswiss_icon_ch2",
                  "start_date": START, "end_date": END, "timezone": "GMT"}
        response = requests.get(URL, params=params, timeout=300)
        response.raise_for_status()
        target.write_bytes(response.content)
        print("downloaded", target.name)
        time.sleep(2)
