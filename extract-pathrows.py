
import shapely
import fiona

import csv
import gzip
from shapely.geometry import shape, mapping

# Source data
africa_extent = 'africa-extent.json'
all_pathrows = '/vsizip/vsicurl/https://prd-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/WRS2_descending_0.zip'

out_csv = 'deafrica-usgs-pathrows.csv.gz'

# Open the data, filter it and turn it into a list of Shapely features
africa_fiona = fiona.open(africa_extent)
pathrows = fiona.open(all_pathrows)

africa = shape(next(iter(africa_fiona))['geometry'])

# Filter for Africa
def africa_region(rec):
    return shape(rec['geometry']).intersects(africa)

pathrows_africa = filter(africa_region, pathrows)

with gzip.open(out_csv, "wt") as f:
    csvwriter = csv.writer(f)
    for feature in pathrows_africa:
        csvwriter.writerow([feature['properties']['PR']])

# # Define a schema to write to
# schema = pathrows.schema

# # And write the output to geojson
# with fiona.open('test.geojson', 'w', 'GeoJSON', schema) as out:
#     for f in pathrows_africa:
#         out.write(f)
