# EAGLE Master Thesis

Master thesis project for the EAGLE (Erasmus Mundus Master in GIScience)
programme. Working with UAV/drone photogrammetry point clouds, QGIS, and
Python.

See [CLAUDE.md](CLAUDE.md) for the full project setup, stack, and conventions.

## Quickstart

```powershell
uv sync              # install Python dependencies into .venv
uv run jupyter lab     # explore data in notebooks/
```

## Structure

- `data/` — raw / interim / processed data (not tracked in git, see `data/CLAUDE.md`)
- `src/master_thesis/` — reusable Python package
- `notebooks/` — exploratory analysis
- `qgis/projects/` — QGIS project files
- `outputs/` — generated figures and maps
- `docs/thesis/` — thesis writing
- `tests/` — tests for `src/`
