"""Closed-depression (candidate doline) detection from a DEM."""

from collections.abc import Callable
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.features
import rasterio.mask
from scipy import ndimage
from shapely.geometry import Point, shape
from skimage.morphology import h_minima
from skimage.segmentation import watershed
from whitebox import WhiteboxTools


def clip_to_aoi(dem_path: Path, aoi_path: Path, output_path: Path) -> None:
    """Clip a DEM to an AOI polygon, cropping to its bounding box."""
    aoi = gpd.read_file(aoi_path)
    with rasterio.open(dem_path) as src:
        if aoi.crs != src.crs:
            aoi = aoi.to_crs(src.crs)
        image, transform = rasterio.mask.mask(src, aoi.geometry, crop=True)
        meta = src.meta.copy()
    meta.update(height=image.shape[1], width=image.shape[2], transform=transform)
    with rasterio.open(output_path, "w", **meta) as dst:
        dst.write(image)


def compute_depth_raster(dem_path: Path, output_path: Path) -> None:
    """Fill every sink in a DEM and write per-pixel fill depth (whitebox DepthInSink).

    This is the slow step (minutes on a full-res DSM) — run once per DEM, then
    call ``extract_depressions`` as many times as needed to try thresholds
    without repeating this.
    """
    wbt = WhiteboxTools()
    wbt.set_verbose_mode(False)
    wbt.set_working_dir(str(dem_path.parent.resolve()))
    wbt.depth_in_sink(str(dem_path.resolve()), str(output_path.resolve()), zero_background=True)


def _extract_regions(
    raster_path: Path,
    condition: Callable[[np.ndarray], np.ndarray],
    stat_fn: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray],
    stat_name: str,
    min_area_m2: float,
) -> gpd.GeoDataFrame:
    """Shared plumbing for extract_depressions/extract_anomalies: threshold a raster,
    keep connected regions above a minimum area, vectorize, attach per-region stats.
    """
    with rasterio.open(raster_path) as src:
        values = src.read(1, masked=True).filled(0)
        transform = src.transform
        crs = src.crs
        px_area_m2 = abs(transform.a * transform.e)

    empty = gpd.GeoDataFrame(
        columns=["label", "area_m2", stat_name, "perimeter_m", "circularity", "geometry"],
        geometry="geometry",
        crs=crs,
    )

    mask = condition(values)
    labeled, n_labels = ndimage.label(mask, structure=np.ones((3, 3)))
    if n_labels == 0:
        return empty

    label_ids = np.arange(1, n_labels + 1)
    areas_m2 = ndimage.sum(mask, labeled, label_ids) * px_area_m2
    stat_vals = stat_fn(values, labeled, label_ids)

    keep = label_ids[areas_m2 >= min_area_m2]
    if len(keep) == 0:
        return empty

    keep_mask = np.isin(labeled, keep)
    filtered_labels = np.where(keep_mask, labeled, 0).astype(np.int32)

    shapes = rasterio.features.shapes(filtered_labels, mask=keep_mask, transform=transform)
    gdf = (
        gpd.GeoDataFrame(
            [{"label": int(value), "geometry": shape(geom)} for geom, value in shapes],
            crs=crs,
        )
        .dissolve(by="label")
        .reset_index()
    )

    stats = dict(
        zip(
            label_ids.tolist(), zip(areas_m2.tolist(), stat_vals.tolist(), strict=True), strict=True
        )
    )
    gdf["area_m2"] = gdf["label"].map(lambda lbl: stats[lbl][0])
    gdf[stat_name] = gdf["label"].map(lambda lbl: stats[lbl][1])
    gdf["perimeter_m"] = gdf.geometry.length
    gdf["circularity"] = 4 * np.pi * gdf["area_m2"] / gdf["perimeter_m"] ** 2

    return gdf


def extract_depressions(
    depth_path: Path,
    min_depth_m: float = 0.3,
    min_area_m2: float = 4.0,
) -> gpd.GeoDataFrame:
    """Threshold a depth-in-sink raster into candidate doline polygons.

    Keeps connected regions deeper than ``min_depth_m`` and larger than
    ``min_area_m2``. Returns polygons with area, max depth, and circularity —
    cheap enough to call repeatedly while tuning thresholds against a fixed
    depth raster from ``compute_depth_raster``. Superseded by
    ``extract_anomalies`` for sloped terrain — see experiment_log.md.
    """
    return _extract_regions(
        depth_path,
        condition=lambda v: v > min_depth_m,
        stat_fn=lambda v, lab, ids: ndimage.maximum(v, lab, ids),
        stat_name="max_depth_m",
        min_area_m2=min_area_m2,
    )


def extract_anomalies(
    dev_path: Path,
    threshold_m: float = -0.22,
    min_area_m2: float = 0.05,
) -> gpd.GeoDataFrame:
    """Threshold a DevFromMeanElev raster into candidate doline polygons.

    Keeps connected regions more negative than ``threshold_m`` (locally lower
    than their neighborhood) and larger than ``min_area_m2``. Default
    threshold and the window size used to build ``dev_path`` should come from
    calibration against real ground truth, not guessed — see
    experiment_log.md for how the -0.22 m / 4 m window default was picked.
    ``min_area_m2`` here is just a speckle filter, not a real size cutoff —
    the anomaly footprint isn't the same thing as the doline's true extent.
    """
    return _extract_regions(
        dev_path,
        condition=lambda v: v < threshold_m,
        stat_fn=lambda v, lab, ids: ndimage.minimum(v, lab, ids),
        stat_name="min_dev_m",
        min_area_m2=min_area_m2,
    )


