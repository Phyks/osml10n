/*
renderer independent name localization
used in german mapnik style available at

https://github.com/giggls/openstreetmap-carto-de

(c) 2018 Sven Geggus <svn-osm@geggus.net>

PostgreSQL Interface for python implementation
Interface is compatible to old
PL/pgSQL implementation

*/


CREATE or REPLACE FUNCTION osml10n_get_placename_from_tags(tags hstore, 
                                                           loc_in_brackets boolean,
                                                           show_brackets boolean DEFAULT false,
                                                           separator text DEFAULT chr(10),
                                                           targetlang text DEFAULT 'de',
                                                           place geometry DEFAULT NULL,
                                                           name text DEFAULT NULL) RETURNS TEXT AS $$
  import plpy
  try:
    import osml10n
  except:
    plpy.error('python module "osml10n" not found')
  if name is not None:
    tags['name'] = name
  return(osml10n.get_placename(tags,loc_in_brackets,show_brackets,separator,targetlang,place))
$$ LANGUAGE plpython3u TRANSFORM FOR TYPE hstore;

CREATE or REPLACE FUNCTION osml10n_get_streetname_from_tags(tags hstore,
                                                            loc_in_brackets boolean,
                                                            show_brackets boolean DEFAULT false,
                                                            separator text DEFAULT ' - ',
                                                            targetlang text DEFAULT 'de',
                                                            place geometry DEFAULT NULL,
                                                            name text DEFAULT NULL) RETURNS TEXT AS $$
  import plpy
  try:
    import osml10n
  except:
    plpy.error('python module "osml10n" not found')
  if name is not None:
    tags['name'] = name
  return(osml10n.get_streetname(tags,loc_in_brackets,show_brackets,separator,targetlang,place))
$$ LANGUAGE plpython3u TRANSFORM FOR TYPE hstore;

CREATE or REPLACE FUNCTION osml10n_get_name_without_brackets_from_tags(tags hstore,
                                                                       targetlang text DEFAULT 'de',
                                                                       place geometry DEFAULT NULL,
                                                                       name text DEFAULT NULL) RETURNS TEXT AS $$
  import plpy
  try:
    import osml10n
  except:
    plpy.error('python module "osml10n" not found')
  if name is not None:
    tags['name'] = name
  return(osml10n.get_latinname(tags,targetlang,place))
$$ LANGUAGE plpython3u TRANSFORM FOR TYPE hstore;

CREATE or REPLACE FUNCTION osml10n_geo_transcript(name text, place geometry DEFAULT NULL) RETURNS TEXT AS $$
  import plpy
  try:
    import osml10n
  except:
    plpy.error('python module "osml10n" not found')
  return(osml10n.geo_transcript(name,place))
$$ LANGUAGE plpython3u;

CREATE or REPLACE FUNCTION osml10n_get_country_name(tags hstore, separator text DEFAULT chr(10), targetlang text DEFAULT 'de') RETURNS TEXT AS $$
  import plpy
  try:
    import osml10n
  except:
    plpy.error('python module "osml10n" not found')
  return(osml10n.get_country_name(tags,separator,targetlang))
$$ LANGUAGE plpython3u TRANSFORM FOR TYPE hstore;

CREATE or REPLACE FUNCTION osml10n_version() RETURNS TEXT AS $$
  import plpy
  try:
    import osml10n
  except:
    plpy.error('python module "osml10n" not found')
  return(osml10n.version())
$$ LANGUAGE plpython3u;
