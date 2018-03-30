#!/usr/bin/python3
#
# (c) 2018 Sven Geggus <svn-osm@geggus.net>
#
# Get country name by avoiding using the generic name tag altogether
#
# This will take advantage of the fact that countries are usually tagged in a
# very extensive manner.
#
# We are thus going to generate a combined string of our target language and
# additional names in the official language(s) of the respective countries.
#
# Official languages are taken from the following website:
# http://wiki.openstreetmap.org/wiki/Nominatim/Country_Codes

# There are 249 countries, thus it will be fast enough as a python dictionary
# and we do not need a database table

from .country_languages import country_languages
import Levenshtein

def get_country_name(
tags,
separator='\n',
targetlang='de'):
  ldistmin=1
  if 'ISO3166-1:alpha2' not in tags:
    return('')
  iso=tags['ISO3166-1:alpha2'].lower()
  names=[]
  # First add our target language to the list of names
  tag='name:'+targetlang
  if tag in tags:
    names.append(tags[tag])
  for lang in country_languages[iso]:
    tag = 'name:'+lang
    if tag in tags:
      if names != []:
        # make shure that ldistall is always bigger than ldistmin by default
        ldistall=ldistmin+1
        for str in names:
          ldist=Levenshtein.distance(str,tags[tag]);
        if (ldistall > ldist):
          ldistall=ldist
        if (ldistall > ldistmin):
          names.append(tags[tag])
  return(separator.join(names))

if __name__ == "__main__":
  print(get_country_name({"ISO3166-1:alpha2": "IN", "name:de": "Indien", "name:hi": "भारत", "name:en": "India"}))
  print()
  print(get_country_name({"ISO3166-1:alpha2": "CA", "name:de": "Kanada", "name:en": "Canada", "name:fr": "Canada"}))
