import math
from typing import Any, Dict, List

def _escape_string(s: str) -> str:
    sb = ['"']
    for ch in s:
        if ch == '"':
            sb.append('\\"')
        elif ch == '\\':
            sb.append('\\\\')
        elif ch == '\n':
            sb.append('\\n')
        elif ch == '\r':
            sb.append('\\r')
        elif ch == '\t':
            sb.append('\\t')
        else:
            sb.append(ch)
    sb.append('"')
    return "".join(sb)

def _serialize_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        if math.isfinite(value):
            return repr(value)
        return "null"
    if isinstance(value, str):
        return _escape_string(value)
    if isinstance(value, dict):
        return _serialize_object(value)
    if isinstance(value, list):
        items = []
        for v in value:
            items.append(_serialize_value(v) + ";")
        return "(" + "".join(items) + ")"
    raise TypeError("unsupported type")

def _serialize_object(d: Dict[str, Any]) -> str:
    parts = []
    parts.append("<")
    for k, v in d.items():
        if not isinstance(k, str):
            raise TypeError("keys must be strings")
        parts.append("[" + k + "]=")
        parts.append(_serialize_value(v))
        parts.append(";")
    parts.append(">")
    return "".join(parts)

def serialize_object(d: Dict[str, Any]) -> str:
    return _serialize_object(d)