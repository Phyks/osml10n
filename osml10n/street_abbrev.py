# OSM name localization for latin languages
#
# python language rewrite usable
# as PL/Python functions and plain python
#
# (c) 2018 Sven Geggus <svn-osm@geggus.net>
#
# Streetname abbreviation functions
#
# currently supported languages:
# en, de, ru, uk
#
# english abbreviations are taken from
# http://www.ponderweasel.com/whats-the-difference-between-an-ave-rd-st-ln-dr-way-pl-blvd-etc/
#
# Please send patches for others!

abbreviations ={
'latin': {
         'de': {
              'Straße': 'Str.', 'straße': 'str.', 'Strasse': 'Str.', 'strasse': 'str.',
              'Gasse': 'G.', 'gasse': 'g.', 'Platz': 'Pl.', 'platz': 'pl.',
              'Professor': 'Prof.', 'Professor-':'Prof.-','Doktor ': 'Dr.', 'Doktor-': 'Dr.-',
              'Bürgermeister ': 'Bgm. ', 'Bürgermeister-': 'Bgm.-', 'Sankt ': 'St. ', 'Sankt-': 'St.-'
               },
         'en': {
               'Boulevard': 'Blvd.', 'Drive': 'Dr.', 'Avenue': 'Ave.', 'Street': 'St.', 'Road': 'Rd.',
               'Lane': 'Ln.', 'Place': 'Pl.', 'Square': 'Sq.', 'Crescent': 'Cres.'
               },
         },
'nonlatin': {
            'ru': {
                  'переулок': 'пер.', 'тупик': 'туп.', 'улица': 'ул.', 'бульвар': 'бул.', 'площадь': 'пл.',
                  'проспект': 'просп.', 'спуск': 'сп.', 'набережная': 'наб.'
                  },
            'uk': {
                  'провулок': 'пров.', 'тупик': 'туп.', 'вулиця': 'вул.', 'бульвар': 'бул.',
                  'площа': 'пл.', 'проспект': 'просп.', 'спуск': 'сп.', 'набережна': 'наб.'
                  }
           }
}

def street_abbrev(name,lang):
  if lang in abbreviations['latin'].keys():
    type = 'latin'
  else:
    type = 'nonlatin'
  # in case of undefined language return unaltered string
  if lang not in abbreviations[type].keys():
    return(name)
  for key in abbreviations[type][lang].keys():
    name=name.replace(key,abbreviations[type][lang][key])
  return(name)
    
def street_abbrev_all(name):
  for type in abbreviations.keys():
    for lang in abbreviations[type].keys():
      name=street_abbrev(name,lang)
  return(name)

def street_abbrev_all_latin(name):
  for lang in abbreviations['latin'].keys():
    name=street_abbrev(name,lang)
  return(name)

def street_abbrev_all_nonlatin(name):
  for lang in abbreviations['nonlatin'].keys():
    name=street_abbrev(name,lang)
  return(name)

