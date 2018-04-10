# OSM name localization for latin languages
#
# python language rewrite usable
# as PL/Python functions and plain python
#
# (c) 2018 Sven Geggus <svn-osm@geggus.net>
#

import re
import unicodedata
from .geo_transcript import geo_transcript
from .street_abbrev import street_abbrev, street_abbrev_all, street_abbrev_all_latin, street_abbrev_all_nonlatin

# 5 most commonly spoken languages using latin script (hopefully)
latin_langs = ["en","es","fr","pt","de"]

# "latin" codeblock are
def isLatin(str):
  for st in str:
    od=ord(st)
    if (od>0x036F):
      if ((od > 0x1FFF) and (od < 0x2070)):
        continue
      return(False)
  return(True)

def unaccent(input_str):
  nfkd_form = unicodedata.normalize('NFKD', input_str)
  only_ascii = nfkd_form.encode('ASCII', 'ignore')
  return(only_ascii.decode('utf-8'))

# Generate a combined name from local_name and on-site name (or do not in some cases)
def gen_combined_name(local_name, name,tags=None):
  if name is None:
    return(local_name)
  nobrackets=False
  
  # We need to do some heuristic and evil hacks here to check if the
  # generation of a combined name is a good idea.
  # 
  # Currently we do the following:
  # If tags is None:
  # If local_name is part of name as a single word, not just as a substring
  # we return name and discard local_name.
  # Otherwise we return a combined name with name and local_name
  #
  # If tags is not None:
  # If local_name is part of name as a single word, not just as a substring
  # we try to extract a second valid name (defined in "name:*" as a single word)
  # from "name". If succeeeded we redefine name and also return a combined name.
  #   
  # This is useful in bilingual areas where name usually contains two langages.
  # E.g.: name="Bolzano - Bozen", target language="de" would be rendered as:
  #
  # Bozen
  # Bolzano
  unacc = unaccent(name)
  unacc_local = unaccent(local_name)
  found = False
  # special case: local_name is part of name
  if unacc_local in unacc:
    # the regexp_replace function below is a quotemeta equivalent
    # http://stackoverflow.com/questions/11442090/implementing-quotemeta-q-e-in-tcl/11442113
    regex = '[\s\(\)\-,;:/\[\]](' + re.escape(unacc_local) + ')[\s\(\)\-,;:/\[\]]'
    if re.search(regex,' '+unacc+' ') is not None:
      if (len(unacc_local) == len(unacc)):
        return(['',name])
      if tags is None:
        nobrackets=True
      else:
        for key in tags.keys():
          if re.match('^name:.+$',key) is not None:
            if ((tags[key]) != local_name):
              regex = '[\s\(\)\-,;:/\[\]](' + re.escape(tags[key]) + ')[\s\(\)\-,;:/\[\]]'
              if re.search(regex,' '+name+' ') is not None:
                # As this regex is also true for 1:1 match we need to ignore this special case
                if (name != (tags[key])):
                  name = tags[key]
                  nobrackets=False
                  found=True
                  break
                else:
                  nobrackets=True
      
        # consider other names than local_name crap in case we did not find any
        if not found:
          return([local_name,''])
    
  if nobrackets:
    return(['',name])
  else:
     return([local_name,name])

# This is the state machine to return the two relevant tags-names for map
# localization as a list. This is basically the core of this code :)
#
# In the nost simple case this would be 'name:<targetlang>' and 'name'.
# If transcription is needed a special tag-name staring with __transcript_
# is returned
def get_relevant_tags(tags,targetlang):

  target_tag = 'name:'+targetlang
  keys = tags.keys()
  if 'name' not in keys:
    tags['name']=''
  if target_tag in keys:
    return([target_tag,'name'])
  # ignore further name tags in case of an empty generic name tag
  if (tags['name']==''):
    return(['',''])
  if isLatin(tags['name']):
    return(['','name'])
  # at this stage name is not latin so we need to have a look at alternatives
  # these are currently int_name, common latin scripts and romanized version of the name
  if 'int_name' in keys:
    if isLatin(tags['int_name']):
      return(['int_name','name'])
  # if any other latin language tag is available use it
  for lang in latin_langs:
    # we already checked for targetlang
    if (lang == targetlang):
      continue
    target_tag = 'name:'+lang;
    if target_tag in keys:
      return([target_tag,'name'])
  
  # try to find a romanized version of the name this usually looks like
  # name:ja_rm or name:kr_rm thus a suitable regex would be name:.+_rm
  # Just use the first tag of this kind found, because having more than one
  # of them does not make sense
  for key in keys:
    if re.match('^name:.+_rm$', key) is not None:
      return([key,'name'])

  # finally as a last resort do transliteration
  return(['__transcript_name','name'])


