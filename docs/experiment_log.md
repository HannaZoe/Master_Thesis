# Experiment log

Running record of analysis attempts — what we tried, on what data, why, what
happened, and what we concluded. Includes failed attempts deliberately —
those are often the most useful record, since they stop us re-trying the
same dead end later. See `CLAUDE.md` for the instruction to keep this
updated.

## Parking lot (later, not now)

Ideas raised mid-work that are deliberately deferred — not forgotten, just
not blocking the current task.

- Mapped dolines are visibly **not circular** — don't lean on circularity as
  a validation/filter criterion once we get to polygon delineation.
- Correlate doline locations/clustering with mapped geological fault lines
  once detection is working — ties into the karst-vs-permafrost research
  question. Fault dataset now sourced, see 2026-08-22 entry below — digitize
  Ortner & Kilian (2022) Fig. 7b and test alignment.
- Test whether doline growth/activity correlates with remotely-sensed
  snow-cover *thinning date* specifically (not just snowmelt volume/timing
  or precipitation) — motivated by Küfmann (2013)'s CO2-limited dissolution
  finding, see 2026-08-22 entry.
- Split the 30-35 mapped features into an old/stable vs. young/active
  population by morphometry (Péntek et al. 2007 shape-fitting; Veress 2017
  diameter/depth/slope baselines) rather than treating them as one
  homogeneous population — motivated by Grüger & Jerz (2011)'s dating of one
  doline to >7000 BP, see 2026-08-22 entry.

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

---

## 2026-08-10 — DevFromMeanElev calibration against 13 manual points

**What we did:** User manually mapped 13 obvious dolines as center points
(`data/manual/Sinkholes.shp`, points only so far, no polygons/diameters
recorded yet). Computed `DevFromMeanElev` at 6 window widths (0.5/1/2/3/5/8 m)
on the 20250820 LiDAR DSM, sampled the value at each manual point and at 200
random background points (excluding a 2 m buffer around manual points), and
compared recall (% of manual points below a threshold) against background
false-positive rate at each window/threshold combination.

**Data:** `data/manual/Sinkholes.shp` (13 points, reprojected from EPSG:4326
to EPSG:32632), cached `20250820` clipped LiDAR DSM.

**Thought:** With real ground truth available, calibrate window size and
threshold empirically instead of guessing — see previous entry.

**Result:** No window/threshold gives clean separation — every combination
has some overlap between manual dolines and background. Best working zone:
**window=5 m, threshold≈-0.3 m** → 77% recall (10/13) at 8% background
false-positive rate. Counterintuitively, smaller windows closer to the
actual doline diameter (0.5-1 m) separate *worse* than the 5 m window, not
better — worth keeping in mind for the methods write-up. With only 13
points, these percentages are coarse (~8 percentage points per point) and
should be treated as a working direction, not a final number.

**Conclusion:** DevFromMeanElev is a real, usable signal (a large
improvement over DepthInSink's slope confound), but not a clean detector on
its own — likely reflects genuine variation in how strong the depression
signal is across a 30 cm-4 m size range, not just method inadequacy. Next:
either map more points for tighter calibration, or run a full detection
pass at window=5m/threshold=-0.3 now and validate visually, or both.
Decision pending user input.

---

## 2026-08-10 — Deeper calibration: 19 points, leave-one-out, DepthInSink combo

**What we did:** User mapped 6 more points (19 total). Expanded window sweep
to 10 widths (0.5-10 m), fine threshold grid, picked best (window,
threshold) per window by Youden's J (recall - background FPR). Then ran
leave-one-out cross-validation over the 19 points (refit window/threshold on
the other 18 each time) to check the choice isn't overfit to these exact
points. Also tested combining DevFromMeanElev with a DepthInSink closedness
requirement (real hydrological sink, not just a locally-low spot), to see if
it screens out linear-gully false positives.

**Data:** `data/manual/Sinkholes.shp` (19 points), 300 background points,
20250820 clipped LiDAR DSM.

**Result:**
- Full-data fit: window=4 m, threshold=-0.22 → recall 84%, background FPR 11%.
- **Leave-one-out: 79% recall (15/19)**, window=4 m chosen in 18/19 folds —
  stable choice, not noise.
- Combining with DepthInSink made things *worse*: recall dropped to 53% for
  only a small FPR improvement (11% -> ~2%). Many real dolines apparently
  don't register as a strongly "closed" sink in DepthInSink's global-fill
  sense, even though DevFromMeanElev picks up their local relief fine.

**Conclusion:** Current best practical method: **DevFromMeanElev, window=4m,
threshold≈-0.2 to -0.22**, ~79-84% recall at ~11% background false-positive
rate. Not combining with DepthInSink. Next: tested whitebox `Geomorphons`
(pit vs. valley landform classification, Jasiewicz & Stepinski 2013) as a
more targeted alternative to the closedness idea — see next entry.

---

## 2026-08-10 — Geomorphons as a supplementary filter (also didn't help)

**What we did:** Computed whitebox `Geomorphons` (search=80 px, forms mode —
classifies each cell into 10 landform types: flat/peak/ridge/shoulder/spur/
slope/hollow/footslope/valley/pit). Checked which classes real dolines fall
into, then tested combining "pit OR hollow" with the DevFromMeanElev
threshold from the previous entry.

**Data:** same 19 manual points + 300 background points, 20250820 clipped
LiDAR DSM.

**Thought:** `Geomorphons` is purpose-built to distinguish real closed pits
from open/linear terrain (valleys, slopes) using a self-adaptive multi-scale
line-of-sight method — more targeted than DepthInSink's global fill for the
slope-vs-doline confusion. Also directly relevant: user independently noted
the mapped dolines aren't circular, which predicts "pit" (needs ~360°
concavity) would undercount them.

