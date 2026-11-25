"""Data modeling for "Untapped Sun": day-ahead SARIMAX forecast of the hourly capacity factor (G3).

Used by notebooks/03_modeling.ipynb (and 04_evaluation.ipynb). Input: data/processed/modeling_dataset.csv,
written by notebooks/02_data_preparation.ipynb (features and model inputs: src/data_preparation.py).
Fitted parameters are cached in data/processed/models/<name>.json (a few KB each).
"""
import gc
import json
import time
from types import SimpleNamespace

import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

from src.data_preparation import ROOT, TZ

MODELS = ROOT / "data" / "processed" / "models"
TAIL = 60 * 24   # hours used to rebuild the model state for forecasting (the state only holds the last 24 hours)


# ---------------------------------------------------------------------------------------------------------------
# 1. Inputs and reference
# ---------------------------------------------------------------------------------------------------------------

def model_inputs(data, columns):
    """Inputs X and target y for SARIMAX. Hours with a missing input get no target (y = NaN), X is set to 0 there."""
    X = data[columns]
    y = data["target"].where(X.notna().all(axis=1))
    return X.fillna(0), y


def monthly_factor_reference(data, train_from, train_to, index):
    """Reference (b) of G3: radiation forecast × one factor per month, factor from the measured radiation (EDA Q17)."""
    t = data.loc[train_from:train_to].dropna(subset=["capacity_factor", "radiation_weighted"])
    f = t["capacity_factor"].groupby(t.index.month).sum() / t["radiation_weighted"].groupby(t.index.month).sum()
    return data.loc[index, "forecast_radiation"] * index.month.map(f)


# ---------------------------------------------------------------------------------------------------------------
# 2. Estimation and day-ahead forecasts
# ---------------------------------------------------------------------------------------------------------------

def start_values(endog, exog, order, seasonal_order, tol=1e-6, max_iter=50):
    """Start values for the SARIMAX likelihood, so that the optimiser needs few iterations on 50,000 hours.

    With errors u_t = Phi * u_{t-24} + e_t the model splits into 24 independent AR(1) chains (one per hour of
    the day), and iterated Cochrane-Orcutt (GLS) gives beta and Phi almost exactly: regress u_t on u_{t-24},
    then y_t - Phi*y_{t-24} on x_t - Phi*x_{t-24}, until Phi stops changing. Without a seasonal term this is OLS.
    A non-seasonal AR(1) term starts at the lag-1 autocorrelation of the remaining error.
    Returns the parameter vector in SARIMAX order: beta, (ar.L1), (ar.S.L24), sigma2.
    """
    y, X = np.asarray(endog, dtype=float), np.asarray(exog, dtype=float)
    ok = ~np.isnan(y)
    beta = np.linalg.lstsq(X[ok], y[ok], rcond=None)[0]
    phi_s = 0.0
    if seasonal_order[0]:
        s = seasonal_order[3]
        for _ in range(max_iter):
            u = y - X @ beta
            pair = ~np.isnan(u[s:]) & ~np.isnan(u[:-s])
            new = (u[s:][pair] @ u[:-s][pair]) / (u[:-s][pair] @ u[:-s][pair])
            beta = np.linalg.lstsq((X[s:] - new * X[:-s])[pair], (y[s:] - new * y[:-s])[pair], rcond=None)[0]
            done = abs(new - phi_s) < tol
            phi_s = new
            if done:
                break
    u = y - X @ beta
    e = u.copy()
    if seasonal_order[0]:
        e[s:] = u[s:] - phi_s * u[:-s]
        e[:s] = np.nan
    params = list(beta)
    if order[0]:
        params.append(pd.Series(e).autocorr(1))
    if seasonal_order[0]:
        params.append(phi_s)
    params.append(np.nanvar(e))
    return np.array(params)


def state_at_end(endog, exog, order, seasonal_order, params):
    """Model with fixed parameters, filtered over the last 60 days only: same state at the end as over all years."""
    return SARIMAX(endog.values[-TAIL:], exog=exog.values[-TAIL:], order=order,
                   seasonal_order=seasonal_order).filter(params)


def fit_or_load(name, endog, exog, order, seasonal_order, standard_errors=False, refit=False):
    """SARIMAX fitted by maximum likelihood, or loaded from data/processed/models/<name>.json if fitted before.

    Only the numbers are cached. low_memory=True keeps the fit on 50,000 hours below about 1 GB.
    Returns a namespace with params, llf, aic, bic, nobs, converged, (bse, pvalues) and `results`,
    the model state at the end of `endog`, ready for day_ahead_forecast().
    """
    path = MODELS / f"{name}.json"
    if path.exists() and not refit:
        info = json.loads(path.read_text(encoding="utf-8"))
    else:
        start = time.time()
        model = SARIMAX(endog.values, exog=exog.values, order=order, seasonal_order=seasonal_order)
        initial = start_values(endog, exog, order, seasonal_order)
        # factr=1e10: stop when the log-likelihood changes by less than ~1e-6 relative (the start values are already close)
        res = model.fit(start_params=initial, disp=False, maxiter=200, low_memory=True, factr=1e10,
                        cov_type="approx" if standard_errors else "none")
        info = {"params": res.params.tolist(), "llf": res.llf, "aic": res.aic, "bic": res.bic,
                "nobs": int(np.isfinite(endog).sum()), "llf_at_start": model.loglike(initial),
                "converged": bool(res.mle_retvals["converged"]), "seconds": time.time() - start,
                "bse": res.bse.tolist() if standard_errors else None,
                "pvalues": res.pvalues.tolist() if standard_errors else None}
        print(f"{name}: fitted in {info['seconds']:.0f} s, converged: {info['converged']}, "
              f"log-likelihood at the start values {info['llf_at_start']:,.1f}, at the maximum {info['llf']:,.1f}")
        MODELS.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(info, indent=1), encoding="utf-8")
        del res, model
        gc.collect()
    info["params"] = np.array(info["params"])
    info["results"] = state_at_end(endog, exog, order, seasonal_order, info["params"])
    return SimpleNamespace(**info)


