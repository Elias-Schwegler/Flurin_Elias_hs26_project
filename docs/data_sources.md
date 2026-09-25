# Data Sources — DSPRO1 HS26 (Energy & SDGs)

Catalogue extracted from `01_Organisation/03_potential_data_sources.pdf` (lecturer-provided).
Use this as the starting point for **Deliverable 3: Data Sources & EDA** (due 30.10.2026 per ILIAS).

> Before combining datasets, check that their **spatial units, boundary versions, time periods,
> coordinate systems and licences are compatible.**

Selection checklist for our project:
- [ ] Relevance to chosen SDG(s)
- [ ] Licence permits redistribution / use
- [ ] Spatial + temporal resolution match
- [ ] Merge keys available (building ID, coordinates, municipality/statistical-area code, date/timestamp)
- [ ] Access method (API / bulk download / portal)

---

## 1. Energy data sources

Sources describing energy production, consumption, infrastructure, prices, trade, technologies or emissions from energy use.

### Switzerland
| Source | Description | Link |
|---|---|---|
| Swiss Federal Office of Energy — energy statistics | Official energy balances, electricity statistics, renewables, prices, sector publications | https://www.bfe.admin.ch/ |
| Swiss Energy Dashboard | Electricity, gas, price, weather, supply-security indicators, open data + API | https://www.energy-dashboard.admin.ch/ |
| opendata.swiss — energy datasets | Federal, cantonal, municipal energy datasets | https://opendata.swiss/de/ |
| Swissgrid grid data | Transmission load, production, cross-border exchange, ancillary services | https://www.swissgrid.ch/en/home/operation/grid-data.html |
| ElCom electricity tariffs | Electricity prices & tariff components by municipality/operator/customer category | https://www.elcom.admin.ch/ |

### Europe
| Source | Description | Link |
|---|---|---|
| Eurostat energy database | Harmonised energy balances, supply, final consumption, prices, renewables, efficiency | https://ec.europa.eu/eurostat/web/energy/data/database |
| ENTSO-E Transparency Platform | Generation, load, prices, cross-border flows, outages, balancing | https://transparency.entsoe.eu/ |
| ENTSO-G Transparency Platform | Gas flows, capacities, network points, LNG, storage | https://transparency.entsog.eu/ |
| JRC Data Catalogue | Energy technologies, buildings, transport, emissions, renewable potential | https://data.jrc.ec.europa.eu/ |
| Open Power System Data | Cleaned European electricity time series, power-plant lists, weather, load profiles | https://open-power-system-data.org/ |
| Ember Electricity Data Explorer | Harmonised generation, demand, imports, power-sector emissions | https://ember-energy.org/data/ |

### Global
| Source | Description | Link |
|---|---|---|
| IEA data & statistics | Country energy balances, indicators, topic datasets (access varies) | https://www.iea.org/data-and-statistics |
| UN Energy Statistics | National production, trade, transformation, consumption | https://unstats.un.org/unsd/energy/ |
| Energy Institute Statistical Review of World Energy | Global fuel/electricity/trade/price/emission time series | https://www.energyinst.org/statistical-review |
| IRENA data | Renewable capacity, generation, costs, finance, employment | https://www.irena.org/Data |
| EIA Open Data (US) | US & international energy statistics | https://www.eia.gov/opendata/ |
| Our World in Data — Energy | Harmonised country energy & electricity indicators (downloadable) | https://ourworldindata.org/energy |
| energydata.info | Electricity access, networks, utilities, demand, renewable resources | https://energydata.info/ |
| Global Energy Monitor trackers | Unit-level power stations, mines, pipelines, infrastructure | https://globalenergymonitor.org/ |
| Nature Scientific Data (energy) | Research unit-level energy infrastructure datasets | https://www.nature.com/sdata/ |

---

## 2. Complementary data (merge with energy)

Explanatory variables, denominators, spatial context or outcome measures.

### Buildings & addresses
| Source | Description | Link |
|---|---|---|
| Federal Register of Buildings and Dwellings | Building coordinates, category, construction period, heating | https://www.housing-stat.ch/ |
| FSO building statistics | Aggregated building stock, dwellings, heating | https://www.bfs.admin.ch/ |
| City of Zurich Open Data | Georeferenced building, entrance, dwelling records | https://data.stadt-zuerich.ch/ |
| EU Building Stock Observatory | European building stock, consumption, renovation, performance | https://energy.ec.europa.eu/topics/energy-efficiency/energy-efficient-buildings/eu-building-stock-observatory |
| OpenStreetMap | Global building footprints, land use, roads, infrastructure (ODbL) | https://www.openstreetmap.org/ |

### Population, households & socioeconomics
| Source | Description | Link |
|---|---|---|
| FSO STAT-TAB | Swiss population, households, income, employment, regional statistics | https://www.pxweb.bfs.admin.ch/ |
| Swiss population & household statistics | Demographic/household variables, official geographic classifications | https://www.bfs.admin.ch/ |
| Eurostat database | European population, income, housing, industry, regional indicators | https://ec.europa.eu/eurostat/data/database |
| World Bank Open Data | Country population, income, development, access, economic indicators | https://data.worldbank.org/ |
| Global Human Settlement Layer | Gridded population, built-up area, settlement classes | https://ghsl.jrc.ec.europa.eu/ |

