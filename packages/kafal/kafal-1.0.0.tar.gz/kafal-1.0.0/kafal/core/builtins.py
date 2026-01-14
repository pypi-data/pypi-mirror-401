from __future__ import annotations

from typing import Dict, Any, List

import talib
import pandas as pd
import numpy as np

# ------------------------------------------------------
# Core TA wrappers
# ------------------------------------------------------


def sma(series, length):
    return pd.Series(talib.SMA(series.values, int(length)), index=series.index)


def ema(series, length):
    return pd.Series(talib.EMA(series.values, int(length)), index=series.index)


def rsi(series, length):
    return pd.Series(talib.RSI(series.values, int(length)), index=series.index)


def macd(source, fast=12, slow=26, sig=9):
    fast = int(fast)
    slow = int(slow)
    sig = int(sig)
    macd_vals, signal_vals, hist_vals = talib.MACD(source.values, fast, slow, sig)
    idx = source.index
    return (
        pd.Series(macd_vals, index=idx),
        pd.Series(signal_vals, index=idx),
        pd.Series(hist_vals, index=idx),
    )


def bbands(source, length=20, std=2.0):
    length = int(length)
    std = float(std)
    upper, middle, lower = talib.BBANDS(source.values, length, std, std)
    idx = source.index
    return (
        pd.Series(upper, index=idx),
        pd.Series(middle, index=idx),
        pd.Series(lower, index=idx),
    )


# ------------------------------------------------------
# Price / series helpers
# ------------------------------------------------------


def nz(series_or_value, replacement=0.0):
    """
    Replace NaN with replacement. Works with scalars or pandas Series.
    """
    if isinstance(series_or_value, pd.Series):
        return series_or_value.fillna(replacement)
    if series_or_value is None or (
        isinstance(series_or_value, float) and np.isnan(series_or_value)
    ):
        return replacement
    return series_or_value


def crossover(series1, series2):
    """
    True where series1 crosses over series2 on this bar.
    """
    s1 = pd.Series(series1)
    s2 = pd.Series(series2)
    prev = s1.shift(1) <= s2.shift(1)
    now = s1 > s2
    return prev & now


def crossunder(series1, series2):
    """
    True where series1 crosses under series2 on this bar.
    """
    s1 = pd.Series(series1)
    s2 = pd.Series(series2)
    prev = s1.shift(1) >= s2.shift(1)
    now = s1 < s2
    return prev & now


def change(series, length=1):
    """
    Equivalent of close - close[length].
    """
    s = pd.Series(series)
    return s - s.shift(int(length))


def percent_change(series, length=1):
    s = pd.Series(series)
    prev = s.shift(int(length))
    return (s - prev) / prev * 100.0


# ---------- price composites & rolling helpers ----------


def hl2(high, low):
    """
    (high + low) / 2
    """
    h = pd.Series(high)
    l = pd.Series(low)
    return (h + l) / 2.0


def hlc3(high, low, close):
    """
    (high + low + close) / 3
    """
    h = pd.Series(high)
    l = pd.Series(low)
    c = pd.Series(close)
    return (h + l + c) / 3.0


def ohlc4(open_, high, low, close):
    """
    (open + high + low + close) / 4
    """
    o = pd.Series(open_)
    h = pd.Series(high)
    l = pd.Series(low)
    c = pd.Series(close)
    return (o + h + l + c) / 4.0


def typical_price(high, low, close):
    """
    Alias for hlc3.
    """
    return hlc3(high, low, close)


def highest(series, length):
    """
    Rolling highest high over window.
    """
    s = pd.Series(series)
    return s.rolling(int(length)).max()


def lowest(series, length):
    """
    Rolling lowest low over window.
    """
    s = pd.Series(series)
    return s.rolling(int(length)).min()


def sum_n(series, length):
    """
    Rolling sum over window.
    """
    s = pd.Series(series)
    return s.rolling(int(length)).sum()


def stdev(series, length):
    """
    Rolling standard deviation over window.
    """
    s = pd.Series(series)
    return s.rolling(int(length)).std()


# ---------- color helper ----------


def rgba(r, g, b, a):
    """
    Return RGBA color string (0-255 for rgb, 0-1 for a).

    Host can map this to its own color type.
    """
    r = int(r)
    g = int(g)
    b = int(b)
    a = float(a)
    return f"rgba({r},{g},{b},{a})"


