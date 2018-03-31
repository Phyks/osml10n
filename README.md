#  Openstreetmap map localisation (OSM l10n) functions
## (used in German mapnik style)

This is a python reimplementation of the localisation functions used in
german mapnik style.  They are well suited for any target language using the
latin alphabet but meight be also usable for others.

This code has originally been developed as PL/pgSQL stored procedures but is
now also available as a python module.

Fortunately the original API is still supported using PL/Python.

However as there is now a native python interface as well it is now possible to
integrate the localisation into the osm data processing e.g. using pyosmium
(https://github.com/osmcode/pyosmium).

The Version Number starts with 3.0, thus Versions 1.x and 2.x will refer to
the PL/pgSQL versions.

A new feature of this code complared to the older versions is the usage of
the PyThaiNLP (https://github.com/PyThaiNLP/pythainlp) library for
transcription of the thai language as ICU (http://site.icu-project.org/) did
not provide the expected results in this case.

### API

Useful functions for map rendering are:

* get_placename
* get_streetname
* get_latinname
* get_country_name

A more low-level function is the get_relevant_tags function which will
return an array of two strings containing a localized and an on-site name.

However, I would not recommend to use it, as there is some heuristic
in the name combination code called from the other functions which will try
to do its best to make a nice non-redundant label for your map.

For backward compatibility the corresponding PostgreSQl functions are:

* osml10n_get_placename_from_tags
* osml10n_get_streetname_from_tags
* osml10n_get_name_without_brackets_from_tags
* osml10n_get_country_name

**Python examples:**

```
get_streetname({'name': 'улица Воздвиженка'},True,False,' - ','de')
-->	ул. Воздвиженка - ul. Vozdviženka

osml10n.get_placename({'name': 'القاهرة', 'name:de': 'Kairo', 'int_name': 'Cairo', 'name:en': 'Cairo'},False,False,'\n','de')
-->	Kairo
	القاهرة

osml10n.get_latinname(get_latinname({'name': 'القاهرة', 'name:de': 'Kairo', 'int_name': 'Cairo', 'name:en': 'Cairo'},'en'))
-->     Cairo

get_country_name({'ISO3166-1:alpha2': 'IN','name:de': 'Indien','name:hi': 'भारत','name:en': 'India'})
-->     Indien
	भारत
	India
```

Have a look at [test-l10n.py](test-l10n.py) for more examples.

**PostgreSQL examples:**

```SQL
select osml10n_get_streetname_from_tags('"name"=>"улица Воздвиженка"',true,false,' - ','de') as name;
-->     ул. Воздвиженка - ul. Vozdviženka

select osml10n_get_placename_from_tags('"name"=>"القاهرة","name:de"=>"Kairo","int_name"=>"Cairo","name:en"=>"Cairo"',false) as name;
-->     Kairo
        القاهرة

select osml10n_get_name_without_brackets_from_tags('"name"=>"القاهرة","name:de"=>"Kairo","int_name"=>"Cairo","name:en"=>"Cairo"','en') as name;
-->     Cairo

select osml10n_get_country_name('"ISO3166-1:alpha2"=>"IN","name:de"=>"Indien","name:hi"=>"भारत","name:en"=>"India"') as name;
-->     Indien
        भारत
        India
```
