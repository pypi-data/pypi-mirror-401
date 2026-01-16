from __future__ import annotations

from typing import Any, Dict, List, Optional

import re
import shlex

import numpy as np
import pandas as pd


def _is_int(s: str) -> bool:
    try:
        int(str(s))
        return True
    except Exception:
        return False


def _is_float(s: str) -> bool:
    try:
        float(str(s))
        return True
    except Exception:
        return False


def _err(msg: str, code: str) -> str:
    return f"{msg} [{code}]"


class VizParserMixin:
    """
    Mixin implementing visualization/alert parsing for Kafal.

    Expects host Interpreter to provide:
      - eval_flow_expr(expr: str, env: dict) -> Any
    """

    # Allowed style keys (minimal validation)
    PLOT_STYLE_KEYS = {"color", "width", "title", "linestyle", "style", "marker"}
    SHAPE_STYLE_KEYS = {"color", "size", "text", "location", "shape"}
    HLINE_STYLE_KEYS = {"color", "width", "linestyle", "title"}
    FILL_STYLE_KEYS = {"color", "alpha", "title"}
    BGCOLOR_STYLE_KEYS = {"color", "alpha"}
    ALERT_STYLE_KEYS = {"message", "severity"}
    TABLE_STYLE_KEYS = {"position", "theme", "compact"}

    # -------------------------
    # Small helpers
    # -------------------------
    def split_top_level(self, s: str, sep: str) -> List[str]:
        """
        Split a string on sep only at top-level parentheses depth (and outside quotes).
        Used for argument splitting inside plot(...), fill(...), table(...).
        """
        parts: List[str] = []
        buf: List[str] = []
        depth = 0
        in_quote: Optional[str] = None

        for ch in s:
            if in_quote is not None:
                buf.append(ch)
                if ch == in_quote:
                    in_quote = None
                continue

            if ch in ("'", '"'):
                in_quote = ch
                buf.append(ch)
                continue

            if ch == "(":
                depth += 1
                buf.append(ch)
                continue

            if ch == ")":
                depth = max(0, depth - 1)
                buf.append(ch)
                continue

            if ch == sep and depth == 0:
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                continue

            buf.append(ch)

        tail = "".join(buf).strip()
        if tail:
            parts.append(tail)
        return parts

    def parse_style(self, style_str: str) -> Dict[str, Any]:
        """
        Parse styles: key=value tokens (quotes supported via shlex).
        Converts ints/floats when possible; keeps everything else as strings.
        """
        styles: Dict[str, Any] = {}
        if not style_str:
            return styles

        try:
            parts = shlex.split(style_str, posix=True)
        except ValueError:
            parts = style_str.split()

        for part in parts:
            if "=" not in part:
                continue
            key, val = part.split("=", 1)
            key = key.strip()
            val = val.strip()
            if not key:
                continue

            if _is_int(val):
                styles[key] = int(val)
            elif _is_float(val):
                styles[key] = float(val)
            else:
                styles[key] = val

        return styles

    def validate_styles(self, kind: str, style: Dict[str, Any]) -> None:
        if not style:
            return

        if kind == "plot":
            allowed = self.PLOT_STYLE_KEYS
        elif kind == "shape":
            allowed = self.SHAPE_STYLE_KEYS
        elif kind == "hline":
            allowed = self.HLINE_STYLE_KEYS
        elif kind == "fill":
            allowed = self.FILL_STYLE_KEYS
        elif kind == "bgcolor":
            allowed = self.BGCOLOR_STYLE_KEYS
        elif kind == "alert":
            allowed = self.ALERT_STYLE_KEYS
        elif kind == "table":
            allowed = self.TABLE_STYLE_KEYS
        else:
            return

        # Core payload keys that are not “style”
        payload_ok = {
            "kind",
            "value",
            "top",
            "bottom",
            "rows",
            "title",
            "condition",
            "message",
        }
        unknown = [k for k in style.keys() if k not in allowed and k not in payload_ok]
        if unknown:
            raise ValueError(
                _err(
                    f"Unknown {kind} style key(s): {unknown}. "
                    "Check the name or move it into the host-rendered config.",
                    "KAFAL-VIZ-STYLE-KEY",
                )
            )

    # -------------------------
    # plot / shape / hline
    # -------------------------
    def parse_plot_line(self, line: str, env: dict) -> Dict[str, Any]:
        """
        plot(expr, style_kv..., ...) - tail_style_kv...
        shape(expr, ...) - ...
        hline(expr, ...) - ...
        """
        if "-" in line:
            plot_part, style_part = line.split("-", 1)
            plot_part = plot_part.strip()
            style_part = style_part.strip()
        else:
            plot_part = line.strip()
            style_part = ""

        kind = None
        inner = None

        m = re.search(r"plot\((.*)\)", plot_part)
        if m:
            kind = "plot"
            inner = m.group(1)
        else:
            m = re.search(r"shape\((.*)\)", plot_part)
            if m:
                kind = "shape"
                inner = m.group(1)
            else:
                m = re.search(r"hline\((.*)\)", plot_part)
                if m:
                    kind = "hline"
                    inner = m.group(1)

        if kind is None or inner is None:
            raise ValueError(
                _err(
                    f'Invalid plot/shape/hline syntax: "{line}". '
                    'Expected "plot(expr, ...)", "shape(expr, ...)", or "hline(expr, ...)".',
                    "KAFAL-VIZ-PLOT-SYNTAX",
                )
            )

        args = self.split_top_level(inner, ",")
        if not args:
            raise ValueError(
                _err(
                    f'"{kind}" requires at least one expression argument. Line: "{line}".',
                    "KAFAL-VIZ-PLOT-ARGS",
                )
            )

        expr = args[0].strip()
        value = self.eval_flow_expr(expr, env)

        style: Dict[str, Any] = {}
        if len(args) > 1:
            style_inside = " ".join(a.strip() for a in args[1:] if a.strip())
            style.update(self.parse_style(style_inside))
        style.update(self.parse_style(style_part))

        style["kind"] = kind
        style["value"] = value

        self.validate_styles(kind, style)
        return style

    # -------------------------
    # fill
    # -------------------------
    def parse_fill_line(self, line: str, env: dict) -> Dict[str, Any]:
        """
        fill(top, bottom, style_kv..., ...) - tail_style_kv...
        """
        if "-" in line:
            fill_part, style_part = line.split("-", 1)
            fill_part = fill_part.strip()
            style_part = style_part.strip()
        else:
            fill_part = line.strip()
            style_part = ""

        m = re.search(r"fill\((.*)\)", fill_part)
        if not m:
            raise ValueError(
                _err(
                    f'Invalid fill syntax: "{line}". Expected "fill(top, bottom, ...)".',
                    "KAFAL-VIZ-FILL-SYNTAX",
                )
            )

        inner = m.group(1)
        args = self.split_top_level(inner, ",")

        if len(args) < 2:
            raise ValueError(
                _err(
                    f'fill requires at least 2 arguments: "fill(top, bottom, ...)". Line: "{line}".',
                    "KAFAL-VIZ-FILL-ARGS",
                )
            )

        top_expr = args[0].strip()
        bottom_expr = args[1].strip()

        top_val = self.eval_flow_expr(top_expr, env)
        bottom_val = self.eval_flow_expr(bottom_expr, env)

        style: Dict[str, Any] = {}
        if len(args) > 2:
            style_inside = " ".join(a.strip() for a in args[2:] if a.strip())
            style.update(self.parse_style(style_inside))
        style.update(self.parse_style(style_part))

        style["kind"] = "fill"
        style["top"] = top_val
        style["bottom"] = bottom_val

        self.validate_styles("fill", style)
        return style

    # -------------------------
    # table
    # -------------------------
    def parse_table_line(self, line: str, env: dict) -> Dict[str, Any]:
        """
        table(title, col1, col2, ...) - position=topright theme=dark compact=true
        """
        if "-" in line:
            table_part, style_part = line.split("-", 1)
            table_part = table_part.strip()
            style_part = style_part.strip()
        else:
            table_part = line.strip()
            style_part = ""

        m = re.search(r"table\((.*)\)", table_part)
        if not m:
            raise ValueError(
                _err(
                    f'Invalid table syntax: "{line}". Expected "table(title, row1, ...)".',
                    "KAFAL-VIZ-TABLE-SYNTAX",
                )
            )

        inner = m.group(1)
        args = self.split_top_level(inner, ",")

        if not args:
            raise ValueError(
                _err(
                    f'table requires at least a title expression: "table(title, ...)". Line: "{line}".',
                    "KAFAL-VIZ-TABLE-ARGS",
                )
            )

        title_expr = args[0].strip()
        title_val = self.eval_flow_expr(title_expr, env)

        row_exprs = [a.strip() for a in args[1:]]
        rows: List[Any] = []
        for expr in row_exprs:
            if not expr:
                continue
            rows.append(self.eval_flow_expr(expr, env))

        style = self.parse_style(style_part)
        style["kind"] = "table"
        style["title"] = title_val
        style["rows"] = rows

        self.validate_styles("table", style)
        return style

    # -------------------------
    # bgcolor
    # -------------------------
    def parse_bgcolor_line(self, line: str, env: dict) -> Dict[str, Any]:
        """
        bgcolor(condition) - color=... alpha=...
        """
        m = re.search(r"bgcolor\((.+?)\)\s*(?:-\s*(.*))?$", line.strip())
        if not m:
            raise ValueError(
                _err(
                    f'Invalid bgcolor syntax: "{line}". '
                    'Expected "bgcolor(condition) - color=... alpha=...".',
                    "KAFAL-VIZ-BGCOLOR-SYNTAX",
                )
            )

        condition_expr = (m.group(1) or "").strip()
        tail = (m.group(2) or "").strip()

        cond = self.eval_flow_expr(condition_expr, env)
        style = self.parse_style(tail)
        style["kind"] = "bgcolor"
        style["condition"] = cond

        self.validate_styles("bgcolor", style)
        return style

    # -------------------------
    # alert
    # -------------------------
    def parse_alert_line(self, line: str, env: dict) -> Dict[str, Any]:
        """
        alert(condition) - message="..." severity="..."
        Also supports a simple message-only tail after '-' if message= isn't provided:
          alert(cond) - "My message"
        """
        m = re.search(r"alert\((.+?)\)\s*(?:-\s*(.*))?$", line.strip())
        if not m:
            raise ValueError(
                _err(
                    f'Invalid alert syntax: "{line}". '
                    'Expected "alert(condition) - message=... severity=...".',
                    "KAFAL-VIZ-ALERT-SYNTAX",
                )
            )

        cond_expr = (m.group(1) or "").strip()
        tail = (m.group(2) or "").strip()

        cond = self.eval_flow_expr(cond_expr, env)
        style = self.parse_style(tail)

        # Back-compat: allow `- "message"` (no key/value)
        if "message" not in style and "-" in line:
            msg_match = re.search(r"-\s*(.+)$", line)
            if msg_match:
                msg = msg_match.group(1).strip()
                if msg and "=" not in msg:
                    style["message"] = msg

        style["kind"] = "alert"
        style["condition"] = cond

        self.validate_styles("alert", style)
        return style
