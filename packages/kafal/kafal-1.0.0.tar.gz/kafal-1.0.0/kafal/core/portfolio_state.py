from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd

# Prefer core implementation; fall back to full strategy_state for older layouts.
try:
    from .strategy_state import StrategyState
except ImportError:  # back-compat if only strategy_state.py exists
    from .strategy_state import StrategyState


class PortfolioState:
    """
    Simple multi-symbol portfolio wrapper around StrategyState.

    - Tracks per-symbol StrategyState instances.
    - Uses a shared cash/equity account conceptually via each StrategyState's
      initial_equity. Current implementation keeps initial_equity per symbol;
      host can aggregate.
    - Provides mark(idx) and finalize() across all symbols.
    """

    def __init__(
        self,
        symbol_prices: Dict[str, pd.Series],
        ohlc_map: Dict[str, Dict[str, Optional[pd.Series]]],
        initial_equity: float = 100000.0,
        commission_perc: float = 0.0,
        slippage: float = 0.0,
        pyramiding: int = 1,
        execution_mode: str = "backtest",
        symbol_configs: Optional[Dict[str, Dict[str, Any]]] = None,
        intrabar_model: str = "none",
        intrabar_steps: int = 0,
    ):
        self.symbol_states: Dict[str, StrategyState] = {}

        self.initial_equity = float(initial_equity)
        self.commission_perc = float(commission_perc)
        self.slippage = float(slippage)
        self.pyramiding = int(pyramiding)

        if execution_mode not in ("backtest", "realistic"):
            raise ValueError("execution_mode must be 'backtest' or 'realistic'")
        self.execution_mode = execution_mode

        self.symbol_configs: Dict[str, Dict[str, Any]] = dict(symbol_configs or {})
        self.intrabar_model = (
            intrabar_model if intrabar_model in ("none", "random_walk") else "none"
        )
        self.intrabar_steps = max(0, int(intrabar_steps))

        # create per-symbol StrategyState
        for symbol, prices in symbol_prices.items():
            ohlc = ohlc_map.get(symbol) or {}
            open_ = ohlc.get("open")
            high = ohlc.get("high")
            low = ohlc.get("low")
            close = ohlc.get("close")
            if close is None:
                close = prices

            sym_cfg = self.symbol_configs.get(symbol, {})
            self.symbol_states[symbol] = StrategyState(
                prices=close,
                initial_equity=self.initial_equity,
                commission_perc=self.commission_perc,
                slippage=self.slippage,
                pyramiding=self.pyramiding,
                open=open_,
                high=high,
                low=low,
                close=close,
                symbol=symbol,
                execution_mode=self.execution_mode,
                symbol_config=sym_cfg,
                intrabar_model=self.intrabar_model,
                intrabar_steps=self.intrabar_steps,
            )

    def _get_state(self, symbol: str) -> StrategyState:
        """
        Internal helper used by SafeEvaluator's PortfolioAPI.
        """
        if symbol not in self.symbol_states:
            raise KeyError(f"Unknown symbol in portfolio: {symbol}")
        return self.symbol_states[symbol]

    # Public alias used by tests / external callers.
    def get_state(self, symbol: str) -> StrategyState:
        return self._get_state(symbol)

    def mark(self, idx: int):
        """
        Mark all symbols on bar idx. The host should ensure idx is in-range
        for each symbol's price series.
        """
        idx = int(idx)
        for st in self.symbol_states.values():
            if idx < len(st.prices):
                st.mark(idx)

    def finalize(self) -> Dict[str, Any]:
        """
        Finalize all symbol strategies and aggregate basic portfolio stats.
        """
        results: Dict[str, Any] = {}
        equity_curves: List[pd.Series] = []
        pnl_curves: List[pd.Series] = []

        for symbol, st in self.symbol_states.items():
            res = st.finalize()
            results[symbol] = res
            equity_curves.append(res["equity"])
            pnl_curves.append(res["pnl"])

        if equity_curves:
            base_index = equity_curves[0].index
            equity_sum = sum(e.reindex(base_index).ffill() for e in equity_curves)
            pnl_sum = sum(p.reindex(base_index).fillna(0.0) for p in pnl_curves)
        else:
            equity_sum = pd.Series(dtype=float)
            pnl_sum = pd.Series(dtype=float)

        # Use a dummy StrategyState instance to reuse _compute_stats logic
        dummy = StrategyState(
            prices=equity_sum if len(equity_sum) else pd.Series(dtype=float)
        )
        stats = dummy._compute_stats(equity_sum, pnl_sum, equity_sum * 0.0)

        return {
            "symbols": results,
            "portfolio_equity": equity_sum,
            "portfolio_pnl": pnl_sum,
            "stats": stats,
        }
