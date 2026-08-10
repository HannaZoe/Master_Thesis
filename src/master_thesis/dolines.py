"""Closed-depression (candidate doline) detection from a DEM."""

from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.features
import rasterio.mask
from scipy import ndimage
from shapely.geometry import shape
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


def extract_depressions(
    depth_path: Path,
    min_depth_m: float = 0.3,
    min_area_m2: float = 4.0,
) -> gpd.GeoDataFrame:
    """Threshold a depth-in-sink raster into candidate doline polygons.

    Keeps connected regions deeper than ``min_depth_m`` and larger than
    ``min_area_m2``. Returns polygons with area, max depth, and circularity —
    cheap enough to call repeatedly while tuning thresholds against a fixed
    depth raster from ``compute_depth_raster``.
    """
    with rasterio.open(depth_path) as src:
        depth = src.read(1, masked=True).filled(0)
        transform = src.transform
        crs = src.crs
        px_area_m2 = abs(transform.a * transform.e)

    empty = gpd.GeoDataFrame(
        columns=["label", "area_m2", "max_depth_m", "perimeter_m", "circularity", "geometry"],
        geometry="geometry",
        crs=crs,
    )

    depression = depth > min_depth_m
    labeled, n_labels = ndimage.label(depression, structure=np.ones((3, 3)))
    if n_labels == 0:
        return empty

    label_ids = np.arange(1, n_labels + 1)
    areas_m2 = ndimage.sum(depression, labeled, label_ids) * px_area_m2
    max_depths = ndimage.maximum(depth, labeled, label_ids)

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
            label_ids.tolist(),
            zip(areas_m2.tolist(), max_depths.tolist(), strict=True),
            strict=True,
        )
    )
    gdf["area_m2"] = gdf["label"].map(lambda lbl: stats[lbl][0])
    gdf["max_depth_m"] = gdf["label"].map(lambda lbl: stats[lbl][1])
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
