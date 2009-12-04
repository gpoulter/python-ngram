#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    try:
        import ez_setup
        ez_setup.use_setuptools()
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

setup(
    name = 'ngram',
    version = '3.1',
    py_modules = ['ngram'],
    zip_safe = True,
    author = 'Michael Albert, Graham Poulter',
    license = 'LGPL',
    url = 'http://www.sourceforge.net/projects/python-ngram',
    description = "A set that retrieves members by N-Gram similarity to a query string.",
    keywords = "ngram string similarity",
)

