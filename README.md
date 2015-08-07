Map Builder
===========

Super hacky script to turn PSMA suburb boundaries into regions based on a
CSV file.

Requires [forklift](https://github.com/infoxchange/docker-forklift) to
configure a PostGIS database -- or it can provide one via Docker.

Requires ogr2ogr, Python 3 and the psycopg2 module.

Usage
-----

First import the
[PSMA](http://data.gov.au/dataset/psma-administrative-boundaries) data:

    forklift ./import_data.sh *.shp

Then process some regions into GeoJSON:

    forklift ./build_map.py << EOF
    Inner North,MORELAND CITY LGA,YARRA CITY LGA,THORNBURY SSC,NORTHCOTE SSC
    Inner East,...
    EOF

License
-------

Released under the 2-clause BSD license.
