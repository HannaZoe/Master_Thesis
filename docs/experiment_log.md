# Experiment log

Running record of analysis attempts — what we tried, on what data, why, what
happened, and what we concluded. Includes failed attempts deliberately —
those are often the most useful record, since they stop us re-trying the
same dead end later. See `CLAUDE.md` for the instruction to keep this
updated.

Entry format:

```
## YYYY-MM-DD — Short title

**What we did:** the actual method/steps
**Data:** which files
**Thought:** the reasoning/hypothesis behind trying this
**Result:** what happened, numbers if applicable
**Conclusion:** what we learned/decided, and what's next
```

---

## 2026-08-10 — Closed-depression detection (DepthInSink), Stage 1: 20250604

**What we did:** Clipped the 20250604 Terra LiDAR DSM to its AOI, ran whitebox
`DepthInSink` (fills every sink, measures fill depth per pixel) to find closed
depressions. Thresholded at depth > 0.3 m, area > 4 m², vectorized to
polygons.

**Data:** `data/raw/20250604/20250604_terra_ppk_lidar_dsm.tif` (Terra LiDAR
DSM, 5 cm), `20250604_aoi.gpkg`.

**Thought:** Closed-depression/fill-difference analysis is the standard
method for DEM-based doline/sinkhole extraction in the karst geomorphometry
literature (Doctor & Doctor 2012; Obu & Podobnikar 2013; Wu et al. 2016).

**Result:** 19 candidates. Checked against the orthomosaic in QGIS — didn't
correspond to real dolines. Most of the AOI on this date is snow-covered;
snow drapes over the true topography and creates its own random depressions
(melt patterns, drifts), which the method picked up instead of karst
features. Includes one large (~8,900 m²) spurious feature.

**Conclusion:** Closed-depression analysis needs a snow-free DSM. Move to
20250820. See `notebooks/01_doline_detection_20250604.ipynb`.

---

## 2026-08-10 — Closed-depression detection retry: 20250820 (snow-free)

**What we did:** Same method (`DepthInSink`) on the August LiDAR DSM instead,
same initial thresholds (depth > 0.3 m, area > 4 m²).

**Data:** `data/raw/20250820/20250820_terra_ppk_lidar_dsm.tif`,
`20250820_aoi.gpkg`.

**Thought:** August should be a snow-free window at ~2000 m on the
Zugspitzplatt, removing the snow confound from the previous attempt.

**Result:** 167 candidates — far more than the ~30-35 dolines described from
imagery. Size-distribution check: 64% of candidates under 25 m², consistent
with bare-rock microkarst/boulder texture noise rather than dolines — not
snow this time, just the terrain's own roughness at 5 cm resolution.

**Conclusion:** Absolute depth/area thresholds are too permissive for bare,
rugged karst terrain. Refactored `src/master_thesis/dolines.py` to split the
slow whitebox step (`compute_depth_raster`) from thresholding
(`extract_depressions`) so thresholds could be swept cheaply without
re-running whitebox each time.

---

## 2026-08-10 — Threshold sweep + count-heuristic calibration (INVALIDATED)

**What we did:** Swept min_area (10/25/50/100 m²) × min_depth (0.3/0.5/1.0 m)
on the cached 20250820 depth raster. `min_area=50 m², min_depth=0.3 m` gave
35 candidates, close to the reported ~30-35 doline count from imagery.

**Data:** cached depth raster from the previous entry.

**Thought:** Count-matching as a quick calibration heuristic, pending a real
visual/ground-truth check — flagged explicitly at the time as "coincidence
worth checking, not validation."

**Result:** User checked visually in QGIS — method is unreliable; false
positives concentrate in areas of complex/sloped topography. Separately,
learned real doline diameters range ~30 cm–4 m (area up to ~12.6 m²) —
meaning the 50 m² threshold used here would have excluded nearly all real
dolines. The 35-candidate count match was coincidental, not a genuine
calibration signal.

**Conclusion:** Absolute-threshold approach abandoned. Root cause:
`DepthInSink` measures depth relative to a *global* fill — on a slope, any
step/ledge/boulder terrace reads as a false closed depression regardless of
which area/depth thresholds are chosen. The method conflates slope roughness
with real collapse features.

---

## 2026-08-10 — Decision: switch to local-relief (TPI-style) method, pause for manual ground truth

**What we did:** Identified whitebox `DevFromMeanElev` (deviation from mean
elevation within a local window — unnormalized Topographic Position Index)
as the fix: measures a cell's anomaly relative to its neighborhood, which
cancels out the regional slope trend instead of using an absolute depth.
Matches the approach in Obu & Podobnikar (2013), already in the thesis's own
background reading.

**Thought:** This method is sensitive to neighborhood window size, which
needs to roughly match real doline scale — and with dolines ranging ~30 cm–4 m
(a >13x range) at 5 cm resolution, the target signal and the confounding
rock-texture noise are close to the same spatial scale. A single window size
will inherently favor one end of that range. Rather than guess a third
threshold set blind, decided to wait for real ground truth.

**Where we landed:** User is manually mapping real dolines (point at center +
outline polygon) from the orthomosaic in QGIS. Once available (~10+
examples), plan is to compute `DevFromMeanElev` at multiple window sizes at
the known doline locations vs. background terrain, and pick window
size/threshold empirically from that — actual calibration against ground
truth instead of another guess. Also gives the thesis a defensible number
("method X correctly identifies Y% of manually mapped dolines") rather than
a coincidental count match.

Next: Claude to prepare a structured geopackage template (point + polygon
layers, linked by ID) for the manual mapping.
