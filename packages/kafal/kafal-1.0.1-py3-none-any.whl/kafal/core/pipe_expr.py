from __future__ import annotations

from typing import Any, Dict, List, Tuple, Optional
import re


def _err(msg: str, code: str) -> str:
    return f"{msg} [{code}]"


class PipeExprMixin:
    """
    Mixin that implements Kafal's pipe syntax:

        x => src | rsi(14)
        y = src | ema(len)

    Expects the host Interpreter to provide:

    - eval_flow_expr(expr: str, env: dict) -> Any
      (used for nested evaluation of the left-hand source expression)
    - _safe.eval(expr: str, env: dict, eval_flow_expr=..., user_functions=...)
      if you want to use the SafeEvaluator for non-pipe expressions.
    - user_functions: Dict[str, Tuple[List[str], str]]
      (optional, passed through to SafeEvaluator when needed)

    The host should also provide:

    - env["ta"] as a dict of TA functions (from builtins.baseenv)
    - env["input"] dict for named inputs, if used in pipe args.
    """

    # -------------------------
    # Public entry used by BlocksMixin
    # -------------------------
    def parse_pipe_assignment_line(self, line: str, env: dict) -> Optional[Dict[str, Any]]:
        """
        Parse:

            name => pipe_expr

        Returns {name: value} or None if the line is not a pipe assignment.
        """
        if "=>" not in line:
            return None

        left, right = line.split("=>", 1)
        var_name = left.strip()
        pipe_expr = right.strip()

        if not var_name:
            raise ValueError(
                _err(
                    f'Invalid pipe assignment: missing variable name before "=>". Line: "{line}".',
                    "KAFAL-PIPE-ASSIGN-NAME",
                )
            )
        if not pipe_expr:
            raise ValueError(
                _err(
                    f'Invalid pipe assignment: missing expression after "=>". Line: "{line}".',
                    "KAFAL-PIPE-ASSIGN-EXPR",
                )
            )

        return {var_name: self.eval_pipe_or_safe(pipe_expr, env)}

    # -------------------------
    # Integration point with SafeEvaluator
    # -------------------------
    def eval_pipe_or_safe(self, expr: str, env: dict) -> Any:
        """
        Evaluate an expression that may contain pipes.

        If there is at least one '|' at top level, use the pipe engine.
        Otherwise, fall back to the host's safe evaluator via self._safe.
        """
        if isinstance(expr, str) and "|" in expr:
            return self._eval_pipe_expr(expr, env)

        # Host is expected to attach SafeEvaluator as self._safe.
        return self._safe.eval(  # type: ignore[attr-defined]
            expr,
            env,
            eval_flow_expr=self.eval_flow_expr,  # type: ignore[attr-defined]
            user_functions=self.user_functions,  # type: ignore[attr-defined]
        )

    # -------------------------
    # Core pipe evaluation
    # -------------------------
    def _eval_pipe_expr(self, expr: str, env: dict) -> Any:
        """
        Evaluate a pipe expression:

            src | fn(a, b, ...)
        """
        parts = self._split_top_level(expr, "|")
        if len(parts) < 2:
            # No actual pipe, just evaluate normally.
            return self._safe.eval(  # type: ignore[attr-defined]
                expr,
                env,
                eval_flow_expr=self.eval_flow_expr,  # type: ignore[attr-defined]
                user_functions=self.user_functions,  # type: ignore[attr-defined]
            )

        source_expr = parts[0].strip()
        # Use host's eval_flow_expr for the left side so nested pipes etc. work.
        val = self.eval_flow_expr(source_expr, env)  # type: ignore[attr-defined]

        input_ns = env.get("input", {}) if isinstance(env.get("input"), dict) else {}

        for stage in parts[1:]:
            stage = stage.strip()
            func_name, arg_tokens = self._parse_func_call(stage)
            func = self._resolve_callable(func_name, env)

            resolved_args: List[Any] = []
            for tok in arg_tokens:
                tok = tok.strip()
                if tok in input_ns:
                    resolved_args.append(input_ns[tok])
                elif tok in env:
                    resolved_args.append(env[tok])
                else:
                    # basic literal parsing
                    try:
                        if re.fullmatch(r"-?\d+", tok):
                            resolved_args.append(int(tok))
                        else:
                            resolved_args.append(float(tok))
                    except Exception:
                        resolved_args.append(tok)

            val = func(val, *resolved_args)

        return val

    # -------------------------
    # Helpers
    # -------------------------
    def _split_top_level(self, s: str, sep: str) -> List[str]:
        """
        Split on `sep` only at top-level parentheses depth (and outside quotes).
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

    def _parse_func_call(self, call: str) -> Tuple[str, List[str]]:
        """
        Parse `fn(a, b, c)` into ("fn", ["a", "b", "c"]).
        """
        m = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*$", call.strip())
        if not m:
            raise ValueError(
                _err(
                    f'Invalid function call syntax in pipe stage: "{call}". '
                    'Expected "fn(arg1, arg2, ...)".',
                    "KAFAL-PIPE-CALL-SYNTAX",
                )
            )

        name = m.group(1).strip()
        args_str = m.group(2).strip()
        if not args_str:
            return name, []

        args = self._split_top_level(args_str, ",")
        return name, [a.strip() for a in args if a.strip()]

    def _resolve_callable(self, func_name: str, env: dict):
        """
        Resolve a function by name from env or env['ta'].
        """
        v = env.get(func_name)
        if callable(v):
            return v

        ta_ns = env.get("ta")
        if isinstance(ta_ns, dict) and callable(ta_ns.get(func_name)):
            return ta_ns[func_name]

        raise ValueError(
            _err(
                f"Unknown function '{func_name}' in pipe expression. "
                "Make sure it is available in env or env['ta'].",
                "KAFAL-PIPE-FUNC-NOT-FOUND",
            )
        )
