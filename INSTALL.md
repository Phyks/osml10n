## Software requirements:

* Postgresql 10.x, PostGIS 2.x and PL/Python for the database Interface
* Python 3.x and a couple of modules for the python module

### required python modules
* pykakasi
* pyicu
* python-Levenshtein
* pythainlp

This code is developed on Debian GNU/Linux stable but should also work on
any other GNU/Linux distribution.

It should also work on other operating systems supported
by python ond PostgreSQL at least in theory.

## Installation of the Python module

Teh following command should be sufficient:

```sh
pip3 install git+https://github.com/giggls/osml10n.git
```

To check if everything worked fine run the test-l10n.py script.

You will also need a module called mod_spatialite.so which is part of the
ibsqlite3-mod-spatialite package on Debian GNU/Linux and Ubuntu
distributions. Otherwise the location aware transcription code will not work
in the python-only version of the code.

## Installation of the Postgresql extension
* clone the code
```sh
git clone https://github.com/giggls/osml10n.git
```
* Fetch country_osm_grid table from nominatim
```sh
curl -s http://www.nominatim.org/data/country_grid.sql.gz |gzip -d >country_osm_grid.sql
```
* run gen_psql_extension.py as root or database user
```sh
gen_psql_extension.py
```
## Activation of Postgresql extension

To activate the extension in your database just call "create extension
osml10n". This will require administrator privileges.
```sql
CREATE EXTENSION osml10n;
```

Afterwards you should be able to do the following:
```sql
yourdb=# select osml10n_version();
 osml10n_version 
-----------------
 3.0
(1 row)
```

