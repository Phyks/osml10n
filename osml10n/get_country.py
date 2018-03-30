#!/usr/bin/python3
# OSM name localization for latin languages
#
# python language rewrite usable
# as PL/Python functions and plain python
#
# (c) 2018 Sven Geggus <svn-osm@geggus.net>
#
# osml10n_get_country function
#
# determine which country the centroid of a geometry object is located

import os

SQLITE_FILE='country_osm_grid.db'

def get_country(lonlat):
  # lonlat can either be a list with 2 elements
  # or a WKB point
  return(get_country_via_sqlite(lonlat))

def get_country_via_sqlite(lonlat):
  if type(lonlat) is not list:
    return None
  
  # check if sqlite file is available
  fn = os.path.join(os.path.dirname(os.path.realpath(__file__)),SQLITE_FILE)
  if not os.path.isfile(fn):
    return None
  import sqlite3
  conn=sqlite3.connect(fn)
  conn.enable_load_extension(True)
  conn.load_extension("mod_spatialite")
  c = conn.cursor()
  q = "SELECT country_code from country_osm_grid \
  where st_contains(geometry, ST_GeomFromText('POINT(%d %d)', 4326))"  % (lonlat[0],lonlat[1])
  c.execute(q)
  res=c.fetchone()
  conn.close()
  return(res[0])

if __name__ == "__main__":
  print("get_country([9,49]) -> got >%s< expected >de<" % get_country([9,49]))
  print("get_country([101,15]) -> got >%s< expected >th<" % get_country([101,15]))
  

