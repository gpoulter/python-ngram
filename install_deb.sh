#!/bin/bash

# Install ngram-similarity while creating a debian package for uninstallation

sudo checkinstall\
 --pkgname=python-ngram-similarity\
 --maintainer=Graham Poulter\
 --pkglicense=LGPL\
 --pkggroup=python\
 --pkgsource=http://pypi.python.org/pypi/ngram\
 --pkgaltsource=http://python-ngram.sourceforge.net\
 --requires=python\
 --deldoc=yes\
 --backup=no\
 python setup.py install
