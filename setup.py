#!/usr/bin/python

from setuptools import setup

#from distutils.core import setup

setup(
    name='ngram',
    version='2.1b',
    py_modules=['ngram'],

    author='Michael Albert, Graham Poulter',
    author_email='skygreen@users.sourceforge.net',
    license='LGPL',

    url='http://www.sourceforge.net/projects/python-ngram',
    description="""A module to calculate the similarity of a pair of strings, and to look up similar strings in a dictionary-like structure. Inspired by Perl's String::Trigram.""",
    keywords="ngram string similarity", 
)