# First one of the three l10n functions
# this one will return a localized name (if possible) and an on-site name
def get_placename(
tags,
targetlang='de',
geometry=None):

  key=get_relevant_tags(tags,targetlang)
  # possible return values of get_relevant_tags are
  # 1. key[0]='' (implies key[1]=latin)
  # 2. key[1]='' (implies key[0]=targetlang)
  # 3. key[0]='' and key[1]=''
  # 4. key[0] is target tag key[1] is name
  # 5. key[0] is something else key[1] is name
  # 6. key[0] needs transcription,  key[1] is name
  if (key[1] != ''):
    if (key[0] == ''):
      # case 1
      return(['',tags[key[1]]])
    # both keys are non empty
    # case 4
    if (key[0] == 'name:'+targetlang):
      return(gen_combined_name(tags[key[0]],tags[key[1]],tags))
    # case 5
    if (key[0][0:12] != '__transcript'):
      return(gen_combined_name(tags[key[0]],tags[key[1]],tags))
    else:
      # case 6
      transcripted=geo_transcript(tags[key[0][13:]],geometry)
      return(gen_combined_name(transcripted,tags[key[1]]))
    
  # cases 2 and 3
  return(['',''])

# Second one of the three l10n functions
# second one will return a localized abbreviated streetname (if possible)
# and an on-site abbreviated streetname
def get_streetname(
tags,
targetlang='de',
geometry=None):

  key=get_relevant_tags(tags,targetlang)
  # possible return values of get_relevant_tags are
  # 1. key[0]='' (implies key[1]=latin)
  # 2. key[1]='' (implies key[0]=targetlang)
  # 3. key[0]='' and key[1]=''
  # 4. key[0] is target tag key[1] is name
  # 5. key[0] is something else key[1] is name
  # 6. key[0] needs transcription,  key[1] is name
  if (key[1] != ''):
    if (key[0] == ''):
      # case 1
      return(['',street_abbrev_all_latin(tags[key[1]])])
    # both keys are non empty
    # case 4
    if (key[0] == 'name:'+targetlang):
      return(gen_combined_name(street_abbrev(tags[key[0]],targetlang),street_abbrev_all(tags[key[1]]),tags))
    # case 5
    if (key[0][0:12] != '__transcript'):
      return(gen_combined_name(street_abbrev(tags[key[0]],'en'),street_abbrev_all(tags[key[1]]),tags))
    else:
      # case 6
      transcripted=geo_transcript(street_abbrev_all_nonlatin(tags[key[0][13:]]),geometry)
      return(gen_combined_name(transcripted,street_abbrev_all_nonlatin(tags[key[1]])))
    
  # cases 2 and 3
  return(['',''])

# Third one of the three l10n functions
# this one will return only a localized latin name (if possible)
def get_latinname(
tags,
targetlang='de',
geometry=None):

  key=get_relevant_tags(tags,targetlang)
  # possible return values of get_relevant_tags are
  # 1. key[0]='' (implies key[1]=latin)
  # 2. key[1]='' (implies key[0]=targetlang)
  # 3. key[0]='' and key[1]=''
  # 4. key[0] is target tag key[1] is name
  # 5. key[0] is something else key[1] is name
  # 6. key[0] needs transcription,  key[1] is name
  if (key[1] != ''):
    if (key[0] == ''):
      # case 1
      return(tags[key[1]])
    # both keys are non empty
    # case 4
    if (key[0] == 'name:'+targetlang):
      return(tags[key[0]])
    # case 5
    if (key[0][0:12] != '__transcript'):
      return(tags[key[0]])
    else:
      # case 6
      return(geo_transcript(tags[key[0][13:]],geometry))
    
  # cases 2 and 3
  return('')

# This will format the list output from the above functions as a
# string usable for rendering
def format_list4map(list,seperator,reverse=False,show_brackets=False):
  
  if reverse:
    list.reverse()
  if show_brackets:
    list[1]='('+list[1]+')'
  if '' in list:
    namestring=''.join(list)
  else:
    namestring=seperator.join(list)
    # Our string is a left-to right text paragraph
    namestring=u'\u202a'+namestring+u'\u202c'
  return(namestring)
  