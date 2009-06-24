#!/bin/bash

# Install ngram-similarity while creating a debian package for uninstallation

sudo checkinstall\
 --pkgname=python-ngram-similarity\
 --maintainer=http://www.grahampoulter.com\
 --pkglicense=GPL\
 --pkggroup=python\
 --pkgsource=http://pypi.python.org/pypi/ngram-similarity\
 --pkgaltsource=http://www.grahampoulter.com\
 --requires=python\
 --deldoc=yes\
 --backup=no\
 python setup.py install
