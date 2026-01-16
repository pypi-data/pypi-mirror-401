from __future__ import annotations

from typing import Any, Dict, List, Optional

import shlex


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


def parse_input_line(
    line: str,
    *,
    inputs: Dict[str, Any],
    inputs_schema: Dict[str, Any],
) -> None:
    """
    Parse an input declaration.

    Supported (both forms):

      @input len:int = 14 min=1 max=100 step=1 title="Length" group="Trend" order=1
      input len:int = 14 min=1 max=100 step=1 title="Length" group="Trend" order=1

      @input src:enum = close options="open,high,low,close" title="Source"
      input src:enum = close options="open,high,low,close" title="Source"

    Mutates:
      - inputs_schema[name] = schema dict
      - inputs[name] = default (only if not already overridden)
    """
    if not isinstance(line, str):
        return

    raw = line.strip()
    if not raw:
        return

    if raw.startswith("@input"):
        body = raw[len("@input") :].strip()
    elif raw.startswith("input"):
        body = raw[len("input") :].strip()
    else:
        return

    if not body:
        # nothing after "input"
        return

    # Split main "name:type" (and maybe inline default) from optional attrs.
    parts = body.split()
    if not parts:
        return

    header = parts[0]
    attr_parts = parts[1:]

    name: Optional[str] = None
    typ = "float"
    default: Any = None
    default_ref: Optional[str] = None
    kind: Optional[str] = None
    options: Optional[List[str]] = None

    # Header: name:type or name
    if ":" in header:
        name_part, type_part = header.split(":", 1)
        name = name_part.strip()
        typ = type_part.strip().lower()
    else:
        name = header.strip()

    if not name:
        # No usable input name
        return

    # Detect inline default like len:int=14 or len=14
    if "=" in header and header.find("=") > header.find(":"):
        name_type, default_str = header.split("=", 1)
        if ":" in name_type:
            name_part, type_part = name_type.split(":", 1)
            name = name_part.strip() or name
            typ = type_part.strip().lower() if type_part.strip() else typ
        else:
            name = name_type.strip() or name
        default = default_str.strip()

    # If default not in header, try attr_parts pattern: name:type = default
    # Example tokens: ["=", "14", "min=1", ...]
    if default is None and attr_parts:
        for idx, p in enumerate(attr_parts):
            if p == "=" and 0 < idx < (len(attr_parts) - 1):
                default = attr_parts[idx + 1]
                attr_parts = attr_parts[:idx] + attr_parts[idx + 2 :]
                break

    # Fallback: last token if numeric (common shorthand)
    if default is None and attr_parts:
        last = attr_parts[-1]
        if last and (_is_int(last) or _is_float(last)):
            default = last
            attr_parts = attr_parts[:-1]

    # Parse extra attributes:
    # min= max= step= title="..." group="..." order= group_order= options="a,b"
    attrs: Dict[str, Any] = {}
    attr_str = " ".join(attr_parts).strip()

    if attr_str:
        try:
            tokens = shlex.split(attr_str, posix=True)
        except ValueError:
            tokens = attr_str.split()

        for tok in tokens:
            if "=" not in tok:
                continue
            k, v = tok.split("=", 1)
            k = k.strip()
            v = v.strip()
            if not k:
                continue

            if k in ("min", "max", "step", "order", "group_order"):
                if _is_int(v):
                    attrs[k] = int(v)
                elif _is_float(v):
                    attrs[k] = float(v)
                else:
                    # Keep non-numeric as string (don't drop it)
                    attrs[k] = v
            elif k == "options":
                # options="a,b,c"
                opts = [s.strip() for s in v.split(",") if s.strip()]
                options = opts
            elif k in ("title", "group"):
                attrs[k] = v
            else:
                attrs[k] = v

    # Normalize type/kind
    if typ in ("enum", "string-list"):
        kind = "enum"
    elif typ in ("bool", "boolean"):
        kind = "bool"
    elif typ in ("int", "integer"):
        kind = "int"
    elif typ in ("float", "price"):
        kind = "float"
    else:
        kind = "string"

    # Convert default; for enum/source we allow env ref (store in default_ref)
    if default is not None:
        if kind == "int" and _is_int(default):
            default = int(default)
        elif kind == "float" and _is_float(default):
            default = float(default)
        elif kind == "bool":
            default = str(default).lower() in ("true", "1", "yes")
        else:
            default_str = str(default)
            default = default_str
            default_ref = default_str

    schema: Dict[str, Any] = {
        "name": name,
        "type": typ,  # original type string from script
        "kind": kind,  # normalized kind for UI
        "default": default,
    }

    if default_ref is not None:
        schema["default_ref"] = default_ref

    if options is not None:
        schema["options"] = options

    schema.update(attrs)
    inputs_schema[name] = schema

    # If no external override, set default now (host can still override via set_inputs before run)
    if name not in inputs and default is not None:
        inputs[name] = default


def parse_define_line(
    line: str,
    *,
    meta: Dict[str, Any],
) -> None:
    """
    Parse a define declaration.

    Example:

      define name="My Indicator" short_name="MyInd" overlay=true precision=2
      define category="momentum" tags="rsi,trend"

    Mutates meta dict in-place.
    """
    if not isinstance(line, str):
        return

    raw = line.strip()
    if not raw.startswith("define"):
        return

    body = raw[len("define") :].strip()
    if not body:
        return

    try:
        tokens = shlex.split(body, posix=True)
    except ValueError:
        tokens = body.split()

    for tok in tokens:
        if "=" not in tok:
            continue
        k, v = tok.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            continue

        # Normalize common keys
        if k == "short_name":
            k = "shortname"

        low = v.lower()
        if low in ("true", "false"):
            meta[k] = (low == "true")
        elif _is_int(v):
            meta[k] = int(v)
        elif _is_float(v):
            meta[k] = float(v)
        else:
            meta[k] = v
