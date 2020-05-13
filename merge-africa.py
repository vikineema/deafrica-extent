#!/usr/bin/env python3

import shapely
import fiona

from shapely.ops import unary_union
from shapely.geometry import shape, mapping

# Don't even bother extracting the data, we can read the shapefile
source_dataset = '/vsizip/data/ne_10m_admin_0_countries_lakes.zip'
dest_dataset = 'africa-extent.json'

# Filter for Africa
def africa_region_un(rec):
    return rec['properties'].get('REGION_UN') == 'Africa'

def filter_further(rec):
# Open the data, filter it and turn it into a list of Shapely features
world = fiona.open(source_dataset)
africa_filtered = filter(filter_further, africa)
africa_shapely = [shape(c['geometry']) for c in africa]

# Union the file (merge all the features together)
africa_unioned = unary_union(africa_shapely)
# Create a convex hull (minimum bounding shape)
africa_convex_hull = africa_unioned.convex_hull
# Buffer it by 2 degrees (means we get an extra scene around the coastlines)
africa_hull_buffer = africa_convex_hull.buffer(1.0)

# Define a schema to write to
schema = {
    'geometry': 'Polygon',
    'properties': {'id': 'int'},
}

# And write the output to geojson
with fiona.open(dest_dataset, 'w', 'GeoJSON', schema) as out:
    out.write({
        'geometry': mapping(africa_hull_buffer),
        'properties': {'id': 1},
    })
