#!/usr/bin/python3
# Thai to Latin transcription code hopefully using
# Royal Thai General System of Transcription (RTGS)
# https://github.com/PyThaiNLP/pythainlp
# (c) 2018 Sven Geggus <svn-osm@geggus.net>

import unicodedata

def split_by_alphabet(str):
  strlist=[]
  target=''
  oldalphabet=unicodedata.name(str[0]).split(' ')[0]
  target=str[0]
  for c in str[1:]:
    alphabet=unicodedata.name(c).split(' ')[0]
    if (alphabet==oldalphabet):
      target=target+c
    else:
      strlist.append(target)
      target=c
    oldalphabet=alphabet
  strlist.append(target)
  return(strlist)

def thai_transcript(inpstr):
  from pythainlp.romanization import romanization
  from pythainlp.tokenize import word_tokenize
  
  stlist=split_by_alphabet(inpstr)
  
  latin = ''
  for st in stlist:
    if (unicodedata.name(st[0]).split(' ')[0] == 'THAI'):
      transcript=[]
      for w in word_tokenize(st):
        transcript.append(romanization(w,engine='royin'))
      latin=latin+' '.join(transcript)
    else:
      latin=latin+st
  return(latin)


if __name__ == "__main__":
  print(split_by_alphabet(u"thai ถนนข้าวสาร 100"))
  print(thai_transcript(u"thai ถนนข้าวสาร 100"))
  