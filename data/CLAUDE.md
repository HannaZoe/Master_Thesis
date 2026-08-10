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

Fill in specifics once real data arrives, e.g.:

```
Raw UAV point clouds: data/raw/<campaign-name>/ — <short description, date acquired>
```
