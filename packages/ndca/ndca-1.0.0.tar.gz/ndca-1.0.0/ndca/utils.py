import os
import tempfile
from typing import Tuple, List, Any


def atomic_write(path: str, data: str, fsync: bool = True) -> None:
    dirpath = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmppath = tempfile.mkstemp(prefix=".ndca-", dir=dirpath)
    try:
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(data)
                f.flush()
                if fsync:
                    try:
                        os.fsync(f.fileno())
                    except Exception:
                        pass
            os.replace(tmppath, path)
            if fsync:
                try:
                    dirfd = os.open(dirpath, os.O_DIRECTORY)
                    try:
                        os.fsync(dirfd)
                    finally:
                        os.close(dirfd)
                except Exception:
                    pass
        except Exception:
            try:
                if os.path.exists(tmppath):
                    os.remove(tmppath)
            except Exception:
                pass
            raise
    finally:
        if os.path.exists(tmppath):
            try:
                os.remove(tmppath)
            except Exception:
                pass


def normalize_path(path: str) -> Tuple[List[str], List[int]]:
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    p = path.strip()
    if p == "":
        return [], []
    if p.startswith("[") and p.endswith("]") and p.count("[") == 1:
        p = p[1:-1].strip()
    parts = p.split(".")
    keys: List[str] = []
    idxs: List[int] = []
    for part in parts:
        if part == "":
            continue
        name = ""
        i = 0
        L = len(part)
        while i < L and part[i] != "[":
            name += part[i]
            i += 1
        if name == "":
            raise ValueError(f"invalid path segment: '{part}'")
        keys.append(name)
        if i < L:
            if part[i] != "[" or not part.endswith("]"):
                raise ValueError(f"invalid bracket syntax in segment: '{part}'")
            idx_text = part[i + 1 : -1].strip()
            if idx_text == "":
                idxs.append(-1)
            else:
                try:
                    idx_val = int(idx_text)
                except Exception:
                    raise ValueError(f"invalid index in segment: '{part}'")
                if idx_val < -1:
                    raise ValueError(f"negative index not allowed (except -1) in '{part}'")
                idxs.append(idx_val)
    return keys, idxs


def deepcopy(obj: Any, _memo: dict = None) -> Any:
    if _memo is None:
        _memo = {}
    obj_id = id(obj)
    if obj_id in _memo:
        return _memo[obj_id]
    if isinstance(obj, dict):
        res = {}
        _memo[obj_id] = res
        for k, v in obj.items():
            res[k] = deepcopy(v, _memo)
        return res
    if isinstance(obj, list):
        res = []
        _memo[obj_id] = res
        for v in obj:
            res.append(deepcopy(v, _memo))
        return res
    if isinstance(obj, tuple):
        res = tuple(deepcopy(v, _memo) for v in obj)
        _memo[obj_id] = res
        return res
    if isinstance(obj, set):
        res = set(deepcopy(v, _memo) for v in obj)
        _memo[obj_id] = res
        return res
    return obj


def merge_dicts(a: dict, b: dict) -> dict:
    if not isinstance(a, dict) or not isinstance(b, dict):
        raise TypeError("merge_dicts expects two dicts")
    res = deepcopy(a)
    for k, v in b.items():
        if k in res and isinstance(res[k], dict) and isinstance(v, dict):
            res[k] = merge_dicts(res[k], v)
        else:
            res[k] = deepcopy(v)
    return res