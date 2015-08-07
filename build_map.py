#!/usr/bin/env python3

"""
Build maps

We are doing this without the json module so we can stream the output.
"""

import os
import csv
import json
import sys
import psycopg2


conn = psycopg2.connect(os.environ['DB_DEFAULT_URL'].replace('postgis',
                                                             'postgres'))

print("""
{
    "type": "FeatureCollection",
    "features": [
""")

reader = csv.reader(sys.stdin)


with conn.cursor() as cursor:
    comma = ''  # will be set on the second pass

    for name, *regions in reader:
        # split regions by whether or not they're LGAS
        suburbs = []
        lgas = []

        for region in regions:
            if region.endswith(' LGA'):
                lgas.append(region[:-4])
            elif region.endswith(' SSC'):
                suburbs.append(region[:-4])

        suburbs = tuple(suburbs)
        lgas = tuple(lgas)

        print(comma)

        cursor.execute('SELECT ST_AsGeoJSON('
                       'ST_SimplifyPreserveTopology(ST_Union(wkb_geometry), '
                       '                            %(tolerance)s)), '
                       'array_agg(loc_name), '
                       'array_agg(DISTINCT lga_name) '
                       'FROM suburbs '
                       'WHERE lga_name IN %(lgas)s OR '
                       '      loc_name IN %(suburbs)s',
                       dict(
                           lgas=lgas or (None,),
                           suburbs=suburbs or (None,),
                           tolerance=0.0001,
                       ))
        geometry, suburbs, lgas = cursor.fetchone()

        print("""
        {
              "type": "Feature",
              "properties": {
                "name": "%s",
                "suburbs": %s,
                "lgas": %s
              },
              "geometry": %s
        }
        """ % (name,
               json.dumps(suburbs),
               json.dumps(lgas),
               geometry or 'null'))

        comma = ','

print("""
    ]
}
""")
