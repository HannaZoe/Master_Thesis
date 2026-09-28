# Literature Feasibility Check: Sentinel-1 InSAR for Doline-Scale Subsidence Monitoring on the Zugspitzplatt

**Purpose:** This document checks whether Sentinel-1 SAR/InSAR, as currently listed as a planned data source in the thesis, is actually capable of detecting multi-temporal surface displacement associated with individual collapse dolines (roughly 0.3–a few m across at the surface, some larger/cave-like) on a high-alpine karst plateau (~2000 m, seasonal snow). Sources were read directly where full text was accessible; where publishers blocked full-text access (ScienceDirect, some MDPI pages returned HTTP 403), citation metadata was confirmed via Crossref and content was cross-checked against multiple independent search-engine excerpts/abstracts of the same paper. This is noted per source below.

---

## 1. Sentinel-1 technical resolution baseline

**Source:** ESA/Copernicus Sentinel-1 mission technical documentation (product specifications for Interferometric Wide Swath, IW, mode), cross-checked against multiple secondary technical summaries (Terrascope data product docs, INPE STAC catalogue).

**Summary:** Sentinel-1 IW mode (the standard acquisition mode over land, including the Alps) has a single-look slant resolution of approximately 5 m (range) × 20 m (azimuth). Standard Ground Range Detected (GRD) products are delivered at 10 m × 10 m pixel spacing with an actual spatial resolution of roughly 20 m × 22 m. Multi-looked/coherence-optimized interferometric processing (needed to reduce phase noise for deformation work) coarsens this further — pixel sizes of 20 m or more are typical in published interferograms, and even PS/DS point clouds derived at native resolution place individual coherent measurement points tens of meters apart at best in non-urban terrain.

**Relevance:** This is the single most decisive fact for this feasibility check. A doline surface expression of 0.3–a few meters is roughly one to two orders of magnitude smaller than a single Sentinel-1 resolution cell (~20×20 m ≈ 400 m²) or even a single 10 m pixel (100 m²). A meter-scale collapse feature cannot occupy, let alone be individually resolved within, a Sentinel-1 pixel — the deformation signal from a small doline would be spatially averaged (diluted) with the surrounding stable ground inside the same resolution cell, likely below the noise floor. This alone rules out *direct, feature-by-feature* imaging of individual dolines with Sentinel-1, independent of any coherence or deformation-magnitude considerations.

---

## 2. Minimum detectable deformation magnitude (general InSAR capability)

**Sources:** Aggregated across several technical summaries and review-style sources (search-engine synthesis of multiple InSAR method papers, not a single full-text review read directly — flagged as lower-confidence, general textbook-level knowledge rather than a single citable study).

**Summary:** Under good conditions (high coherence, long time series, atmospheric correction), Sentinel-1 InSAR time series techniques (PSI/SBAS) can resolve deformation *rates* down to roughly 2–5 mm/yr at a *point* (a persistent or distributed scatterer), and single-interferogram line-of-sight precision is on the order of a few mm to ~1 cm. This is well within the plausible magnitude range of early-stage doline subsidence (which could plausibly be mm–cm scale before collapse). So the *magnitude* sensitivity of InSAR is, in principle, adequate — the problem is not that InSAR is too coarse in displacement measurement, it is that (a) it needs a usable scatterer at exactly the right ~10–20 m location, and (b) it needs coherence over the observation interval, both of which are the binding constraints in alpine karst terrain, not the deformation-magnitude sensitivity itself.

**Relevance:** Clarifies that the feasibility problem for this thesis is fundamentally a *spatial resolution / coherent scatterer availability* problem, not a *deformation-sensitivity* problem. This distinction matters for how the thesis frames the InSAR limitation.

---

## 3. Persistent/distributed scatterer density in vegetated, rural, non-urban terrain

**Sources:** Search-synthesized findings from multiple PS-InSAR methodology papers (Hooper et al. 2004, *Geophysical Research Letters*, "A new method for measuring deformation on volcanoes and other natural terrains using InSAR persistent scatterers"; and related distributed-scatterer literature). Full text of the underlying papers was not successfully retrieved (paywalled/blocked); findings are based on consistent, repeated statements across independent secondary sources rather than a single verified full-text read, so treat as **moderate confidence**.

