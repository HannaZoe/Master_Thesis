# src/master_thesis/

Installable package (via `uv`) holding reusable code — anything called from
more than one notebook/script, or complex enough to want tests. One-off
exploratory code stays in `notebooks/`, not here.

## Conventions

- Type hints on function signatures.
- `pathlib.Path`, not string paths.
- Functions take/return data (arrays, GeoDataFrames, paths) rather than
  reading global config or hardcoding paths from `data/` — callers (notebooks,
  scripts) decide which files to point at.
- No I/O side effects on import — importing a module shouldn't read files or
  print anything.
- New submodules only when there's an actual second caller; don't pre-build
  a `preprocessing/`, `io/`, `analysis/` split before there's code to put in
  each one.

Tests for this package go in `tests/`, mirroring the module structure.
