#!/usr/bin/env python3

import shapely
import fiona

import csv
import gzip
from shapely.geometry import shape, mapping

# Source data
africa_extent = 'africa-extent.json'
all_mgrs = '/vsizip/data/sentinel_2_tiles_africa.zip'

out_csv = 'deafrica-mgrs-tiles.csv.gz'

# Open the data, filter it and turn it into a list of Shapely features
africa_fiona = fiona.open(africa_extent)
mgrs = fiona.open(all_mgrs)

africa = shape(next(iter(africa_fiona))['geometry'])

# Filter for Africa
def africa_region(rec):
    return shape(rec['geometry']).intersects(africa)

mgrs_africa = filter(africa_region, mgrs)

with gzip.open(out_csv, "wt") as f:
    csvwriter = csv.writer(f)
    for feature in mgrs_africa:
        csvwriter.writerow([feature['properties']['Name']])


# # Define a schema to write to
# schema = {
#     'geometry': 'Polygon',
#     'properties': {'id': 'int'},
# }

# # And write the output to geojson
# with fiona.open(dest_dataset, 'w', 'GeoJSON', schema) as out:
#     out.write({
#         'geometry': mapping(africa_hull_buffer_exclusions),
#         'properties': {'id': 1},
#     })

# # Also write the bbox, because why not?!
# with fiona.open(dest_bbox, 'w', 'GeoJSON', schema) as out:
#     out.write({
#         'geometry': mapping(africa_hull_buffer_exclusions.envelope),
#         'properties': {'id': 1},
#     })
