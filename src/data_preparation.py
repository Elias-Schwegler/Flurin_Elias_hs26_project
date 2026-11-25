"""Data preparation for "Untapped Sun": from the cleaned hourly table to one dataset with every model input.

Used by notebooks/02_data_preparation.ipynb.
Input:  data/processed/hourly_dataset.csv, written by notebooks/combined/combined_eda.ipynb (joining and
        cleaning of the four sources, all decisions on the raw data).
Output: data/processed/modeling_dataset.csv, read by notebooks/03_modeling.ipynb and 04_evaluation.ipynb.

Time axis: fixed CET (UTC+1, no clock changes); every stamp marks the START of the hour.

Rule for every model input: a value for an hour of day D may only use information that exists at the end
of day D-1 (forecasts made the day before, the calendar and the position of the sun, values measured on
D-1 or earlier).
"""
from pathlib import Path

import numpy as np
import pandas as pd

TZ = "Etc/GMT-1"                                   # fixed CET = UTC+1 (the minus sign is correct for this name)
ROOT = Path(__file__).resolve().parents[1]
HOURLY_DATASET = ROOT / "data" / "processed" / "hourly_dataset.csv"
MODELING_DATASET = ROOT / "data" / "processed" / "modeling_dataset.csv"
LATITUDE, LONGITUDE = 47.10, 8.14                  # centre of the four Lucerne stations
FORECAST_START = pd.Timestamp("2024-01-20", tz=TZ)  # first day with an archived ICON-D2 forecast

# Periods of the time series. The final model is trained on everything before the test year.
PERIODS = {
    "training": ("2019-01-01", "2023-12-31 23:00"),
    "warm-up": ("2024-01-01", "2024-01-19 23:00"),     # observed, but no forecast archived yet
    "validation": ("2024-01-20", "2024-12-31 23:00"),  # choose the model
    "test": ("2025-01-01", "2025-12-31 23:00"),        # used once, in 04_evaluation.ipynb
}


# ---------------------------------------------------------------------------------------------------------------
# 1. Loading
# ---------------------------------------------------------------------------------------------------------------

def _read(path):
    df = pd.read_csv(path, index_col=0)
    df.index = pd.to_datetime(df.index, utc=True).tz_convert(TZ)
    return df


def load_hourly(path=HOURLY_DATASET):
    """The hourly table of the EDA (61,368 hours x 24 columns), index in fixed CET."""
    return _read(path)


def load_modeling_dataset(path=MODELING_DATASET):
    """The output of 02_data_preparation.ipynb: hourly table + features + model inputs."""
    return _read(path)


# ---------------------------------------------------------------------------------------------------------------
# 2. Features
# ---------------------------------------------------------------------------------------------------------------

def sun_position(index, latitude=LATITUDE, longitude=LONGITUDE):
    """Sine of the sun's elevation in the middle of each hour and clear-sky radiation in W/m².

    Known years ahead (astronomy), so no leakage. Declination and equation of time after Spencer (1971),
    clear-sky global radiation after Haurwitz (1945): 1098 * cos(z) * exp(-0.057 / cos(z)).
    """
    t = index + pd.Timedelta(minutes=30)
    doy = t.dayofyear.values
    hour = t.hour.values + t.minute.values / 60
    g = 2 * np.pi / 365 * (doy - 1 + (hour - 12) / 24)
    declination = (0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g)
                   + 0.000907 * np.sin(2 * g) - 0.002697 * np.cos(3 * g) + 0.00148 * np.sin(3 * g))
    equation_of_time = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g)
                                 - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    solar_minutes = hour * 60 - 60 + 4 * longitude + equation_of_time      # CET is UTC+1
    hour_angle = np.radians(solar_minutes / 4 - 180)
    lat = np.radians(latitude)
    cos_zenith = np.sin(lat) * np.sin(declination) + np.cos(lat) * np.cos(declination) * np.cos(hour_angle)
    clear_sky = np.where(cos_zenith > 0, 1098 * cos_zenith * np.exp(-0.057 / np.maximum(cos_zenith, 1e-3)), 0.0)
    return pd.DataFrame({"sin_elevation": np.clip(cos_zenith, 0, None), "clear_sky": clear_sky}, index=index)


def add_features(df):
    """Calendar, sun position and signals of the previous day. Returns a copy."""
    out = df.copy()
    out[["sin_elevation", "clear_sky"]] = sun_position(out.index)
    angle = 2 * np.pi * out.index.dayofyear / 365.25
    out["season_cos"], out["season_sin"] = np.cos(angle), np.sin(angle)

    # Signals of day D-1, measured, so known at the end of D-1
    daily = out.resample("D").agg({"capacity_factor": "mean", "clear_sky": "mean", "radiation_PIL": "mean",
                                    "radiation_mean": "mean", "temperature_LUZ": "mean"})
    daily["production_index"] = daily["capacity_factor"] / (daily["clear_sky"] / 1000)
    daily["fog"] = ((daily["radiation_PIL"] > 2 * daily["radiation_mean"])          # same rule as EDA Q13
                    & (daily["radiation_PIL"] * 24 / 1000 >= 1.5)).astype(float)
    daily["cold"] = ((daily["temperature_LUZ"] < 1) & daily.index.month.isin([11, 12, 1, 2, 3])).astype(float)
    previous = daily.shift(1)                                                      # value of D-1 on day D
    day = out.index.normalize()
    out["yday_production_index"] = previous["production_index"].reindex(day).values
    out["yday_fog"] = previous["fog"].reindex(day).values
    out["yday_cold"] = previous["cold"].reindex(day).values
    return out