**Summary:** Outside of buildings, roads, rock outcrops, and other stable hard-surface reflectors, natural terrain — especially vegetated, snow-affected, or weathering ground — produces low and unstable radar backscatter, resulting in very low densities of usable coherent measurement points (persistent scatterers). This is a well-established, general limitation of PS-InSAR in non-urban settings.

**Relevance:** The Zugspitzplatt is bare karst rock, scree, and alpine grassland/snow — not a city. This could actually work *in favor of* PS-InSAR in one narrow sense (exposed bare limestone pavement can be a stable, coherent reflector, unlike vegetated soil), but the plateau's dolines themselves are not guaranteed to coincide with a coherent scatterer, and there is no control over *where* the few available coherent points fall relative to a specific doline of interest.

---

## 4. Alpine-specific coherence limitations: snow cover, steep slopes, seasonal change

### 4a. Giffard-Roisin, S., Boudaour, S., Doin, M.-P., Yan, Y., & Atto, A. (2022). "Land cover classification of the Alps from InSAR temporal coherence matrices." *Frontiers in Remote Sensing*, 3, 932491. https://doi.org/10.3389/frsen.2022.932491

**Read status:** Full text read directly (Frontiers HTML).

**Summary:** Uses Sentinel-1 temporal coherence matrices over the French Alps to classify land cover, exploiting the fact that different surfaces decorrelate differently over a year. Confirms that SAR/InSAR in the Alps is "affected by distortions in mountainous areas" — specifically foreshortening, layover, and shadowing — which the authors document causing real classification errors (e.g., a forest area misclassified as water because it sat in radar shadow behind a mountain). The paper treats seasonal coherence loss (snow, vegetation phenology) as a *feature* for land-cover classification rather than a problem, but explicitly frames this same seasonal decorrelation as something that "complicates accurate deformation measurement" and that must be understood and corrected for before displacement estimates can be trusted in alpine terrain. No quantitative coherence-vs-snow numbers are given in this paper.

**Relevance:** A directly relevant, current (2022), Alps-specific source confirming — from people actively working with Sentinel-1 coherence in this exact mountain range — that geometric distortion (steep slopes) and seasonal decorrelation (snow, vegetation) are real, active problems for deformation work in the Alps, not hypothetical ones.

### 4b. Bussard, R.C., Dufek, J., Wauthier, C., & Townsend, M. (2025). "Quantifying the Effects of Volcanic Snow Cover on InSAR Coherence Using a Computationally Inexpensive Neural Network." *Journal of Geophysical Research: Machine Learning and Computation*. https://doi.org/10.1029/2024JH000553

**Read status:** Not fully read (403 on full text); findings drawn from consistent search-engine excerpts of the abstract/results, cross-checked across two independent search queries. **Moderate confidence.**

**Summary:** Studies Mount St. Helens (a seasonally snow-covered volcanic edifice, a reasonable analogue for a snow-covered alpine plateau) using Sentinel-1 coherence and Landsat-8-derived snow cover maps (2014–2021). Finds that average interferometric coherence over bare rock can drop by up to ~70% when snow is present (documented elsewhere as coherence collapsing from ~1.0 to ~0.2–0.3). Critically, forward modeling in the paper shows that "most centimeter-or-above scale simulated ground movement is hidden by snow," which is typically present from December through March.

**Relevance:** This is a near-direct analogue for the Zugspitzplatt problem: seasonal snow at high elevation can mask even centimeter-scale deformation for several months of the year, directly cutting into the usable observation window and the ability to build a continuous, coherent time series across doline-relevant seasons (snowmelt/thaw periods, which are also mechanically the most likely times for karst-related subsidence to occur).

---

## 5. Precedent studies: InSAR applied to karst subsidence / sinkhole monitoring

### 5a. Aporto, L.J.A., Mabaquiao, L.C.S., Garcia, L.M., et al. (2026). "Sinkhole Monitoring and Early Warning Detection in the Karst Landscapes of Guimaras Island, Philippines Using Interferometric Synthetic Aperture Radar (InSAR) Satellite Data." *ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, X-5/W4-2025, 43–50. https://doi.org/10.5194/isprs-annals-X-5-W4-2025-43-2026

