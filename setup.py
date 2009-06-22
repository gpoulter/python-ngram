#!/usr/bin/python

#import ez_setup
#ez_setup.use_setuptools()
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
    description="A dictionary-like data structure to retrieve objects similar to a query object using N-Gram similarity",
    keywords="ngram string similarity",
)
