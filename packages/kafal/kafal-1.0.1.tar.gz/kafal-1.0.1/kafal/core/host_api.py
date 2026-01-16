from __future__ import annotations

from typing import Any, Callable, Dict, Optional

import pandas as pd

ALLOWED_SECURITY_FIELDS = {"open", "high", "low", "close", "volume"}


def _err(msg: str, code: str) -> str:
    # Standardised Kafal error prefix for easier log filtering.
    return f"Kafal: {msg} [{code}]"


def get_ohlcv(
    symbol: str,
    timeframe: str,
    host_api: Dict[str, Any],
) -> pd.DataFrame:
    """
    Helper to call host_api['request_ohlcv'] and validate it returns a DataFrame.

    This is the v2 OHLCV API used by request_security(expr=...) style calls.
    """
    # Back-compat: support both "request_ohlcv" and legacy "requestohlcv"
    fn = host_api.get("request_ohlcv") or host_api.get("requestohlcv")

    if fn is None or not callable(fn):
        # Message expected by tests when the function is missing.
        # Keep the legacy sentence intact so older regex-based tests don't break.
        raise ValueError(
            _err(
                "requestsecurityexpr requires hostapirequestohlcv returning a DataFrame.",
                "KAFAL-HOST-OHLCV-MISSING",
            )
        )

    df = fn(symbol, timeframe)

    if not isinstance(df, pd.DataFrame):
        # Message expected by tests when the function returns wrong type.
        # Keep the legacy sentence intact so older regex-based tests don't break.
        raise ValueError(
            _err(
                "hostapirequestohlcv must return a pandas DataFrame.",
                "KAFAL-HOST-OHLCV-TYPE",
            )
        )

    return df


class HostAPI:
    """
    Thin wrapper around host-provided API dict.

    Exposes:
      - request_security(symbol, timeframe, field_or_expr, gaps=...)
    """

    def __init__(
        self,
        host_api: Optional[Dict[str, Any]] = None,
        hostapi: Optional[Dict[str, Any]] = None,  # legacy alias for tests / older code
    ):
        # Prefer explicit host_api; fall back to legacy name if provided.
        if host_api is None and hostapi is not None:
            host_api = hostapi
        self.host_api: Dict[str, Any] = host_api or {}

        # v1 per-field API: new + legacy spellings
        self._host_req_series: Optional[Callable[..., pd.Series]] = None
        fn_series = self.host_api.get("request_security")
        if fn_series is None:
            # legacy key, kept for back-compat
            fn_series = self.host_api.get("requestsecurity")
        if fn_series is not None:
            if not callable(fn_series):
                raise ValueError(
                    _err(
                        "host_api['request_security' or 'requestsecurity'] must be callable if provided.",
                        "KAFAL-HOST-REQSERIES-CALLABLE",
                    )
                )
            self._host_req_series = fn_series  # type: ignore[assignment]

        # v2 OHLCV API
        fn_ohlcv = self.host_api.get("request_ohlcv")
        if fn_ohlcv is not None and not callable(fn_ohlcv):
            raise ValueError(
                _err(
                    "host_api['request_ohlcv'] must be callable if provided.",
                    "KAFAL-HOST-OHLCV-CALLABLE",
                )
            )

    # -----------------------
    # request_security core
    # -----------------------
    def request_security(
        self,
        symbol: str,
        timeframe: str,
        expr_or_field: str,
        gaps: str = "off",
    ) -> pd.Series:
        """
        Unified security request helper.

        - If expr_or_field is a simple field in ALLOWED_SECURITY_FIELDS and a per-field
          host function exists (v1), delegate directly to host.
        - Otherwise, require host_api['request_ohlcv'] and evaluate expr_or_field
          against the returned DataFrame.
        """
        expr_or_field = str(expr_or_field)

        # Fast path: v1 per-field API if available and field is simple OHLCV
        if (
            expr_or_field in ALLOWED_SECURITY_FIELDS
            and self._host_req_series is not None
        ):
            s = self._host_req_series(symbol, timeframe, expr_or_field)
            if not isinstance(s, pd.Series):
                raise ValueError(
                    _err(
                        "host_api['request_security' or 'requestsecurity'] must return a pandas Series.",
                        "KAFAL-HOST-REQSERIES-TYPE",
                    )
                )
            return s

        # Fallback: v2 OHLCV API, evaluate expression or field on returned DataFrame
        df = get_ohlcv(symbol, timeframe, self.host_api)

        if expr_or_field in df.columns:
            out = df[expr_or_field]
        else:
            # Evaluate an expression using the DataFrame columns in a safe namespace
            local_env: Dict[str, Any] = {col: df[col] for col in df.columns}
            try:
                out = eval(expr_or_field, {"__builtins__": {}}, local_env)
            except Exception as e:
                raise ValueError(
                    _err(
                        f"Error evaluating security expression '{expr_or_field}': {e}",
                        "KAFAL-HOST-REQEXPR-EVAL",
                    )
                )

        if isinstance(out, pd.DataFrame):
            # collapse single-column DF to Series for convenience
            if out.shape[1] == 1:
                out = out.iloc[:, 0]
            else:
                raise ValueError(
                    _err(
                        "request_security expression must result in a Series, not a multi-column DataFrame.",
                        "KAFAL-HOST-REQEXPR-MULTICOL",
                    )
                )
        if not isinstance(out, pd.Series):
            raise ValueError(
                _err(
                    "request_security expression must evaluate to a pandas Series.",
                    "KAFAL-HOST-REQEXPR-TYPE",
                )
            )

        # Optional gap handling (simple modes)
        gaps = str(gaps).lower()
        if gaps == "ffill":
            out = out.ffill()
        elif gaps == "on":
            # leave as-is, user is responsible for gaps
            pass
        else:
            # "off" -> no special handling; keep raw
            pass

        return out

    # Back-compat alias used by older tests / codepaths
    def requestsecurity(
        self,
        symbol: str,
        timeframe: str,
        expr_or_field: str,
        gaps: str = "off",
    ) -> pd.Series:
        return self.request_security(symbol, timeframe, expr_or_field, gaps=gaps)


