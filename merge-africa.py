#!/usr/bin/env python3

import fiona
from shapely.geometry import mapping, shape
from shapely.ops import unary_union

# Don't even bother extracting the data, we can read the shapefile
source_dataset = "/vsizip/data/ne_10m_admin_0_countries.zip"
source_exclusions = "data/exclusions.json"

dest_dataset = "kenya-extent.json"
dest_bbox = "kenya-extent-bbox.json"


# Filter for Kenya
def filter_by_name(rec):
    return rec["properties"].get("NAME") == "Kenya"


# Open the data, filter it and turn it into a list of Shapely features
world = fiona.open(source_dataset, mode="r", driver="ESRI Shapefile")
kenya = filter(filter_by_name, world)
kenya_shapely = [shape(c["geometry"]) for c in kenya]

# Union the file (merge all the features together)
kenya_unioned = unary_union(kenya_shapely)
# Create a convex hull (minimum bounding shape)
kenya_convex_hull = kenya_unioned.convex_hull
# Buffer it by 2 degrees (means we get an extra scene around the coastlines)
kenya_hull_buffer = kenya_convex_hull.buffer(1.0)

# Exclude some areas
exclusions = fiona.open(source_exclusions)
exclusions_shapely = unary_union([shape(c["geometry"]) for c in exclusions])

kenya_hull_buffer_exclusions = kenya_hull_buffer.difference(exclusions_shapely)

# Define a schema to write to
schema = {
    "geometry": "Polygon",
    "properties": {"bbox": "str"},
}

# And write the output to geojson
with fiona.open(dest_dataset, "w", "GeoJSON", schema) as out:
    out.write(
        {
            "geometry": mapping(kenya_hull_buffer_exclusions),
            "properties": {"bbox": str(kenya_hull_buffer_exclusions.envelope.bounds)},
        }
    )

# Also write the bbox, because why not?!
with fiona.open(dest_bbox, "w", "GeoJSON", schema) as out:
    out.write(
        {
            "geometry": mapping(kenya_hull_buffer_exclusions.envelope),
            "properties": {"bbox": str(kenya_hull_buffer_exclusions.envelope.bounds)},
        }
    )
