# Causation hypothesis: karst dissolution vs. permafrost thaw on the Zugspitzplatt

Working synthesis from a literature pass (2026-08-22) through papers gathered so
far. States a composite hypothesis for *why* the 30-35 mapped features exist,
grounded in site-specific evidence rather than the generic "karst or
permafrost" framing in the original proposal. Supersedes that framing: the two
mechanisms are not competing explanations for one homogeneous population, they
plausibly act on different subsets of the features, or on the same feature at
different stages of its history.

## The composite hypothesis

Features on the Zugspitzplatt are most plausibly **inception or seismic
dolines, initiated along mapped fault sets, subsequently enlarged by
snowmelt-timing-driven CO2 corrosion (not simple thermal dissolution), with a
subset locally reactivated or deepened by melting relict ground ice trapped in
the depression itself.**

That is a chain of four distinct, individually-evidenced claims, not one
diffuse idea:

1. **Structural control on location.** Dolines preferentially initiate at
   lithological/structural discontinuities (a fault, a bed contact, a
   fracture zone) rather than uniformly across the plateau (Sauro 2003 —
   "inception" and "underprinting" dolines; also introduces "seismic
   dolines," funnel depressions forming directly along faults reactivated by
   earthquakes, later indistinguishable from ordinary solution dolines). Gams
   (2000) gives a mechanistic reason this should be true: more fractured rock
   has more specific surface area exposed to moisture, so dissolution
   initiates faster there, and growth is then self-reinforcing as the
   soil/rock interface area outpaces the plan-view opening.

2. **A real fault dataset exists to test this against.** Ortner & Kilian
   (2022) remapped the structural geology of the Wetterstein/Mieming massif
   and explicitly name and orient three fault sets crossing the Zugspitzplatt
   directly: the E-trending sinistral **Puitental** set, the NE-trending
   sinistral **Loisach** set, and the WNW-trending dextral **Ammer** set
   (their Fig. 7b has the mapped traces). This was previously a data gap
   (parking-lot item in `experiment_log.md`) — it no longer is.

3. **Karst dissolution here is snowmelt-timing-limited, not
   temperature-limited.** Küfmann (2013, field lysimeters run directly on the
   Zugspitzplatt subnival zone through the 2008 ablation season) found
   dissolution rate is CO2-limited: atmospheric CO2 diffuses down through the
   snowpack and is diurnally depleted, so solution rates peak only when snow
   *thins* late in the season and atmospheric exchange resumes (max 28 mg/l
   CaCO3 under 20 cm snow), not simply with warmer meltwater as the classic
   Corbel (1959) "cold water is more aggressive" model would predict. Wetzel
   (2004), monitoring the Partnach spring that drains this exact catchment
   (Wetterstein limestone, 11.4 km2), independently confirms the karst system
   is active and fast (conduit flow ~400 m/h, top decile of Dinaric karst
   systems) and explicitly names dolines as recharge points into it.
   **Testable prediction:** doline growth/activity should correlate with
   remotely-sensed snow-cover *thinning timing*, not raw precipitation or
   air-temperature sums — a different variable than what the original
   proposal's research direction 2 specified.

4. **A subset is plausibly permafrost/relict-ice driven, but not via regional
   alpine permafrost.** Gude & Barsch (2005), the single most load-bearing
   paper found so far, establish that regional permafrost is essentially
   *absent* on the Zugspitzplatt surface itself (BTS survey mean -1.2 degC,
   PERMAMAP model puts the plateau below the modeled permafrost limit) except
   in small relict-ice patches in moraine/bedrock — meaning any permafrost
   effect at the 30-35 dolines is a **local cold-trap phenomenon** (a doline
   floor pools cold air and snow, locally sustaining ground ice long after
   regional permafrost retreated), not "typical" alpine permafrost thaw. They
   also report a **named, site-specific precedent**: subsidence in the
   rack-railway tunnel where it cuts through frozen debris inside a doline on
   the Zugspitzplatt, stabilized only by pumping concrete into the resulting
   void — direct documented evidence of thermokarst collapse from melting
   relict ground ice at this exact location, plus a lake at the foot of the
   south slope that drained suddenly, "presumably caused by thermokarst and
   not just by karst processes."

## Age heterogeneity: the population is probably not one thing

Grüger & Jerz (2011 publ., dated 2010) excavated and pollen/AMS-dated the fill
of an actual named doline on the Zugspitzplatt (~120 m south of the
Weisses-Tal lift station, 2290 m): basal fill dates to 7415+/-30 BP
(early-Atlantic Holocene thermal optimum), the site was never overridden by
ice since then (the mid-Holocene Löbben re-advance, ~3400-3100 BP, came close
but stopped short), and the fill is loess-like, accumulating continuously and
slowly (~1 m in ~7400 years) — not a catastrophic infill event.

This means the 30-35 mapped features very likely mix an **old, stable,
slowly-filling solution-doline population** with a **younger, still-active
population** (of which the thermokarst-tunnel case above is one confirmed
member). Practical implication: a single genetic story for "the dolines"
collapses this distinction. Splitting the population — by morphometry first
(see below), ideally by direct dating of a subsample later — should be a
goal, not an afterthought.

## Morphometric handle on the split (before any dating is feasible)

