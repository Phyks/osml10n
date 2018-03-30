# Any to Latin transliteration code
# basically just a libicu cal
# (c) 2018 Sven Geggus <svn-osm@geggus.net>

def icu_translit(unistr):
  import icu
  import unicodedata

  tr = icu.Transliterator.createInstance('Any-Latin').transliterate
  
  return(unicodedata.normalize('NFC', tr(unistr)))


  