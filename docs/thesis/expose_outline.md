# MSc Exposé — working outline

Structure modeled on Wagner (2022, `msc_expose_Wagner.pdf`, supervisor-provided
example): Framing & Rationale -> Study area -> Data & Methods -> RQ-specific
methods -> References. Adapted for two research questions instead of one, and
a dedicated Data section (Wagner had one sensor archive; this thesis has
several).

Status: outline only, not yet drafted as prose. Open items that need an
answer before section 1/3/4 can be written are marked `[OPEN]` below and
listed again at the end.

---

## 1. Framing and Rationale

Flow:

1. Opening: Zugspitze/Zugspitzplatt setting. `[OPEN: which elevation to lead
   with — Zugspitze summit (2962 m) vs. the Zugspitzplatt plateau itself
   (~2000 m, the actual study area) — confirm intended framing.]`
2. Karst geohazards as a well-studied phenomenon across settings (breadth
   first, establishes this isn't a niche curiosity): evaporite karst
   (halite/gypsum, e.g. Dead Sea), anthropogenic/man-made collapse, classic
   carbonate karst (tower karst / turmkarst, China).
3. Narrow to the Zugspitzplatt: dolines here previously used as Holocene
   climate/pollen archives (Grüger & Jerz 2011) but understudied as a
   geomorphological/hazard phenomenon in its own right.
4. Define terms — doline vs. sinkhole. Working line: the two are very
   largely synonymous; "doline" is the term preferred in the
   European/karst-geomorphology tradition (Sauro 2003; Gutiérrez et al.
   2008; Veress 2017), "sinkhole" more common in North American and applied
   hazard-engineering usage. The substantive distinction worth making is
   genetic type, not naming — Gutiérrez et al. (2008)'s classification
   (cover/bedrock/caprock x collapse/suffosion/sagging) is the actual
   framework to cite here.
5. Introduce thermokarst as a mechanism: topography formed by melting of
   ice-rich ground (permafrost or *relict* ground ice), producing
   subsidence/collapse independent of dissolution. This is where Gude &
   Barsch (2005)'s documented Zugspitzplatt tunnel-subsidence case lands.
6. State the causation question: karst dissolution vs. permafrost/relict-ice
   thaw vs. both — draw directly on `causation_hypothesis.md` (Gude &
   Barsch's tunnel case, Küfmann's snow-thinning-timing-dependent
   dissolution, Ortner & Kilian's mapped fault sets).
7. Fold in the fieldwork surprise as motivation, not a results teaser:
   features larger and more cave-like than expected, visible
   frost-shattering on exposed rock — argues for a dedicated multi-method
   study, not a single detection pass. `[OPEN: a concrete number here would
   land better than "many" — how many dolines confirmed in total now, and
   is there a standout example (largest, or clearest cave/shaft) worth
   naming as a motivating case, the way Gude & Barsch's tunnel case is
   used?]`
8. Transition — why this matters (relevance): proximity to hiking
   infrastructure (geohazard angle) + visibly changing shapes already
   apparent across existing multi-date imagery (directly motivates RQ2).
9. Secondary aim: the data available is rich enough to actually
   characterize doline shape/morphometry, not just presence/absence —
   sets up the morphometric-classification literature already reviewed
   (Péntek/Veress/Lóczy 2007; Veress 2017 baselines) for later use.
10. Close with the two RQs as bullets (Wagner-style):
    - RQ1: How many dolines are there, where, how are they spatially
      distributed/clustered, and how can they be identified via remote
      sensing?
    - RQ2: How are the dolines changing over time, and what is driving
      that change?

## 2. Study area

- Zugspitze/Zugspitzplatt: location, elevation, Wetterstein limestone,
  Northern Calcareous Alps nappe structure, mapped fault sets (Puitental /
  Loisach / Ammer — Ortner & Kilian 2022).
- Prior and ongoing research at this exact site, positioning the thesis
  within an active multi-group research site rather than a blank slate:
  permafrost/BTS survey (Gude & Barsch 2005), ERT permafrost monitoring
  (Krautblatter et al. 2010), karst hydrology (Wetzel 2004, Partnach
  spring), doline dissolution dynamics (Küfmann 2013), doline dating
  (Grüger & Jerz 2011).
- Fieldwork: Aug 2026 campaign — what was done (ground-truthing, UAV
  acquisition) and what was found (larger/cave-like features, frost-
  shattering signs, confirmed doline count). Belongs at the end of this
  section as the bridge into Data & Methods.

## 3. Data & Methods (general)

- UAV data across three prior epochs (Oct 2024, Jun 2025, Aug 2025) plus
  the new Aug 2026 acquisition — RGB, multispectral, LiDAR, thermal.
  `[OPEN: need actual band/resolution specifics per sensor/date for this
  section — pull from Elio's flight documentation or existing
  notebooks/metadata rather than guessing.]`
- Processing pipeline: Agisoft (SfM/photogrammetry) -> whitebox (terrain
  derivatives) -> current Python/GIS stack (geopandas, rasterio, laspy,
  scikit-learn).
- Publicly available data:
  - Bavarian DGM1 (1 m LiDAR DEM, geodaten.bayern.de, EPSG:25832).
  - Bavaria historical DOP orthophoto archive, 2003-2024 (already scripted
    — `scripts/download_bavaria_dop.py`).
  - Sentinel-1 (InSAR, for RQ2 surface change).
  - `[OPEN, checked 2026-09-22: CORONA declassified imagery. Resolution
    only clears the <3 m bar for the late missions — KH-4A ~2.75 m
    (1962-69), KH-4B ~1.8 m at frame center degrading to ~2.7 m at frame
    edges (1967-72); everything earlier (KH-1 to KH-4) is 7.6-12 m, not
    usable. Actual scene-level coverage over the Zugspitzplatt could NOT
    be confirmed — USGS's public "coverage map" KML turned out to be a
    single global placeholder polygon, not real per-scene footprints, so
    it answers nothing. CORONA's primary targets were denied/Eastern-bloc
    areas; Western/NATO Europe coverage exists but was incidental, so
    there's genuine uncertainty this site was flown at all. Needs an
    actual interactive EarthExplorer search (free account, draw AOI,
    filter Declassified Data -> Declass 1, check frame previews) — a
    5-minute check, but requires the JS map UI. Treat as a bonus data
    source if it pans out, not a committed one for the exposé.]`
  - Zugspitze summit station meteorological data (precipitation,
    temperature, snow).
- The manually confirmed dolines (`data/manual/Sinkholes.shp`, now expanded
  post-fieldwork) as the label set / ground truth for RQ1 and the change
  baseline for RQ2.
- Tools: Python as primary analysis environment, QGIS for
  visualization/manual work, SAGA GIS as a secondary option for specific
  terrain algorithms not covered by whitebox.
- State explicitly that the methodology is partly experimental/exploratory
  by design — which specific algorithm/approach works is itself part of
  what RQ1 investigates, not a gap in the proposal.

## 4. RQ1 — Detection / mapping methodology

- Framed as: build a model on the confirmed dolines using the full
  multi-sensor stack (UAV RGB/multispectral/LiDAR/thermal), then evaluate
  what's achievable using only publicly-available data (DGM1 + public
  orthophoto, no UAV/thermal) — a transferability/domain-generalization
  framing.
- Algorithm deliberately left open (not deep learning, per prior
  discussion — most likely a classical/statistical approach given the
  ~30-40 label count, informed by the detection-method literature already
  reviewed: SinkholeNet's RGB+slope fusion result, Dou et al. 2015's OBIA
  approach, and the cautionary lesson from the prior Dead Sea U-Net
  attempt about training deep models from scratch on this few labels).
- Transferability test area: left deliberately unspecified in the exposé —
  state the goal as testing against other alpine regions where dolines
  occur (could be the rest of the Zugspitze, another alpine massif, or
  wider still), with the actual limiting factor being available processing
  power rather than data availability. Resolved 2026-09-22, no longer
  open.

## 5. RQ2 — Change quantification & driver correlation

- Multi-temporal surface change: UAV/LiDAR DEM differencing across the
  three-plus-one epochs, possibly Sentinel-1 InSAR, to quantify how much
  the dolines are actually changing (not just confirm that they are).
- Correlate against snow-cover *thinning date* specifically (not bulk melt
  volume or raw precipitation) — Küfmann (2013)'s mechanism gives this as
  the variable that should actually matter, a sharper hypothesis than a
  generic "correlate with snowmelt."
- Frost-weathering observations from fieldwork as a second driver
  candidate alongside karst dissolution timing — direct link to the
  causation question from section 1.

## References

Pull from `causation_hypothesis.md` (Gude & Barsch 2005; Wetzel 2004;
Küfmann 2013; Grüger & Jerz 2011; Ortner & Kilian 2022; Sauro 2003; Gams
2000; Veress 2017; Péntek/Veress/Lóczy 2007; Gutiérrez et al. 2008;
Krautblatter et al. 2010) plus the detection-method papers from the same
literature pass (Yavariabdi et al. 2023 "SinkholeNet"; Dou et al. 2015) and
Wagner (2022) as the structural template.

---

## Open items (collected)

1. Which elevation to lead the framing with — Zugspitze summit vs.
   Zugspitzplatt plateau.
2. A concrete post-fieldwork doline count, and whether there's a single
   standout cave/shaft example worth naming in section 1.
3. UAV sensor band/resolution specifics per epoch, for section 3.
4. Whether CORONA imagery actually has usable coverage over the
   Zugspitzplatt (resolution checked 2026-09-22 — only KH-4A/KH-4B,
   1967-72, clear the <3 m bar; coverage itself still unconfirmed, needs a
   manual EarthExplorer search).