- Péntek, Veress & Lóczy (2007) fit doline cross-sectional profiles to a
  parametric "meridian function" (three shape parameters controlling
  steepness/curvature/width) derived from field surveys, giving four
  quantitative shape classes (widening-at-rim-and-base,
  widening-at-base-only, widening-at-rim-only, deepening-without-widening).
  This is a ready-made, non-ad-hoc alternative to circularity (already ruled
  out as a filter, see `experiment_log.md` 2026-08-14 entries) for
  classifying the UAV-DEM-derived profiles of the mapped dolines.
- Veress (2017) gives published diameter/depth/wall-slope baselines for
  alpine "schachtdolines" (vertical-walled, snow-patch-driven deepening;
  mean diameter 9.4 m, depth 6.5 m, slope 54-78 degrees) and smaller solution
  dolines (diameter 7.1 m, depth 2.0 m) from comparable Alpine/Dinaric
  glaciokarst settings — a direct comparison baseline once polygon (not just
  point) geometry is available for the manually mapped features.
- Both Gutierrez, Guerrero & Lucha (2008) and Sauro (2003) independently warn
  about **equifinality**: collapse-looking morphology does not prove a
  collapse origin (sagging, solutional, and collapse mechanisms can converge
  on similar final shapes; a present-day "drawdown" doline in Sauro's worked
  example began life as a collapse doline). This is a real methodological
  constraint on how confidently the thesis can assign a mechanism from UAV
  morphology alone — an argument for triangulating with the fault-alignment
  test and multi-temporal change detection rather than resting on shape
  classification by itself.

## What this changes about the existing research directions

- Research direction 2 ("correlating doline activity with precipitation,
  snowmelt timing, Zugspitze summit air temperature") should specifically add
  **snow-cover thinning date** as its own variable, not just snowmelt
  timing/volume — Küfmann's mechanism predicts thinning timing is the
  relevant driver, and it is a different (and separately obtainable, e.g.
  from UAV/Sentinel snow-cover series) signal than bulk melt volume.
- The fault/lineament correlation flagged as a parking-lot item (no dataset
  sourced) is now unblocked: Ortner & Kilian (2022) Fig. 7b can be digitized
  and tested against doline long-axis orientation and cluster alignment.
- If subsurface fieldwork happens in August 2026, Krautblatter et al. (2010)
  provide a validated ERT protocol and a resistivity-temperature calibration
  curve *for this exact bedrock* (Wetterstein limestone) from a gallery on
  the Zugspitze itself — removes the need to redo lab calibration from
  scratch. Thermal UAV (already a proposed data source, not yet used) is a
  cheaper non-contact analog for the same seasonal thaw-front signal near
  the surface.

## References (full citations, as extracted from the source PDFs)

- Gude, M. & Barsch, D. (2005). Assessment of geomorphic hazards in
  connection with permafrost occurrence in the Zugspitze area (Bavarian
  Alps, Germany). *Geomorphology*, 66, 85-93.
- Wetzel, K.-F. (2004). On the hydrology of the Partnach area in the
  Wetterstein Mountains (Bavarian Alps). *Erdkunde*, 58(2), 172-186.
- Küfmann, C. (2013). Solution dynamics at the rock/snow interface during
  the ablation period in the subnival karst of the Wetterstein Mountains.
  [Manuscript; final publication venue not confirmed from the PDF itself —
  verify before citing in the thesis.]
- Grüger, E. & Jerz, H. (2010/2011). Untersuchung einer Doline auf dem
  Zugspitzplatt. *E&G Quaternary Science Journal*, 59(1-2), 66-75.
- Ortner, H. & Kilian, S. (2022). Thrust tectonics in the Wetterstein and
  Mieming mountains, and a new tectonic subdivision of the Northern
  Calcareous Alps. *International Journal of Earth Sciences*, 111, 543-571.
- Sauro, U. (2003). Dolines and sinkholes: aspects of evolution and problems
  of classification. *Acta Carsologica*, 32(2), 41-52.
- Gams, I. (2000). Doline morphogenetic processes from global and local
  viewpoints. *Acta Carsologica*, 29(2), 123-138.
- Veress, M. (2017). Solution doline development on glaciokarst in alpine
  and Dinaric areas. *Earth-Science Reviews*, 173, 31-48.
- Peentek, K., Veress, M. & Loeczy, D. (2007). A morphometric classification
  of solution dolines. *Zeitschrift fuer Geomorphologie*, 51(1), 19-30.
- Gutierrez, F., Guerrero, J. & Lucha, P. (2008). A genetic classification
  of sinkholes illustrated from evaporite paleokarst exposures in Spain.
  *Environmental Geology*, 53, 993-1006.
- Krautblatter, M., Verleysdonk, S., Flores-Orozco, A. & Kemna, A. (2010).
  Temperature-calibrated imaging of seasonal changes in permafrost rock
  walls by quantitative electrical resistivity tomography (Zugspitze,
  German/Austrian Alps). *Journal of Geophysical Research: Earth Surface*,
  115, F02003.

## Open items / not yet resolved

- Küfmann (2013) citation is from a manuscript PDF; confirm final published
  venue (journal, year) before using in the thesis bibliography.
- None of the above directly dates when the *younger* subset of dolines
  formed — Grüger & Jerz only dates one old, stable example. Direct dating
  of a suspected-young feature (if one is identified by morphometry or
  multi-temporal change detection) would be needed to actually test the
  "recent thermokarst reactivation" half of the hypothesis, not just argue
  it's plausible.
- The fault-alignment test (direction 2 above) has not been run yet — this
  document states the hypothesis and unblocks the data, it does not report a
  result.
