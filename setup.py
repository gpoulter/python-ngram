#!/usr/bin/python

#import ez_setup
#ez_setup.use_setuptools()
from setuptools import setup

setup(
    name='ngram',
    version='2.1',
    py_modules=['ngram'],
    zip_safe=True,

    author='Michael Albert, Graham Poulter',
    author_email='skygreen@users.sourceforge.net',
    license='LGPL',

    url='http://www.sourceforge.net/projects/python-ngram',
    description="""A module to calculate the similarity of a pair of strings, and to look up similar strings in a dictionary-like structure. Inspired by Perl's String::Trigram.""",
    keywords="ngram string similarity",
)