### Weather & climate
| Source | Description | Link |
|---|---|---|
| MeteoSwiss Open Data | Swiss station observations, climate series, gridded products | https://www.meteoswiss.admin.ch/services-and-publications/service/open-data.html |
| Copernicus CDS / ERA5 | Global hourly reanalysis (temperature, wind, radiation, precipitation) | https://cds.climate.copernicus.eu/ |
| NASA POWER | Global solar & meteorological time series via API | https://power.larc.nasa.gov/ |
| NOAA climate data | Global station, climate and extreme-weather records | https://www.ncei.noaa.gov/ |

### Land use, terrain & spatial constraints
| Source | Description | Link |
|---|---|---|
| swisstopo geodata | Topography, elevation, imagery, boundaries, base maps | https://www.swisstopo.admin.ch/ |
| FSO land-use statistics | Land cover and land-use change in Switzerland | https://www.bfs.admin.ch/ |
| Copernicus Land Monitoring Service | Land cover, urban form, vegetation | https://land.copernicus.eu/ |
| Copernicus Urban Atlas | Detailed land use for European urban areas | https://land.copernicus.eu/local/urban-atlas |

### Mobility & transport
| Source | Description | Link |
|---|---|---|
| Open Transport Data Switzerland | Public-transport stops, schedules, real-time movements | https://opentransportdata.swiss/ |
| Swiss electric-mobility information | EV and charging-infrastructure data links | https://www.bfe.admin.ch/ |
| European Alternative Fuels Observatory | Vehicles, charging, alternative-fuel infrastructure | https://alternative-fuels-observatory.ec.europa.eu/ |
| Eurostat transport database | Vehicles, passenger/freight activity, modal split, infrastructure | https://ec.europa.eu/eurostat/web/transport/data/database |

### Economy, industry & prices
| Source | Description | Link |
|---|---|---|
| FSO national economy statistics | Swiss GDP, production, employment, sector structure | https://www.bfs.admin.ch/ |
| OECD Data Explorer | Economic activity, industry, prices, taxation, environment | https://data-explorer.oecd.org/ |

### Environment, emissions & health
| Source | Description | Link |
|---|---|---|
| FOEN environmental data | Swiss greenhouse gases, air pollution, water, biodiversity, noise | https://www.bafu.admin.ch/ |
| FOEN hydrological data | River flow, lake levels, water temperature | https://www.hydrodaten.admin.ch/ |
| EEA Datahub | European emissions, air quality, climate, environment | https://www.eea.europa.eu/en/datahub |
| UNFCCC greenhouse-gas data | Official national GHG inventories | https://unfccc.int/ghg-inventory-data |
| EDGAR emissions database | Global gridded & country emissions by sector/pollutant | https://edgar.jrc.ec.europa.eu/ |
| Copernicus Atmosphere Monitoring Service | Atmospheric composition, air-quality products | https://atmosphere.copernicus.eu/ |
| Protected Planet / GBIF | Protected areas, species occurrence (ecological constraints) | https://www.protectedplanet.net/ , https://www.gbif.org/ |

---

## Validated PV-specific sources (for the PV-potential project)

- BFE Solarenergiepotenziale der Schweizer Gemeinden (CSV/JSON/XLS, per-municipality rooftop+facade potential): https://www.bfe-ogd.ch/ogd52/Solarenergiepotenziale_Gemeinden_Daecher_und_Fassaden.csv
- BFE solar irradiation maps, 30°/75°/90° tilt (GPKG/WMS/WMTS): https://opendata.swiss/de/dataset/solare-einstrahlung-auf-eine-30-nach-suden-geneigte-flache
- CH-POA300 hourly plane-of-array irradiance, 300 m, 2004–2020 + 2016 (EnviDat, attribution): https://doi.org/10.16904/ENVIDAT.632
- pvlib-python (BSD-3) irradiance → PV output: https://pvlib-python.readthedocs.io
- Swissgrid grid data (validation): https://www.swissgrid.ch/en/home/operation/grid-data.html

See `project_proposals.md` for scope and processability notes.

## Candidate project directions (energy × SDG)
- **SDG 7 (Affordable & Clean Energy):** renewable potential vs. demand at municipality level (MeteoSwiss/NASA POWER + swisstopo + ElCom tariffs).
- **SDG 11 (Sustainable Cities):** building heating mix vs. building age (Building Register + OGD Zurich + EUROSTAT).
- **SDG 13 (Climate Action):** power-sector emission intensity (Ember/ENTSO-E) combined with cross-border flows.
- **SDG 9 (Industry/Infrastructure):** grid congestion vs. generation (Swissgrid load + ENTSO-E exchange).