**Read status:** Full text read directly.

**Summary:** Uses Sentinel-1 (2024–2025) with PSI (StaMPS workflow) over karst terrain on Guimaras Island. Produced 26,529 PS points, of which 3,807 showed subsidence, with velocities up to –36 mm/yr in one municipality. Critically, the authors state that PS points were concentrated **"primarily in built-up and urban areas"** and that PSI's usefulness is limited where "persistent scatterers are sparse, particularly in vegetated areas where sinkholes commonly occur" — the study explicitly notes this gap requires ground validation to actually link detected subsidence to sinkhole hazard.

**Relevance:** This is the most directly on-topic precedent found (Sentinel-1 + PSI + karst sinkholes, published 2026). It is also the clearest confirmation of the exact problem anticipated for the Zugspitzplatt: even in a study explicitly designed to find karst subsidence with Sentinel-1, the method's coverage collapses precisely in the non-urban, vegetated/natural terrain where the actual karst features are — the built environment is what makes PSI work, and the plateau has essentially none.

### 5b. Orhan, O., Oliver-Cabrera, T., Wdowinski, S., Yalvac, S., & Yakar, M. (2021). "Land Subsidence and Its Relations with Sinkhole Activity in Karapınar Region, Turkey: A Multi-Sensor InSAR Time Series Study." *Sensors*, 21(3), 774. https://doi.org/10.3390/s21030774

**Read status:** Full text read directly (PMC).

**Summary:** Combines Sentinel-1 (87 images, 2014–2018, ~100 m processed ground resolution in this study) and COSMO-SkyMed X-band (25 images, ~20 m resolution) with SBAS over a 2,940 km² closed basin with 332 catalogued sinkholes. Detected regional subsidence up to 60–70 mm/yr. However, the key finding for feasibility purposes: **"most sinkholes occur in decorrelated areas (masked areas with no subsidence information) or in areas with a negligible subsidence rate,"** and specifically, "all of the sinkholes formed during the InSAR observed period... developed in agricultural lands," where seasonal land-use/vegetation change caused decorrelation that meant **no InSAR subsidence information was available at all at the locations that actually collapsed.**

**Relevance:** This is arguably the single most important precedent for an honest feasibility verdict. Even with a much longer observation baseline, a larger and more actively subsiding karst system, and a supplementary X-band sensor, this study could not link InSAR-detected deformation to the locations of actual sinkhole formation — the sinkholes formed where InSAR had no data (decorrelated) or negligible signal, not where the deformation was largest. This is a direct, sobering precedent against assuming that InSAR precursor signals will reliably appear at doline locations.

### 5c. Azar, M.K., Hamedpour, A., Maghsoudi, Y., & Perissin, D. (2021). "Analysis of the Deformation Behavior and Sinkhole Risk in Kerdabad, Iran Using the PS-InSAR Method." *Remote Sensing*, 13(14), 2696. https://doi.org/10.3390/rs13142696

**Read status:** Citation confirmed via Crossref; content from consistent search-engine excerpts (full text blocked). **Moderate confidence.**

**Summary:** PS-InSAR with Sentinel-1 (Jan 2015–Aug 2018) applied to a carbonate-karst sinkhole near Kerdabad, Hamedan province, Iran, that collapsed in August 2018. The sinkhole itself was ~40 m in diameter and ~40 m deep — i.e., roughly one Sentinel-1 resolution cell across, at minimum, and two orders of magnitude larger than a typical doline surface expression on the Zugspitzplatt. The study found ~3 cm/yr of precursor subsidence in the area.

**Relevance:** Confirms that Sentinel-1 PS-InSAR *can* detect precursor subsidence ahead of a karst collapse — but only at a feature size (~40 m) far larger than a doline (0.3–a few m). This is a useful positive precedent for "regional/large karst feature" monitoring, but it does not support meter-scale, individual-doline detection; if anything, the fact that a headline success story in this literature is built around a 40-m-wide collapse reinforces how far outside InSAR's practical range true doline-scale features sit.

### 5d. Kim, J.-W., Lu, Z., & Degrandpre, K. (2016). "Ongoing Deformation of Sinkholes in Wink, Texas, Observed by Time-Series Sentinel-1A SAR Interferometry (Preliminary Results)." *Remote Sensing*, 8(4), 313. https://doi.org/10.3390/rs8040313

