#!/bin/bash

# Install ngram-similarity while creating a debian package for uninstallation

sudo checkinstall\
 --pkgname=python-ngram-similarity\
 --maintainer=Graham Poulter\
 --pkglicense=LGPL\
 --pkggroup=python\
 --pkgsource=http://pypi.python.org/pypi/ngram\
 --pkgaltsource=http://packages.python.org/ngram\
 --requires=python\
 --deldoc=yes\
 --backup=no\
 python setup.py install
