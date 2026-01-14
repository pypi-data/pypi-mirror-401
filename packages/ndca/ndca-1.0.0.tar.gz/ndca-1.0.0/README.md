NDCA 1.0.0 — Nested Data Collection API

NDCA (Nested Data Collection API) is a high-performance, secure, and production-ready Python library for managing deeply nested structured data using a compact, human-readable format. It is designed for reliability, atomic persistence, safe in-memory operations, and a clean, intuitive API suitable for scripts, services, and small-to-medium projects.

Key Features:
- **Human-readable format:** Store and read nested dictionaries and lists in a clear, concise structure.
- **Safe operations:** All reads and writes use deep-copy semantics to prevent accidental mutation.
- **Atomic file writes:** Data is safely persisted to disk, ensuring integrity even during crashes or interruptions.
- **Optional autosave:** Automatically save changes to the assigned file (`file("x.ndca", autosave=True)`).
- **Flexible path-based access:** Get, write, and delete nested values using dot notation for dictionaries (`a.b.c`) and bracket notation for lists (`arr[0]`, `arr[]`).
- **Merge and append:** Merge dictionaries (`merge`) or append items to lists (`append`) effortlessly.
- **Pop and update:** Remove or retrieve values (`pop(path, default)`) and update values with a callback (`update(path, fn, default)`).
- **Numeric and boolean utilities:** Increment numbers (`incr(path, step)`) and toggle booleans (`toggle(path)`).
- **Key management:** Rename keys or paths (`rename(old_path, new_path)`) and clear any path safely (`clear_path(path)`).
- **Full serialization support:** Convert to and from NDCA text format (`dumps(data)` / `loads(text)`).
- **Version:** 1.0.0 — stable, fully-featured, and production-ready.

Usage Example:
```python
from ndca import NDCA, file, get, write, delete, wipe, save, dump, merge, append, pop, update, incr, toggle, rename, clear_path, loads, dumps

db = NDCA("data.ndca", autosave=True)
db.write("user.name", "Viren")
db.append("user.scores", 10)
db.incr("user.level")
db.toggle("user.active")
db.rename("user.name", "user.username")
text = db.dumps()
new_data = loads(text)