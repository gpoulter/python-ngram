#!/usr/bin/python

import inspect
import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # pylint: disable=W402

ROOT = os.path.dirname(inspect.getfile(inspect.currentframe()))

classifiers = """
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Topic :: Text Processing :: Linguistic
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.2
"""

params = dict()

with open(os.path.join(ROOT, 'README')) as docs:
    params['description'] = docs.readline()
    params['long_description'] = docs.read()

params['classifiers'] = [c.strip()
    for c in classifiers.split('\n') if c.strip()]

if sys.version_info >= (3,):
    params['use_2to3'] = True
    params['convert_2to3_doctests'] = ['doc/tutorial.rst']

setup(
    name='ngram',
    version='3.2.1',
    py_modules=['ngram'],
    zip_safe=True,
    author='Graham Poulter, Michael Albert',
    maintainer='Graham Poulter',
    author_email='http://www.grahampoulter.com',
    license='http://www.gnu.org/copyleft/lesser.html',
    url='http://github.com/gpoulter/python-ngram',
    download_url='http://pypi.python.org/pypi/ngram',
    keywords="ngram string similarity",
    test_suite='test_ngram',
    scripts=['scripts/csvjoin.py'],
    platforms=['any'],
    **params
)
