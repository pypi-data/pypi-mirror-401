from typing import Any, List, Union, Optional, Dict, Tuple, Callable
import os
from .parser import NDCAParser
from .serializer import serialize_object
from .utils import atomic_write, normalize_path, deepcopy, merge_dicts

version = "1.0.0"

class NDCAError(Exception):
    pass

_sentinel = object()

class NDCA:
    def __init__(self, filename: Optional[str] = None, autosave: bool = False):
        self._data: dict = {}
        self.filename: Optional[str] = None
        self.autosave = bool(autosave)
        self._dirty = False
        if filename:
            self.file(filename, autosave=self.autosave)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.autosave and self._dirty and self.filename:
            self.save()
        return False

    def file(self, filename: str, autosave: Optional[bool] = None, create: bool = True):
        if autosave is not None:
            self.autosave = bool(autosave)
        self.filename = filename
        if os.path.exists(filename):
            self.load(filename)
        else:
            self._data = {}
            if create:
                self.save()
        return self

    def set_autosave(self, autosave: bool):
        self.autosave = bool(autosave)
        return self

    def load(self, filename: Optional[str] = None):
        path = filename or self.filename
        if not path:
            raise NDCAError("no filename")
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        self._data = self.loads(text)
        self._dirty = False
        return self

    def save(self, filename: Optional[str] = None):
        path = filename or self.filename
        if not path:
            raise NDCAError("no filename")
        atomic_write(path, self.dumps(self._data))
        self._dirty = False
        return self

    def get(self, path: str, default: Any = None):
        keys, idxs = normalize_path(path)
        node = self._data
        try:
            for k in keys:
                if not isinstance(node, dict):
                    return default
                node = node[k]
            for idx in idxs:
                if not isinstance(node, list) or not (0 <= idx < len(node)):
                    return default
                node = node[idx]
            return deepcopy(node)
        except Exception:
            return default

    def exists(self, path: str) -> bool:
        return self.get(path, _sentinel) is not _sentinel

    def dump(self) -> dict:
        return deepcopy(self._data)

    def write(self, path: str, value: Any):
        keys, idxs = normalize_path(path)
        if not keys:
            raise NDCAError("invalid path")
        node = self._data
        for k in keys[:-1]:
            if k not in node or not isinstance(node[k], dict):
                node[k] = {}
            node = node[k]
        last = keys[-1]
        if idxs:
            if last not in node or not isinstance(node[last], list):
                node[last] = []
            lst = node[last]
            for i, idx in enumerate(idxs):
                if i == len(idxs) - 1:
                    if idx == -1:
                        lst.append(deepcopy(value))
                    else:
                        if idx < 0:
                            raise NDCAError("negative index")
                        while idx >= len(lst):
                            lst.append(None)
                        lst[idx] = deepcopy(value)
                else:
                    while idx >= len(lst):
                        lst.append([])
                    if not isinstance(lst[idx], list):
                        lst[idx] = []
                    lst = lst[idx]
        else:
            node[last] = deepcopy(value)
        self._dirty = True
        if self.autosave and self.filename:
            self.save()
        return self

    def delete(self, path: str):
        keys, idxs = normalize_path(path)
        if not keys:
            return self
        node = self._data
        for k in keys[:-1]:
            if k in node and isinstance(node[k], dict):
                node = node[k]
            else:
                return self
        last = keys[-1]
        if last not in node:
            return self
        if idxs:
            target = node[last]
            if not isinstance(target, list):
                return self
            parent = target
            for i, idx in enumerate(idxs):
                if i == len(idxs) - 1:
                    if 0 <= idx < len(parent):
                        parent.pop(idx)
                else:
                    if 0 <= idx < len(parent) and isinstance(parent[idx], list):
                        parent = parent[idx]
                    else:
                        return self
        else:
            node.pop(last, None)
        self._dirty = True
        if self.autosave and self.filename:
            self.save()
        return self

    def wipe(self):
        self._data = {}
        self._dirty = True
        if self.autosave and self.filename:
            self.save()
        return self

    def keys(self):
        return list(self._data.keys())

    def merge(self, other: Union[dict, 'NDCA']):
        src = other._data if isinstance(other, NDCA) else other
        self._data = merge_dicts(self._data, src)
        self._dirty = True
        if self.autosave and self.filename:
            self.save()
        return self

    def append(self, path: str, value: Any):
        keys, _ = normalize_path(path)
        if not keys:
            raise NDCAError("invalid path")
        node = self._data
        for k in keys[:-1]:
            if k not in node or not isinstance(node[k], dict):
                node[k] = {}
            node = node[k]
        last = keys[-1]
        if last not in node or not isinstance(node[last], list):
            node[last] = []
        node[last].append(deepcopy(value))
        self._dirty = True
        if self.autosave and self.filename:
            self.save()
        return self

    def pop(self, path: str, default: Any = None):
        val = self.get(path, _sentinel)
        if val is _sentinel:
            return default
        self.delete(path)
        return val

    def update(self, path: str, fn: Callable[[Any], Any], default: Any = None):
        cur = self.get(path, default)
        self.write(path, fn(cur))
        return self

    def incr(self, path: str, step: Union[int, float] = 1):
        cur = self.get(path, 0)
        if not isinstance(cur, (int, float)):
            raise NDCAError("not numeric")
        self.write(path, cur + step)
        return self

    def toggle(self, path: str):
        cur = self.get(path, False)
        if not isinstance(cur, bool):
            raise NDCAError("not boolean")
        self.write(path, not cur)
        return self

    def rename(self, old_path: str, new_path: str):
        val = self.get(old_path, _sentinel)
        if val is _sentinel:
            return self
        self.write(new_path, val)
        self.delete(old_path)
        return self

    def clear_path(self, path: str):
        val = self.get(path, _sentinel)
        if val is _sentinel:
            return self
        if isinstance(val, dict):
            self.write(path, {})
        elif isinstance(val, list):
            self.write(path, [])
        else:
            self.delete(path)
        return self

    def dumps(self, data: Optional[dict] = None) -> str:
        return serialize_object(self._data if data is None else data)

    def loads(self, text: str) -> dict:
        return NDCAParser(text).parse()

