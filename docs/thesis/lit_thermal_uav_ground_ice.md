# Literature review: Thermal UAV imagery for near-surface ground ice / thermokarst detection

Compiled for the Zugspitzplatt doline thesis (thermokarst hypothesis for collapse dolines). Scope: UAV/airborne thermal infrared (TIR) methodology for detecting near-surface ground ice or permafrost; thermal UAV/remote sensing applications in karst and doline settings; Alpine/mountain permafrost precedent at meter-scale resolution; and practical survey-condition guidance. Sources were read in full where open access allowed; where only abstract/metadata could be retrieved (publisher paywalls, bot-blocked), this is stated explicitly and the entry is weighted accordingly in the synthesis.

---

## 1. Messmer, J. & Groos, A. R. (2024). "A low-cost and open-source approach for supraglacial debris thickness mapping using UAV-based infrared thermography." *The Cryosphere*, 18, 719–746. https://doi.org/10.5194/tc-18-719-2024

**Read:** full text (open access, Copernicus).

**Summary:** A DJI Mavic Pro fitted with a FLIR Vue Pro R 640 (~140 g, claimed accuracy ±5 °C or 5% of reading) flown at 100 m AGL with 75% overlap, radiometric orthomosaics built in a fully open-source pipeline (ExifTool → OpenDroneMap/SfM → QGIS/R). Surface temperature is used as a proxy for *debris thickness* over glacier ice: thin debris lets more subsurface heat through and reads warmer; thick debris insulates and reads cooler. This requires: (1) atmospheric-transmission correction using flight altitude and water-vapour pressure from a nearby station, (2) a reflected-radiation correction using aluminium-foil-wrapped GCPs, and (3) an assumed emissivity (0.95 for debris/limestone-type material, 0.97 for ice/snow) which the authors flag as a genuine, unresolved source of uncertainty needing site-specific validation. Afternoon acquisition (13:00–15:00) under clear, calm conditions was necessary to get enough thermal heterogeneity to be useful; the method needs 40+ in-situ ground-truth points for calibration and is only demonstrated for debris <~50 cm thick over a known ice interface.

**Relevance:** This is the most methodologically transferable paper found — cheap hardware, open-source workflow, explicit radiometric correction steps, and an honest uncertainty discussion. But note what it actually demonstrates: a *known, laterally continuous* ice body under a *variable-thickness insulating cover*, where the calibration target (debris thickness) is the thing being inferred, not "ice present/absent." For the Zugspitzplatt this is the closest published analogue to the physical logic needed (surface T as insulation/heat-flux proxy) but it also shows how much correction and ground truth is required before a thermal orthomosaic means anything quantitative — a raw thermal photo is not usable science-grade data without this pipeline.

---

## 2. Kaiser, S., Boike, J., Grosse, G., & Langer, M. (2022). "The Potential of UAV Imagery for the Detection of Rapid Permafrost Degradation: Assessing the Impacts on Critical Arctic Infrastructure." *Remote Sensing*, 14(23), 6107. https://doi.org/10.3390/rs14236107

**Read:** full text (via cached rendering).

**Summary:** Despite the title, this study does **not** use thermal imagery at all — it detects permafrost degradation via RGB structure-from-motion photogrammetry and repeat point-cloud differencing (M3C2), i.e. surface *subsidence*, not surface *temperature*. It documents ~0.35 m of median displacement at a Dalton Highway thermal-erosion site between 2018–2019 surveys, and explicitly states the method only works for multi-year, large-magnitude change (registration RMSE ~1 m), not seasonal or subtle degradation.

**Relevance:** Important negative/clarifying finding for this project: a paper that reads as directly on-topic from its title is actually an RGB-photogrammetry displacement study, not a thermal one. This is a useful caution when scoping the literature — "UAV + permafrost degradation" papers frequently mean geometric change detection, not thermal ground-ice detection. For Zugspitzplatt, repeat UAV photogrammetry (DEM differencing across survey epochs) is a separate, better-evidenced tool for detecting doline subsidence than thermal imagery is for detecting the ice driving it.

---

## 3. van der Sluijs, J., Kokelj, S. V., Fraser, R. H., Tunnicliffe, J., & Lacelle, D. (2018). "Permafrost Terrain Dynamics and Infrastructure Impacts Revealed by UAV Photogrammetry and Thermal Imaging." *Remote Sensing*, 10(11), 1734. https://doi.org/10.3390/rs10111734

**Read:** full text (via cached rendering).

