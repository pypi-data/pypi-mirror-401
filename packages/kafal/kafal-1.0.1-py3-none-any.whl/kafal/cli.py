# kafal/cli.py

import argparse
import sys
import textwrap
from pathlib import Path
from typing import Optional

import pandas as pd

from kafal.core.interpreter import KafalInterpreter


# Single source of truth for CLI version (sync with installer)
CLI_VERSION = "1.0.0"


# --------- helpers ---------


def _print_error(msg: str) -> None:
    sys.stderr.write(f"Kafal: {msg}\n")
    sys.stderr.flush()


def _load_demo_data() -> pd.DataFrame:
    """
    Fallback OHLCV data for quick runs when no host data wiring exists.

    This mirrors the README-style synthetic series:
    a simple trending close with fixed spread for high/low.
    """
    dates = pd.date_range("2025-01-01", periods=200, freq="1h")
    # Use a NumPy array or list so arithmetic works elementwise
    steps = pd.Series(range(200), index=dates, dtype="float64")
    close = 100.0 + 0.1 * steps

    df = pd.DataFrame(
        {
            "open": close.shift(1).fillna(close.iloc[0]),
            "high": close + 1.0,
            "low": close - 1.0,
            "close": close,
            "volume": 1_000,
        },
        index=dates,
    )
    return df



def _read_script(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        _print_error(f"script not found: {path}")
        sys.exit(1)
    except OSError as exc:
        _print_error(f"could not read script {path}: {exc}")
        sys.exit(1)


def _ensure_kf_extension(name: str) -> str:
    p = Path(name)
    if p.suffix.lower() != ".kf":
        p = p.with_suffix(".kf")
    return str(p)


# --------- commands ---------


def cmd_run(args: argparse.Namespace) -> int:
    """
    kafal run <file.kf>

    - Loads the .kf script.
    - Uses a synthetic OHLCV DataFrame for now.
    - Runs in strategy mode and prints a brief stats summary. [file:6][file:31]
    """
    script_path = Path(args.file)
    code = _read_script(script_path)

    df = _load_demo_data()

    intr = KafalInterpreter()  # basic config; host_api=None [file:6][file:28]
    try:
        result = intr.run(code, df, mode="strategy")
    except Exception as exc:
        # Let the internal error messages (KAFAL- codes) bubble through,
        # but prepend a short CLI prefix.
        _print_error(f"runtime error while executing script: {exc}")
        return 1

    strategy = result.get("strategy") or {}
    stats = strategy.get("stats") or {}

    print(f"File   : {script_path}")
    print(f"Mode   : strategy")
    print("Stats  :")
    if not stats:
        print("  (no stats returned)")
        return 0

    # Print a few common keys if present; fall back to generic dump.
    key_order = [
        "net_profit",
        "max_drawdown",
        "win_rate",
        "trades",
        "exposure",
        "sharpe",
    ]
    shown = set()
    for k in key_order:
        if k in stats:
            print(f"  {k:14}: {stats[k]}")
            shown.add(k)

    for k, v in stats.items():
        if k not in shown:
            print(f"  {k:14}: {v}")

    return 0


def cmd_check(args: argparse.Namespace) -> int:
    """
    kafal check <file.kf>

    - Parses and validates the script by running it on a tiny synthetic
      DataFrame, but ignores outputs.
    - Useful for syntax / sandbox errors without focusing on stats. [file:29]
    """
    script_path = Path(args.file)
    code = _read_script(script_path)

    # Minimal DF (few rows) just to force parse/eval.
    df = _load_demo_data().iloc[:10]

    intr = KafalInterpreter()
    try:
        intr.run(code, df, mode="chart")
    except Exception as exc:
        _print_error(f"script invalid: {exc}")
        return 1

    print(f"{script_path}: OK")
    return 0


def cmd_version(_: argparse.Namespace) -> int:
    """
    kafal version

    - Prints CLI/runtime version string.
    """
    print(f"kafal {CLI_VERSION}")
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    """
    kafal doctor

    - Basic self-diagnostic:
      * Imports key modules.
      * Prints environment info.
    """
    print("Kafal doctor")
    print("------------")
    print(f"CLI version : {CLI_VERSION}")
    print(f"Python      : {sys.version.split()[0]}")

    # Import checks
    problems = []

    try:
        import kafal.core.interpreter  # noqa
    except Exception as exc:  # pragma: no cover - defensive
        problems.append(f"interpreter import failed: {exc}")

    try:
        import kafal.core.strategy_state  # noqa
    except Exception as exc:  # pragma: no cover
        problems.append(f"strategy_state import failed: {exc}")

    try:
        import kafal.core.portfolio_state  # noqa
    except Exception as exc:  # pragma: no cover
        problems.append(f"portfolio_state import failed: {exc}")

    if problems:
        print("Status      : PROBLEMS")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("Status      : OK")
    return 0


TEMPLATE_EMA = textwrap.dedent(
    """\
// Simple EMA crossover strategy template

len_fast = 10
len_slow = 30

fast = ema(close, len_fast)
slow = ema(close, len_slow)

plot(close) - title="Close"
plot(fast)  - title="Fast EMA"  color=rgba(0,255,0,0.9)
plot(slow)  - title="Slow EMA"  color=rgba(255,0,0,0.9)

long_cond  = crossover(fast, slow)
short_cond = crossunder(fast, slow)

// Modern trading API
trade.long(long_cond,  size=1.0)
trade.short(short_cond, size=1.0)

"""
)


def cmd_new(args: argparse.Namespace) -> int:
    """
    kafal new <name>

    - Creates a new .kf script from a simple EMA crossover template. [file:6]
    """
    filename = _ensure_kf_extension(args.name)
    path = Path(filename)

    if path.exists() and not args.force:
        _print_error(f"file already exists: {path} (use --force to overwrite)")
        return 1

    try:
        path.write_text(TEMPLATE_EMA, encoding="utf-8")
    except OSError as exc:
        _print_error(f"could not write file {path}: {exc}")
        return 1

    print(f"Created {path}")
    return 0


# --------- argument parsing ---------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kafal",
        description="Kafal DSL runtime CLI (indicators, strategies, research).",
    )

    subparsers = parser.add_subparsers(
        title="commands", dest="command", metavar="<command>"
    )

    # run
    p_run = subparsers.add_parser(
        "run",
        help="run a Kafal script on demo OHLCV data",
    )
    p_run.add_argument("file", help="path to .kf script")
    p_run.set_defaults(func=cmd_run)

    # check
    p_check = subparsers.add_parser(
        "check",
        help="validate a Kafal script (syntax / sandbox)",
    )
    p_check.add_argument("file", help="path to .kf script")
    p_check.set_defaults(func=cmd_check)

    # version
    p_version = subparsers.add_parser(
        "version",
        help="print Kafal CLI version",
    )
    p_version.set_defaults(func=cmd_version)

    # doctor
    p_doctor = subparsers.add_parser(
        "doctor",
        help="run self-diagnostics for the Kafal runtime",
    )
    p_doctor.set_defaults(func=cmd_doctor)

    # new
    p_new = subparsers.add_parser(
        "new",
        help="create a new .kf script from a template",
    )
    p_new.add_argument("name", help="base name for the script (with or without .kf)")
    p_new.add_argument(
        "--force",
        action="store_true",
        help="overwrite if file already exists",
    )
    p_new.set_defaults(func=cmd_new)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
