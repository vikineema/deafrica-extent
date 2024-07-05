#!/usr/bin/env python3
import csv
import gzip

import fiona
from shapely.geometry import shape

# Source data
kenya_extent = "kenya-extent.json"
all_mgrs = "/vsizip/data/sentinel_2_tiles_africa.zip"

out_csv = "dekenya-mgrs-tiles.csv.gz"

# Open the data, filter it and turn it into a list of Shapely features
kenya_fiona = fiona.open(kenya_extent)
mgrs = fiona.open(all_mgrs)

kenya = shape(next(iter(kenya_fiona))["geometry"])


# Filter for Kenya
def kenya_region(rec):
    return shape(rec["geometry"]).intersects(kenya)


mgrs_kenya = filter(kenya_region, mgrs)

with gzip.open(out_csv, "wt") as f:
    csvwriter = csv.writer(f)
    for feature in mgrs_kenya:
        csvwriter.writerow([feature["properties"]["Name"]])


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