**Result:** Confirmed the shape prediction — only 4/19 manual points
classify as strict "pit"; 8/19 classify as "hollow" (partial concavity),
matching the non-circular shapes. "Pit" alone: 21% recall, ~0% background
FPR (too strict to use alone). Combining DevFromMeanElev (window=4m) with
"pit OR hollow" required: recall dropped from 84% to 53% at threshold=-0.22,
while FPR only dropped from 11% to 5% — worse Youden's J (0.48 vs 0.73) than
DevFromMeanElev alone, same pattern as the DepthInSink combo attempt.

**Conclusion:** Two independent supplementary-filter attempts (DepthInSink
closedness, Geomorphons landform class) both underperformed the plain
DevFromMeanElev threshold — stopping here rather than continuing to chase
combinations. **Final calibrated method for the first-pass detection:
DevFromMeanElev, window=4m, threshold=-0.22 m, no additional filter.**
~79-84% recall, ~11% background false-positive rate. Next: run this across
the full 20250820 AOI to produce the first candidate doline map.

---

## 2026-08-10 — Full-AOI run: point calibration doesn't transfer to whole raster

**What we did:** Ran the calibrated method (`extract_anomalies`, window=4m,
threshold=-0.22) across the *entire* clipped 20250820 AOI, not just the
19+300 sampled points used for calibration. Refactored `dolines.py`:
extracted shared threshold/vectorize logic into `_extract_regions`, added
`extract_anomalies` (DevFromMeanElev-based) alongside the older
`extract_depressions` (DepthInSink-based).

**Data:** full clipped 20250820 LiDAR DSM (`data/interim/..._dev81.tif`,
window=4m, cached from calibration), `data/manual/Sinkholes.shp` (19 points).

**Thought:** With a calibrated window/threshold in hand, run it for real.

**Result:** **14,920 candidates** — unusable, ~400x too many. The point-based
recall/FPR from calibration doesn't predict full-raster candidate *count*:
sampling checks whether N discrete locations pass a threshold, but applied to
every pixel, bare rock's continuous small-scale roughness produces enormous
speckle (many small, separate below-threshold patches) that random point
sampling at n=300 never surfaced. Checked whether real dolines'
anomaly-region footprints differ from noise: 16/19 manual points fall inside
a candidate polygon (matches ~84% recall from calibration); those matched
polygons have median area 15 m² (25th pct 9.4 m²) vs. all-candidates median
of only 0.43 m² — a real signal, but even an aggressive area cutoff (10 m²)
still leaves ~1,159 candidates and drops 4/16 real matches to get there.
Circularity doesn't help either — real dolines have *lower* circularity
(median 0.18) than the noise pool (median 0.22), consistent with the user's
observation that they aren't round; ruled out as a filter.

