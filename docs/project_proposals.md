# Project Proposals & Data Processability

Brainstorm based on `03_potential_data_sources.pdf`. Ranked for **pandas/numpy-level simplicity**
(no heavy ML, no GenAI per curriculum) while staying SDG-aligned.

**Processability score:** 5 = trivial (clean CSV/API, one `read_*`), 4 = easy, 3 = moderate,
2 = fiddly (geo/netCDF), 1 = heavy tooling. *Higher = friendlier.*

> Constraint: DSPRO1 wants *clear, reproducible* work and a dashboard/statistical story.
> Foundation models are optional (and the curriculum says they are not desired as the core).

---

## Research findings (validated Aug 2026)

**TimesFM status** — Google's open time-series foundation model is now at **3.0** (Aug 2026); repo
`google-research/timesfm` (33.7k ⭐), HF weights `google/timesfm-3.0-pytorch`. TimesFM 3.0 adds
native multivariate + past-only/past-and-future covariates, and ranks #1 on fev-bench / TIME / GIFT-Eval.
- Install: `pip install timesfm[torch]`, GPU (`device="cuda"`) or MLX on Apple silicon.
- ⚠️ **Licence:** source Apache-2.0, weights ≤2.5 Apache-2.0, but **3.0 weights are non-commercial**
  (`timesfm-non-commercial-license-v1.0`) — fine for a student project, cite it.
- Verdict: technically feasible; keep as **stretch only** (curriculum prefers no foundation models as core).

**Swiss PV data is already public and rich** → the novelty shifts from *computing potential* (already
done by BFE/sonnendach.ch) to *temporal production simulation + forecasting*:
- **BFE Solarenergiepotenziale der Schweizer Gemeinden** — CSV/JSON/XLS rooftop+facade potential per
  municipality: https://www.bfe-ogd.ch/ogd52/Solarenergiepotenziale_Gemeinden_Daecher_und_Fassaden.csv
- **BFE solar irradiation maps** (30°/75°/90° tilt) — GPKG/WMS/WMTS on opendata.swiss.
- **CH-POA300** — hourly plane-of-array irradiance, 300 m, 2004–2020 + typical year 2016 (EnviDat,
  attribution licence): https://doi.org/10.16904/ENVIDAT.632 — the temporal backbone. Full data is
  ~700–800 GB, but stats bundles are ~1.3–1.8 GB (start there).
- **pvlib-python** (BSD-3, NumFOCUS) converts irradiance → PV AC output: https://pvlib-python.readthedocs.io
- **Swissgrid grid data** (load/generation/cross-border flows) for validation: https://www.swissgrid.ch/en/home/operation/grid-data.html

**Licences:** BFE/CH-POA300 = attribution required; OSM = ODbL; pvlib = BSD-3.

---

## A. Your idea — National max-PV production + meteorology (recommended)

**SDGs:** 7 (Clean Energy), 13 (Climate Action), 11 (Sustainable Cities)
**Idea:** Estimate theoretical maximum PV electricity potential from rooftop area × irradiance ×
module efficiency, weight by historic weather, and (stretch) forecast future production with
**Google TimesFM**.

**Positioning:** BFE already publishes static potential per municipality, so add value by **modelling
the temporal dimension** (hourly/seasonal production) and **forecasting**, not just mapping potential.

**MVP (deliverable-ready):**
1. Municipality rooftop potential from the BFE CSV (already tabular + clean).
2. Hourly irradiance from CH-POA300 statistics / typical-year (or MeteoSwiss / NASA POWER).
3. Convert irradiance → kWh with `pvlib` models; aggregate to municipality × day/month profiles.
4. Validate simulated profile against Swissgrid generation; report error.

**Stretch:** TimesFM zero-shot forecast of irradiance/production to 2050 under a simple scenario.

**Assessment:** Strong, own the story, directly energy-SDG. Real risks:
- Whole-Switzerland scale is big → start with **one canton** as MVP, expand later.
- CH-POA300 is huge → use the stats bundle, not the raw 800 GB.
- TimesFM needs GPU/non-commercial weights → keep as extension only.

**Data processability:** potential CSV 5, irradiance 3 (large netCDF), pvlib 4, validation 4.
Overall **medium** once scoped to a canton.

