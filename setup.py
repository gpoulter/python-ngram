#!/usr/bin/python

import inspect
import os
import sys
from setuptools import setup

ROOT = os.path.dirname(inspect.getfile(inspect.currentframe()))

classifiers = """
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)
License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Natural Language :: English
Topic :: Text Processing
Topic :: Text Processing :: Indexing
Topic :: Text Processing :: Linguistic
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
"""

params = dict()

with open(os.path.join(ROOT, 'README')) as docs:
    params['long_description'] = docs.read()

params['classifiers'] = [c.strip()
    for c in classifiers.split('\n') if c.strip()]

setup(
    name='ngram',
    description='A `set` subclass providing fuzzy search based on N-grams.',
    version='4.0.0',
    license='LGPLv3+',
    py_modules=['ngram'],
    zip_safe=True,
    author='Graham Poulter, Michael Albert',
    maintainer='Graham Poulter',
    url='http://github.com/gpoulter/python-ngram',
    download_url='http://pypi.python.org/pypi/ngram',
    keywords="ngram set string text similarity",
    scripts=['scripts/csvjoin.py'],
    platforms=['any'],
    **params
)