**Conclusion:** Area/shape post-filtering alone isn't enough — the core
problem is that per-pixel static thresholding can't distinguish "shallow
noisy dip" from "genuinely prominent depression." Added `scikit-image` and
started testing `skimage.morphology.h_minima` — an extended-minima transform
that keeps regional minima with at least a given depth/prominence `h`
relative to their surrounding terrain, rather than any pixel crossing a
static value. More principled fix for exactly this speckle problem than
another round of ad-hoc thresholds.

**Where we ended (session cut short, user had to log off):** h-minima test
was mid-run (`h` in [0.15, 0.2, 0.3, 0.4, 0.5], checking resulting region
count + how many of the 19 manual points get flagged) when the session
ended — no results yet. The test code is saved as the last two cells of
`notebooks/03_doline_calibration_20250820.ipynb` (marked WIP), not yet
executed to completion.

**Next step:** Rerun those WIP cells, pick an `h` that gets candidate count
into a plausible range (tens, not thousands) while keeping recall reasonable
— same recall/FPR-style evaluation as the DevFromMeanElev calibration
earlier in this doc. If h-minima works, fold the validated method into
`src/master_thesis/doline_detection.py` properly (a real function, not a
scratch test) and re-run the full-AOI detection. If it *doesn't* get the count down
enough on its own, worth trying it combined with the area-based cutoff from
this entry (9-10 m², grounded in real matched-polygon sizes) — the two
might compound better together than either did alone.

---

## 2026-08-11 — h-minima debugged (wrong tool usage), then watershed, still too many candidates

**What we did:** First reran the WIP h-minima cells (new session) — got 0/19
manual hits at every `h` tested, which smelled like a bug rather than a real
result. Verified the coordinate transform was correct (matched `rasterio`'s
own `.index()` exactly). Root cause turned out to be a misunderstanding of
`h_minima` itself: a synthetic bowl test showed it flags only the single
deepest pixel of a basin, not the basin's extent — manually-placed points
almost never land on that exact pixel. Fixed by using h-minima seeds to grow
full basins via `skimage.segmentation.watershed` (mask constrained to
`dev < 0`), then checking whether manual points fall *inside* the resulting
basin polygons instead of on the seed pixel. Then swept window size (6/8/10 m,
using already-cached DevFromMeanElev rasters) x h (0.3/0.5/0.8) to see if a
larger, more-smoothed input reduces candidate count further.

**Data:** 19 manual points, 20250820 clipped LiDAR DSM, cached DevFromMeanElev
rasters at several window widths.

