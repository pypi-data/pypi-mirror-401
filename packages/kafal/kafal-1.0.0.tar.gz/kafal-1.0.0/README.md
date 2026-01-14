# kafal

**kafal** is a compact scripting layer for building trading indicators, strategies, and research factors on top of pandas OHLCV data.  
It sits between raw Python and chart / execution UIs:

- **DSL** for signals, risk, and execution.
- **TA + quant primitives** (TA‑Lib wrappers, rolling stats, z‑scores, etc.) wired straight into your script.
- A configurable **strategy engine** with realistic fills, intrabar simulation, and portfolio aggregation.

**Write strategy logic fast, run it anywhere Python runs.**

> Status: **alpha / experimental** – API is stabilising; small breaking changes may still happen before 1.0.

---

## 60‑second Quickstart

Install:

```bash
pip install kafal
```

### 1. Indicator + crossover strategy in one script

```python
import pandas as pd
from kafal.core.interpreter import KafalInterpreter
```

Create a toy OHLCV DataFrame:

```python
dates = pd.date_range("2025-01-01", periods=200, freq="1H")
close = pd.Series(100 + 0.1 * range(200), index=dates)

df = pd.DataFrame(
    {
        "open": close.shift(1).fillna(close.iloc),
        "high": close + 1.0,
        "low": close - 1.0,
        "close": close,
        "volume": 1_000,
    },
    index=dates,
)
```

Kafal script (as a string):

```python
code = """
// Simple EMA crossover strategy

len_fast = 10
len_slow = 30

fast = ema(close, len_fast)
slow = ema(close, len_slow)

plot(close) - title="Close"
plot(fast)  - title="Fast EMA"  color=rgba(0,255,0,0.9)
plot(slow)  - title="Slow EMA"  color=rgba(255,0,0,0.9)

long_cond  = crossover(fast, slow)
short_cond = crossunder(fast, slow)

// Modern trading API (preferred)
trade.long(long_cond,  size=1.0)
trade.short(short_cond, size=1.0)
"""
```

Run it:

```python
intr = KafalInterpreter()
result = intr.run(code, df, mode="strategy")

plots    = result["plots"]
strategy = result["strategy"]
equity   = strategy["equity"]
trades   = strategy["trades"]
stats    = strategy["stats"]
```

- Feed `plots` into your chart layer.  
- Use `equity` / `trades` / `stats` for a basic backtest view.

### 2. Strategy with inputs and the modern `trade.*` API

```python
indicator_code = """
define name="EMA Cross (Inputs)" overlay=true category="trend"

input fast_len:int 10  min=2  max=50  step=1  title="Fast EMA"
input slow_len:int 30  min=5  max=200 step=1  title="Slow EMA"

fast = ema(close, fast_len)
slow = ema(close, slow_len)

plot(fast) - color=rgba(0,255,0,0.9) title="Fast"
plot(slow) - color=rgba(255,0,0,0.9) title="Slow"

long_cond  = crossover(fast, slow)
short_cond = crossunder(fast, slow)

trade.long(long_cond,  size=1.0)
trade.short(short_cond, size=1.0)
"""
```

```python
intr = KafalInterpreter()
intr.set_inputs({"fast_len": 12, "slow_len": 34})

result = intr.run(indicator_code, df, mode="strategy")

strategy      = result["strategy"]
stats         = strategy["stats"]
inputs_schema = result["inputs_schema"]
```

- `inputs_schema` tells your UI which sliders / controls to render.  
- `set_inputs` lets your app push UI values back into the script.

For more copy‑pasteable scripts, see:

- `docs/Quickstart.md`
- `docs/Indicator_cookbook.md`
- `docs/Strategy_cookbook.md`

---

## Public API surface (host‑facing)

### Core class

```python
from kafal.core.interpreter import KafalInterpreter
```

Typical construction:

```python
intr = KafalInterpreter(
    host_api=None,           # dict of data callbacks (see Host API)
    max_request_calls=50,    # safety cap for cross-symbol requests
    initial_equity=100_000.0,
    commission_perc=0.0,
    slippage=0.0,
    pyramiding=1,
    execution_mode="backtest",   # "backtest" | "realistic"
    symbol_configs=None,         # per-symbol dealing config
    intrabar_model="none",       # "none" | "random_walk"
    intrabar_steps=0,            # synthetic ticks per bar if intrabar_model != "none"
)
```

### Modes

```python
result = intr.run(code, df, mode="chart")     # visuals + optional strategy
result = intr.run(code, df, mode="strategy")  # same payload, host treats as strategy
result = intr.run(code, df, mode="research")  # focus on features; visuals optional
```

---

## Host API (data access)

All external data is explicit and host‑controlled, via a small host API.

- `request_security(symbol, timeframe, field_or_expr, gaps="off" | "ffill" | "on")`  
- `host_api["request_security"]` / `"requestsecurity"` → v1 per‑field API (returns `Series`).  
- `host_api["request_ohlcv"]` / `"requestohlcv"` → v2 OHLCV API (returns `DataFrame`).

Scripts never open files, hit the network, or touch OS APIs.

Minimal example:

```python
import pandas as pd
from kafal.core.host_api import HostAPI
from kafal.core.interpreter import KafalInterpreter

def request_ohlcv(symbol: str, timeframe: str) -> pd.DataFrame:
    # You decide where data comes from (DB, gateway, CSV, etc.)
    df = load_ohlcv_from_somewhere(symbol, timeframe)
    # Must be a DataFrame with at least: open, high, low, close, volume
    return df

host_api = {"request_ohlcv": request_ohlcv}
intr = KafalInterpreter(host_api=host_api)

result = intr.run(code, df, mode="chart")
```

Inside the script:

```flowscript
// Uses host_api["request_ohlcv"] under the hood
other_close = request_security("NIFTY", "1D", "close")
spread      = close - other_close
plot(spread) - title="Spread vs NIFTY"
```

---

## Sandbox & safety model

Kafal scripts are **untrusted** by default. The interpreter enforces:

- No filesystem, network, or OS access.  
- `__builtins__` cleared during eval.  
- AST validator that blocks attribute access, imports, lambdas, comprehensions, etc.  
- Loop bounds capped by `MAX_FOR_RANGE`.  
- `request_*` calls limited via `max_request_calls`.  

Host‑side, you only expose controlled callbacks via `host_api`; everything else is locked down by the sandbox.

---

## What `run()` returns

`result = intr.run(code, df, ...)` yields a dict with these main fields:

- **Visual layer**
  - `result["plots"]`
  - `result["shapes"]`
  - `result["hlines"]`
  - `result["bgcolors"]`
  - `result["fills"]`
  - `result["tables"]`
  - `result["alerts"]`

- **Strategy payload**

  ```python
  strat    = result["strategy"]
  equity   = strat["equity"]    # Series
  pnl      = strat["pnl"]       # Series
  position = strat["position"]  # Series
  trades   = strat["trades"]    # List[dict]
  stats    = strat["stats"]     # Dict[str, Any]
  ```

- **Meta / research**
  - `result["inputs_schema"]` – description of `input.*` fields.  
  - `result["meta"]` – user metadata from `define` lines.  
  - `result["features"]` – named research features (in research mode).  
  - `result["mode"]` – echo of the mode you passed.

These keys are stable for the 0.1 line; new keys may be added in future versions.

---

## DSL snapshot (what you can write)

### Series and TA

```flowscript
mid    = hl2(high, low)
trend  = ema(close, 50)
vol_z  = zscore(volume, 50)

plot(mid)   - color=rgba(255,255,0,0.9) title="HL2"
plot(trend) - color=rgba(0,200,255,0.9) title="EMA 50"
plot(vol_z) - color=rgba(255,165,0,0.9) title="Vol zscore"
```

### Control flow and arrays

```flowscript
sumval = 0
for i in 0..10 {
    if i > 5 {
        sumval = sumval + 1
    }
}

arr = array()
for i in 0..5 {
    array_push(arr, i)
}

plot(sumval) - title="Counter"
```

### Functions and pipes

```flowscript
fn atr_band(src, len, mult) = src + atr(len) * mult

upper   = atr_band(close, 14,  2.0)
lower   = atr_band(close, 14, -2.0)
signal  = close | rsi(14) | sma(9)

plot(upper)  - title="ATR Upper"
plot(lower)  - title="ATR Lower"
plot(signal) - title="RSI SMA"
```

For a deeper walkthrough, see `docs/Quickstart.md` plus the indicator & strategy cookbooks.

---

## Examples in this repo

You already have runnable examples wired to the interpreter and portfolio engine:

- `examples/run_research_example.py` – single‑symbol research mode.  
- `examples/run_universe_research.py` – multi‑symbol research / factor panel.  
- `examples/run_strategy_example.py` – single‑symbol strategy backtest.  

Run them:

```bash
python examples/run_strategy_example.py
python examples/run_research_example.py
python examples/run_universe_research.py
```

These act as “host skeletons” you can copy into your own app.

---

## Embedding Kafal in your app

1. **Install & import**

   ```bash
   pip install kafal
   ```

   ```python
   from kafal.core.interpreter import KafalInterpreter
   ```

2. **Provide data**

   - Build a pandas `DataFrame` with `open`, `high`, `low`, `close`, `volume`.  
   - Optionally implement `request_ohlcv` / `request_security` to support multi‑symbol or multi‑timeframe scripts.

3. **Expose scripting**

   - Let users upload `.kf` files or edit scripts in a text area.  
   - Read into `code: str`, then call `intr.run(code, df, host_api=..., mode=...)`.

4. **Render outputs**

   - Map `plots`, `fills`, `shapes`, `hlines`, `bgcolors`, `tables` to your chart library.  
   - Use `result["strategy"]["equity"]`, `["pnl"]`, `["trades"]`, `["stats"]` for backtest panels.  
   - Use `result["features"]` for factor research and ranking dashboards.

5. **Lock in behaviour with tests**

   - Mirror patterns from `kafal/tests/test_kafal.py`:
     - host API error behaviour you depend on.  
     - `"backtest"` vs `"realistic"` execution.  
     - presence and types of keys in `run()` output.  
     - portfolio aggregation in `PortfolioState`.

     
Errors & troubleshooting
-------------------------

Kafal surfaces structured runtime errors to make debugging easier.

- All runtime errors are prefixed with `Kafal:` and carry a stable `KAFAL-*` code at the end.  
  - Example: `Kafal: execution_mode must be 'backtest' or 'realistic'. [KAFAL-EXEC-MODE]`  
  - Example: `Kafal: host_api['request_ohlcv'] must return a pandas DataFrame. [KAFAL-HOST-OHLCV-TYPE]`  

- Codes are **stable** and searchable:
  - `KAFAL-EXEC-*` – interpreter configuration issues (e.g. bad `execution_mode` or `run(mode=...)`).  
  - `KAFAL-EXPR-*` – DSL expression / sandbox issues (e.g. blocked `.attr`, lambdas, invalid operators).  
  - `KAFAL-HOST-*` – host integration issues (e.g. missing or wrong‑type `request_security` / `request_ohlcv`).  

If you see a Kafal error:

- Read the human message; it always includes **what went wrong** and usually **how to fix**.  
- Use the `KAFAL-*` code in your logs, tests, or docs search to find the relevant contract or section.