**Summary:** Combines UAV photogrammetry with a SenseFly ThermoMAP sensor (7.5–13.5 µm, 0.1 °C resolution) over Arctic thaw slumps/thermokarst terrain. Thermal data is used only *qualitatively*: exposed, actively thawing ground-ice headwalls read colder than stable headwalls draped in a veneer of thawed sediment, letting analysts visually distinguish "active" from "stabilized" ice exposures. Critically, the sensor assumes emissivity = 1 (i.e., captures uncorrected radiant, not true kinetic, temperature), the mosaic was never corrected for topography or emissivity, and the authors state outright that the raw output was "sufficient for qualitative interpretation" only — no quantitative ice-depth relationship is derived or claimed, and no optimal time-of-day is specified.

**Relevance:** A second, more explicit demonstration that even well-resourced Arctic thermokarst studies stop at qualitative, visually-interpreted thermal contrast (exposed ice vs. covered ice at the surface) rather than any depth-quantified ground-ice signal. This sets a realistic ceiling on what the Zugspitzplatt thermal dataset can be expected to show: possible qualitative anomalies at exposed features, not a quantitative subsurface-ice map, unless a much more rigorous (Messmer & Groos-style) correction pipeline is applied.

---

## 4. Kellerer-Pirklbauer, A. (2019). "Long-term monitoring of sporadic permafrost at the eastern margin of the European Alps (Hochreichart, Seckauer Tauern range, Austria)." *Permafrost and Periglacial Processes*, 30(4), 260–277. https://doi.org/10.1002/ppp.2021

**Read:** full text (PMC, open access).

**Summary:** 15 years of ground-truth Alpine permafrost monitoring (2004–2018) using data-logger ground temperatures at 12 sites, BTS (bottom-temperature-of-snow) surveys (394 points), ERT (24 profiles), and a fixed camera for snow patterns — **no thermal remote sensing or UAV imagery used at all**. Found sporadic permafrost at ~2400 m persisting at only slightly-below-0 °C, with statistically significant warming 2000–2018 and a projection that the permafrost will likely disappear within decades. Notably flags that BTS single-campaign snapshots are "highly vulnerable to fail" due to randomness in snow conditions, and that ERT is difficult to interpret in substrate "rich in open voids" (i.e., karst).

**Relevance:** Directly useful context, not for its thermal methodology (it has none) but for two things: (1) it is an actual published precedent for the ERT-void-interpretation problem that is directly relevant to Zugspitzplatt's karstified Wetterstein limestone bedrock, reinforcing why Krautblatter (2010) and Scandroglio et al. (2026) had to validate ERT carefully for this exact lithology; and (2) it is a reminder that the standard Alpine permafrost-monitoring toolkit (loggers, BTS, ERT) as practiced by the most relevant regional research groups still does not routinely include thermal UAV — this method has not been mainstreamed even in the closest comparable Alpine permafrost research tradition.

---

## 5. Scandroglio, R., Weber, S., Limbrock, J. K., & Krautblatter, M. (2026). "Field-validated imaging of decadal and seasonal changes in permafrost bedrock using quantitative electrical resistivity tomography (Zugspitze, Germany/Austria)." *The Cryosphere*, 20, 4787–4809. https://doi.org/10.5194/tc-20-4787-2026

**Read:** full text (open access, Copernicus).

**Summary:** The project's own reference ERT study. Electrodes were placed inside the Kammstollen tunnel (i.e., subsurface, not surface arrays) across 6 transects, run monthly 2014–2023, resolving a frozen lens with roughly 20–30 m vertical extent and distinguishing frozen/partially-frozen/unfrozen zones via k-means clustering on a field-calibrated temperature–resistivity relation. The paper discusses passive seismic monitoring and relative gravimetry as regional complementary geophysical methods. **It does not mention thermal imaging, UAV surveys, or any remote-sensing method, nor does it mention dolines, sinkholes, or thermokarst** anywhere in the reviewed content.

**Relevance:** Confirms that the validated ERT precedent for this exact bedrock is a deep (tunnel-based), decadal, geophysical method with no thermal-UAV component — i.e., there is no existing published bridge between the ERT ground-truth and a thermal-UAV proxy at Zugspitzplatt. Any claim that thermal UAV is a "cheaper complement to ERT" for this site would be a novel contribution of the thesis, not something supported by prior work at this location. Also useful as confirmation that dolines/thermokarst are not yet addressed in the group's own published Zugspitze permafrost literature — reinforcing that this thesis's core linkage (dolines ↔ relict ice ↔ thermal signal) is genuinely unstudied ground, not something to search harder for.

---

## 6. Cagnazzo, C. & Angelini, S. (2025). "Vertical Temperature Profile Test by Means of Using UAV: An Experimental Methodology in a Karst Sinkhole of the Apulia Region (Italy)." *Meteorology*, 4(2), 15. https://doi.org/10.3390/meteorology4020015

