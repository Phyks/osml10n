#!/usr/bin/python3

import sys
import osml10n

def printresult(expected,result):
  sys.stdout.write("Expected >%s<, got >%s<:" % (expected,result))
  if (result != expected):
    sys.stdout.write('\t[\033[1;31mFAILED\033[0;0m]\n')
  else:
    sys.stdout.write('\t[\033[0;32mOK\033[0;0m]\n')

sys.stdout.write("calling osml10n python module test functions:\n\n")

sys.stdout.write("transcription/transliteration functions:\n")

sys.stdout.write("osml10n.kanji_transcript('漢字 100 abc') --> ")
printresult('Kanji  100 abc',osml10n.kanji_transcript('漢字 100 abc'))
sys.stdout.write("osml10n.icu_translit('漢字 100 abc') --> ")
printresult('hàn zì 100 abc',osml10n.icu_translit('漢字 100 abc'))

sys.stdout.write("osml10n.icu_translit('Москва́') --> ")
printresult('Moskvá',osml10n.icu_translit('Москва́'))

sys.stdout.write("osml10n.thai_transcript('เชียงใหม่') --> ")
printresult('chiangaim',osml10n.thai_transcript('เชียงใหม่'))
sys.stdout.write("osml10n.thai_transcript('thai ถนนข้าวสาร 100') --> ")
printresult('thai thnn khaotan 100',osml10n.thai_transcript('thai ถนนข้าวสาร 100'))

sys.stdout.write("osml10n.geo_transcript('東 京',[140,40])")
printresult('Toukyou',osml10n.geo_transcript('東京',[140,40]))
sys.stdout.write("osml10n.geo_transcript('東 京',[100,30])")
printresult('dōng jīng',osml10n.geo_transcript('東京',[100,30]))

sys.stdout.write("\nosml10n.get_country([9,49]) --> ")
printresult('de',osml10n.get_country([9,49]))

sys.stdout.write("osml10n.get_country([101,15]) --> ")
printresult('th',osml10n.get_country([101,15]))

sys.stdout.write("\nl10n functions:\n")
sys.stdout.write("get_placename({'name': 'Москва́', 'name:de': 'Moskau', 'name:en': 'Moscow'},'de')\n")
printresult(['Moskau', 'Москва́'],osml10n.get_placename({'name': 'Москва́', 'name:de': 'Moskau', 'name:en': 'Moscow'},'de'))

sys.stdout.write("get_placename({'name': 'Москва́', 'name:de': 'Moskau', 'name:en': 'Moscow'},'en')\n")
printresult(['Moscow', 'Москва́'],osml10n.get_placename({'name': 'Москва́', 'name:de': 'Moskau', 'name:en': 'Moscow'},'en'))

sys.stdout.write("get_placename({'name': 'Москва́', 'name:de': 'Moskau'},'en')\n")
printresult(['Moskvá', 'Москва́'],osml10n.get_placename({'name': 'Москва́'},'en'))

sys.stdout.write("get_placename({'name': 'القاهرة', 'name:de': 'Kairo', 'int_name': 'Cairo', 'name:en': 'Cairo'})\n")
printresult(['Kairo', 'القاهرة'],osml10n.get_placename({'name': 'القاهرة', 'name:de': 'Kairo', 'int_name': 'Cairo', 'name:en': 'Cairo'}))

sys.stdout.write("osml10n.get_placename({'name': 'Brixen - Bressanone','name:de': 'Brixen','name:it': 'Bressanone'},'de')\n")
printresult(['Brixen', 'Bressanone'],osml10n.get_placename({"name": "Brixen - Bressanone","name:de": "Brixen","name:it": "Bressanone"},'de'))

sys.stdout.write("get_placename({'name': 'Bautzen - Budyšiń', 'name:de': 'Bautzen', 'name:hsb': 'Budyšiń'},'de')\n")
printresult(['Bautzen', 'Budyšiń'],osml10n.get_placename({'name': 'Bautzen - Budyšiń', 'name:de': 'Bautzen', 'name:hsb': 'Budyšiń'},'de'))

