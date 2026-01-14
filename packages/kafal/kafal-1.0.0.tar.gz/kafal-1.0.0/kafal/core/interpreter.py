from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import math
from itertools import product

import pandas as pd

from .builtins import base_env
from .portfolio_state import PortfolioState
from .strategy_state import StrategyState
from .host_api import HostAPIMixin
from .parser_viz import VizParserMixin
from .parser_blocks import BlocksMixin
from .safe_eval import SafeEvaluator
from .meta_inputs import parse_define_line, parse_input_line
from .pipe_expr import PipeExprMixin


def _errmsg(msg: str, code: str) -> str:
    # Standardised Kafal error prefix for easier log filtering.
    return f"Kafal: {msg} [{code}]"


class KafalInterpreter(HostAPIMixin, VizParserMixin, BlocksMixin, PipeExprMixin):
    """
    Core Kafal DSL interpreter.

    This class is intentionally thin and delegates to:
    - HostAPIMixin (host_api.py)
    - VizParserMixin (parser_viz.py)
    - BlocksMixin (parser_blocks.py)
    - PipeExprMixin (pipe_expr.py)
    - SafeEvaluator (safe_eval.py)
    - parse_input_line / parse_define_line (meta_inputs.py)
    """

    MAX_FOR_RANGE = 1000

    def __init__(
        self,
        host_api: Optional[Dict[str, Any]] = None,
        hostapi: Optional[Dict[str, Any]] = None,  # legacy alias (kept to avoid breaking older codepaths)
        max_request_calls: int = 50,
        initial_equity: float = 100000.0,
        commission_perc: float = 0.0,
        slippage: float = 0.0,
        pyramiding: int = 1,
        execution_mode: str = "backtest",  # backtest | realistic
        symbol_configs: Optional[Dict[str, Dict[str, Any]]] = None,
        intrabar_model: str = "none",  # none | random_walk
        intrabar_steps: int = 0,
    ):
        # Prefer explicit host_api; fall back to legacy name if provided.
        if host_api is None and hostapi is not None:
            host_api = hostapi

        self.host_api: Dict[str, Any] = dict(host_api or {})

        self.inputs: Dict[str, Any] = {}
        self.inputs_schema: Dict[str, Any] = {}
        self.user_functions: Dict[str, Tuple[List[str], str]] = {}

        self.max_request_calls = int(max_request_calls)

        self.meta: Dict[str, Any] = {}

        self.initial_equity = float(initial_equity)
        self.commission_perc = float(commission_perc)
        self.slippage = float(slippage)
        self.pyramiding = int(pyramiding)

        if execution_mode not in ("backtest", "realistic"):
            raise ValueError(
                _errmsg(
                    "execution_mode must be 'backtest' or 'realistic'.",
                    "KAFAL-EXEC-MODE",
                )
            )
        self.execution_mode = execution_mode

        self.symbol_configs: Dict[str, Dict[str, Any]] = dict(symbol_configs or {})

        intrabar_model = (intrabar_model or "none").lower()
        self.intrabar_model = intrabar_model if intrabar_model in ("none", "random_walk") else "none"
        self.intrabar_steps = max(0, int(intrabar_steps))

        # Safe evaluator instance (name `_safe` expected by PipeExprMixin / SafeEvaluator)
        self._safe = SafeEvaluator()

    def set_inputs(self, inputs: dict):
        """External override of inputs (e.g., UI values)."""
        self.inputs = inputs or {}

    def set_host_api(self, host_api: Optional[Dict[str, Any]]):
        """Replace host API injection."""
        self.host_api = dict(host_api or {})

    def optimize_grid(
        self,
        code: str,
        df: pd.DataFrame,
        grid: Dict[str, List[Any]],
        metric: str = "sharpe",
        host_api: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Run a simple grid search over input parameters from Python.
        Returns a list sorted by metric descending.
        """
        param_names = list(grid.keys())
        param_values = list(grid.values())

        results: List[Dict[str, Any]] = []
        for combo in product(*param_values):
            params = dict(zip(param_names, combo))
            self.set_inputs(params)
            out = self.run(code, df, host_api=host_api, mode="strategy")
            strat = out.get("strategy") or {}
            stats = strat.get("stats") or {}
            value = stats.get(metric, float("nan"))
            try:
                value = float(value)
            except Exception:
                value = float("nan")
            results.append({"params": params, "metric": value, "stats": stats, "raw": out})

        results.sort(key=lambda r: (math.isnan(r["metric"]), r["metric"]), reverse=True)
        return results

    def run(
        self,
        code: str,
        df: pd.DataFrame,
        host_api: Optional[Dict[str, Any]] = None,
        mode: str = "chart",  # chart | strategy | research
    ) -> Dict[str, Any]:
        """
        Execute a Kafal script.

        mode:
        - "chart": visuals + strategy payload (backwards-compatible default).
        - "strategy": same as chart; host can treat it as strategy-focused.
        - "research": focus on features; visuals/strategy can be ignored by host.
        """
        if mode not in ("chart", "strategy", "research"):
            raise ValueError(
                _errmsg(
                    "mode must be 'chart', 'strategy', or 'research'.",
                    "KAFAL-RUN-MODE",
                )
            )

        # Reset per-run metadata
        self.inputs_schema = {}
        self.meta = {}

        # Build base env
        env = base_env(df)

        # Attach portfolio/strategy state
        open_ = df["open"] if "open" in df.columns else None
        high = df["high"] if "high" in df.columns else None
        low = df["low"] if "low" in df.columns else None
        close = df["close"] if "close" in df.columns else None

        symbol_prices = {"chart": close}
        ohlc_map = {"chart": {"open": open_, "high": high, "low": low, "close": close}}

        portfolio_state = PortfolioState(
            symbol_prices=symbol_prices,
            ohlc_map=ohlc_map,
            initial_equity=self.initial_equity,
            commission_perc=self.commission_perc,
            slippage=self.slippage,
            pyramiding=self.pyramiding,
            execution_mode=self.execution_mode,
            symbol_configs=self.symbol_configs,
            intrabar_model=self.intrabar_model,
            intrabar_steps=self.intrabar_steps,
        )

        env["portfolio_state"] = portfolio_state
        env["strategy_state"] = portfolio_state.symbol_states["chart"]

        effective_host_api = self.host_api if host_api is None else dict(host_api)
        self.attach_host_api(env, df, effective_host_api)

        # Parse program
        lines = code.splitlines()
        executable_lines: List[str] = []
        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("fn "):
                self.register_function(line)
                continue

            if line.startswith("input ") or line.startswith("input\t") or line == "input":
                parse_input_line(line, inputs=self.inputs, inputs_schema=self.inputs_schema)
                continue

            if line.startswith("define ") or line.startswith("define\t") or line == "define":
                parse_define_line(line, meta=self.meta)
                continue

            executable_lines.append(raw_line)

        # Resolve inputs for script
        env["input"] = {}
        for name, schema in self.inputs_schema.items():
            if name in self.inputs:
                env["input"][name] = self.inputs[name]
            else:
                env["input"][name] = schema.get("default")

        # Feature registry (research mode)
        features: Dict[str, Any] = {}

        def feature(name: Any, value: Any):
            key = str(name)
            if isinstance(value, pd.Series):
                features[key] = value
                return
            try:
                s = pd.Series(value, index=df.index)
                features[key] = s
            except Exception:
                features[key] = value

        env["feature"] = feature
        env["run_mode"] = mode

        # Outputs
        plots: List[Dict[str, Any]] = []
        shapes: List[Dict[str, Any]] = []
        hlines: List[Dict[str, Any]] = []
        bgcolors: List[Dict[str, Any]] = []
        alerts: List[Dict[str, Any]] = []
        fills: List[Dict[str, Any]] = []
        tables: List[Dict[str, Any]] = []

        # Execute script (block engine supports nested if/for)
        self.execute_block_lines(
            executable_lines, env, plots, shapes, hlines, bgcolors, alerts, fills, tables
        )

        # Mark engine on every bar, then finalize
        strategy_result = None
        if isinstance(env.get("portfolio_state"), PortfolioState):
            pf = env["portfolio_state"]
            for bar_i in range(len(df)):
                pf.mark(bar_i)
            strategy_result = pf.finalize()
        elif isinstance(env.get("strategy_state"), StrategyState):
            st = env["strategy_state"]
            for bar_i in range(len(df)):
                st.mark(bar_i)
            strategy_result = st.finalize()

        return {
            "plots": plots,
            "shapes": shapes,
            "hlines": hlines,
            "bgcolors": bgcolors,
            "alerts": alerts,
            "fills": fills,
            "tables": tables,
            "strategy": strategy_result,
            "meta": dict(self.meta),
            "inputs_schema": dict(self.inputs_schema),
            "features": features,
            "mode": mode,
        }

    def register_function(self, line: str) -> None:
        body = line[3:].strip()  # remove leading "fn "
        name_params, expr = body.split("=", 1)
        name_params = name_params.strip()
        expr = expr.strip()

        import re as _re

        m = _re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\((.*)\)$", name_params)
        if not m:
            raise ValueError(
                _errmsg(
                    "Invalid function definition line. Expected: fn name(arg1, arg2) = expr.",
                    "KAFAL-USERFN-SYNTAX",
                )
            )

        name = m.group(1)
        params_str = m.group(2).strip()
        params = [p.strip() for p in params_str.split(",") if p.strip()] if params_str else []
        self.user_functions[name] = (params, expr)

    # ------------------------------------------------------
    # Expression evaluation (SafeEvaluator + pipes)
    # ------------------------------------------------------
    def eval_expr(self, expr: str, env: dict) -> Any:
        """
        Public expression entry used by:
        - BlocksMixin
        - VizParserMixin
        - HostAPIMixin for secondary symbol expressions
        - SafeEvaluator user functions
        """
        return self.eval_pipe_or_safe(expr, env)

    def build_eval_env(self, env: dict) -> dict:
        """
        Helper to get the full eval env including trade/portfolio APIs from a base env.
        Used by tests/host integration.
        """
        return self._safe.build_eval_env(
            env,
            eval_flow_expr=self.eval_flow_expr,
            user_functions=self.user_functions,
        )

    # Back-compat names used by older mixins (parser_viz / parser_blocks / SafeEvaluator)
    def eval_flow_expr(self, expr: str, env: dict) -> Any:
        """
        Legacy entrypoint name kept for compatibility with existing mixins.
        Delegates to eval_pipe_or_safe.
        """
        return self.eval_pipe_or_safe(expr, env)

    def _build_eval_env(self, env: dict) -> dict:
        """
        Legacy helper name used in older codepaths; delegates to build_eval_env
        but passes the same hook.
        """
        return self._safe.build_eval_env(
            env,
            eval_flow_expr=self.eval_flow_expr,
            user_functions=self.user_functions,
        )


# Backward compatibility alias for older imports
FlowScriptInterpreter = KafalInterpreter