---

## B. Heat-pump vs. fossil heating suitability (strong, simpler)

**SDGs:** 7, 11, 13
Municipality/building-grade indicator of where a heat pump is technically suitable (building age,
construction period) and where fossil heating still dominates; join outdoor-temperature profiles.
Output: map + "switch potential" ranking. **Data:** Building Register (2), FSO building stats (3),
MeteoSwiss (3). Mostly tabular joins → **high processability (~4)**. Very dashboard-friendly.

---

## C. Grid congestion / cross-border exchange (SDG 9 + 7)

Swissgrid load + ENTSO-E flows + Ember generation to surface region-hour risk periods.
**Data:** Swissgrid (4), ENTSO-E API (3), Ember (5). High processability, clean time series.

---

## D. Municipal renewable share vs. demand (SDG 7)

Compare OWID/Ember country data + FSO population/consumption. Simple ratios and plots.
**Data:** Our World in Data (5), Ember (5), FSO STAT-TAB (3). **Highest processability.**

---

## E. EV charging-infrastructure gap (SDG 7, 9, 11)

EV registrations vs. charging points vs. population/municipality; nearest-charger distance.
**Data:** OSM chargers (2), EAFO (3), FSO (3). Nice accessibility/fairness angle.

---

## F. Hydropower seasonality & water temperature (SDG 7, 13)

FOEN hydro + MeteoSwiss climate series; seasonal trend + water-temp effect on cooling/hydro.
**Data:** FOEN hydro (3), MeteoSwiss (3). Moderate.

---

## G. Household energy-poverty indicators (SDG 7, 1)

Tariffs vs. income vs. building heating type → affordability flag by municipality.
**Data:** ElCom tariffs (4), FSO income (3), Building Register (2). Very tabular → easy.

---

## Comparison

| # | Proposal | SDGs | Feasibility | Wow factor | Data prep |
|---|---|---|---|---|---|
| A | Max PV + meteo (+TimesFM) | 7/13/11 | medium | high | geo + API |
| B | Heat-pump switch potential | 7/11/13 | **high** | high | tabular joins |
| C | Grid congestion | 9/7 | high | medium | time series |
| D | Renewable vs. demand | 7 | **very high** | low | ratios |
| E | EV charger gap | 7/9/11 | medium | medium | geo |
| F | Hydro seasonality | 7/13 | medium | medium | time series |
| G | Energy poverty | 7/1 | high | medium | tabular |

---

## Data processability ranking (all sources from the org doc)

| Score | Sources | Format / access | Prep |
|---|---|---|---|
| 5 | Our World in Data, Ember | CSV download | drop-in, group-by |
| 4 | ElCom tariffs, Swissgrid, EIA, energydata.info | CSV/XLSX/API | clean, join keys |
| 3 | ENTSO-E, ENTSO-G, Eurostat, FSO STAT-TAB, MeteoSwiss, FOEN hydro, GBIF | API/CSV | JSON/XML parse, tidy |
| 2 | OSM, Building Register, swisstopo, GHSL, EDGAR, GEM trackers | GeoJSON/PBF/netCDF | geopandas / raster |
| 1 | ERA5/CDS, Copernicus products, IEA | netCDF/portal | xarray, auth, heavy |

**Licence watch-outs:** OSM = ODbL (attribution + share-alike), ERA5/Copernicus = attribution required.
Note in `docs/data_sources.md`.

---

## Recommendation

Go with **A** (your idea) but **scope the MVP to one canton** so it's feasible in semester time;
budget TimesFM strictly as a stretch goal. **B** and **G** are the safest fallbacks if A feels too
wide. The PV idea has the clearest SDG-7 hook and the best story for the pitch.

**Concrete first datasets for A:** BFE municipality potential CSV (`bfe-ogd.ch/ogd52/...`,
attribution) + CH-POA300 typical-year stats (`doi.org/10.16904/ENVIDAT.632`) + `pvlib` +
Swissgrid validation. Start with a single canton, monthly aggregation, then extend to hourly.

**Suggested SDG framing:** SDG 7.2/7.3 (renewable share), SDG 7.a (clean-energy access),
SDG 13.2 (climate action) — and reference the Swissgrid PV-integration white paper for context.