_DEFAULT = NDCA()

def file(filename: str, autosave: bool = False):
    global _DEFAULT
    _DEFAULT = NDCA(filename, autosave=bool(autosave))
    return _DEFAULT

def get(path: str, default: Any = None):
    return _DEFAULT.get(path, default)

def write(path: str, value: Any):
    return _DEFAULT.write(path, value)

def delete(path: str):
    return _DEFAULT.delete(path)

def wipe():
    return _DEFAULT.wipe()

def load(filename: str, autosave: bool = False):
    return file(filename, autosave=autosave)

def save():
    return _DEFAULT.save()

def dump():
    return _DEFAULT.dump()

def keys():
    return _DEFAULT.keys()

def exists(path: str) -> bool:
    return _DEFAULT.exists(path)

def merge(other: Union[dict, NDCA]):
    return _DEFAULT.merge(other)

def append(path: str, value: Any):
    return _DEFAULT.append(path, value)

def pop(path: str, default: Any = None):
    return _DEFAULT.pop(path, default)

def update(path: str, fn: Callable[[Any], Any], default: Any = None):
    return _DEFAULT.update(path, fn, default)

def incr(path: str, step: Union[int, float] = 1):
    return _DEFAULT.incr(path, step)

def toggle(path: str):
    return _DEFAULT.toggle(path)

def rename(old_path: str, new_path: str):
    return _DEFAULT.rename(old_path, new_path)

def clear_path(path: str):
    return _DEFAULT.clear_path(path)

def loads(text: str) -> dict:
    return NDCA().loads(text)

def dumps(data: dict) -> str:
    return NDCA().dumps(data)