**Read status:** Citation confirmed via Crossref; content from search-engine excerpts (full text blocked). **Moderate confidence.**

**Summary:** Time-series Sentinel-1A (plus ERS and ALOS PALSAR for longer baseline) InSAR over the well-known Wink Sink collapse features in the Permian Basin, Texas (each of these sinkholes is on the order of 100+ m across — large collapse features, not karst dolines but salt-dissolution/oil-field-induced collapse). Found precursor deformation signals up to nine years before collapse, and post-collapse subsidence up to 130 mm/yr in surrounding zones.

**Relevance:** Another "success" case, but again at a feature scale (hundreds of meters) far above doline scale, and in a different geologic setting (salt karst/anthropogenic oil-field collapse in flat desert terrain — no alpine relief, no snow, no vegetation decorrelation). Not a close analogue to the Zugspitzplatt in either target size or terrain difficulty.

### 5e. Oliver-Cabrera, T., Wdowinski, S., & Kruse, S. (2022). "Detection of Sinkhole Activity in West-Central Florida Using InSAR Time Series Observations." *Remote Sensing of Environment*, 269, 112793. https://doi.org/10.1016/j.rse.2021.112793

**Read status:** Citation confirmed (publisher-indexed PDF title/metadata); content from search-engine excerpts and a companion FIU press release (full text blocked, PDF fetch failed). **Moderate confidence.**

