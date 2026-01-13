import os
import tempfile
import io
from typing import Tuple, List, Any

def atomic_write(path: str, data: str, fsync: bool = True) -> None:
    dirpath = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmppath = tempfile.mkstemp(prefix=".ndca-", dir=dirpath)
    try:
        with io.open(fd, "w", encoding="utf-8") as f:
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
    finally:
        if os.path.exists(tmppath):
            try:
                os.remove(tmppath)
            except Exception:
                pass

def normalize_path(path: str) -> Tuple[List[str], List[int]]:
    if not isinstance(path, str):
        raise ValueError("path must be string")
    p = path.strip()
    if p.startswith("[") and p.endswith("]"):
        p = p[1:-1]
    if p == "":
        return [], []
    parts = p.split(".")
    keys = []
    idxs = []
    for part in parts:
        if part == "":
            continue
        if "[" in part and part.endswith("]"):
            name, rest = part.split("[",1)
            idxpart = rest[:-1]
            keys.append(name)
            if idxpart == "":
                idxs.append(-1)
            else:
                try:
                    idxs.append(int(idxpart))
                except Exception:
                    raise ValueError("invalid index")
        else:
            keys.append(part)
    return keys, idxs

def deepcopy(obj: Any):
    if isinstance(obj, dict):
        return {k: deepcopy(v) for k,v in obj.items()}
    if isinstance(obj, list):
        return [deepcopy(v) for v in obj]
    return obj

def merge_dicts(a: dict, b: dict) -> dict:
    res = deepcopy(a)
    for k,v in b.items():
        if k in res and isinstance(res[k], dict) and isinstance(v, dict):
            res[k] = merge_dicts(res[k], v)
        else:
            res[k] = deepcopy(v)
    return res