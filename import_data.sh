#!/bin/bash -e
#
# Run under Forklift
#

DB_DEFAULT_URL="${DB_DEFAULT_URL//postgis/postgres}"

echo "$DB_DEFAULT_URL"

psql "$DB_DEFAULT_URL" << EOF
DROP TABLE IF EXISTS suburbs;
EOF

for file in "$@"; do
    echo "Importing $file"
    ogr2ogr -append \
        -f "PostgreSQL" PG:"$DB_DEFAULT_URL" \
        "$file" \
        -nln "suburbs" \
        -nlt MULTIPOLYGON \

done