**Summary:** This is the single most methodologically relevant precedent in terms of what sensor characteristics are actually required — and it deliberately does **not** use Sentinel-1. It uses TerraSAR-X, a much higher-resolution X-band sensor (spatial resolution 25 cm–1 m, roughly 20–80× finer than Sentinel-1's ~20 m), with PSI (StaMPS/SARPROZ), over 1.7–2.5 years, in suburban West-Central Florida (cover-collapse sinkhole terrain with buildings/roads as scatterers). Detected localized subsidence at rates of –3 to –6 mm/yr at sites with existing built infrastructure to serve as coherent scatterers.

**Relevance:** This is the most important negative-by-implication finding for this thesis. Researchers who specifically wanted to detect *localized*, sinkhole-scale subsidence chose **high-resolution X-band TerraSAR-X, not Sentinel-1**, precisely because fine resolution and abundant hard-surface scatterers (buildings, pavement) were needed to isolate small subsidence footprints. The Zugspitzplatt has neither the fine-resolution sensor nor the built infrastructure. This strongly suggests that even the more modest goal of "localized" (not full doline-scale) subsidence detection is a stretch for Sentinel-1 in this setting, based on what the specialists in this exact sub-field chose to use instead.

---

## 6. Cross-cutting technical point: Sentinel-1 vs. higher-resolution SAR

Synthesizing 5c/5d (Sentinel-1 successes at 40 m+ features) against 5e (TerraSAR-X needed for sub-decameter localized detection) makes the resolution argument concrete: every located precedent where InSAR successfully detected precursor deformation at *sub-hundred-meter* scale used a finer-resolution sensor than Sentinel-1 (TerraSAR-X at 0.25–1 m, or COSMO-SkyMed at ~3 m/20 m as a supplementary sensor in 5b), and even those studies were working with man-made "hard target" scatterers (buildings, roads) that a remote, unvegetated alpine karst plateau largely lacks in the relevant form (dolines themselves are not buildings). No precedent was found anywhere of individual meter-scale natural karst collapse features being resolved by satellite InSAR of any resolution — Sentinel-1 or otherwise.

---

## Ranked Synthesis (most to least decisive for the feasibility question)

1. **Pixel/resolution mismatch (Section 1, 6):** Sentinel-1's ~20 m resolution cell is 1–2 orders of magnitude larger than a doline's surface expression (0.3–few m). This is a hard physical ceiling, not a processing or tuning problem — no amount of stacking, SBAS, or PSI refinement recovers spatial resolution the sensor never had. **Most decisive factor.**
2. **No precedent at doline scale, anywhere:** Every karst/sinkhole InSAR precedent found (Iran, Turkey, Texas, Philippines) operates at collapse-feature scales of tens to hundreds of meters — the domain where a subsidence bowl can plausibly span multiple resolution cells. None demonstrate meter-scale detection, with or without Sentinel-1.
3. **Alpine coherence loss compounds the problem (Section 4):** Seasonal snow (Dec–Mar analogue at Mt. St. Helens; presumably longer at ~2000 m in the Bavarian Alps), steep-slope geometric distortion (foreshortening/layover/shadow, confirmed for the Alps directly by Giffard-Roisin et al. 2022), and vegetation/scree instability would further degrade an already resolution-limited signal, likely leaving large parts of the plateau without usable coherent time series for a significant fraction of the year — the very months (snowmelt/thaw) when karst subsidence is mechanically most plausible.
4. **Scatterer geometry is uncontrollable:** Even where coherence exists, PS/DS points fall wherever the terrain happens to provide stable backscatter (rock outcrops, boulders), not necessarily at or near a specific doline of interest — confirmed by the Karapinar study's central finding that actual sinkholes formed precisely where InSAR had no usable signal.
5. **Deformation-magnitude sensitivity is not the bottleneck (Section 2):** If a usable, well-located, coherent scatterer existed, Sentinel-1 could plausibly detect the mm–cm-scale precursor signals that karst subsidence produces. This is the one respect in which InSAR is not disqualified — but it is moot given points 1–4.

## Feasibility Verdict

**Individual, doline-scale (meter-scale) subsidence detection with Sentinel-1 InSAR is not realistically feasible on the Zugspitzplatt, and the literature does not support listing it as a viable direct method for this purpose.** The core issue is an unbridgeable spatial-resolution mismatch (≥20 m pixels vs. ≤few-meter targets), not a fixable processing limitation, and it is compounded by well-documented alpine coherence problems (seasonal snow, steep-slope geometric distortion, sparse coherent scatterers away from bare rock) that are directly confirmed for the Alps in the literature reviewed here. Every located precedent for InSAR detecting karst-related subsidence operates at a feature scale one to two orders of magnitude larger than a doline, and the one study that specifically pursued localized, sub-decameter sinkhole detection deliberately used a much higher-resolution commercial X-band sensor (TerraSAR-X) rather than Sentinel-1. The Karapınar (Turkey) study is a particularly important cautionary precedent: even at a much larger scale with a longer observation record, the sinkholes that actually formed did so in areas where InSAR had no usable signal at all, not where deformation was detected.

This does **not** mean Sentinel-1 InSAR has no legitimate role in the thesis. A defensible, literature-supported repositioning would be: (a) use Sentinel-1 PSI/SBAS only to screen for **broader, plateau-scale or sub-catchment-scale subsidence trends** (tens of meters to hundreds of meters, e.g. a diffuse settling zone or a cluster of dolines expressed as a coherent-if-noisy regional signal) rather than to resolve individual features; (b) treat any Sentinel-1 signal as a coarse hazard-screening layer to be *cross-validated*, not as a primary doline-detection tool — consistent with how Aporto et al. (2026) and Orhan et al. (2021) both explicitly required ground validation/other data to make sense of their InSAR results; or (c) drop InSAR as a data source for individual doline monitoring in this thesis and rely instead on higher-resolution methods already better suited to meter-scale change detection (repeat UAV LiDAR/photogrammetry, terrestrial laser scanning, or GNSS at known doline sites), reserving Sentinel-1 (if used at all) for basin-scale context rather than the core doline-monitoring objective. Given the mismatch documented here, option (c), or a much-qualified version of (a), is the honest framing — Sentinel-1 InSAR should not be presented in the thesis as a method expected to resolve individual collapse dolines.

---

## Note on source access

Several relevant papers (ScienceDirect articles, some MDPI "htm" pages) returned HTTP 403 to automated fetching and could not be read in full; for these, citation metadata was verified independently via Crossref, and content claims were cross-checked across multiple independent search-engine excerpts of the same paper before being included, and are flagged above as "moderate confidence" rather than presented as directly verified full-text reads. Three sources (Giffard-Roisin et al. 2022, Aporto et al. 2026, Orhan et al. 2021) were read in full and are the highest-confidence sources underpinning the verdict above.
