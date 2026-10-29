# fieldwork/

Material for the August 2026 Zugspitzplatt field campaign, grouped by
activity rather than split across `data/`'s raw/interim/processed/manual
split — everything about this one trip lives together.

- `presentation/` — the team briefing deck (`.odp`) and its source
  figures/photos. See its own history in `docs/experiment_log.md` for how
  the content was built and reviewed.
- `qfield/` — the QField project (`.qgz` + GeoPackage) built ahead of the
  trip for structured field data entry (person/type/notes/lat/lon). Turned
  out to be used in the field, but shared back as a local export rather
  than synced via QFieldCloud — see `field_data/raw/` for that actual
  output. Revisit setting up real QFieldCloud sync before the next trip now
  that the project schema is confirmed to work in practice.
- `field_data/` — the real field-collected data, two independent sources
  from 2026-08-27 (a field-notes app export, and the QField project's own
  export). Same split as `data/`:
  - `field_data/raw/` — **not tracked in git** (gitignored, see root
    `.gitignore`), data exactly as received, ~170MB of photos + device
    exports. Never edit in place.
  - `field_data/field_verification_20260827_{lower,higher}.gpkg` — **tracked
    in git**, same exception as `data/manual/` (small, original, not
    regenerable). Cleaned/structured output of `scripts/import_field_notes.py`
    — depth/width parsed from free-text field notes where unambiguous, with
    explicit `review_flag`/`unit_inferred` columns marking anything that
    needed a judgment call rather than silently guessing. Read
    `scripts/import_field_notes.py`'s module docstring and the
    2026-10-29 `docs/experiment_log.md` entry before trusting a value from
    here — several entries are deliberately null with a flag explaining why,
    and that's the honest result, not a bug to fix.

Not yet decided: whether/how to merge the field-verified locations that
don't match anything in `data/manual/Sinkholes.shp` /
`Suspicious_Areas.shp` into those files — that changes the project's
ground-truth dataset, so it needs an explicit decision, not a silent merge.
