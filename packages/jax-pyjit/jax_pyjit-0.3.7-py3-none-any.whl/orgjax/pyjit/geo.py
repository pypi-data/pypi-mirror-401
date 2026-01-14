import geopandas as gpd
from geopandas import GeoDataFrame
from pathlib import Path
from shapely.geometry import box
from math import ceil


def normalize(file: Path, patch_size: int) -> GeoDataFrame:
    # Take some geojson and normalize it
    # so that it fits in a specific patch size.
    # This routine may need more work to be useful
    # for reintal layer workflow.

    # Read the (geo) json and modify it as needed.
    frame: GeoDataFrame = gpd.read_file(file)
    frame["geometry"] = frame.geometry.apply(
        normalize_to_patch_size, patch_size=patch_size
    )
    return frame


def normalize_to_patch_size(geom, patch_size: int):
    # Normalize the geometry to the nearest multiple of patch_size
    minx, miny, maxx, maxy = geom.bounds
    cx = (minx + maxx) / 2.0
    cy = (miny + maxy) / 2.0
    width = maxx - minx
    height = maxy - miny
    norm_width = ceil(width / patch_size) * patch_size
    norm_height = ceil(height / patch_size) * patch_size
    return box(
        cx - norm_width / 2.0,
        cy - norm_height / 2.0,
        cx + norm_width / 2.0,
        cy + norm_height / 2.0,
    )
