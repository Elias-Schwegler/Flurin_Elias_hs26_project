# Project Plan – until Coaching 2 (week of 12 Oct 2026)

Team: Elias Schwegler, Flurin Yenigün · Coach: Dr. Dimitris Mousadakos

## Tasks until next coaching

| Task | Owner | Due |
|---|---|---|
| D1: project name in README (branch `dlv1-title-pitch`) | Elias | Thu 15 Oct |
| D1: pitch, 3–5 sentences, in README; open PR with coach as reviewer | Flurin | Thu 15 Oct |
| Data check: Energy-Charts + MeteoSwiss (coverage, gaps, time zones) | Elias | next coaching |
| Data check: SFOE plant register (plausibility, capacity growth in Lucerne) | Flurin | next coaching |
| Draft SMART goals for D2 | both | Mon 12 Oct (team meeting) |

## Data check – relevance and quality

Load each source once and fill in the table. Scores from 1 (poor) to 5 (good).

| Criterion | Energy-Charts (solar CH) | MeteoSwiss station Luzern | SFOE plant register |
|---|---|---|---|
| Content | hourly solar generation, CH (MW) | radiation, temperature, sunshine | one row per plant: kW, start date, tilt, orientation |
| Time coverage | | | snapshot, plants in operation only |
| Spatial / temporal resolution | Switzerland / 1 h | 1 station / 10 min, 1 h | per plant / – |
| Missing values (% of hours) | | | – |
| Time zone, daylight saving | | | – |
| Plausibility (negative values, night values, outliers) | | | |
| Licence / attribution | | attribution «Source: MeteoSwiss» | attribution required |
| Relevance (1–5) | | | |
| Quality (1–5) | | | |
| Notes | | | |

Questions we should be able to answer:
1. From which year on is each source usable, and how many hours are missing?
2. Do the time stamps of the sources match (UTC vs. local time)?
3. What is the biggest quality issue, and how do we handle it?

## Draft SMART goals (for D2, due 22 Oct)

Values in `[…]` are placeholders, to be set after the data check.

| # | Goal | Measured by | Due |
|---|---|---|---|
| G1 | Build a cleaned, documented hourly dataset (2018–2025) combining Swiss solar generation with MeteoSwiss weather data. | ≥ `[95]` % of hours covered; every cleaning step documented | 12 Nov (D3) |
| G2 | Quantify how strongly solar generation follows the weather (correlation with global radiation per season; daily and seasonal profiles). | correlations reported per season; profiles visualised | 12 Nov (D3) |
| G3 | Build a day-ahead SARIMAX forecast that beats a seasonal-naive baseline; TimesFM as optional benchmark. | MAE ≥ `[10]` % lower than baseline on `[last 3 months of 2025]` | 3 Dec (D4) |
| G4 | Provide an interactive dashboard with the key EDA findings and forecast vs. actual for a selected week. | runs locally, reproducible via README | 11 Jan 2027 |

## Open questions

- **Weather data:** a single station (Luzern) vs. several stations (e.g. weighted by installed PV capacity from the plant register) vs. gridded or reanalysis data.
- **Forecast inputs:** a real day-ahead forecast can only use information available the day before (weather *forecasts*, not measured weather of the same day).
- **Licences:** confirm the Energy-Charts terms of use before publishing data or figures.

---
*AI use: this plan was drafted with AI assistance (Claude) and will be reviewed by both team members on 12 Oct.*
