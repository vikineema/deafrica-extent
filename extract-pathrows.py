import csv
import gzip

import fiona
from shapely.geometry import shape

# Source data
kenya_extent = "kenya-extent.json"
# Changed url see https://cran.rediris.es/web/packages/ecochange/NEWS
all_pathrows = "/vsizip/vsicurl/https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/WRS2_descending_0.zip"

out_csv = "dekenya-usgs-pathrows.csv.gz"

# Open the data, filter it and turn it into a list of Shapely features
kenya_fiona = fiona.open(kenya_extent)
pathrows = fiona.open(all_pathrows)

kenya = shape(next(iter(kenya_fiona))["geometry"])


# Filter for Kenya
def kenya_region(rec):
    return shape(rec["geometry"]).intersects(kenya)


pathrows_kenya = filter(kenya_region, pathrows)

with gzip.open(out_csv, "wt") as f:
    csvwriter = csv.writer(f)
    for feature in pathrows_kenya:
        csvwriter.writerow([feature["properties"]["PR"]])

# # Define a schema to write to
# schema = pathrows.schema

# # And writmgrs_africae the output to geojson
# with fiona.open('test.geojson', 'w', 'GeoJSON', schema) as out:
#     for f in pathrows_africa:
#         out.write(f)