def conversion_factor(df, radiation="radiation_weighted", min_radiation=50):
    """Capacity factor per kW/m² of radiation, per month (rows) and hour (columns).

    Daylight hours with more than `min_radiation` W/m²; cells with fewer than 30 hours are left empty.
    Also returns the same factor per bin of the sun's elevation.
    """
    light = df[df[radiation] > min_radiation].dropna(subset=["capacity_factor"])
    group = [light.index.month, light.index.hour]
    factor = light["capacity_factor"].groupby(group).sum() / light[radiation].groupby(group).sum() * 1000
    factor = factor.where(light["capacity_factor"].groupby(group).size() >= 30).unstack()
    factor.index.name, factor.columns.name = "month", "hour"
    bins = pd.cut(light["sin_elevation"], np.arange(0, 1.01, 0.05))
    by_elevation = light.groupby(bins, observed=True).apply(
        lambda t: t["capacity_factor"].sum() / t[radiation].sum() * 1000, include_groups=False)
    by_elevation.index = [b.mid for b in by_elevation.index]
    return factor, by_elevation


# ---------------------------------------------------------------------------------------------------------------
# 3. Model inputs (exogenous variables of SARIMAX)
# ---------------------------------------------------------------------------------------------------------------

# Every input is linear in the radiation, so the model stays a linear regression with SARMA errors.
# Radiation enters in kW/m² so that all coefficients have a similar size (helps the optimiser).
INPUTS = {
    "rad": "radiation input r in kW/m²",
    "rad_elev": "r × sine of the sun's elevation",
    "rad_season_cos": "r × cos(day of the year)",
    "rad_season_sin": "r × sin(day of the year)",
    "rad_squared": "r²",
    "clear": "clear-sky radiation in kW/m²",
    "clear_season_cos": "clear-sky radiation × cos(day of the year)",
    "rad_yday_index": "r × yesterday's production index",
    "rad_yday_fog": "r × yesterday was a fog day",
    "clear_yday_fog": "clear-sky radiation × yesterday was a fog day",
    "rad_yday_cold": "r × yesterday was a cold winter day",
}

# The three sets compared on the validation year in 03_modeling.ipynb
FEATURE_SETS = {
    "radiation only": ["rad"],
    "physics": ["rad", "rad_elev", "rad_season_cos", "rad_season_sin", "rad_squared", "clear", "clear_season_cos"],
    "physics + day before": list(INPUTS),
}


def exog_matrix(df, columns=None, radiation="forecast_radiation"):
    """Model inputs from the features. `radiation` is the forecast, the measured radiation or `radiation_input`."""
    r = df[radiation] / 1000
    c = df["clear_sky"] / 1000
    candidates = {
        "rad": r,
        "rad_elev": r * df["sin_elevation"],
        "rad_season_cos": r * df["season_cos"],
        "rad_season_sin": r * df["season_sin"],
        "rad_squared": r ** 2,
        "clear": c,
        "clear_season_cos": c * df["season_cos"],
        "rad_yday_index": r * df["yday_production_index"],
        "rad_yday_fog": r * df["yday_fog"],
        "clear_yday_fog": c * df["yday_fog"],
        "rad_yday_cold": r * df["yday_cold"],
    }
    return pd.DataFrame({k: candidates[k] for k in (columns or list(INPUTS))}, index=df.index)


# ---------------------------------------------------------------------------------------------------------------
# 4. The modeling dataset
# ---------------------------------------------------------------------------------------------------------------

def period_of(index):
    """Name of the period (training, warm-up, validation, test) for every hour."""
    out = pd.Series("not used", index=index)
    for name, (start, end) in PERIODS.items():
        out[(index >= pd.Timestamp(start, tz=TZ)) & (index <= pd.Timestamp(end, tz=TZ))] = name
    return out


def build_modeling_dataset(hourly):
    """Hourly table + features + radiation input + target + period + the 11 model inputs."""
    df = add_features(hourly)
    # measured radiation as a stand-in until the archived forecasts start, the forecast afterwards
    df["radiation_input"] = df["radiation_weighted"].where(df.index < FORECAST_START, df["forecast_radiation"])
    # night hours (sun below the horizon) are not modelled: the forecast is set to 0 there
    df["target"] = df["capacity_factor"].where(df["clear_sky"] > 0)
    df["period"] = period_of(df.index)
    return pd.concat([df, exog_matrix(df, radiation="radiation_input")], axis=1)