def postprocess(prediction, clear_sky):
    """A capacity factor lies between 0 and 1 and is 0 while the sun is below the horizon."""
    p = prediction.clip(0, 1)
    p[clear_sky.reindex(p.index) == 0] = 0.0
    return p


def day_ahead_forecast(results, exog, endog, start, end, origin_hour=0):
    """Rolling day-ahead forecast with fixed parameters.

    For every day D in [start, end] the model state is updated with all observations up to the origin
    (00:00 of D, i.e. the end of D-1; or 12:00 of D-1 with `origin_hour=12`) and the 24 hours of D are
    forecast. The parameters are NOT re-estimated, so no information of the forecast period enters them.
    `results` must be fitted on data that ends exactly at the first origin.
    """
    current, out = results, []
    lead = pd.Timedelta(hours=(24 - origin_hour) % 24)
    one = pd.Timedelta(hours=1)
    for d in pd.date_range(start, end, freq="D", tz=TZ):
        x_target = exog.loc[d:d + 23 * one]
        x_all = exog.loc[d - lead:d + 23 * one]          # gap between origin and 00:00 of D, then day D
        f = np.asarray(current.forecast(steps=len(x_all), exog=x_all.values))[len(x_all) - len(x_target):]
        out.append(pd.Series(f, index=x_target.index))
        new = slice(d - lead, d + 23 * one - lead)       # the 24 observed hours up to the next origin
        current = current.extend(endog.loc[new].values, exog=exog.loc[new].values)
    return pd.concat(out)


# ---------------------------------------------------------------------------------------------------------------
# 3. Scores
# ---------------------------------------------------------------------------------------------------------------

def mae_pct(prediction, truth):
    """MAE in % of the mean of the observed values of the same hours (definition of EDA Q17)."""
    ok = prediction.notna() & truth.notna()
    return (prediction[ok] - truth[ok]).abs().mean() / truth[ok].mean() * 100


def rmse_pct(prediction, truth):
    """Root mean squared error in % of the mean of the observed values."""
    ok = prediction.notna() & truth.notna()
    return np.sqrt(((prediction[ok] - truth[ok]) ** 2).mean()) / truth[ok].mean() * 100


def r_squared(prediction, truth):
    """1 - SSE / SST."""
    ok = prediction.notna() & truth.notna()
    p, y = prediction[ok], truth[ok]
    return 1 - ((p - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def skill(model_error, reference_error):
    """1 - error(model) / error(reference); 0.10 = 10 % less error than the reference."""
    return 1 - model_error / reference_error


def score_table(predictions, truth, daylight):
    """Hourly MAE, daily MAE, RMSE, MAE per season block and R² for several predictions (dict name -> Series)."""
    rows = {}
    month = truth.index.month
    winter, summer = month.isin([11, 12, 1, 2]), month.isin([5, 6, 7, 8])
    for name, p in predictions.items():
        p = p.reindex(truth.index)
        rows[name] = {
            "MAE hourly, %": mae_pct(p, truth),
            "MAE daily, %": mae_pct(p.resample("D").mean(), truth.resample("D").mean()),
            "RMSE hourly, %": rmse_pct(p, truth),
            "MAE Nov-Feb, %": mae_pct(p[winter], truth[winter]),
            "MAE May-Aug, %": mae_pct(p[summer], truth[summer]),
            "R² hourly": r_squared(p, truth),
            "R² daylight": r_squared(p[daylight], truth[daylight]),
        }
    return pd.DataFrame(rows).T


def bootstrap_skill(prediction, reference, truth, n=2000, block_days=7, seed=0):
    """Uncertainty of the skill: moving-block bootstrap over whole days (blocks of `block_days` days).

    Days are drawn in blocks because the errors of neighbouring days are correlated (weather periods).
    Returns an array of n skill values.
    """
    rng = np.random.default_rng(seed)
    ok = prediction.notna() & reference.notna() & truth.notna()
    frame = pd.DataFrame({"m": (prediction - truth).abs(), "r": (reference - truth).abs()})[ok]
    values = frame.groupby(frame.index.normalize()).sum().values
    n_days = len(values)
    n_blocks = int(np.ceil(n_days / block_days))
    out = np.empty(n)
    for i in range(n):
        starts = rng.integers(0, n_days - block_days + 1, n_blocks)
        rows = (starts[:, None] + np.arange(block_days)).ravel()[:n_days]
        s = values[rows].sum(axis=0)
        out[i] = 1 - s[0] / s[1]
    return out