# -----------------------
# Plot capture helpers
# -----------------------
def _coerce_series(value: Any, df: pd.DataFrame) -> Optional[pd.Series]:
    """
    Convert a Kafal 'plot' value into a pandas Series aligned to df.index.
    Supports:
      - pd.Series
      - list/tuple/ndarray-like
      - scalar (broadcast)
    """
    if value is None:
        return None

    if isinstance(value, pd.Series):
        return value

    # scalar -> broadcast
    if isinstance(value, (int, float)):
        return pd.Series([float(value)] * len(df), index=df.index)

    # list/ndarray-like
    try:
        s = pd.Series(value)
    except Exception:
        return None

    # Align length if possible (common when indicators output shorter arrays)
    if len(s) == len(df):
        s.index = df.index
        return s

    if len(s) < len(df):
        # right-align (match your JS buildLineData right-align behavior)
        pad = [None] * (len(df) - len(s))
        s2 = pd.Series(pad + s.tolist(), index=df.index)
        return s2

    # longer than df -> trim from end
    s3 = pd.Series(s.tolist()[-len(df) :], index=df.index)
    return s3


def attach_host_api(
    interpreter: Any,
    env: Dict[str, Any],
    df: pd.DataFrame,
    host_api: Optional[Dict[str, Any]],
) -> None:
    """
    Attach host API helpers into the interpreter environment.

    Exposes:
      env["request_security"] as callable wired to HostAPI(host_api).request_security.
      env["plot"] as a capture helper that records to env["_kafal_out"]["plots"].
    """
    host_api = host_api or {}
    host = HostAPI(host_api)

    # Bind request_security into env for scripts
    env["request_security"] = host.request_security

    # Standard output container (interpreter can also merge its own outputs)
    out = env.get("_kafal_out")
    if not isinstance(out, dict):
        out = {}
        env["_kafal_out"] = out
    plots = out.get("plots")
    if not isinstance(plots, list):
        plots = []
        out["plots"] = plots

    def plot(
        value: Any,
        title: Optional[str] = None,
        color: Optional[str] = None,
        width: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Script-callable plot().

        Stores a stable schema so your Django integration can always read:
          out["plots"][i]["value"]  -> pd.Series
        """
        s = _coerce_series(value, df)
        plots.append(
            {
                "id": title or "plot",
                "title": title,
                "value": s,
                "style": {
                    "color": color,
                    "width": width,
                    **({} if not kwargs else {"extra": kwargs}),
                },
            }
        )
        return value

    env["plot"] = plot


class HostAPIMixin:
    """
    Backwards-compatible mixin used by KafalInterpreter.

    Exposes:
      - self.host_api (dict)
      - attach_host_api(self, env, df, host_api) helper
    """

    def __init__(self, *args, host_api: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        # default host_api; can be overridden at run() call time
        self.host_api: Dict[str, Any] = host_api or {}

    def attach_host_api(
        self,
        env: Dict[str, Any],
        df: pd.DataFrame,
        host_api: Optional[Dict[str, Any]] = None,
    ) -> None:
        # effective host_api = explicit passed in run() or the one on self
        effective_host_api = host_api if host_api is not None else self.host_api
        attach_host_api(self, env, df, effective_host_api)
