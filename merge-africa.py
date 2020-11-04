#!/usr/bin/env python3

import shapely
import fiona

from shapely.ops import unary_union
from shapely.geometry import shape, mapping

# Don't even bother extracting the data, we can read the shapefile
source_dataset = '/vsizip/data/ne_10m_admin_0_countries.zip'
source_exclusions = 'data/exclusions.json'

dest_dataset = 'africa-extent.json'
dest_bbox = 'africa-extent-bbox.json'

# Filter for Africa
def africa_region_un(rec):
    return rec['properties'].get('REGION_UN') == 'Africa'

def filter_further(rec):
    # Filtering out Saint Helena based on Adam Lewis' email 13 May 2020
    return rec['properties'].get('NAME') != 'Saint Helena'

# Open the data, filter it and turn it into a list of Shapely features
world = fiona.open(source_dataset)
africa = filter(africa_region_un, world)
africa_filtered = filter(filter_further, africa)
africa_shapely = [shape(c['geometry']) for c in africa_filtered]

# Union the file (merge all the features together)
africa_unioned = unary_union(africa_shapely)
# Create a convex hull (minimum bounding shape)
africa_convex_hull = africa_unioned.convex_hull
# Buffer it by 2 degrees (means we get an extra scene around the coastlines)
africa_hull_buffer = africa_convex_hull.buffer(1.0)

# Exclude some areas
exclusions = fiona.open(source_exclusions)
exclusions_shapely = unary_union([shape(c['geometry']) for c in exclusions])

africa_hull_buffer_exclusions = africa_hull_buffer.difference(exclusions_shapely)

# Define a schema to write to
schema = {
    'geometry': 'Polygon',
    'properties': {'id': 'int'},
}

# And write the output to geojson
with fiona.open(dest_dataset, 'w', 'GeoJSON', schema) as out:
    out.write({
        'geometry': mapping(africa_hull_buffer_exclusions),
        'properties': {'id': 1},
    })

# Also write the bbox, because why not?!
with fiona.open(dest_bbox, 'w', 'GeoJSON', schema) as out:
    out.write({
        'geometry': mapping(africa_hull_buffer_exclusions.envelope),
        'properties': {'id': 1},
    })
