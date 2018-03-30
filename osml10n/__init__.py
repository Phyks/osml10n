# external API
from .osml10n_version import osml10n_version

def version():
  return(osml10n_version)

# internal functions
from .kanji_transcript import kanji_transcript
from .thai_transcript import thai_transcript
from .icu_translit import icu_translit
from .get_localized_name import get_placename,get_streetname,get_latinname,gen_combined_name,get_relevant_tags
from .get_country import get_country
from .geo_transcript import geo_transcript,translit
from .street_abbrev import street_abbrev, street_abbrev_all, street_abbrev_all_latin, street_abbrev_all_nonlatin
from .get_country_name import get_country_name