def extract_basins(
    dev_path: Path,
    h: float = 0.5,
    min_area_m2: float = 1.0,
) -> gpd.GeoDataFrame:
    """Candidate dolines via h-minima-seeded watershed segmentation.

    Best-performing method tested so far (see experiment_log.md), but still
    finds far more candidates than real dolines on this terrain -- bare
    alpine karst rock has roughly an order of magnitude more "prominent"
    local minima than actual dolines. Treat the output as a shortlist for
    manual review in QGIS, not a final answer.

    Seeds come from skimage.morphology.h_minima (regional minima with depth
    >= h relative to their surroundings, not just a static threshold), grown
    to their full extent via watershed, masked to dev < 0 so basins stop at
    a sensible rim instead of eating the whole raster.
    """
    with rasterio.open(dev_path) as src:
        dev = src.read(1, masked=True).filled(0)
        transform = src.transform
        crs = src.crs
        px_area_m2 = abs(transform.a * transform.e)

    empty = gpd.GeoDataFrame(
        columns=["label", "area_m2", "min_dev_m", "perimeter_m", "circularity", "geometry"],
        geometry="geometry",
        crs=crs,
    )

    seed_labels, n_seeds = ndimage.label(h_minima(dev, h), structure=np.ones((3, 3)))
    if n_seeds == 0:
        return empty

    basins = watershed(dev, markers=seed_labels, mask=dev < 0)
    label_ids, counts = np.unique(basins[basins > 0], return_counts=True)
    areas_m2 = counts * px_area_m2

    big_enough = areas_m2 >= min_area_m2
    keep = label_ids[big_enough]
    if len(keep) == 0:
        return empty
    kept_areas = areas_m2[big_enough]
    min_devs = ndimage.minimum(dev, basins, keep)

    keep_mask = np.isin(basins, keep)
    filtered = np.where(keep_mask, basins, 0).astype(np.int32)
    shapes = rasterio.features.shapes(filtered, mask=keep_mask, transform=transform)
    gdf = (
        gpd.GeoDataFrame(
            [{"label": int(value), "geometry": shape(geom)} for geom, value in shapes],
            crs=crs,
        )
        .dissolve(by="label")
        .reset_index()
    )

    stats = dict(
        zip(keep.tolist(), zip(kept_areas.tolist(), min_devs.tolist(), strict=True), strict=True)
    )
    gdf["area_m2"] = gdf["label"].map(lambda lbl: stats[lbl][0])
    gdf["min_dev_m"] = gdf["label"].map(lambda lbl: stats[lbl][1])
    gdf["perimeter_m"] = gdf.geometry.length
    gdf["circularity"] = 4 * np.pi * gdf["area_m2"] / gdf["perimeter_m"] ** 2

    return gdf


def detect_dolines(
    dem_path: Path,
    work_dir: Path,
    min_depth_m: float = 0.3,
    min_area_m2: float = 4.0,
) -> gpd.GeoDataFrame:
    """Convenience wrapper: compute the depth raster and threshold it once.

    Prefer calling ``compute_depth_raster`` + ``extract_depressions``
    directly when trying multiple thresholds on the same DEM.
    """
    work_dir.mkdir(parents=True, exist_ok=True)
    depth_path = work_dir / f"{dem_path.stem}_depth.tif"
    compute_depth_raster(dem_path, depth_path)
    return extract_depressions(depth_path, min_depth_m=min_depth_m, min_area_m2=min_area_m2)


def compute_dev_from_mean_elev(dem_path: Path, output_path: Path, filter_px: int) -> None:
    """Local relief: elevation minus the mean elevation in an NxN window (whitebox
    DevFromMeanElev). Unlike DepthInSink, this cancels out the regional slope trend,
    since it compares each cell to its own neighborhood rather than a global fill.
    ``filter_px`` should be odd; roughly match it to the target feature diameter.
    """
    wbt = WhiteboxTools()
    wbt.set_verbose_mode(False)
    wbt.set_working_dir(str(dem_path.parent.resolve()))
    wbt.dev_from_mean_elev(
        str(dem_path.resolve()), str(output_path.resolve()), filterx=filter_px, filtery=filter_px
    )


def sample_raster(raster_path: Path, points: gpd.GeoDataFrame) -> np.ndarray:
    """Sample a single-band raster's value at each point (reprojecting if needed)."""
    with rasterio.open(raster_path) as src:
        pts = points.to_crs(src.crs) if points.crs != src.crs else points
        coords = [(geom.x, geom.y) for geom in pts.geometry]
        return np.array([val[0] for val in src.sample(coords)])


def random_points_in_polygon(
    polygon,
    n: int,
    crs,
    exclude: gpd.GeoSeries | None = None,
    exclude_buffer_m: float = 2.0,
    seed: int | None = None,
) -> gpd.GeoDataFrame:
    """Random points inside a polygon, for background/control sampling.

    Excludes points within ``exclude_buffer_m`` of any geometry in ``exclude``
    (e.g. known doline locations), so background stats aren't contaminated by
    real features that happen to land in the "background" sample.
    """
    rng = np.random.default_rng(seed)
    exclude_union = exclude.buffer(exclude_buffer_m).union_all() if exclude is not None else None
    minx, miny, maxx, maxy = polygon.bounds

    points: list[Point] = []
    while len(points) < n:
        candidate = Point(rng.uniform(minx, maxx), rng.uniform(miny, maxy))
        if not polygon.contains(candidate):
            continue
        if exclude_union is not None and exclude_union.contains(candidate):
            continue
        points.append(candidate)

    return gpd.GeoDataFrame(geometry=points, crs=crs)
