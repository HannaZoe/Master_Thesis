# EAGLE Master Thesis

## Academic context

**Topic:** Collapse dolines (sinkholes) on the Zugspitzplatt — surface change,
subsurface processes, and geohazard characterization.

**Program:** M.Sc. EAGLE (Applied Earth Observation and Geoanalysis),
University of Würzburg.

**People:**
- Prof. Tobias Ullmann (Uni Würzburg, remote sensing) — primary supervisor
- Dr. Djamil Al-Halbouni (Uni Leipzig, geology/geophysics) — co-supervisor
- Elio Rauth (PhD student, Uni Würzburg) — field collaborator, source of the
  original UAV datasets and field access

**Background:** Elio's UAV surveys of the Zugspitzplatt (Sonnalpin–Knorrhütte
route) show 30–35 collapse dolines of varied morphology (water-filled/dry,
size, possible spatial clustering). Dolines as a standalone subject are
under-studied here specifically — the area is well covered for hydrogeology
(Goldscheider et al. 2014) and permafrost, plus one palaeoclimate-archive
paper on a single doline (Grüger & Jerz, 2010/2011), but not as a
geomorphological phenomenon in its own right. Open question: are these driven
by (glacio)karst dissolution, permafrost thaw, or both interacting — a link
with some precedent elsewhere (Veress 2012/2017/2024; Securo et al. 2022;
Colucci & Guglielmin 2019) but thin evidence in this specific alpine setting.
Connects to documented permafrost degradation on the Zugspitze (Wagner et al.
2023; Schröder & Krautblatt 2018). Related to Hanna's prior Dead Sea sinkhole
work (with Eoghan Holohan/UCD and Djamil Al-Halbouni; EGU 2023; under review
as egusphere-2025-5280, NHESS) — same collapse-doline dynamics, different
setting (evaporite karst vs. alpine glaciokarst).

**Research directions (not finalized, will narrow over time):**
1. Surface change time series — multi-temporal UAV optical/LiDAR comparison,
   Sentinel-1 SAR for subsidence/displacement, Bavarian DGM1 as a pre-UAV
   baseline.
2. Subsurface/process understanding — thermal UAV for surface-temperature
   anomalies (permafrost degradation signatures); correlating doline activity
   with precipitation, snowmelt timing, Zugspitze summit air temperature.
3. Geohazard assessment — spatial risk mapping of active/expanding features
   relative to hiking infrastructure; a transferable change-detection method
   for inaccessible high-alpine karst terrain.

**Data sources (expected, not all confirmed):**
- Elio's UAV campaigns (Oct 2024, Jun 2025, Aug 2025) — RGB, multispectral,
  LiDAR, thermal
- New UAV acquisition, fieldwork 26–28 Aug 2026 — photogrammetry, LiDAR,
  thermal
- Sentinel-1 SAR — multi-temporal InSAR
- Bavarian DGM1 — 1 m airborne LiDAR DEM, CC BY 4.0, geodaten.bayern.de,
  native CRS ETRS89/UTM32N (EPSG:25832)
- Planet Labs archive (SuperDove/SkySat) — possible, via Werkstudent access,
  unconfirmed
- Zugspitze summit station — precipitation, snowmelt timing, air temperature
- Proposed geophysical fieldwork (pending Djamil): ERT profiles, passive
  seismic/HVSR (preferred over ERT/MASW for logistics on bare alpine karst),
  possibly soil temperature loggers, dGNSS/RTK rim monitoring, TLS for
  steep/overhanging walls

**Timeline:** fieldwork 26–28 August 2026.

## Working conventions

- Write code like a senior EO researcher: concise, correct, readable — not
  verbose, not over-engineered. Reach for well-maintained packages
  (`geopandas`, `rasterio`, `laspy`, `open3d`, `whitebox`, `scipy`,
  `scikit-learn`, ...) over hand-rolling something they already do well.
- When a domain/methodological choice is genuinely ambiguous (delineation
  method, permafrost proxy, which CRS/transform, statistical test choice),
  ask rather than guessing — a wrong scientific assumption is more expensive
  than a clarifying question.
- Before committing to an analysis approach, actively look for what's wrong
  with it first — question assumptions, check for confounds, sanity-check
  against known values/literature — the way a critical reviewer would, rather
  than running with the first plausible approach. Say so out loud if
  something looks off, even mid-task.
- Ground methods in published approaches where they exist (karst
  geomorphology, permafrost remote sensing, UAV photogrammetry/LiDAR
  processing) rather than improvising a novel method by default.
- Run `uv run ruff check --fix` and `uv run ruff format` before any commit —
  lint-clean is a precondition for committing, not a follow-up step.
- No AI attribution in git history — plain commit messages, no
  "Co-Authored-By: Claude" / "Generated with Claude Code" trailers.

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
- **Linting**: `ruff` (check + format), dev dependency — see Working conventions.

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
uv run ruff check --fix && uv run ruff format   # lint + format before committing
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

## Data & CRS conventions

- Coordinate reference systems: state the CRS explicitly in every script/
  notebook that reads or writes spatial data — don't rely on an implicit
  default. Bavarian state data (DGM1 etc.) natively uses ETRS89/UTM32N
  (EPSG:25832) — treat that as the project's default working CRS unless a
  specific dataset/analysis calls for another (e.g. UAV processing in a local
  project CRS, or a geographic CRS for Sentinel-1 products).
- File naming: lowercase, hyphen-separated, no spaces (matches the rest of
  this repo's convention).
- Large binary data never gets committed to git, even in `data/processed/` —
  see `data/CLAUDE.md` for where it actually lives.
