#!/usr/bin/python

import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

setup(
    name='ngram',
    version='3.0',
    py_modules=['ngram'],
    zip_safe=True,

    author='Michael Albert, Graham Poulter',
    author_email='skygreen@users.sourceforge.net',
    license='LGPL',

    url='http://www.sourceforge.net/projects/python-ngram',
    description="A set class that can search its members by N-Gram similarity to a query string",
    keywords="ngram string similarity",
)
