from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

import ast
import re

import numpy as np
import pandas as pd

from .portfolio_state import PortfolioState
from .strategy_state import StrategyState


# Safety limits (keep aligned with interpreter defaults)
MAX_EXPR_LEN = 10_000
MAX_AST_NODES = 2_000
MAX_EXPR_CACHE = 512


class UnsafeExpressionError(ValueError):
    pass


def _err(msg: str, code: str) -> str:
    # Standardised Kafal error prefix for easier log filtering.
    return f"Kafal: {msg} [{code}]"


class SafeAstValidator(ast.NodeVisitor):
    _ALLOWED_BINOPS = (
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
    )
    _ALLOWED_UNARYOPS = (ast.UAdd, ast.USub, ast.Not)
    _ALLOWED_BOOLOPS = (ast.And, ast.Or)
    _ALLOWED_CMPOPS = (
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
    )

    def __init__(self, allowed_call_names: set[str]):
        self._allowed_call_names = allowed_call_names

    def validate(self, tree: ast.AST) -> None:
        node_count = sum(1 for _ in ast.walk(tree))
        if node_count > MAX_AST_NODES:
            raise UnsafeExpressionError(
                _err(
                    f"Expression is too complex (>{MAX_AST_NODES} AST nodes). "
                    "Split it into smaller steps.",
                    "KAFAL-EXPR-COMPLEXITY",
                )
            )
        self.visit(tree)

    def visit(self, node: ast.AST) -> Any:
        if isinstance(node, ast.Attribute):
            raise UnsafeExpressionError(
                _err(
                    'Attribute access is not allowed in expressions (".attr" is blocked). '
                    "Use built-in helpers or intermediate assignments instead.",
                    "KAFAL-EXPR-ATTR",
                )
            )
        if isinstance(node, ast.Subscript):
            raise UnsafeExpressionError(
                _err(
                    "Indexing is restricted in expressions. "
                    'Use history(series, n) or array_get(...) instead of "x[...]".',
                    "KAFAL-EXPR-INDEX",
                )
            )
        if isinstance(
            node, (ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
        ):
            raise UnsafeExpressionError(
                _err(
                    "Inline lambdas and comprehensions are not supported in Kafal scripts. "
                    "Move this logic into precomputed Series in your host.",
                    "KAFAL-EXPR-LAMBDA",
                )
            )
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise UnsafeExpressionError(
                _err(
                    "Imports are not allowed inside Kafal expressions. "
                    "Provide data or helpers via the host API instead.",
                    "KAFAL-EXPR-IMPORT",
                )
            )
        return super().visit(node)

    def visit_Expression(self, node: ast.Expression) -> Any:
        return self.visit(node.body)

    def visit_Name(self, node: ast.Name) -> Any:
        if "__" in node.id or node.id.startswith("_"):
            raise UnsafeExpressionError(
                _err(
                    f"Name '{node.id}' is reserved and cannot be used in scripts.",
                    "KAFAL-EXPR-NAME",
                )
            )
        return None

    def visit_Constant(self, node: ast.Constant) -> Any:
        return None

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        if not isinstance(node.op, self._ALLOWED_BINOPS):
            raise UnsafeExpressionError(
                _err(
                    f"Binary operator '{type(node.op).__name__}' is not allowed in expressions.",
                    "KAFAL-EXPR-BINOP",
                )
            )
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        if not isinstance(node.op, self._ALLOWED_UNARYOPS):
            raise UnsafeExpressionError(
                _err(
                    f"Unary operator '{type(node.op).__name__}' is not allowed in expressions.",
                    "KAFAL-EXPR-UNARYOP",
                )
            )
        self.visit(node.operand)

    def visit_BoolOp(self, node: ast.BoolOp) -> Any:
        if not isinstance(node.op, self._ALLOWED_BOOLOPS):
            raise UnsafeExpressionError(
                _err(
                    f"Boolean operator '{type(node.op).__name__}' is not allowed in expressions.",
                    "KAFAL-EXPR-BOOLOP",
                )
            )
        for v in node.values:
            self.visit(v)

    def visit_Compare(self, node: ast.Compare) -> Any:
        for op in node.ops:
            if not isinstance(op, self._ALLOWED_CMPOPS):
                raise UnsafeExpressionError(
                    _err(
                        f"Comparison operator '{type(op).__name__}' is not allowed in expressions.",
                        "KAFAL-EXPR-CMPOP",
                    )
                )
        self.visit(node.left)
        for c in node.comparators:
            self.visit(c)

    def visit_Call(self, node: ast.Call) -> Any:
        if node.keywords:
            # Keep old behavior: DSL expressions cannot use kw-args.
            raise UnsafeExpressionError(
                _err(
                    "Keyword arguments are not allowed in DSL expressions. "
                    "Call functions with positional arguments only.",
                    "KAFAL-EXPR-KWARGS",
                )
            )
        if not isinstance(node.func, ast.Name):
            raise UnsafeExpressionError(
                _err(
                    "Only simple function calls are allowed in expressions "
                    "(no attribute or method calls like obj.fn()).",
                    "KAFAL-EXPR-CALL-SHAPE",
                )
            )
        fn = node.func.id
        if fn not in self._allowed_call_names:
            raise UnsafeExpressionError(
                _err(
                    f"Call to unknown function '{fn}'. "
                    "Check the name or expose it via the Kafal environment.",
                    "KAFAL-EXPR-FUNC-NOT-FOUND",
                )
            )
        for a in node.args:
            self.visit(a)


class SafeEvaluator:
    """
    Safe expression evaluator used by the interpreter.

    - Rewrites:
      - history syntax: x[1] -> history(x, 1)
      - if/then/else: if c then a else b -> (c) ? (a) : (b) -> where(c, a, b)
      - ternary: c ? a : b -> where(c, a, b)
    - Validates AST
    - Evaluates with __builtins__={}
    """

    def __init__(
        self,
        *,
        max_expr_len: int = MAX_EXPR_LEN,
        max_expr_cache: int = MAX_EXPR_CACHE,
    ):
        self._max_expr_len = int(max_expr_len)
        self._max_expr_cache = int(max_expr_cache)
        self._expr_cache: Dict[str, Any] = {}

    def eval(
        self,
        expr: str,
        env: dict,
        *,
        eval_flow_expr: Optional[Callable[[str, dict], Any]] = None,
        user_functions: Optional[Dict[str, Tuple[List[str], str]]] = None,
    ):
        if not isinstance(expr, str):
            raise ValueError(
                _err(
                    "Expression must be provided as a string.",
                    "KAFAL-EXPR-TYPE",
                )
            )

        expr = expr.strip()
        if len(expr) > self._max_expr_len:
            raise ValueError(
                _err(
                    f"Expression is too long (>{self._max_expr_len} characters). "
                    "Break it into smaller expressions.",
                    "KAFAL-EXPR-LENGTH",
                )
            )

        try:
            expr = self.rewrite_if_then_else(expr)
            expr = self.rewrite_ternary(expr)
            expr = self.rewrite_history(expr)

            local_env = self.build_eval_env(
                env,
                eval_flow_expr=eval_flow_expr,
                user_functions=user_functions,
            )
            code_obj = self.compile_safe_expr(expr, local_env)
            return eval(code_obj, {"__builtins__": {}}, local_env)
        except UnsafeExpressionError:
            # Re-raise Kafal-specific safety errors as-is.
            raise
        except Exception as e:
            raise ValueError(
                _err(
                    f"Cannot evaluate expression '{expr}': {e}",
                    "KAFAL-EXPR-EVAL",
                )
            ) from e

    def compile_safe_expr(self, expr: str, local_env: dict):
        cached = self._expr_cache.get(expr)
        if cached is not None:
            return cached

        tree = ast.parse(expr, mode="eval")

        allowed_call_names = {
            name
            for name, val in local_env.items()
            if callable(val)
            and isinstance(name, str)
            and name
            and not name.startswith("_")
            and "__" not in name
        }

        validator = SafeAstValidator(allowed_call_names)
        validator.validate(tree)

        code_obj = compile(tree, "", "eval")

        if len(self._expr_cache) >= self._max_expr_cache:
            self._expr_cache.pop(next(iter(self._expr_cache)))
        self._expr_cache[expr] = code_obj
        return code_obj

    @staticmethod
    def rewrite_history(expr: str) -> str:
        pattern = re.compile(r"\b([a-zA-Z_]\w*)\s*\[\s*(\d+)\s*\]")
        out = expr
        for _ in range(10):
            prev = out
            out = pattern.sub(lambda m: f"history({m.group(1)}, {m.group(2)})", out)
            if out == prev:
                break
        return out

    @staticmethod
    def rewrite_if_then_else(expr: str) -> str:
        if "if " in expr and " then " in expr and " else " in expr:
            m = re.match(r"\s*if\s+(.+?)\s+then\s+(.+?)\s+else\s+(.+)\s*$", expr)
            if m:
                cond, a, b = m.group(1), m.group(2), m.group(3)
                return f"({cond}) ? ({a}) : ({b})"
        return expr

    @staticmethod
    def rewrite_ternary(expr: str) -> str:
        if "?" not in expr or ":" not in expr:
            return expr
        m = re.match(r"\s*(.+?)\s*\?\s*(.+?)\s*:\s*(.+)\s*$", expr)
        if not m:
            return expr
        cond, a, b = m.group(1), m.group(2), m.group(3)
        return f"where({cond}, {a}, {b})"
    @staticmethod
    def _pf_get_state(pf: Any, symbol: str) -> StrategyState:
        # Support both get_state() and _get_state() depending on which version is present.
        getter = getattr(pf, "get_state", None) or getattr(pf, "_get_state", None)
        if getter is None or not callable(getter):
            raise AttributeError(
                _err(
                    "PortfolioState is missing get_state/_get_state; "
                    "cannot resolve per-symbol strategy state.",
                    "KAFAL-PORTFOLIO-GETSTATE",
                )
            )
        return getter(symbol)

    def build_eval_env(
        self,
        env: dict,
        *,
        eval_flow_expr: Optional[Callable[[str, dict], Any]] = None,
        user_functions: Optional[Dict[str, Tuple[List[str], str]]] = None,
    ) -> dict:
        local_env = dict(env)

        # ----------------------------
        # Back-compat aliases (surgical)
        # ----------------------------
        # Some parts of the pipeline normalize names and may call requestsecurity(...)
        # even if the DSL source used request_security(...).
        if "request_security" in local_env and "requestsecurity" not in local_env:
            local_env["requestsecurity"] = local_env["request_security"]
        if "requestsecurity" in local_env and "request_security" not in local_env:
            local_env["request_security"] = local_env["requestsecurity"]

        def history(x, n=1):
            if isinstance(x, pd.Series):
                return x.shift(int(n))
            raise TypeError(
                _err(
                    "history(x, n) expects a pandas Series as the first argument.",
                    "KAFAL-EXPR-HISTORY",
                )
            )

        def where(cond, a, b):
            idx = None
            if isinstance(cond, pd.Series):
                idx = cond.index
            elif isinstance(a, pd.Series):
                idx = a.index
            elif isinstance(b, pd.Series):
                idx = b.index

            out = np.where(cond, a, b)
            return pd.Series(out, index=idx) if idx is not None else out

        local_env["history"] = history
        local_env["where"] = where

        # strategy API (single/chart symbol)
        strategy_state = env.get("strategy", {}).get("state")
        if isinstance(strategy_state, StrategyState):
            # legacy functions (backwards compatible)
            def strategy_long(idx, size=1.0):
                strategy_state.long(int(idx), float(size))

            def strategy_short(idx, size=1.0):
                strategy_state.short(int(idx), float(size))

            def strategy_close(idx):
                strategy_state.close(int(idx))

            local_env["strategy_long"] = strategy_long
            local_env["strategy_short"] = strategy_short
            local_env["strategy_close"] = strategy_close

            # modern trade DSL (chart symbol only)
            class TradeAPI:
                def __init__(self, state: StrategyState):
                    self._state = state

                def long(self, signal, size=1.0):
                    self._apply_signal(signal, size, side="long")

                def short(self, signal, size=1.0):
                    self._apply_signal(signal, size, side="short")

                def close(self, signal=None):
                    if signal is None:
                        idx = len(self._state.prices) - 1
                        self._state.close(idx)
                        return
                    if isinstance(signal, pd.Series):
                        for i, v in enumerate(signal):
                            if bool(v):
                                self._state.close(i)
                    else:
                        if bool(signal):
                            idx = len(self._state.prices) - 1
                            self._state.close(idx)

                def limit_long(
                    self,
                    price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    self._place_order_with_price(
                        price,
                        size,
                        side="long",
                        otype="limit",
                        tif=tif,
                        group_id=group_id,
                        reduce_only=reduce_only,
                        expire_after_bars=expire_after_bars,
                    )

                def limit_short(
                    self,
                    price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    self._place_order_with_price(
                        price,
                        size,
                        side="short",
                        otype="limit",
                        tif=tif,
                        group_id=group_id,
                        reduce_only=reduce_only,
                        expire_after_bars=expire_after_bars,
                    )

                def stop_long(
                    self,
                    price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    self._place_order_with_price(
                        price,
                        size,
                        side="long",
                        otype="stop",
                        tif=tif,
                        group_id=group_id,
                        reduce_only=reduce_only,
                        expire_after_bars=expire_after_bars,
                    )

                def stop_short(
                    self,
                    price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    self._place_order_with_price(
                        price,
                        size,
                        side="short",
                        otype="stop",
                        tif=tif,
                        group_id=group_id,
                        reduce_only=reduce_only,
                        expire_after_bars=expire_after_bars,
                    )

                def bracket_long(
                    self,
                    entry_price,
                    tp_price,
                    sl_price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                ):
                    gid = group_id or f"br_{id(self._state)}_{len(getattr(self._state, 'orders', []))}"
                    self.limit_long(entry_price, size=size, tif=tif, group_id=gid)
                    self.limit_short(
                        tp_price,
                        size=size,
                        tif=tif,
                        group_id=gid,
                        reduce_only=True,
                    )
                    self.stop_short(
                        sl_price,
                        size=size,
                        tif=tif,
                        group_id=gid,
                        reduce_only=True,
                    )

                def bracket_short(
                    self,
                    entry_price,
                    tp_price,
                    sl_price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                ):
                    gid = group_id or f"br_{id(self._state)}_{len(getattr(self._state, 'orders', []))}"
                    self.limit_short(entry_price, size=size, tif=tif, group_id=gid)
                    self.limit_long(
                        tp_price,
                        size=size,
                        tif=tif,
                        group_id=gid,
                        reduce_only=True,
                    )
                    self.stop_long(
                        sl_price,
                        size=size,
                        tif=tif,
                        group_id=gid,
                        reduce_only=True,
                    )

                def _apply_signal(self, signal, size, side: str):
                    if isinstance(signal, pd.Series):
                        for i, v in enumerate(signal):
                            if bool(v):
                                bar_size = size.iloc[i] if isinstance(size, pd.Series) else size
                                if side == "long":
                                    self._state.long(i, float(bar_size))
                                else:
                                    self._state.short(i, float(bar_size))
                    else:
                        if bool(signal):
                            idx = len(self._state.prices) - 1
                            bar_size = float(size.iloc[-1]) if isinstance(size, pd.Series) else float(
                                size
                            )
                            if side == "long":
                                self._state.long(idx, bar_size)
                            else:
                                self._state.short(idx, bar_size)

                def _place_order_with_price(
                    self,
                    price,
                    size,
                    *,
                    side: str,
                    otype: str,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    if isinstance(price, pd.Series):
                        for i, v in enumerate(price):
                            if pd.isna(v):
                                continue
                            level = float(v)
                            bar_size = size.iloc[i] if isinstance(size, pd.Series) else size
                            if otype == "limit":
                                self._state.place_limit(
                                    side=side,
                                    idx=i,
                                    size=float(bar_size),
                                    price=level,
                                    tif=tif,
                                    group_id=group_id,
                                    reduce_only=reduce_only,
                                    expire_after_bars=expire_after_bars,
                                )
                            else:
                                self._state.place_stop(
                                    side=side,
                                    idx=i,
                                    size=float(bar_size),
                                    price=level,
                                    tif=tif,
                                    group_id=group_id,
                                    reduce_only=reduce_only,
                                    expire_after_bars=expire_after_bars,
                                )
                    else:
                        level = float(price)
                        idx = len(self._state.prices) - 1
                        bar_size = float(size.iloc[-1]) if isinstance(size, pd.Series) else float(
                            size
                        )
                        if otype == "limit":
                            self._state.place_limit(
                                side=side,
                                idx=idx,
                                size=bar_size,
                                price=level,
                                tif=tif,
                                group_id=group_id,
                                reduce_only=reduce_only,
                                expire_after_bars=expire_after_bars,
                            )
                        else:
                            self._state.place_stop(
                                side=side,
                                idx=idx,
                                size=bar_size,
                                price=level,
                                tif=tif,
                                group_id=group_id,
                                reduce_only=reduce_only,
                                expire_after_bars=expire_after_bars,
                            )

            local_env["trade"] = TradeAPI(strategy_state)

        # portfolio API (multi-symbol)
        portfolio_state = env.get("portfolio", {}).get("state")
        if isinstance(portfolio_state, PortfolioState):

            class PortfolioAPI:
                def __init__(self, pf: PortfolioState):
                    self._pf = pf

                def long(self, symbol, signal, size=1.0):
                    self._apply_signal(symbol, signal, size, side="long")

                def short(self, symbol, signal, size=1.0):
                    self._apply_signal(symbol, signal, size, side="short")

                def close(self, symbol, signal=None):
                    st = SafeEvaluator._pf_get_state(self._pf, symbol)
                    if signal is None:
                        idx = len(st.prices) - 1
                        st.close(idx)
                        return
                    if isinstance(signal, pd.Series):
                        for i, v in enumerate(signal):
                            if bool(v):
                                st.close(i)
                    else:
                        if bool(signal):
                            idx = len(st.prices) - 1
                            st.close(idx)

                def limit_long(
                    self,
                    symbol,
                    price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    self._place(
                        symbol,
                        price,
                        size,
                        side="long",
                        otype="limit",
                        tif=tif,
                        group_id=group_id,
                        reduce_only=reduce_only,
                        expire_after_bars=expire_after_bars,
                    )

                def limit_short(
                    self,
                    symbol,
                    price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    self._place(
                        symbol,
                        price,
                        size,
                        side="short",
                        otype="limit",
                        tif=tif,
                        group_id=group_id,
                        reduce_only=reduce_only,
                        expire_after_bars=expire_after_bars,
                    )

                def stop_long(
                    self,
                    symbol,
                    price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    self._place(
                        symbol,
                        price,
                        size,
                        side="long",
                        otype="stop",
                        tif=tif,
                        group_id=group_id,
                        reduce_only=reduce_only,
                        expire_after_bars=expire_after_bars,
                    )

                def stop_short(
                    self,
                    symbol,
                    price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    self._place(
                        symbol,
                        price,
                        size,
                        side="short",
                        otype="stop",
                        tif=tif,
                        group_id=group_id,
                        reduce_only=reduce_only,
                        expire_after_bars=expire_after_bars,
                    )

                def bracket_long(
                    self,
                    symbol,
                    entry_price,
                    tp_price,
                    sl_price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                ):
                    st = SafeEvaluator._pf_get_state(self._pf, symbol)
                    gid = group_id or f"br_{symbol}_{id(st)}_{len(getattr(st, 'orders', []))}"
                    self.limit_long(symbol, entry_price, size=size, tif=tif, group_id=gid)
                    self.limit_short(
                        symbol,
                        tp_price,
                        size=size,
                        tif=tif,
                        group_id=gid,
                        reduce_only=True,
                    )
                    self.stop_short(
                        symbol,
                        sl_price,
                        size=size,
                        tif=tif,
                        group_id=gid,
                        reduce_only=True,
                    )

                def bracket_short(
                    self,
                    symbol,
                    entry_price,
                    tp_price,
                    sl_price,
                    size=1.0,
                    *,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                ):
                    st = SafeEvaluator._pf_get_state(self._pf, symbol)
                    gid = group_id or f"br_{symbol}_{id(st)}_{len(getattr(st, 'orders', []))}"
                    self.limit_short(symbol, entry_price, size=size, tif=tif, group_id=gid)
                    self.limit_long(
                        symbol,
                        tp_price,
                        size=size,
                        tif=tif,
                        group_id=gid,
                        reduce_only=True,
                    )
                    self.stop_long(
                        symbol,
                        sl_price,
                        size=size,
                        tif=tif,
                        group_id=gid,
                        reduce_only=True,
                    )

                def _apply_signal(self, symbol, signal, size, side: str):
                    st = SafeEvaluator._pf_get_state(self._pf, symbol)
                    if isinstance(signal, pd.Series):
                        for i, v in enumerate(signal):
                            if bool(v):
                                bar_size = size.iloc[i] if isinstance(size, pd.Series) else size
                                if side == "long":
                                    st.long(i, float(bar_size))
                                else:
                                    st.short(i, float(bar_size))
                    else:
                        if bool(signal):
                            idx = len(st.prices) - 1
                            bar_size = float(size.iloc[-1]) if isinstance(size, pd.Series) else float(
                                size
                            )
                            if side == "long":
                                st.long(idx, bar_size)
                            else:
                                st.short(idx, bar_size)

                def _place(
                    self,
                    symbol,
                    price,
                    size,
                    *,
                    side: str,
                    otype: str,
                    tif: str = "GTC",
                    group_id: Optional[str] = None,
                    reduce_only: bool = False,
                    expire_after_bars: Optional[int] = None,
                ):
                    st = SafeEvaluator._pf_get_state(self._pf, symbol)
                    if isinstance(price, pd.Series):
                        for i, v in enumerate(price):
                            if pd.isna(v):
                                continue
                            level = float(v)
                            bar_size = size.iloc[i] if isinstance(size, pd.Series) else size
                            if otype == "limit":
                                st.place_limit(
                                    side=side,
                                    idx=i,
                                    size=float(bar_size),
                                    price=level,
                                    tif=tif,
                                    group_id=group_id,
                                    reduce_only=reduce_only,
                                    expire_after_bars=expire_after_bars,
                                )
                            else:
                                st.place_stop(
                                    side=side,
                                    idx=i,
                                    size=float(bar_size),
                                    price=level,
                                    tif=tif,
                                    group_id=group_id,
                                    reduce_only=reduce_only,
                                    expire_after_bars=expire_after_bars,
                                )
                    else:
                        level = float(price)
                        idx = len(st.prices) - 1
                        bar_size = float(size.iloc[-1]) if isinstance(size, pd.Series) else float(
                            size
                        )
                        if otype == "limit":
                            st.place_limit(
                                side=side,
                                idx=idx,
                                size=bar_size,
                                price=level,
                                tif=tif,
                                group_id=group_id,
                                reduce_only=reduce_only,
                                expire_after_bars=expire_after_bars,
                            )
                        else:
                            st.place_stop(
                                side=side,
                                idx=idx,
                                size=bar_size,
                                price=level,
                                tif=tif,
                                group_id=group_id,
                                reduce_only=reduce_only,
                                expire_after_bars=expire_after_bars,
                            )

            local_env["portfolio"] = PortfolioAPI(portfolio_state)

        # User functions: fn name(args...) = expr
        if user_functions:
            if eval_flow_expr is None:
                raise ValueError(
                    _err(
                        "build_eval_env requires eval_flow_expr when user_functions are provided.",
                        "KAFAL-EXPR-USERFN-EVAL",
                    )
                )

            for name, (params, body_expr) in user_functions.items():

                def make_func(p=params, body=body_expr):
                    def _f(*args):
                        local = dict(env)
                        for i, pname in enumerate(p):
                            if i < len(args):
                                local[pname] = args[i]
                        return eval_flow_expr(body, local)

                    return _f

                local_env[name] = make_func()

        return local_env