**Read:** full text (via cached rendering).

**Summary:** A DJI Phantom 3 Pro carrying a temperature data logger (not a thermal camera — this is a point-sensor vertical air-temperature profile, not thermal imagery) flown vertically to 80 m above a sinkhole floor, validated against three ground weather stations. Found strong cold-air-pooling thermal inversions under high-pressure winter conditions: >1 °C/m cooling near the floor, >4 °C difference between floor and 80 m height in the morning.

**Relevance:** Confirms (using UAV, though not thermal-imaging UAV) that dolines/sinkholes are strong cold-air traps under calm, clear, stable-anticyclone conditions — a real physical confound for any thermal-UAV survey over a doline: near-surface air-temperature inversions inside the depression will overprint any weaker ground-surface-temperature signal related to subsurface ice, especially in early morning. This is directly actionable: any Zugspitzplatt thermal-UAV survey needs to distinguish "cold because of pooled night air in the basin" from "cold because of ice-cored ground," which are physically different signals with very different persistence.

---

## 7. Dobos, A., Dobos, E., & Farkas, R. (2025). "Terrain-Based High-Resolution Microclimate Modeling for Cold-Air-Pool-Induced Frost Risk Assessment in Karst Depressions." *Climate*, 13(10), 205. https://doi.org/10.3390/climate13100205

**Read:** full text (via cached rendering).

**Summary:** Combines a 2.4 cm UAV-photogrammetry DSM with SAGA GIS terrain indices (sky-view factor, wind exposition, cold-air-flow accumulation) and ground dataloggers, **plus radiometric thermal-camera (Seek Thermal) surveys used specifically to validate the spatiotemporal position of the cold-air pool inside a sinkhole (Mohos sinkhole, Hungary) through the day**. Found extreme cooling at the sinkhole floor (daily T-min differences of up to −16 °C vs. nearby control points; absolute minimum −28.2 °C), that inversions can persist through daytime on shaded slopes even under full sun, and that under strongly stable anticyclonic conditions the inversion can remain intact all day. Thermal imagery captured the boundary/timing of inversion breakdown and re-establishment.

**Relevance:** The strongest close analogue found for "thermal camera + doline" as a validated field method — but note its target variable is **cold-air-pool position/persistence** (a near-surface *atmospheric* phenomenon), not ground ice. It is genuinely useful methodology (thermal surveys on transitional-season dates, repeated through a diurnal cycle, cross-validated against terrain indices and loggers) and directly warns that a doline's own microclimate (radiative cooling, sky-view factor, wind sheltering) will dominate its surface thermal signature independent of anything happening in the ground beneath it. For Zugspitzplatt, this means a single thermal UAV pass over a doline is at serious risk of just imaging the cold-air-pool/inversion pattern of the depression's geometry, not a ground-ice signal — unless survey timing and conditions are chosen specifically to suppress this confound (e.g., avoiding calm clear nights/mornings, or explicitly separating air-temperature effects via multi-time-of-day repeat surveys as this paper does).

---

## 8. Pérez-García, J. L., Sánchez-Gómez, M., Gómez-López, J. M., et al. (2018). "Georeferenced thermal infrared images from UAV surveys as a potential tool to detect and characterize shallow cave ducts." *Engineering Geology*, 246, 277–287. https://doi.org/10.1016/j.enggeo.2018.09.014

**Read:** abstract + multiple independent secondary summaries (publisher/ResearchGate paywalled/bot-blocked; full text not obtained — treat findings below as reliable but not independently verified against original figures/tables).

**Summary:** UAV-borne TIR camera survey over a limestone doline field with known shaft/cave entrances in the Betic Cordillera, southern Spain. Detection relies on thermal inertia contrast between cave-conditioned air and the rock surface. The main shaft was thermally monitored at depth and showed two distinct seasonal regimes: summer thermal/air stratification (little surface expression) vs. winter upward airflow and temperature homogenization (strong surface expression). **Winter dawn surveys gave the most distinctive thermal anomalies** at cave entrances — i.e., maximum air-temperature contrast between the (relatively warm, buffered) cave air and the (very cold, radiatively-cooled) rock surface.

**Relevance:** This is the one study found that is a near-exact geomorphological analogue — a doline field in karstified limestone, UAV thermal camera, entrance/conduit detection. The key transferable finding is the *seasonal/diurnal asymmetry*: the karst-air-exchange signal is strong in winter (especially dawn) and weak/absent in summer. If Zugspitzplatt's existing thermal UAV data was collected in summer (the only season UAVs are normally flown on this snow-covered plateau), this paper's own logic suggests any karst-airflow-driven signal would be at its weakest, and whatever thermal contrast is visible is more likely dominated by insolation/surface-cover effects than by subsurface air or ice. This is an important caution to check against the actual acquisition metadata of the project's thermal dataset.

