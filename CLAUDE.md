# EAGLE Master Thesis

## Status

Setup phase — topic and research question not yet finalized. Working assumption:
point cloud data will come from UAV/drone photogrammetry (structure-from-motion),
not airborne LiDAR or TLS. Update this section once the topic is locked in —
it should always state the current research question in one or two sentences.

## Stack

- **Python**: managed with `uv`, not conda. Deliberate choice — see "Why uv, not
  conda" below before suggesting a switch.
- **Editor**: VS Code.
- **GIS**: QGIS (standalone install) for visualization, cartography, and manual
  vector/raster inspection. Analysis and processing live in Python scripts/
  notebooks, not QGIS's own Python console, so work stays scriptable and
  reproducible. QGIS project files live in `qgis/projects/`.
- **Point clouds**: `laspy` (+ `lazrs` for LAZ compression) for I/O, `open3d`
  for registration/filtering/visualization, `whitebox` for terrain/raster
  derivatives. No PDAL — see below.
- **Raster/vector**: `rasterio`, `geopandas`, `shapely`, `pyproj`, `fiona`.

### Why uv, not conda

Geospatial packages (GDAL, PDAL) are notoriously hard to install via plain pip
on Windows because they wrap C++ libraries without official wheels. Conda-forge
normally solves this, but the explicit choice here is `uv`. Consequences:

- **PDAL is intentionally excluded** from dependencies — no reliable pip/uv
  install path on Windows. If a task genuinely needs PDAL (e.g. a specific
  filter only PDAL implements), the options are: (a) find an `open3d`/`laspy`/
  `whitebox` equivalent first, (b) call the PDAL CLI via subprocess if it's
  installed separately (e.g. bundled with QGIS/OSGeo4W), or (c) flag it to the
  user rather than silently trying to pip-install it.
- `rasterio`, `fiona`, `pyproj`, `shapely` all ship self-contained wheels on
  Windows, so they're safe to use freely.
- If GDAL-level functionality is needed beyond what `rasterio`/`fiona` expose,
  prefer calling QGIS's bundled GDAL/Python via subprocess over trying to pip
  install `gdal` directly.

## Environment setup

```powershell
uv sync              # creates .venv and installs locked dependencies
uv add <package>      # add a new dependency (updates pyproject.toml + lockfile)
uv run python ...     # run a script inside the project environment
uv run jupyter lab     # launch JupyterLab
```

Point VS Code's Python interpreter at `.venv\Scripts\python.exe` in this folder.

## Folder map

```
Master/
├── data/            raw / interim / processed — see data/CLAUDE.md, not tracked in git
├── src/master_thesis/   installable package — see src/CLAUDE.md
├── notebooks/       exploratory analysis (Jupyter)
├── qgis/projects/   .qgz/.qgs project files (tracked in git — small XML/sqlite)
├── outputs/         figures/ and maps/ — regenerable, gitignored
├── docs/thesis/     the actual thesis writing
└── tests/           tests for code in src/
```

## Conventions

- Coordinate reference systems: state the CRS explicitly in every script/
  notebook that reads or writes spatial data — don't rely on an implicit
  default. Note the project's standard working CRS here once chosen.
- File naming: lowercase, hyphen-separated, no spaces (matches the rest of
  this repo's convention).
- Large binary data never gets committed to git, even in `data/processed/` —
  see `data/CLAUDE.md` for where it actually lives.
