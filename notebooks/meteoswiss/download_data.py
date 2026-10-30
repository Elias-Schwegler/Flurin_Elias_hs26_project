"""Download the MeteoSwiss raw files used by meteoswiss_eda.ipynb into data/ (about 90 MB).

Run once from this folder: python download_data.py
Source: MeteoSwiss open data, https://data.geo.admin.ch/browser/index.html#/collections/ch.meteoschweiz.ogd-smn
"""
from pathlib import Path

import requests

BASE = "https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn"
DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

files = [f"{st}/ogd-smn_{st}_h_{part}.csv" for st in ["luz", "moa", "spf", "ego", "pil"]
         for part in ["historical_2010-2019", "historical_2020-2029", "recent"]]
files += ["luz/ogd-smn_luz_d_historical.csv", "luz/ogd-smn_luz_d_recent.csv",
          "ogd-smn_meta_stations.csv", "ogd-smn_meta_parameters.csv"]

for rel in files:
    target = DATA / Path(rel).name
    if not target.exists():
        response = requests.get(f"{BASE}/{rel}", timeout=180)
        response.raise_for_status()
        target.write_bytes(response.content)
        print("downloaded", target.name)
