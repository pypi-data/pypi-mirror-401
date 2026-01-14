from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import re

import numpy as np
import pandas as pd


def _err(msg: str, code: str) -> str:
    return f"{msg} [{code}]"


class BlocksMixin:
    """
    Mixin implementing { ... } block parsing + execution for Kafal scripts.

    This is extracted from interpreter.py and expects the host Interpreter class
    to provide the following methods (same names as in the monolith):

      - eval_flow_expr(expr: str, env: dict) -> Any
      - parse_pipe_assignment_line(line: str, env: dict) -> Dict[str, Any] | None
      - parse_plot_line(line: str, env: dict) -> Dict[str, Any]   (returns dict with "kind")
      - parse_fill_line(line: str, env: dict) -> Dict[str, Any]
      - parse_table_line(line: str, env: dict) -> Dict[str, Any]
      - parse_bgcolor_line(line: str, env: dict) -> Dict[str, Any]
      - parse_alert_line(line: str, env: dict) -> Dict[str, Any]

    It also expects MAX_FOR_RANGE / MAXFORRANGE to exist on the class or module.
    """

    # -------------------------
    # Block collection
    # -------------------------
    def collect_block(self, lines: List[str], start_idx: int) -> Tuple[List[str], int]:
        """
        Collect a { ... } block starting at the line after a header that ends with '{'.

        Returns:
          (block_lines, next_index_after_block)

        Nested blocks are handled by tracking brace depth using count("{") and count("}").
        """
        block: List[str] = []
        depth = 1  # we enter with one open "{" from the header

        i = int(start_idx)
        while i < len(lines):
            raw = lines[i]
            line = raw.strip()

            open_count = line.count("{")
            close_count = line.count("}")
            depth += open_count
            depth -= close_count

            if line and depth == 0:
                i += 1
                break

            block.append(raw)
            i += 1

        return block, i

    # -------------------------
    # Block execution
    # -------------------------
    def execute_block_lines(
        self,
        block_lines: List[str],
        env: dict,
        plots: List[Dict[str, Any]],
        shapes: List[Dict[str, Any]],
        hlines: List[Dict[str, Any]],
        bgcolors: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
        fills: List[Dict[str, Any]],
        tables: List[Dict[str, Any]],
    ) -> None:
        """
        Execute a list of lines as a block, using the same rules as the main loop.
        Allows nested if/for/plot/etc.
        """
        i = 0
        n = len(block_lines)

        while i < n:
            raw = block_lines[i]
            line = raw.strip()

            if not line or line.startswith("#"):
                i += 1
                continue

            # nested if-chain
            if line.startswith("if") and line.rstrip().endswith("{"):
                i = self.execute_if_chain(
                    block_lines,
                    i,
                    env,
                    plots,
                    shapes,
                    hlines,
                    bgcolors,
                    alerts,
                    fills,
                    tables,
                )
                continue

            # nested for-loop
            if line.startswith("for") and line.rstrip().endswith("{"):
                i = self.execute_for_block(
                    block_lines,
                    i,
                    env,
                    plots,
                    shapes,
                    hlines,
                    bgcolors,
                    alerts,
                    fills,
                    tables,
                )
                continue

            # pipe assignment: x => src | rsi(14)
            if "=>" in line and "|" in line:
                result = self.parse_pipe_assignment_line(line, env)
                if result:
                    env.update(result)
                i += 1
                continue

            # viz
            if line.startswith("plot") or line.startswith("shape") or line.startswith("hline"):
                viz = self.parse_plot_line(line, env)
                kind = viz.get("kind")
                if kind == "plot":
                    plots.append(viz)
                elif kind == "shape":
                    shapes.append(viz)
                else:
                    hlines.append(viz)
                i += 1
                continue

            if line.startswith("fill"):
                band = self.parse_fill_line(line, env)
                fills.append(band)
                i += 1
                continue

            if line.startswith("table"):
                tbl = self.parse_table_line(line, env)
                tables.append(tbl)
                i += 1
                continue

            if line.startswith("bgcolor"):
                bg = self.parse_bgcolor_line(line, env)
                bgcolors.append(bg)
                i += 1
                continue

            if line.startswith("alert"):
                al = self.parse_alert_line(line, env)
                alerts.append(al)
                i += 1
                continue

            # assignment: name = expr
            if "=" in line:
                name, expr = line.split("=", 1)
                name = name.strip()
                expr = expr.strip()
                env[name] = self.eval_flow_expr(expr, env)
                i += 1
                continue

            i += 1

    # -------------------------
    # if / elseif / else blocks
    # -------------------------
    def execute_if_chain(
        self,
        lines: List[str],
        i: int,
        env: dict,
        plots: List[Dict[str, Any]],
        shapes: List[Dict[str, Any]],
        hlines: List[Dict[str, Any]],
        bgcolors: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
        fills: List[Dict[str, Any]],
        tables: List[Dict[str, Any]],
    ) -> int:
        """
        if cond { ... }
        elseif cond { ... }
        else if cond { ... }
        else { ... }
        """
        n = len(lines)
        branches: List[Tuple[Optional[str], List[str]]] = []

        header = lines[i].strip()
        cond_part = header[2:].strip()  # remove leading 'if'
        if cond_part.endswith("{"):
            cond_part = cond_part[:-1].strip()

        block, j = self.collect_block(lines, i + 1)
        branches.append((cond_part, block))

        while j < n:
            look = lines[j].strip()

            if look.startswith("elseif") and look.rstrip().endswith("{"):
                cond = look[len("elseif") :].strip()
                if cond.endswith("{"):
                    cond = cond[:-1].strip()
                block, j = self.collect_block(lines, j + 1)
                branches.append((cond, block))
                continue

            if look.startswith("else if") and look.rstrip().endswith("{"):
                cond = look[len("else if") :].strip()
                if cond.endswith("{"):
                    cond = cond[:-1].strip()
                block, j = self.collect_block(lines, j + 1)
                branches.append((cond, block))
                continue

            if look.startswith("else") and look.rstrip().endswith("{"):
                block, j = self.collect_block(lines, j + 1)
                branches.append((None, block))
                break

            break

        chosen: Optional[List[str]] = None
        for cond_expr, b in branches:
            if cond_expr is None:
                chosen = b
                break

            cond_val = self.eval_flow_expr(cond_expr, env)
            cond_true = bool(np.any(cond_val))
            if cond_true:
                chosen = b
                break

        if chosen:
            self.execute_block_lines(
                chosen,
                env,
                plots,
                shapes,
                hlines,
                bgcolors,
                alerts,
                fills,
                tables,
            )

        return j

    # -------------------------
    # for blocks
    # -------------------------
    def execute_for_block(
        self,
        lines: List[str],
        i: int,
        env: dict,
        plots: List[Dict[str, Any]],
        shapes: List[Dict[str, Any]],
        hlines: List[Dict[str, Any]],
        bgcolors: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
        fills: List[Dict[str, Any]],
        tables: List[Dict[str, Any]],
    ) -> int:
        """
        Supported headers:

          for i in 0..10 {
          for i in 0..bar_index {
          for x in my_array {

        End expression must evaluate to an integer for range loops.
        Iterables can be list/tuple/np.ndarray/pd.Series.
        """
        header = lines[i].strip()

        m_range = re.match(
            r"for\s+([a-zA-Z_]\w*)\s+in\s+(.+?)\.\.(.+?)\s*\{\s*$", header
        )
        m_iter = None
        if not m_range:
            m_iter = re.match(r"for\s+([a-zA-Z_]\w*)\s+in\s+(.+?)\s*\{\s*$", header)

        if not m_range and not m_iter:
            raise ValueError(
                _err(
                    f'Invalid for-loop header: "{header}". '
                    'Use "for i in 0..N" or "for x in my_array".',
                    "KAFAL-BLOCK-FOR-SYNTAX",
                )
            )

        max_for = getattr(self, "MAX_FOR_RANGE", getattr(self, "MAXFORRANGE", 1000))

        var_name: str
        iterator_values: List[Any]

        if m_range:
            var_name = m_range.group(1)
            start_expr = m_range.group(2).strip()
            end_expr = m_range.group(3).strip()

            start_val = self.eval_flow_expr(start_expr, env)
            end_val = self.eval_flow_expr(end_expr, env)

            try:
                start_i = int(start_val)
                end_i = int(end_val)
            except Exception:
                raise ValueError(
                    _err(
                        "For-loop range must evaluate to integers. "
                        f'Received start="{start_val}", end="{end_val}".',
                        "KAFAL-BLOCK-FOR-RANGE-TYPE",
                    )
                )

            if (end_i - start_i) > max_for:
                raise ValueError(
                    _err(
                        f"For-loop range too large (> {max_for}). "
                        "Use a smaller range or pre-aggregate your data.",
                        "KAFAL-BLOCK-FOR-RANGE",
                    )
                )

            iterator_values = list(range(start_i, end_i + 1))
        else:
            var_name = m_iter.group(1)
            iterable_expr = m_iter.group(2).strip()

            value = self.eval_flow_expr(iterable_expr, env)

            if isinstance(value, pd.Series):
                iterator_values = list(value.values.tolist())
            elif isinstance(value, (list, tuple, np.ndarray)):
                iterator_values = list(value)
            else:
                raise ValueError(
                    _err(
                        "For-loop iterable must be array/Series-like "
                        f'(list, tuple, numpy array, or Series). Got: "{type(value).__name__}".',
                        "KAFAL-BLOCK-FOR-ITERABLE",
                    )
                )

            if len(iterator_values) > max_for:
                raise ValueError(
                    _err(
                        f"For-loop iterable too long (> {max_for} elements). "
                        "Downsample or slice the data before looping.",
                        "KAFAL-BLOCK-FOR-ITERABLE-LEN",
                    )
                )

        block_lines, j = self.collect_block(lines, i + 1)

        for v in iterator_values:
            env[var_name] = v
            self.execute_block_lines(
                block_lines,
                env,
                plots,
                shapes,
                hlines,
                bgcolors,
                alerts,
                fills,
                tables,
            )

        return j
