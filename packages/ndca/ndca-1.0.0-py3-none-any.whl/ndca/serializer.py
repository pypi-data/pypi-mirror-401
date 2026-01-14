import math
from typing import Any, Dict, List, Set

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

def _serialize_value(value: Any, path: str, visited: Set[int]) -> str:
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
        return _serialize_object(value, path, visited)
    if isinstance(value, (list, tuple)):
        return _serialize_list(list(value), path, visited)
    raise TypeError(f"unsupported type at {path}: {type(value).__name__}")

def _serialize_list(lst: List[Any], path: str, visited: Set[int]) -> str:
    obj_id = id(lst)
    if obj_id in visited:
        raise TypeError(f"circular reference detected at {path}")
    visited.add(obj_id)
    try:
        items: List[str] = []
        for i, v in enumerate(lst):
            item_path = f"{path}[{i}]"
            items.append(_serialize_value(v, item_path, visited) + ";")
        return "(" + "".join(items) + ")"
    finally:
        visited.remove(obj_id)

def _serialize_object(d: Dict[str, Any], path: str = "<root>", visited: Set[int] = None) -> str:
    if visited is None:
        visited = set()
    obj_id = id(d)
    if obj_id in visited:
        raise TypeError(f"circular reference detected at {path}")
    visited.add(obj_id)
    try:
        parts: List[str] = []
        parts.append("<")
        for k in sorted(d.keys()):
            if not isinstance(k, str):
                raise TypeError(f"keys must be strings at {path}, found {type(k).__name__}")
            v = d[k]
            key_path = f"{path}.{k}"
            parts.append("[" + k + "]=")
            parts.append(_serialize_value(v, key_path, visited) + ";")
        parts.append(">")
        return "".join(parts)
    finally:
        visited.remove(obj_id)

def serialize_object(d: Dict[str, Any]) -> str:
    if not isinstance(d, dict):
        raise TypeError("serialize_object expects a dict as top-level value")
    return _serialize_object(d, path="<root>", visited=set())