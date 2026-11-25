"""Download the raw files used by bfe_register_eda.ipynb into data/ (about 85 MB).

Run once from this folder: python download_data.py
Sources: SFOE plant register, https://opendata.swiss/de/dataset/elektrizitatsproduktionsanlagen
Energy-Charts installed power, https://api.energy-charts.info, CC BY 4.0
MeteoSwiss station list, https://data.geo.admin.ch/browser/index.html#/collections/ch.meteoschweiz.ogd-smn
"""
import zipfile
from pathlib import Path

import requests

REGISTER = ("https://data.geo.admin.ch/ch.bfe.elektrizitaetsproduktionsanlagen/"
            "csv/2056/ch.bfe.elektrizitaetsproduktionsanlagen.zip")
INSTALLED = "https://api.energy-charts.info/installed_power"
STATIONS = "https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn/ogd-smn_meta_stations.csv"
DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

target = DATA / "ch.bfe.elektrizitaetsproduktionsanlagen.zip"
if not target.exists():
    response = requests.get(REGISTER, timeout=300)
    response.raise_for_status()
    target.write_bytes(response.content)
    print("downloaded", target.name)
with zipfile.ZipFile(target) as z:
    z.extractall(DATA)

target = DATA / "installed_power_ch_yearly.json"
if not target.exists():
    params = {"country": "ch", "time_step": "yearly", "installation_decommission": "false"}
    response = requests.get(INSTALLED, params=params, timeout=180)
    response.raise_for_status()
    target.write_bytes(response.content)
    print("downloaded", target.name)

target = DATA / "ogd-smn_meta_stations.csv"
if not target.exists():
    response = requests.get(STATIONS, timeout=180)
    response.raise_for_status()
    target.write_bytes(response.content)
    print("downloaded", target.name)
