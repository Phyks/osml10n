#!/usr/bin/python3
#
# This script will generate a Postgresql extension called osml10n
# It aims to be compatible with the old osml10n functions
# written in PL/pgSQL

import sys
import os
import glob
import osml10n
from subprocess import check_output

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def die(msg):
  sys.stderr.write(msg)
  sys.exit(1)

if not os.path.isfile("country_osm_grid.sql"):
  sys.stderr.write('ERROR: file "country_osm_grid.sql" not found\n')
  die('Download via "curl -s http://www.nominatim.org/data/country_grid.sql.gz |gzip -d >country_osm_grid.sql"?\n')
  
argc=len(sys.argv)

if (argc >2):
  die('usage: %s ?extdir?\n' % sys.argv[0])

if (argc == 1):
  # try to find psql extension dir
  try:
    extd=check_output(["pg_config", "--sharedir"]).decode('utf-8').strip()+'/extension'
  except:
    sys.stderr.write('unable to find PostgreSQL extension directory\n')
    die('please try with commandline argument e.g. /usr/share/postgresql/10/extension\n')
else:
  extd=sys.argv[1]

if not os.access(extd, os.W_OK):
  die('can not write to directory: "%s"\n' % extd)

# delete old files
try:
  for f in glob.glob("osml10n--*.sql"):
    os.remove(f)
  os.remove("osml10n.control")
except:
  pass
  
# psql extension file osml10n--<version>.sql
osml10n_version=osml10n.version()
extfile=extd+'/'+"osml10n--%s.sql" % osml10n_version
fd=open(extfile,"w+")

clname=extd+'/'+"osml10n_country_osm_grid.data"
cld=open(clname,"w+")

txt='''-- complain if script is sourced in psql, rather than via CREATE EXTENSION
\echo Use "CREATE EXTENSION osml10n" to load this file. \quit'
'''
fd.write(txt)

gln=open("plpgsql/get_localized_name.sql").read()
fd.write(gln)

# write table data to osml10n_country_osm_grid.data file
with open("country_osm_grid.sql") as cog:
  data=False
  for line in cog:
    if line.startswith('\\.'):
      data=False
    if data:
      cld.write(line)
    if line.startswith("COPY country_osm_grid"):
      data=True
cld.close()

txt='''
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE country_osm_grid (
    country_code character varying(2),
    area double precision,
    geometry geometry
);

COPY country_osm_grid (country_code, area, geometry) FROM '%s';

CREATE INDEX idx_country_osm_grid_geometry ON country_osm_grid USING gist (geometry);
GRANT SELECT on country_osm_grid to public;
''' % clname
fd.write(txt)
fd.close()

fd=open(extd+'/'+"osml10n.control","w+")
with open("osml10n.control.in") as ctlin:
  for line in ctlin:
    line=line.replace('VERSION', osml10n_version)
    fd.write(line)
fd.close()