# ------------------------------------------------------
# Array helpers
# ------------------------------------------------------


def array():
    """
    Create a new Kafal array (Python list).
    """
    return []


def array_push(arr, value):
    """
    Push a value into array, return array so it can be chained.
    """
    arr.append(value)
    return arr


def array_get(arr, index):
    """
    Get value at index from array.
    """
    return arr[int(index)]


def array_set(arr, index, value):
    """
    Set value at index in array, extending with None if needed.
    """
    idx = int(index)
    if idx >= len(arr):
        arr.extend([None] * (idx + 1 - len(arr)))
    arr[idx] = value
    return arr


def array_size(arr):
    """
    Return current size of array.
    """
    return len(arr)


def array_pop(arr):
    """
    Pop last element; returns popped value or None if empty.
    """
    if not arr:
        return None
    return arr.pop()


def array_clear(arr):
    """
    Clear all elements from array.
    """
    arr.clear()
    return arr


# ------------------------------------------------------
# TA-Lib function map
# ------------------------------------------------------

TA_FUNCTIONS: Dict[str, Any] = {
    # Trend / moving averages / oscillators
    "adx": lambda h, l, c, t: talib.ADX(h.values, l.values, c.values, int(t)),
    "cci": lambda h, l, c, t: talib.CCI(h.values, l.values, c.values, int(t)),
    "stoch": lambda h, l, c, t: talib.STOCH(h.values, l.values, c.values, int(t)),
    "roc": lambda c, t=10: talib.ROC(c.values, int(t)),
    # Volume
    "obv": lambda c, v: talib.OBV(c.values, v.values),
    # Volatility
    "atr": lambda h, l, c, t: talib.ATR(h.values, l.values, c.values, int(t)),
    "natr": lambda h, l, c, t: talib.NATR(h.values, l.values, c.values, int(t)),
    # Candles
    "doji": lambda o, h, l, c: talib.CDLDOJI(
        o.values, h.values, l.values, c.values
    ),
    "hammer": lambda o, h, l, c: talib.CDLHAMMER(
        o.values, h.values, l.values, c.values
    ),
    "engulfing": lambda o, h, l, c: talib.CDLENGULFING(
        o.values, h.values, l.values, c.values
    ),
}

# Back-compat alias if interpreter expects `ta`
ta = TA_FUNCTIONS

# ------------------------------------------------------
# Math helpers (scalar-or-series aware)
# ------------------------------------------------------


def _scalar_or_series_unary(fn, x):
    if isinstance(x, pd.Series):
        return pd.Series(fn(x.values), index=x.index)
    return fn(x)


def math_abs(x):
    return _scalar_or_series_unary(np.abs, x)


def math_round(x, n=0):
    n = int(n)
    if isinstance(x, pd.Series):
        return x.round(n)
    return round(x, n)


def math_floor(x):
    return _scalar_or_series_unary(np.floor, x)


def math_ceil(x):
    return _scalar_or_series_unary(np.ceil, x)


def math_sqrt(x):
    return _scalar_or_series_unary(np.sqrt, x)


def math_log(x, base=np.e):
    if isinstance(x, pd.Series):
        vals = np.log(x.values)
        if base != np.e:
            vals = vals / np.log(base)
        return pd.Series(vals, index=x.index)
    v = np.log(x)
    if base != np.e:
        v = v / np.log(base)
    return v


def math_exp(x):
    return _scalar_or_series_unary(np.exp, x)


def math_max(a, b):
    if isinstance(a, pd.Series) or isinstance(b, pd.Series):
        as_ = pd.Series(a)
        bs_ = pd.Series(b)
        return pd.concat([as_, bs_], axis=1).max(axis=1)
    return max(a, b)


def math_min(a, b):
    if isinstance(a, pd.Series) or isinstance(b, pd.Series):
        as_ = pd.Series(a)
        bs_ = pd.Series(b)
        return pd.concat([as_, bs_], axis=1).min(axis=1)
    return min(a, b)


# ------------------------------------------------------
# Risk / regime / stats helpers
# ------------------------------------------------------


def atr_stop(price, atr_series, mult=2.0, direction="long"):
    """
    Simple ATR-based stop.

    direction: 'long' -> price - mult*atr, 'short' -> price + mult*atr.
    """
    mult = float(mult)
    direction = str(direction).lower()
    price = pd.Series(price)
    atr_series = pd.Series(atr_series)
    if direction == "long":
        stop = price - mult * atr_series
    elif direction == "short":
        stop = price + mult * atr_series
    else:
        raise ValueError("atr_stop: direction must be 'long' or 'short'.")
    return stop


