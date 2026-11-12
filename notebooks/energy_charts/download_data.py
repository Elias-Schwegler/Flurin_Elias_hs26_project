"""Download the Energy-Charts raw files used by energy_charts_eda.ipynb into data/ (about 8 MB).

Run once from this folder: python download_data.py
Source: Energy-Charts (Fraunhofer ISE), https://api.energy-charts.info, CC BY 4.0
"""
import time
from pathlib import Path

import requests

URL = "https://api.energy-charts.info/public_power"
DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

for year in range(2015, 2027):
    target = DATA / f"public_power_ch_{year}.json"
    if not target.exists():
        params = {"country": "ch", "start": f"{year}-01-01T00:00Z", "end": f"{year + 1}-01-01T00:00Z"}
        response = requests.get(URL, params=params, timeout=180)
        while response.status_code == 429:  # rate limit: wait as long as the server asks
            time.sleep(int(response.headers.get("retry-after", 10)) + 2)
            response = requests.get(URL, params=params, timeout=180)
        response.raise_for_status()
        target.write_bytes(response.content)
        print("downloaded", target.name)
        time.sleep(8)
