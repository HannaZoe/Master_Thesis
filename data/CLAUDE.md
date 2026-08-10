# data/

Nothing in this folder is tracked in git (see root `.gitignore`) except the
`.gitkeep` placeholders that keep the folder structure visible. Point cloud
and raster data are too large and not text-diffable, so git is the wrong tool
for them.

- `raw/` — data exactly as received (from the drone processing pipeline,
  a supervisor, an open dataset, etc.). Never edit or overwrite files here.
  If a source needs correcting, that's a new file, not an edit.
- `interim/` — intermediate outputs of a processing step that aren't the
  final product (e.g. a filtered point cloud before classification).
  Safe to delete and regenerate from `raw/` + a script in `src/`.
- `processed/` — final, analysis-ready outputs (e.g. a CHM, a classified
  point cloud). Also regenerable from `raw/` + code — don't treat this as
  a permanent store either.

## Naming convention (Elio's UAV deliverables)

Files follow `{date}_{software}_{positioning}_{sensor}_{product}.tif`,
one folder per acquisition date under `raw/`:

- **software**: `agisoft` (Agisoft Metashape, SfM photogrammetry) · `terra`
  (DJI Terra — used for the LiDAR-derived products and one RGB reprocess)
- **positioning**: `rtk` (real-time kinematic GNSS) · `ppk` (post-processed
  kinematic GNSS — generally more accurate, applied after the flight)
- **sensor**: `rgb` · `ms` (multispectral) · `lidar`
- **product**: `dsm` (digital surface model, raster) · `om` (orthomosaic,
  raster)

Keep this convention for anything new that lands in `raw/` — new campaign =
new `YYYYMMDD/` folder, same filename pattern.

## Current contents (as of 2026-08-10)

| Date | Sensor(s) | Products | Notes |
|---|---|---|---|
| `20241025/` | RGB, multispectral, LiDAR | Agisoft MS DSM/OM, Terra LiDAR DSM, Terra RGB DSM/OM, `aoi.gpkg` | Earliest campaign |
| `20250604/` | RGB, multispectral, LiDAR | Agisoft MS DSM/OM, Terra LiDAR DSM, Terra RGB DSM/OM, `aoi.gpkg` | Most complete campaign |
| `20250606/` | RGB | Agisoft RGB DSM/OM | |
| `20250717/` | RGB | Agisoft RGB DSM/OM | |
| `20250820/` | RGB, LiDAR | Terra LiDAR DSM, Terra RGB DSM/OM, `aoi.gpkg` | Most recent campaign |

All Terra-derived DSMs are EPSG:32632 (WGS84/UTM 32N), ~5 cm resolution.
Agisoft multispectral products are delivered in EPSG:4326 (geographic) —
need reprojecting to EPSG:32632 before any spatial analysis (area/depth
calculations are meaningless in degrees). Per-date raster extents differ
slightly (flight coverage varies), so cross-date comparison needs clipping
to a common overlap or the AOI polygon first.

**Three dates now have LiDAR DSMs** (`20241025`, `20250604`, `20250820`),
spanning Oct 2024 → Aug 2025 (~10 months) — enough for real change detection,
not just single-date morphology mapping.

~24 GB total. **No raw point cloud files (`.las`/`.laz`)** — everything is
already-rasterized DSM/orthomosaic output from Agisoft/DJI Terra. If
point-cloud-level processing is needed (custom classification, ground/canopy
separation) rather than working from the DSMs as delivered, raw `.las`/`.laz`
files would need to be requested from Elio separately. Thermal data hasn't
arrived either.

## Where the actual data lives

Local disk only, directly under `data/raw/` etc. on this machine (the tower).
Coding/processing work happens only on this device for now — no cross-machine
sync (bwSync&Share client didn't work out, OneDrive's 10 GB quota is too
small for point cloud data anyway). Revisit if that changes.

No backup currently exists beyond this one machine. Elio's UAV data (and
anything from the August 2026 fieldwork) is not reproducible if lost, so at
minimum an occasional manual copy to an external drive is worth doing once
real data lands here — flagging this now rather than after something goes
wrong.