sys.stdout.write("get_placename({'name': 'Roma','name:de': 'Rom'})\n")
printresult(['Rom', 'Roma'],osml10n.get_placename({'name': 'Roma','name:de': 'Rom'}))

sys.stdout.write("get_streetname({'name': 'Doktor-No-Straße'})\n")
printresult('Dr.-No-Str.',osml10n.get_streetname({'name': 'Doktor-No-Straße'}))
sys.stdout.write("get_streetname({'name': 'Dr. No Street','name:de': 'Professor-Doktor-No-Straße'})\n")
printresult(['Prof.-Dr.-No-Str.', 'Dr. No St.'],osml10n.get_streetname({'name': 'Dr. No Street','name:de': 'Professor-Doktor-No-Straße'}))
sys.stdout.write("get_latinname({'name': 'Dr. No Street','name:de': 'Doktor-No-Straße'})\n")
printresult('Doktor-No-Straße',osml10n.get_latinname({'name': 'Dr. No Street','name:de': 'Doktor-No-Straße'}))
sys.stdout.write("get_streetname({'name': 'улица Воздвиженка','name:en': 'Vozdvizhenka Street'},'de')\n")
printresult(['Vozdvizhenka St.', 'ул. Воздвиженка'],osml10n.get_streetname({'name': 'улица Воздвиженка','name:en': 'Vozdvizhenka Street'},'de'))
sys.stdout.write("get_streetname({'name': 'улица Воздвиженка'},'de')\n")
printresult(['ul. Vozdviženka', 'ул. Воздвиженка'],osml10n.get_streetname({'name': 'улица Воздвиженка'},'de'))
sys.stdout.write("get_streetname({'name': 'вулиця Молока'},'de')\n")
printresult(['vul. Moloka', 'вул. Молока'],osml10n.get_streetname({'name': 'вулиця Молока'},'de'))
sys.stdout.write("get_placename({'name': '주촌  Juchon', 'name:ko': '주촌','name:ko_rm': 'Juchon'})\n")
printresult(['Juchon', '주촌'],osml10n.get_placename({'name': '주촌  Juchon', 'name:ko': '주촌','name:ko_rm': 'Juchon'}))
sys.stdout.write("get_placename({'name': '주촌', 'name:ko': '주촌','name:ko_rm': 'Juchon'})\n")
printresult(['Juchon', '주촌'],osml10n.get_placename({'name': '주촌', 'name:ko': '주촌','name:ko_rm': 'Juchon'}))

sys.stdout.write("get_country_name({'ISO3166-1:alpha2': 'IN','name:de': 'Indien','name:hi': 'भारत','name:en': 'India'})\n")
printresult(['Indien', 'भारत', 'India'],osml10n.get_country_name({'ISO3166-1:alpha2': 'IN','name:de': 'Indien','name:hi': 'भारत','name:en': 'India'}))

sys.stdout.write("\nformat_list4map function:\n")

sys.stdout.write("format_names(['Indien', 'भारत', 'India'],' -- '\n")
printresult('‪Indien -- भारत -- India‬',osml10n.format_list4map(['Indien', 'भारत', 'India'],' -- '))

sys.stdout.write("format_names(['ул. Воздвиженка','ul. Vozdviženka'],' - ',True,False)\n")
printresult('‪ul. Vozdviženka - ул. Воздвиженка‬',osml10n.format_list4map(['ул. Воздвиженка','ul. Vozdviženka'],' - ',True,False))

sys.stdout.write("format_names(['ул. Воздвиженка','ul. Vozdviženka'],' ',False,False)\n")
printresult('‪ул. Воздвиженка (ul. Vozdviženka)‬',osml10n.format_list4map(['ул. Воздвиженка','ul. Vozdviženka'],' ',False,True))

sys.stdout.write("format_names(['ул. Воздвиженка','ul. Vozdviženka'],' - ',True,True)\n")
printresult('‪ул. Воздвиженка - ul. Vozdviženka‬',osml10n.format_list4map(['ул. Воздвиженка','ul. Vozdviženka'],' - ',False,False))


