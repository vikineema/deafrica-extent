# Digital Earth Africa Extent Polygon

A process of identifying a boundary polygon for working with satellite data over Africa

To run this process you need Python 3 with Shapely and Fiona installed and either wget or 
to manually download the [Natural Earth admin 0 countries dataset](https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip).

To run the process with Make, do the following:

- `make get-natural-earth`  (downloads the source data)
- `make extract-africa-hull` (extracts Africa and creates a buffered convex hull).

And to extract the CSV of MGRS tiles, do:

- `make extract-mgrs-codes`.

Notes:

- Africa is defined as features that have "REGIONS_UN = Africa" in the NE dataset
- The African areas are unioned, then a convex hull is created
- This resulting convex hull is buffered by 1 degree.

The derived dataset [africa-extent.json](africa-extent.json) is derived from Natural Earth, which is in the public domain, see: [https://www.naturalearthdata.com/about/](https://www.naturalearthdata.com/about/).
