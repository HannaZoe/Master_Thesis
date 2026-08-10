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

Fill this in once real data arrives — path to the external drive / network
location / cloud storage where the raw files actually live, since they're
not in git. Example:

```
Raw UAV point clouds: <drive/path> — <short description, date acquired>
```

Keeping this section current is more important than it looks: it's the only
record of where the source data is once it's not in the repo.