---

## 9. Gil, D., Sánchez-Gómez, M., & Tovar-Pescador, J. (2025). "Microclimate variability in a highly dynamic karstic system." *Geosciences*, 15(8), 280. https://doi.org/10.3390/geosciences15080280

**Read:** full text (via cached rendering).

**Summary:** Five years (2017–2022) of temperature/humidity dataloggers at 0–13 m depth across eight cave entrances in a Mediterranean karst system, cross-referenced with WRF reanalysis meteorology. Confirms strong, predictable seasonal chimney-effect airflow (winter-running vs. summer-running entrances) and near-constant deep-karst equilibrium temperature. Cites Pérez-García et al. (2018) as a *potential* detection tool but did not itself use thermal imagery.

**Relevance:** Reinforces (independently of #8) that karst conduit/void systems generate genuine, physically well-understood, and large (multi-°C) thermal anomalies at entrances — but driven by *cave-air chimney convection*, which requires an open connected void/conduit system with measurable airflow. This mechanism does not obviously apply to a doline whose collapse is driven by *thaw of an isolated, sealed body of relict ground ice* with no active air conduit — a physically different (and likely much weaker, more diffuse) thermal signature than an open cave shaft. This is a meaningful caution against over-extrapolating the promising karst-cave thermal literature (topic 2) to the ground-ice mechanism this thesis actually investigates.

---

## 10. Alphonse, A. B., Osuch, M., Wawrzyniak, T., & Hanselmann, N. (2024). "Spatio-temporal variability of surface temperatures in High Arctic periglacial environment using UAV thermal imagery and in-situ measurements." *GIScience & Remote Sensing*, 62(1). https://doi.org/10.1080/15481603.2024.2435851

**Read:** abstract/metadata only (publisher site returned a bot-verification wall on every fetch attempt, including via proxy; DOAJ open-access repository copy also blocked). Findings below are therefore lower-confidence and should be re-checked against the primary text before citing in the thesis (open-access CC-BY, so the PDF should be obtainable directly by the user, e.g. via institutional network or by visiting the DOI link in a normal browser).

**Summary (from abstract/search metadata):** UAV thermal camera survey of ground and water temperatures in a High Arctic periglacial catchment (SW Spitsbergen), paired with in-situ measurements, addressing thermal-drift correction and data harmonization across repeat UAV thermal surveys.

**Relevance:** Potentially one of the most relevant precedents (periglacial terrain, UAV thermal, multi-temporal, explicit sensor drift-correction methodology) but could not be verified in full text within this session. Flagged as a priority follow-up: the user should retrieve this open-access paper directly and check specifically (a) what ground-truth relationship, if any, it establishes between surface temperature and subsurface ice/thaw state, and (b) its stated drift-correction/calibration procedure, which could be directly reusable for processing the Zugspitzplatt dataset.

---

## Cross-cutting points from broader (snippet-level) search, not tied to one deep-read source

- **Depth sensitivity is shallow and rarely quantified.** Across the permafrost/periglacial thermal-UAV literature, no source found here gives a validated, general depth-of-detection figure for ground ice from surface thermal imagery; where a method is quantitative at all (Messmer & Groos, debris thickness), it is calibrated to a specific site and cover type, not transferable as a rule of thumb. Treat any "thermal IR sees X cm down" claim with skepticism unless traced to a specific validated study.
- **Diurnal timing matters enormously and is site-specific.** Studies that report timing effects (glacier debris: early-mid afternoon; karst cave entrances: winter dawn; sinkhole cold-air pooling: worst near dawn after clear calm nights) agree the *direction* of the effect (surveys need to target maximum, unconfounded thermal contrast) but not a single universal time window — the optimal window has to be derived for the target mechanism and site, not borrowed from a different setting.
- **Snow, vegetation, moisture, and micro-topography are the dominant confounds at doline/meter scale**, consistently flagged across both the permafrost active-layer literature and the karst microclimate literature. A collapse doline is exactly the kind of micro-topographic depression (variable snow retention, shading, cold-air pooling, possible standing water) where these confounds are strongest, not weakest.
- **Emissivity correction for carbonate rock is non-trivial** — general thermography literature confirms limestone/calcite does not fit standard "spectrally smooth" temperature–emissivity separation algorithms, and several UAV studies reviewed above either assumed emissivity = 1 (uncorrected, van der Sluijs et al. 2018) or used literature-value approximations with acknowledged uncertainty (Messmer & Groos 2024). Any quantitative use of the Zugspitzplatt thermal dataset will need its own emissivity handling for Wetterstein limestone, not an assumption carried over from ice/snow or debris studies.

---

## Ranked synthesis (most to least directly useful for this project)

1. **Dobos, Dobos & Farkas (2025)** and **Cagnazzo & Angelini (2025)** — best methodological precedent for what a thermal (or thermal-adjacent) UAV/sensor survey of *this specific landform type* (karst doline/sinkhole) actually shows: strong, well-documented cold-air-pooling signals that are real, physically important, but are a *confound* for ground-ice detection, not the ground-ice signal itself. Essential reading before interpreting the existing thermal dataset.
2. **Pérez-García et al. (2018)** and **Gil, Sánchez-Gómez & Tovar-Pescador (2025)** — the closest geomorphological analogue (doline field, karst, UAV thermal), but the mechanism they detect (chimney-effect cave airflow through open conduits) is physically distinct from thaw of an isolated relict ice body, and the seasonal/diurnal asymmetry they report (winter dawn >> summer) is a serious caution if the project's thermal survey was flown in summer.
3. **Messmer & Groos (2024)** — best template for an actual processing pipeline (radiometric correction, GCPs, emissivity handling, open-source tools) if the project wants to move from a qualitative thermal orthomosaic to something quantitatively defensible.
4. **van der Sluijs et al. (2018)** and **Kellerer-Pirklbauer (2019)** and **Kaiser et al. (2022)** — collectively set realistic expectations: even in well-funded, closely-related permafrost/thermokarst research (including the nearest Alpine-permafrost research tradition to this project), thermal UAV imagery is either absent from the standard toolkit or used only for qualitative, visually-interpreted contrast — never as a validated, depth-quantified ground-ice proxy.
5. **Scandroglio et al. (2026)** — confirms there is no existing thermal-UAV/ERT bridge at this exact site; the linkage would be a novel (and unvalidated) contribution of this thesis, not an established complement.
6. **Alphonse et al. (2024)** — flagged as a priority follow-up read (full text not obtained); potentially very relevant but unverified here.

## Honest overall assessment

Thermal UAV imagery is a real, established tool for two things this project does **not** primarily need: (a) qualitative visual discrimination between exposed/bare ground-ice and covered/vegetated ground in already-known thermokarst terrain (Arctic slump literature), and (b) detection of strong, mechanistically well-understood convective air-exchange anomalies at open karst conduits and cold-air-pooling in closed depressions. Neither of these is the same problem as inferring the presence, depth, or thaw state of an *isolated, sealed body of relict ground ice beneath a doline floor from its surface temperature* — no source located in this search establishes that relationship, quantitatively or even robustly qualitatively, at any site, karst or otherwise. The physical logic that would make it work (insulating overburden reduces surface heat flux from a cold body below, analogous to Messmer & Groos's debris-thickness proxy) is plausible but unvalidated for ground ice under karst regolith, and it is directly competing, at the same spatial scale, with a much better-documented and generally stronger confound: doline-scale cold-air pooling and micro-topographic radiative effects (points 6–7 above), which will dominate the surface thermal signal of a closed depression under exactly the calm, clear conditions that would otherwise be chosen for a "good" thermal survey.

Practically, this means: the project's already-collected thermal UAV epoch is very unlikely to be usable, on its own, as direct evidence of relict ground ice — but it could still be scientifically useful in a narrower, better-supported role: (1) as a qualitative/exploratory dataset to flag candidate dolines with anomalous surface-temperature patterns for follow-up ERT (the validated method for this bedrock), rather than as a standalone proxy; (2) if — and only if — the acquisition metadata show it was flown under clear, calm, low-wind conditions with a known time-of-day and season, ideally repeated across a diurnal cycle to allow the cold-air-pool/inversion signal to be modeled and subtracted (per Dobos et al.'s approach) rather than being mistaken for a ground-ice signal; and (3) only with a proper radiometric/emissivity correction pipeline (per Messmer & Groos) rather than raw brightness-temperature interpretation. If the existing survey was a single summer daytime pass with no repeat/diurnal component and no radiometric calibration or ground-truth points, the honest recommendation is to treat it as a low-value exploratory layer at best, and to prioritize ERT (already validated for this bedrock) as the primary ground-ice evidence, using thermal UAV — if flown again — as a hypothesis-generating reconnaissance tool with a carefully chosen (winter dawn, clear, calm, ideally multi-pass) acquisition window rather than as primary proof.
