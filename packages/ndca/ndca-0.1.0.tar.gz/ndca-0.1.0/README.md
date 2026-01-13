# NDCA 0.1.0 — Nested Data Collection API

NDCA (Nested Data Collection API) is a fast, secure, and production-ready Python library for storing, reading, and manipulating nested structured data using a compact human-readable format. NDCA is designed for robustness, atomic persistence, safe in-memory operations and an ergonomic API suitable for scripts, services and small-to-medium projects.

---

## Highlights

- Human-readable NDCA format for nested objects and lists  
- Deep-copy safety on reads/writes to avoid accidental mutation  
- Atomic file writes to protect data integrity on crashes or interruptions  
- Optional autosave per-file instance (`file("x.ndca", autosave=True)`)  
- Path-based get/write/delete API supporting nested keys and list indices  
- Merge, append, remove-from-list, dump/load-from-text, and CLI-friendly behavior  
- Version `0.1.0` — stable initial feature set