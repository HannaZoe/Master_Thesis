"""Download historical Bavaria DOP20 orthophotos (2003-present) over an AOI.

Uses the free, no-auth WMS "Historische DOP" service from the Bavarian
surveying administration. For each available year, checks the actual flight
date via GetFeatureInfo and only downloads years that fall in a configurable
snow-free month window -- see SNOW_FREE_MONTHS below.

Important: the month filter is a heuristic, not proof. We already got burned
once trusting a date as "probably snow-free" (the June 2025 UAV flight turned
out to still be mostly under snow -- see docs/experiment_log.md). Every
downloaded image also gets a rough brightness-based snow warning, but you
still need to eyeball each result in QGIS before using it for mapping.

Usage:
    uv run python scripts/download_bavaria_dop.py
"""

from __future__ import annotations

import re
import urllib.request
from datetime import date
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.mask
from rasterio.merge import merge

WMS_BASE = "https://geoservices.bayern.de/od/wms/histdop/v1/histdop?"
AOI_PATH = Path("data/manual/Zugspitze_AOI.geojson")
OUT_DIR = Path("data/raw/bavaria_dop_hist")
# native to this service; project default is EPSG:32632, reproject explicitly if combining
CRS = "EPSG:25832"

SNOW_FREE_MONTHS = {6, 7, 8, 9}  # June-September; adjust if too strict/loose
MAX_DATES_PER_YEAR = 2
TILE_SIZE_M = 1000  # well under the WMS's 6000x6000 px cap at 20cm resolution
SNOW_WARNING_THRESHOLD = (
    0.5  # fraction of AOI flagged bright+low-saturation; below this still usable
)


def available_years() -> list[int]:
    """Ask the service what years it actually has, instead of assuming."""
    url = WMS_BASE + "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities"
    xml = urllib.request.urlopen(url).read().decode()
    years = {int(y) for y in re.findall(r"by_dop_(\d{4})_h<", xml)}
    return sorted(years)


def capture_dates_in_aoi(year: int, aoi_bounds: tuple[float, float, float, float]) -> list[date]:
    """Query GetFeatureInfo at a grid of points across the AOI to find which
    actual capture date(s) this year's mosaic covers here. A single annual
    layer can span more than one date if the AOI straddles a flight seam.
    """
    minx, miny, maxx, maxy = aoi_bounds
    xs = np.linspace(minx, maxx, 4)
    ys = np.linspace(miny, maxy, 3)

    found: set[date] = set()
    for x in xs:
        for y in ys:
            half = 25
            bbox = f"{x - half},{y - half},{x + half},{y + half}"
            url = (
                WMS_BASE + "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo"
                f"&LAYERS=by_dop_{year}_h&QUERY_LAYERS=by_dop_{year}_h_info"
                f"&CRS={CRS}&BBOX={bbox}&WIDTH=50&HEIGHT=50&I=25&J=25"
                "&INFO_FORMAT=text/plain&FEATURE_COUNT=1"
            )
            try:
                text = urllib.request.urlopen(url).read().decode()
            except Exception:
                continue
            match = re.search(r"ua = '(\d{2})\.(\d{2})\.(\d{4})'", text)
            if match:
                day, month, yr = (int(v) for v in match.groups())
                found.add(date(yr, month, day))
    return sorted(found)


def _tile_bounds(minx: float, miny: float, maxx: float, maxy: float, size: float):
    x = minx
    while x < maxx:
        y = miny
        x_end = min(x + size, maxx)
        while y < maxy:
            y_end = min(y + size, maxy)
            yield (x, y, x_end, y_end)
            y = y_end
        x = x_end


def fetch_tile(year: int, bounds: tuple[float, float, float, float]) -> rasterio.io.MemoryFile:
    minx, miny, maxx, maxy = bounds
    width = max(1, round((maxx - minx) / 0.2))
    height = max(1, round((maxy - miny) / 0.2))
    url = (
        WMS_BASE + "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap"
        f"&LAYERS=by_dop_{year}_h&CRS={CRS}"
        f"&BBOX={minx},{miny},{maxx},{maxy}&WIDTH={width}&HEIGHT={height}"
        "&FORMAT=image/tiff&STYLES="
    )
    data = urllib.request.urlopen(url).read()
    memfile = rasterio.io.MemoryFile(data)
    return memfile


