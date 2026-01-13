from typing import Any, List, Union, Optional, Dict, Tuple
import os
from .parser import NDCAParser, NDCAParseError
from .serializer import serialize_object
from .utils import atomic_write, normalize_path, deepcopy, merge_dicts

version = "0.1.0"

class NDCAError(Exception):
    pass

class NDCA:
    def __init__(self, filename: Optional[str] = None, autosave: bool = False):
        self._data: dict = {}
        self.filename: Optional[str] = None
        self.autosave = bool(autosave)
        self._dirty = False
        if filename:
            self.file(filename, autosave=self.autosave)

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
        parsed = self.loads(text)
        self._data = parsed
        self._dirty = False
        return self

    def save(self, filename: Optional[str] = None):
        path = filename or self.filename
        if not path:
            raise NDCAError("no filename")
        text = self.dumps(self._data)
        atomic_write(path, text)
        self._dirty = False
        return self

    def get(self, path: str, default: Any = None):
        keys, idxs = normalize_path(path)
        node = self._data
        try:
            for k in keys:
                if isinstance(node, dict):
                    node = node[k]
                else:
                    return default
            for idx in idxs:
                if isinstance(node, list) and 0 <= idx < len(node):
                    node = node[idx]
                else:
                    return default
            return deepcopy(node)
        except Exception:
            return default

    def write(self, path: str, value: Any):
        keys, idxs = normalize_path(path)
        if not keys:
            raise NDCAError("invalid path")
        node = self._data
        for k in keys[:-1]:
            if k not in node or not isinstance(node[k], dict):
                node[k] = {}
            node = node[k]
        last_key = keys[-1]
        if idxs:
            if last_key not in node or not isinstance(node[last_key], list):
                node[last_key] = []
            lst = node[last_key]
            for i, idx in enumerate(idxs):
                if i == len(idxs) - 1:
                    if idx == -1:
                        lst.append(deepcopy(value))
                    else:
                        if idx < 0:
                            raise NDCAError("negative index not allowed")
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
            node[last_key] = deepcopy(value)
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
        last_key = keys[-1]
        if last_key not in node:
            return self
        if idxs:
            target = node[last_key]
            if not isinstance(target, list):
                return self
            parent = target
            for i, idx in enumerate(idxs):
                if i == len(idxs) - 1:
                    if 0 <= idx < len(parent):
                        parent.pop(idx)
                else:
                    if 0 <= idx < len(parent):
                        parent = parent[idx]
                    else:
                        return self
        else:
            node.pop(last_key, None)
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

    def exists(self, path: str) -> bool:
        return self.get(path, object()) is not object()

    def dump(self) -> dict:
        return deepcopy(self._data)

    def load_from_text(self, text: str):
        self._data = self.loads(text)
        self._dirty = True
        if self.autosave and self.filename:
            self.save()
        return self

    def merge(self, other: Union[dict, 'NDCA']):
        src = other._data if isinstance(other, NDCA) else other
        self._data = merge_dicts(self._data, src)
        self._dirty = True
        if self.autosave and self.filename:
            self.save()
        return self

    def append(self, path: str, value: Any):
        keys, idxs = normalize_path(path)
        if not keys:
            raise NDCAError("invalid path")
        node = self._data
        for k in keys[:-1]:
            if k not in node or not isinstance(node[k], dict):
                node[k] = {}
            node = node[k]
        last_key = keys[-1]
        if last_key not in node or not isinstance(node[last_key], list):
            node[last_key] = []
        node[last_key].append(deepcopy(value))
        self._dirty = True
        if self.autosave and self.filename:
            self.save()
        return self

    def remove_from_list(self, path: str, value: Any):
        lst = self.get(path, None)
        if isinstance(lst, list):
            try:
                lst.remove(value)
                self.write(path, lst)
            except ValueError:
                pass
        return self

    def dumps(self, data: Optional[dict] = None) -> str:
        d = self._data if data is None else data
        return serialize_object(d)

    def loads(self, text: str) -> dict:
        parser = NDCAParser(text)
        return parser.parse()

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

def remove_from_list(path: str, value: Any):
    return _DEFAULT.remove_from_list(path, value)

def loads(text: str) -> dict:
    return NDCA().loads(text)

def dumps(data: dict) -> str:
    return NDCA().dumps(data)