**Result:** Watershed fixed the recall problem (up to 17-19/19 depending on
h/window — much better than point-threshold's 79-84%) but candidate *count*
is still far too high at every setting tried. Best case: window=10m, h=0.8 ->
692 basins, 12/19 (63%) recall. Larger/smoother windows do reduce count
(4277 -> 692 going from 6m/h=0.3 to 10m/h=0.8) but plateau nowhere near the
~30-35 target, and recall drops as thresholds tighten enough to get there.

**Conclusion:** This isn't a tuning problem anymore, it's a real limit —
bare alpine karst rock at 5cm resolution has more genuinely "prominent"
local minima than there are real dolines, by roughly an order of magnitude,
regardless of window size, h, or segmentation method. Five different
approaches now (absolute threshold, DepthInSink combo, Geomorphons combo,
h-minima, h-minima+watershed) all hit the same wall. Topography alone likely
isn't sufficient to fully automate this at the target precision — next
avenue worth trying, if pursued further, is combining topographic evidence
with the RGB orthophoto (e.g. water-filled dolines should have a distinct
spectral signature unlike generic rock texture, which pure elevation
analysis can't see). For now: treat automated detection as a *shortlist
generator* (narrows ~30M pixels down to a few hundred/thousand candidates
worth a human look), not a final answer — manual visual screening in QGIS
remains necessary regardless of which of these settings gets used.

---

## 2026-08-14 — Historical Bavaria DOP download script

**What we did:** Built `scripts/download_bavaria_dop.py` to pull historical
20cm orthophotos over `data/manual/Zugspitze_AOI.geojson` from Bavaria's free
"Historische DOP" WMS (2003-present, no auth). Confirmed the real service
details first (endpoint, layer names `by_dop_{year}_h`, date field via
GetFeatureInfo) rather than guessing from docs. For each year: samples a
grid of points across the AOI to find actual flight date(s) (a single annual
layer can span >1 date if the AOI straddles a flight seam), keeps only dates
in a snow-free month window (June-Sept default), tiles+mosaics the GetMap
requests (AOI is 1836x880m, over the WMS's 6000x6000px/1200m cap), clips to
the AOI polygon, and flags a rough brightness/saturation-based snow warning
per downloaded image.

**Data:** `data/manual/Zugspitze_AOI.geojson`, Bavaria WMS
`geoservices.bayern.de/od/wms/histdop/v1/histdop`.

**Thought:** Date alone isn't proof of snow-free conditions — already
learned that the hard way with the June 2025 UAV flight — so this needed
two independent, imperfect heuristics (date + pixel brightness) rather than
trusting either alone, and the docstring says so explicitly.

**Result:** First real run hung for 38 minutes doing essentially nothing
(confirmed via Get-Process: ~3s actual CPU time) — root cause was missing
timeouts on every `urllib.request.urlopen()` call, so one slow/stuck request
blocked forever. Fixed with a 20s timeout for small text queries and a
separate 90s timeout + 3x retry for the larger GetMap image tiles (these
genuinely need longer, confirmed by a real transient timeout that succeeded
on retry). Also made per-year failures non-fatal so one bad year doesn't
kill the whole run.

Final run: 23 years checked in ~15s, 10 qualifying dates found (2003-2024,
most years have no coverage for this specific AOI since Bavaria flies
North/South in alternating cycles), all 10 downloaded successfully. Visually
checked 4 of the 10 against their snow-proxy scores: heuristic tracks real
usability reasonably well, but the Zugspitzplatt's permanent snowfield
(Schneeferner) inflates the score somewhat for every date regardless of
season — a "45%" borderline file (2003) was actually fine, "82-87%" files
(2020, 2024) were genuinely washed out. 2003-2005 imagery is also natively
40cm resolution upsampled to a 20cm grid by the server, not real 20cm detail.

**Conclusion:** Script works and is committed. Best-looking dates for manual
mapping: 2006, 2009, 2012, 2015 (all under 50% snow-proxy). 2018/2020/2022/
2024 dates are probably not usable without a closer look. Lesson for any
future network-calling script in this project: always set an explicit
timeout, never trust a bare `urlopen()` call not to hang indefinitely.

---

## 2026-08-14 — Spectral (orthophoto brightness) signal, then combined with topography

**What we did:** User visually checked the 2003 historical imagery and
noted many dolines already appear present that early — worth remembering
for the karst-vs-permafrost question, but doesn't itself disprove permafrost
involvement (presence-at-one-date can't distinguish "old karst feature" from
"formed early in a decades-long degradation trend"; the diagnostic question
is activity/growth rate over time, not first appearance). Parked that for
now, continued with detection.

Hypothesis: a real bowl-shaped depression should look locally *darker* than
its surroundings in the orthophoto (shadow from the bowl geometry itself, or
water pooling) — a signal pure elevation can't see. Computed a "deviation
from local mean brightness" on the 20250820 RGB orthomosaic (same trick as
DevFromMeanElev, applied to a grayscale/brightness band instead of
elevation, resampled to 5cm), calibrated against manual points (now 34,
up from 19) the same way: window sweep, LOOCV, then — having been burned
twice by point-level stats not surviving full-raster application — an
actual full-AOI polygon check against manual points, not just pixel values.

**Data:** `data/raw/20250820/20250820_terra_ppk_rgb_om.tif` (2.12cm RGB
orthomosaic), 34 manual points, 300 background points.

**Result:** Point-level stats looked excellent (LOOCV recall 85%, window=10m,
threshold=-2.0, FPR=1%) — but polygon-level full-AOI recall at that same
threshold/area-cutoff was only 38% (13/34), because at a strict threshold
the connected "dark core" of many real dolines is smaller than the area
filter. Checking recall across area cutoffs showed the identical
threshold-vs-count tradeoff topography had: min_area=0.02 -> 39,812
candidates at 85% recall; min_area=2.0 -> 24 candidates at 15% recall. No
free lunch.

Tried combining topographic (window=4m, threshold=-0.2) AND spectral
(window=10m, threshold=-1.5) as a joint pixel-wise mask, on the theory that
each channel's noise source (rock crevices vs. individual rock shadows)
shouldn't correlate, so requiring both should suppress noise
multiplicatively. Point-level stats looked even better (85% recall, 1% FPR)
than either alone. Full-raster result: 324 candidates, 15/34 (44%) recall —
barely better than spectral alone (198 candidates, 38%), and *more*
candidates despite being an AND of two conditions (looser individual
thresholds than spectral-alone's strict single threshold let more total
area through even after intersecting).

**Conclusion:** Every method tried across both sessions — absolute
threshold, DevFromMeanElev, DepthInSink combo, Geomorphons combo,
h-minima+watershed, spectral brightness, and topo+spectral combined — hits
the same wall: candidate count in the "reviewable hundreds" range caps
recall around 40-65%; recall above 80% means thousands+ of candidates.
Nothing tested so far breaks this tradeoff. Point-level/sampled statistics
are now confirmed unreliable predictors of full-raster performance across
three independent methods — always validate the actual polygon output
against manual points before trusting a calibration number again.

Given manual mapping is already at 34 points and evidently working well,
recommending to the user: treat the best current automated output
(`data/processed/20250820_candidate_dolines_combined.gpkg`, 324 candidates)
as a cross-check shortlist against manual mapping, not a replacement for it,
rather than continuing to chase incremental algorithm tuning. Decision
pending user input.

---

## 2026-08-14 — Susceptibility model v1: Random Forest + terrain/spectral covariates (20250820, benchmark run)

**What we did:** Following a scope-narrowing conversation with Elio (permafrost
degradation as the cause is now de-emphasized — dolines were already present
in 2003 imagery; new focus is doline growth-over-time plus a genuine
multi-sensor detection *method* as a thesis contribution in its own right, not
just detection-by-thresholding), built a susceptibility/factor-importance
model instead of another detection threshold: presence points (34 manual) +
background (300 random) sampled against a covariate stack, fit with a Random
Forest, importance read via permutation importance + partial dependence —
same framing as karst/landslide susceptibility mapping and presence-background
SDMs (MaxEnt etc). Scoped to 20250820 only (richest single-epoch dataset —
LiDAR DSM + RGB ortho).

New covariates derived (`src/master_thesis/terrain_covariates.py`, whitebox
wrappers): slope, aspect (converted to northness/eastness — aspect itself is
circular, unsafe to feed a model directly), plan/profile curvature,
roughness, TWI (flow-accumulation-based). Combined with the existing
DevFromMeanElev (4m window) and RGB brightness deviation (10m window) from
earlier calibration, plus geomorphon class (one-hot).

Used spatial cross-validation (`GroupKFold` over a coarse 4x4 spatial block
grid) instead of naive random k-fold, since points aren't spatially
independent and random splits have inflated apparent performance elsewhere
in this project.

**Data:** `data/raw/20250820/20250820_terra_ppk_lidar_dsm.tif` (clipped),
`20250820_terra_ppk_rgb_om.tif`, 34 manual points, 300 background points.
Notebook: `notebooks/05_susceptibility_model_20250820.ipynb`.

**Thought:** explicitly framed as a benchmark/pipeline-validation run, not a
final result — fieldwork lands in ~2 weeks (26-28 Aug 2026) and will bring
better/fresh data, at which point this gets a proper rerun. Today's goal was
just confirming the pipeline runs end to end.

**Result:**
- Pipeline ran clean end to end.
- Point-level performance looked excellent: naive random CV AUC 0.97, spatial
  CV AUC ~0.97 on the folds that had both classes present — but one of five
  spatial folds was degenerate (single-class, AUC undefined), because 34
  presence points spread across only 12 occupied spatial blocks means some
  folds get zero presence points. A real data-scarcity issue for spatial CV
  at this sample size, not a bug — should resolve once more field-verified
  points exist post-fieldwork.
- Permutation importance (fit on all data) was dominated almost entirely by
  `brightness_dev` (importance 0.046); every topographic covariate, including
  `local_relief` (DevFromMeanElev, previously shown to have real standalone
  signal in earlier calibration), came out at ~machine-epsilon — the noise
  floor. Working hypothesis, not yet tested: brightness deviation in an
  orthophoto is itself heavily shading-driven, i.e. a function of local
  slope/aspect/curvature — so it may be acting as a compressed proxy for
  exactly the topographic information the other covariates carry, leaving
  them nothing to add at the margin once brightness is already in the model.
  Worth checking directly (a covariate correlation matrix) before reading
  this ranking as "topography doesn't matter here."
- Full-raster susceptibility surface (coarsened to 0.5m resolution for
  tractability — native 5cm over the full AOI is 600M+ pixels, not reasonable
  to push through `predict_proba` for a first pass) hit the same tradeoff
  wall as every prior method: threshold 0.3 → 79% recall (27/34) but 3,256
  candidate regions; threshold 0.5 → 62% recall (21/34), 417 regions;
  threshold 0.9 → 29% recall (10/34), 53 regions. No threshold gives both a
  reviewable candidate count and high recall.

**Conclusion:** Fourth independent confirmation in this project that
point-level/sampled statistics do not predict full-raster performance — a
multivariate Random Forest with near-perfect point-level AUC still hits the
same ~40-65%-recall-for-reviewable-count ceiling on the actual raster as
every univariate threshold method tried before it. This increasingly looks
like a real property of the data/terrain rather than a limitation of any one
algorithm. The more useful output from this run isn't the susceptibility map
itself — it's the importance ranking, and even that needs the
brightness/topography confound checked before it means anything. Known
limitations to fix before the fieldwork rerun: spatial CV block size needs
revisiting with a larger point set; permutation importance was computed
in-sample (documented as such, not a bug, but worth a held-out version too);
no thermal/multispectral available for this date.

---

## 2026-08-22 — Environment setup on laptop; literature review of downloaded papers

**What we did:** First session on a different machine (laptop, not the usual
tower) — ran `uv sync` fresh, confirmed it installs cleanly (145 packages, no
PDAL issues, same as documented tower setup). Then read through ~20 PDFs the
user had already downloaded into their Downloads folder (papers gathered for
this thesis but not yet read/synthesized), split across two parallel review
passes, filtering out unrelated personal/administrative files mixed into the
same folder.

**Data:** Papers listed in `docs/thesis/causation_hypothesis.md` references
section; also read (lower relevance, not written up separately): Rittig
(2012) MSc thesis, Clayton (1964) on ice-surface "karst," Tuffen (2010) on
deglaciation-triggered volcanism, Dou et al. (2015) OBIA+genetic-algorithm
sinkhole detection, Yavariabdi et al. (2023) "SinkholeNet" (RGB+slope fusion
CNN), and the user's own prior Dead Sea sinkhole work (a failed U-Net
attempt, a snow-depth/TPI terrain study on this same Zugspitze UAV data, and
a Dead Sea sinkhole-mapping poster).

**Thought:** Read as a critical scientist, not a summarizer — for each paper,
ask whether it actually bears on (a) automated detection, (b) the
karst-vs-permafrost causation question, (c) doline morphometry/classification,
or (d) geohazard assessment, and say plainly when it doesn't.

**Result:** Wrote up a composite causation hypothesis (see
`docs/thesis/causation_hypothesis.md`) — the "karst or permafrost" framing
was too coarse; site-specific evidence (Gude & Barsch 2005's documented
thermokarst collapse in a Zugspitzplatt doline; Küfmann 2013's CO2-limited,
snow-thinning-timing-dependent dissolution; Wetzel 2004's active fast karst
drainage; Grüger & Jerz 2011's >7000 BP dating of one doline; Ortner & Kilian
2022's named fault sets crossing the plateau) supports a more specific
composite: fault-initiated (inception/seismic doline) features, enlarged by
snowmelt-thinning-driven CO2 corrosion, with a subset locally reactivated by
melting relict ground ice — plausibly a mixed old/young population, not one
homogeneous group.

On detection: SinkholeNet's RGB+slope fusion (not RGB alone) is the most
promising unaddressed lead for the recall-vs-false-positive wall hit five
times already in this project — but the user's own prior U-Net attempt on
Dead Sea sinkholes degenerated to a near-constant predictor with a
comparably small label set (~30 non-exhaustive labels), a real cautionary
data point against training a CNN from scratch here too. A frozen
self-supervised/foundation-model backbone (e.g. DINOv2) or promptable
zero-shot model (SAM2) fine-tuned lightly on far fewer labels was flagged as
a lower-risk alternative, not yet tried.

**Conclusion:** Causation hypothesis write-up complete
(`docs/thesis/causation_hypothesis.md`), including full citations and three
concrete open items. Detection-method and morphometric-split ideas added to
the parking lot above, not yet run. Next, pending user direction: either the
fault-alignment GIS test, the morphometric old/young split, or a first pass
at an RGB+slope fused detector.