def risk_percent_equity(equity, risk_pct, stop_distance):
    """
    Position size = equity * (risk_pct/100) / stop_distance.

    equity: float or Series (account equity per bar).
    stop_distance: Series of (entry - stop) in price units.
    """
    risk_pct = float(risk_pct)
    eq = pd.Series(equity) if not isinstance(equity, pd.Series) else equity
    dist = pd.Series(stop_distance)
    risk_frac = risk_pct / 100.0
    risk_amount = eq * risk_frac
    size = risk_amount / dist.replace(0, np.nan)
    return size.fillna(0.0)
def trend_strength(price, lookback=100):
    """
    Returns a 0-1 trend strength measure based on normalized slope of EMA.
    0 ~ flat, 1 ~ strong trend.
    """
    lookback = int(lookback)
    p = pd.Series(price)
    ema_fast = p.ewm(span=max(2, lookback // 5), adjust=False).mean()
    ema_slow = p.ewm(span=lookback, adjust=False).mean()
    spread = ema_fast - ema_slow
    vol = p.rolling(lookback).std()
    strength = (spread.abs() / (vol + 1e-9)).clip(0, 10)
    return (strength / 10.0).fillna(0.0)


def vol_regime(vol_series, lookback=50):
    """
    Classifies volatility into regimes: 0=low, 1=medium, 2=high.

    Based on rolling percentile of ATR or any vol measure.
    """
    lookback = int(lookback)
    v = pd.Series(vol_series).abs()
    roll = v.rolling(lookback)
    qlow = roll.quantile(0.33)
    qhigh = roll.quantile(0.66)
    regime = pd.Series(0, index=v.index, dtype="int64")
    regime = regime.where(v <= qlow, 1)
    regime = regime.where(v <= qhigh, 2)
    return regime.fillna(0)


# ------------------------------------------------------
# Statistical helpers
# ------------------------------------------------------


def zscore(series, length=50):
    """
    Rolling z-score: (x - mean) / std over window.
    """
    length = int(length)
    s = pd.Series(series)
    mean = s.rolling(length).mean()
    std = s.rolling(length).std()
    z = (s - mean) / (std + 1e-9)
    return z


def rolling_corr(x, y, length=50):
    """
    Rolling correlation between two series.
    """
    length = int(length)
    xs = pd.Series(x)
    ys = pd.Series(y)
    return xs.rolling(length).corr(ys)


def rolling_beta(y, x, length=50):
    """
    Rolling beta of y relative to x: cov / var.
    """
    length = int(length)
    ys = pd.Series(y)
    xs = pd.Series(x)
    cov = ys.rolling(length).cov(xs)
    var = xs.rolling(length).var()
    beta = cov / (var + 1e-9)
    return beta


# ------------------------------------------------------
# Normalization helpers
# ------------------------------------------------------


def normalize(series, length=100):
    """
    Normalize to 0-1 over rolling window: (x - min) / (max - min).
    """
    length = int(length)
    s = pd.Series(series)
    roll_min = s.rolling(length).min()
    roll_max = s.rolling(length).max()
    norm = (s - roll_min) / (roll_max - roll_min + 1e-9)
    return norm.clip(0.0, 1.0)


def standardize(series, length=100):
    """
    Standardize to mean 0, std 1 over rolling window.
    """
    length = int(length)
    s = pd.Series(series)
    mean = s.rolling(length).mean()
    std = s.rolling(length).std()
    return (s - mean) / (std + 1e-9)


# ------------------------------------------------------
# Cross-sectional / factor helpers (Batch A)
# ------------------------------------------------------


def rank(series, ascending=True):
    """
    Time-series rank normalized to [0, 1].

    ascending=True -> lowest value gets rank 0, highest 1.
    """
    s = pd.Series(series)
    order = s.rank(method="average", ascending=ascending, na_option="keep")
    denom = order.max()
    if denom == 0 or np.isnan(denom):
        return s * np.nan
    return (order - 1) / (denom - 1 + 1e-9)


def winsorize(series, z=3.0):
    """
    Winsorize a Series by clipping to mean ± z * std.
    """
    s = pd.Series(series)
    mu = s.mean()
    sigma = s.std()
    if sigma == 0 or np.isnan(sigma):
        return s
    lower = mu - float(z) * sigma
    upper = mu + float(z) * sigma
    return s.clip(lower, upper)


def cs_zscore(series):
    """
    Global z-score over time: (x - mean) / std.
    """
    s = pd.Series(series)
    mu = s.mean()
    sigma = s.std()
    return (s - mu) / (sigma + 1e-9)


def decile(series, n=10):
    """
    Assign decile (0..n-1) based on global distribution of the Series.
    """
    s = pd.Series(series)
    n = int(n)
    if n <= 1:
        return pd.Series(0, index=s.index)
    r = rank(s, ascending=True)
    r_clamped = r.clip(0.0, 1.0 - 1e-9)
    buckets = (r_clamped * n).astype("int64")
    return buckets


# ------------------------------------------------------
# Execution / cost helpers (Batch B)
# ------------------------------------------------------


def slippage_model(spread, vol, notional, k=1.0):
    """
    Simple slippage model in price terms.

    slippage ≈ k * spread + k * (vol * notional_scale)
    """
    spread_s = pd.Series(spread)
    vol_s = pd.Series(vol)
    notional_s = pd.Series(notional, index=spread_s.index)
    k = float(k)

    med_notional = notional_s.median()
    if med_notional == 0 or np.isnan(med_notional):
        notional_scale = 1.0
    else:
        notional_scale = notional_s / med_notional

    slip = k * spread_s + k * vol_s * notional_scale
    return slip.fillna(0.0)


def impact_cost(volume, adv, k=1.5):
    """
    Simple market impact cost model in % of price.

    impact_pct ≈ k * (volume / adv) ** 0.5
    """
    vol_s = pd.Series(volume)
    adv_s = pd.Series(adv).replace(0, np.nan)
    k = float(k)
    participation = (vol_s / adv_s).clip(lower=0.0)
    impact = k * np.sqrt(participation)
    return impact.fillna(0.0)


def total_trade_cost(price, slippage_price, impact_pct, commission_pct=0.0):
    """
    Combine slippage, market impact, and commission into total cost in price units.
    """
    p = pd.Series(price)
    slip = pd.Series(slippage_price, index=p.index)
    impact = pd.Series(impact_pct, index=p.index) / 100.0
    comm = float(commission_pct) / 100.0

    impact_cost_price = impact * p
    commission_price = comm * p
    total = slip + impact_cost_price + commission_price
    return total.fillna(0.0)


# ------------------------------------------------------
# Portfolio / allocation helpers (Batch C)
# ------------------------------------------------------


def vol_target_weight(returns, target_vol=0.1, lookback=50, min_weight=0.0, max_weight=10.0):
    """
    Volatility targeting for a single return series.

    weight_t ≈ target_vol / realized_vol_t
    """
    r = pd.Series(returns)
    lookback = int(lookback)
    rv = r.rolling(lookback).std()
    w = float(target_vol) / (rv + 1e-9)
    w = w.clip(lower=float(min_weight), upper=float(max_weight))
    return w.fillna(0.0)


def risk_parity_weights(returns_df: pd.DataFrame, lookback=50, min_weight=0.0):
    """
    Approximate risk parity weights from a DataFrame of return series.
    """
    if returns_df is None or len(getattr(returns_df, "columns", [])) == 0:
        return pd.DataFrame(index=pd.Index([]), columns=[])

    df = pd.DataFrame(returns_df)
    lookback = int(lookback)
    vol = df.rolling(lookback).std()
    inv_vol = 1.0 / (vol + 1e-9)
    inv_vol = inv_vol.clip(lower=0.0)
    inv_vol = inv_vol.where(inv_vol >= float(min_weight), float(min_weight))

    weight_sum = inv_vol.sum(axis=1).replace(0, np.nan)
    weights = inv_vol.div(weight_sum, axis=0)
    return weights.fillna(0.0)


def equal_weight(n_assets, min_weight=0.0):
    """
    Equal weight per asset for a given number of assets.
    """
    n = int(n_assets)
    if n <= 0:
        return 0.0
    w = 1.0 / n
    if w < float(min_weight):
        w = float(min_weight)
    return w
# ------------------------------------------------------
# Multi-asset utilities
# ------------------------------------------------------


def pair_ratio(sym1_close, sym2_close):
    """
    Simple price ratio between two assets. Both should be Series aligned to same index.
    """
    s1 = pd.Series(sym1_close)
    s2 = pd.Series(sym2_close)
    return s1 / s2.replace(0, np.nan)


def basket_close(close_series_list: List[pd.Series]):
    """
    Average close of a basket of assets.

    close_series_list: list of Series with aligned index.
    """
    if not close_series_list:
        return pd.Series(dtype="float64")
    cols = [pd.Series(s) for s in close_series_list]
    df = pd.concat(cols, axis=1)
    return df.mean(axis=1)


# ------------------------------------------------------
# Base environment for Kafal execution
# ------------------------------------------------------


def base_env(df: pd.DataFrame) -> dict:
    """
    Create the base environment for Kafal/FlowScript execution.

    Provides OHLCV series, TA functions, math helpers, arrays,
    advanced quant helpers, and placeholders for strategy/request.
    """
    bar_index = pd.Series(range(len(df)), index=df.index)
    time = pd.Series(df.index.astype("int64") // 10**9, index=df.index)
    env: Dict[str, Any] = {}

    # OHLCV
    env["open"] = df["open"]
    env["high"] = df["high"]
    env["low"] = df["low"]
    env["close"] = df["close"]
    env["volume"] = df["volume"]

    # Core indicators
    env["sma"] = sma
    env["ema"] = ema
    env["rsi"] = rsi
    env["macd"] = macd
    env["bbands"] = bbands

    # Series helpers
    env["nz"] = nz
    env["crossover"] = crossover
    env["crossunder"] = crossunder
    env["change"] = change
    env["percent_change"] = percent_change

    # Price composites / rolling helpers
    env["hl2"] = hl2
    env["hlc3"] = hlc3
    env["ohlc4"] = ohlc4
    env["typical_price"] = typical_price
    env["highest"] = highest
    env["lowest"] = lowest
    env["sum_n"] = sum_n
    env["stdev"] = stdev

    # Arrays / buffers
    env["array"] = array
    env["array_push"] = array_push
    env["array_get"] = array_get
    env["array_set"] = array_set
    env["array_size"] = array_size
    env["array_pop"] = array_pop
    env["array_clear"] = array_clear

    # TA namespace
    env["ta"] = TA_FUNCTIONS

    # Math helpers at DSL level
    env["abs"] = math_abs
    env["round"] = math_round
    env["floor"] = math_floor
    env["ceil"] = math_ceil
    env["sqrt"] = math_sqrt
    env["log"] = math_log
    env["exp"] = math_exp
    env["max"] = math_max
    env["min"] = math_min

    # Advanced quant helpers
    env["atr_stop"] = atr_stop
    env["risk_percent_equity"] = risk_percent_equity
    env["trend_strength"] = trend_strength
    env["vol_regime"] = vol_regime
    env["zscore"] = zscore
    env["rolling_corr"] = rolling_corr
    env["rolling_beta"] = rolling_beta
    env["normalize"] = normalize
    env["standardize"] = standardize
    env["pair_ratio"] = pair_ratio
    env["basket_close"] = basket_close
    # Batch A
    env["rank"] = rank
    env["winsorize"] = winsorize
    env["cs_zscore"] = cs_zscore
    env["decile"] = decile
    # Batch B
    env["slippage_model"] = slippage_model
    env["impact_cost"] = impact_cost
    env["total_trade_cost"] = total_trade_cost
    # Batch C
    env["vol_target_weight"] = vol_target_weight
    env["risk_parity_weights"] = risk_parity_weights
    env["equal_weight"] = equal_weight

    # Color helpers / namespace
    env["rgba"] = rgba
    env["color"] = {
        "red": "red",
        "blue": "blue",
        "green": "green",
        "orange": "orange",
        "purple": "purple",
    }

    # Low-level namespaces / meta
    env["math"] = np
    env["np"] = np
    env["pd"] = pd
    env["bar_index"] = bar_index
    env["time"] = time

    # Strategy / request placeholders (wired by interpreter)
    env["strategy"] = {}
    env["request"] = {}

    # Constants
    env["na"] = np.nan
    env["true"] = True
    env["false"] = False

    return env


# Back-compat alias expected by interpreter.py
def baseenv(df: pd.DataFrame) -> dict:
    """
    Backward-compatible name for the base environment builder.
    """
    return base_env(df)
