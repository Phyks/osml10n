#!/usr/bin/python3
import os

# get version number from source
osml10n_version = None
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'osml10n', 'osml10n_version.py')) as f:
    for line in f:
        line = line.strip()
        if line.startswith('osml10n_version'):
            osml10n_version = line.split('=')[1].strip().strip("\"'")
assert osml10n_version is not None

from distutils.core import setup
setup(
    name='osml10n',
    packages=['osml10n'],
    install_requires=[
          'pykakasi','pyicu','python-Levenshtein','pythainlp'
      ],
    version=osml10n_version,
    description='OSM localization for languages with latin alphabet based one name* tags and transliteration',
    author='Sven Geggus',
    author_email='sven-osm@geggus.net',
    url='https://github.com/giggls/osml10n',
    download_url='https://github.com/giggls/osml10n/'
                 'osml10n/tarball/0.0.7',
    keywords=['l10n', 'OSM', 'Openstreetmap'],
    package_data={'': ['country_osm_grid.db']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: LGPL-3.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
