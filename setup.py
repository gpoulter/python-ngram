#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    try:
        from distribute_setup import use_setuptools
        use_setuptools()
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

extra = {}
import sys
if sys.version_info >= (3,):
    extra['use_2to3'] = True
    extra['convert_2to3_doctests'] = ['doc/tutorial.rst']

setup(
    name = 'ngram',
    version = '3.1',
    py_modules = ['ngram'],
    zip_safe = True,
    author = 'Graham Poulter, Michael Albert',
    license = 'LGPL',
    url = 'http://packages.python.org/ngram',
    download_url = 'http://pypi.python.org/pypi/ngram',
    description = "A set that retrieves members by N-Gram similarity to a query string.",
    keywords = "ngram string similarity",
    test_suite = 'test_ngram',
    **extra
)
