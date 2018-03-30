#!/bin/sh
#
# quick and dirty shell-script for converting the postgresql dump
# country_osm_grid.sql to an sqlite database
# unfortunately this will currently need a postgresql database
#
output=osml10n/country_osm_grid.db

if [ -f $output ]; then
  echo "output file \"$output\" already exists!"
  exit 0
fi

if ! [ -f country_osm_grid.sql ]; then
  echo -n "Trying to download country_grid.sql.gz from nominatim.org... "
  curl -s http://www.nominatim.org/data/country_grid.sql.gz |gzip -d >country_osm_grid.sql
fi

if ! [ -f country_osm_grid.sql ]; then
  echo "failed."
  exit 1
else
  echo "done."
fi

echo "Importing to PostgreSQL..."
psql -f country_osm_grid.sql >/dev/null
echo "Exporting into spatialite..."
ogr2ogr -progress -dsco SPATIALITE=YES -f "SQLITE" -gt 65536 $output PG: country_osm_grid
echo "Removing table form PostgreSQL"
echo "drop table country_osm_grid;" |psql  >/dev/null
rm country_osm_grid.sql

