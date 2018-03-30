# Kanji to Latin transcription code
# basically just a Pykakasi call
# https://github.com/miurahr/pykakasi
# (c) 2018 Sven Geggus <svn-osm@geggus.net>

def kanji_transcript(kanji):
  import pykakasi
  
  kakasi = pykakasi.kakasi()
  kakasi.setMode("H","a")
  kakasi.setMode("K","a")
  kakasi.setMode("J","a")
  kakasi.setMode("r","Hepburn")
  kakasi.setMode("s", True)
  kakasi.setMode("E", "a")
  kakasi.setMode("a", None)
  kakasi.setMode("C", True)
  converter  = kakasi.getConverter()
  return(converter.do(kanji))


  