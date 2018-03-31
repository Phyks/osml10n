#!/usr/bin/python3
#
# OSM name localization for latin languages
#
# python language rewrite usable
# as PL/Python functions and plain python
#
# (c) 2018 Sven Geggus <svn-osm@geggus.net>
#
# * a generic transcription geo_transcript
# * a geolocation aware transcription function
#
# This uses either a geolocation aware transcription or
# an alphabet specific transcription. Fallback is
# ICU in any case.
#

import unicodedata
from .thai_transcript import thai_transcript
from .icu_translit import icu_translit
from .get_country import get_country
from .kanji_transcript import kanji_transcript

# check if string contains characters in
# requested alphabet
def containsAlphabet(str,alphabet):
  for st in str:
    if (unicodedata.name(st[0]).split(' ')[0] == alphabet):
      return(True)
  return(False)

# likely faster then containsAlphabet(name,'THAI')
def containsTHAI(str):
  for st in str:
    if ((ord(st) >= 0x0E00) and (ord(st) <= 0x0E7F )):
      return(True)
  return(False)

def translit(name):
  # currently supported language dependent transcriptions
  # * thai
  # * ...
  # more will possibly follow :)
  if containsTHAI(name):
    return(thai_transcript(name))
  # add other alphabet transcription functions
  # here as above:
  # if containsAlphabet(name,'NEWALPHABET'):
  # return(newalphabet_transcript(name))
  
  # fallback transliteration method is ICU
  return(icu_translit(name))


def geo_transcript(name, lonlat):
  if lonlat is None:
    return(translit(name))
  
  country=get_country(lonlat);
  if (country=='jp'):
    if containsAlphabet(name,'CJK'):
      return(kanji_transcript(name))
  if (country=='th'):
    if containsTHAI(name):
       return(thai_transcript(name))
       
  return(icu_translit(name))