def download_year(year: int, capture_date: date, aoi: gpd.GeoDataFrame, out_dir: Path) -> Path:
    minx, miny, maxx, maxy = aoi.total_bounds
    tiles = list(_tile_bounds(minx, miny, maxx, maxy, TILE_SIZE_M))
    print(f"  downloading {len(tiles)} tile(s) for {year} ({capture_date})...")

    memfiles = [fetch_tile(year, b) for b in tiles]
    datasets = [mf.open() for mf in memfiles]
    mosaic, transform = merge(datasets)

    meta = datasets[0].meta.copy()
    meta.update(height=mosaic.shape[1], width=mosaic.shape[2], transform=transform)

    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"bavaria_dop20_{capture_date.isoformat()}_raw.tif"
    with rasterio.open(raw_path, "w", **meta) as dst:
        dst.write(mosaic)

    for ds in datasets:
        ds.close()
    for mf in memfiles:
        mf.close()

    # clip to the actual AOI polygon, not just its bounding box
    clipped_path = out_dir / f"bavaria_dop20_{capture_date.isoformat()}.tif"
    with rasterio.open(raw_path) as src:
        image, clip_transform = rasterio.mask.mask(src, aoi.geometry, crop=True)
        clip_meta = src.meta.copy()
    clip_meta.update(height=image.shape[1], width=image.shape[2], transform=clip_transform)
    with rasterio.open(clipped_path, "w", **clip_meta) as dst:
        dst.write(image)
    raw_path.unlink()

    return clipped_path


def snow_proxy_fraction(tif_path: Path) -> float:
    """Rough heuristic only: fraction of pixels that are bright and low-saturation
    (snow-like). Bright rock/scree can also trigger this -- always check visually.
    """
    with rasterio.open(tif_path) as src:
        rgb = src.read([1, 2, 3]).astype(np.float32)
    brightness = rgb.mean(axis=0)
    saturation = rgb.max(axis=0) - rgb.min(axis=0)
    snow_like = (brightness > 190) & (saturation < 30)
    valid = brightness > 0  # exclude nodata/black border from clipping
    if valid.sum() == 0:
        return 0.0
    return snow_like[valid].mean()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    log_path = OUT_DIR / "download_log.txt"
    log_file = log_path.open("a", encoding="utf-8")

    def log(msg: str) -> None:
        print(msg)
        log_file.write(msg + "\n")

    log(f"\n=== run started {date.today().isoformat()} ===")

    aoi = gpd.read_file(AOI_PATH).to_crs(CRS)
    bounds = tuple(aoi.total_bounds)

    log("Checking which years have snow-free coverage over the AOI...")
    plan: list[tuple[int, date]] = []
    for year in available_years():
        dates = capture_dates_in_aoi(year, bounds)
        snow_free = [d for d in dates if d.month in SNOW_FREE_MONTHS]
        skipped = [d for d in dates if d.month not in SNOW_FREE_MONTHS]
        if skipped:
            skipped_str = [d.isoformat() for d in skipped]
            log(f"  {year}: skipping {skipped_str} (outside snow-free months)")
        if snow_free:
            plan.extend((year, d) for d in snow_free[:MAX_DATES_PER_YEAR])

    if not plan:
        log("No snow-free-window imagery found for this AOI. Nothing to download.")
        log_file.close()
        return

    log(f"\n{len(plan)} date(s) to download: {[(y, d.isoformat()) for y, d in plan]}\n")

    for year, capture_date in plan:
        out_path = OUT_DIR / str(year)
        final = out_path / f"bavaria_dop20_{capture_date.isoformat()}.tif"
        if final.exists():
            snow_frac = snow_proxy_fraction(final)
            flag = (
                " <-- POSSIBLE SNOW, CHECK VISUALLY" if snow_frac > SNOW_WARNING_THRESHOLD else ""
            )
            log(f"{year} ({capture_date}): already downloaded (snow-proxy: {snow_frac:.0%}){flag}")
            continue

        path = download_year(year, capture_date, aoi, out_path)
        snow_frac = snow_proxy_fraction(path)
        flag = " <-- POSSIBLE SNOW, CHECK VISUALLY" if snow_frac > SNOW_WARNING_THRESHOLD else ""
        log(f"  saved {path} (snow-proxy: {snow_frac:.0%}){flag}")

    log_file.close()


if __name__ == "__main__":
    main()
