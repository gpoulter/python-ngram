.. NGram documentation master file, created by
   sphinx-quickstart on Fri Dec  4 14:04:06 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NGram's documentation!
=================================

Contents:

.. toctree::
   :maxdepth: 2

   tutorial
   ngram

Introduction
============

The NGram class extends the Python set class with the ability
to search for set members ranked by their N-Gram string similarity
to the query. There are also methods for comparing a pair of strings.

NGram is hosted at the `Python Package Index
<http://pypi.python.org/pypi/ngram>`_, and this is the online
documentation.

How does it work?
=================

The set stores arbitrary items by using a specified "key" function
to produce a string representation of set members suitable for N-gram indexing.
By default it simply calls str() on the objects.

The N-grams are obtained by splitting strings into overlapping substrings
of N (usually N=3) characters in length and association is maintained from
each distinct N-Gram to items that use it.

To find items similar to a query string, it splits the query into N-grams,
collects all items sharing at least one N-gram with the query,
and ranks the items by score based on the ratio of shared to unshared
N-grams between strings.

Installation
============

Install from `PyPI <http://pypi.python.org/pypi/ngram>`_
using `pip installer <http://www.pip-installer.org/en/latest/index.html>`_::

   pip install ngram

It should run on Python 2.6, Python 2.7 and Python 3.2

Release Notes
=============
Version 3.2.1
-------------
    * Fix bug in symmetric_difference_update method
    * Update release notes / changelog
    * Update tutorial


Version 3.2.0
-------------

NEW FEATURES
    * "csvjoin" script performs SQL-like join between CSV tables based on string similarity.
    * NGram instances can now be pickled/unpickled (added __reduce__)
    * Add searchitem method to search by item (search method takes a string)
    * Add find and finditem methods to return 1 result instead of a list.

BREAKING CHANGES
    * iconv parameter is now the "key" parameter (matches the sorted() builtin)
    * qconv parameter no longer exists: use searchitem method to query by item
    * the `ngrams_pad` method is deprecated for new `split` and `splititem` methods
    * the `ngrams` method is deprecated (equivalent `_split` is for internal use)

OTHER IMPROVEMENTS
    * Converted Mercurial repo to Git
    * Corrected indentation from 3 to 4 spaces
    * Added tox to run tests on Python 2.7 and 3.2

Version 3.1.0
-------------

NEW FEATURES
    * Python 3 support via 2to3
    * Sphinx documentation generation
    * Tutorial documentation

BREAKING CHANGES
    * str_item and str_query params are now iconv and qconv

BUG FIXES
    * Integer division bug (e.g. arises when warp is 2 not 2.0)

MINOR CHANGES
    * Setuptools replaced by Distribute (for Python 3)
    * Docstrings now reStructuredText for Sphinx

Version 3.0.0
-------------
This was a major refactoring without back-compatibility.

NEW FEATURES
    * Accepts any hashable item - no longer limited to strings.
    * Re-written as subclass of set, gaining all set operations.
    * Docstrings added. Using Epydoc API doc generator.

IMPROVEMENTS
    * Eliminated innermost level of dictionaries, reducing memory usage.
    * Revised to use Python 2.6 idioms. Losing Python 2.2 compatibility.
    * Renamed things to follow PEP 8
    * Refactored the NGram class (new method decomposition)


Version 2.0.0b2
---------------
This was the code committed to Subversion by Exhuma.

History
=======

In 2007, Michel Albert (exhuma) wrote the python-ngram module based on the Perl
String::Trigram module by Tarek Ahmed, and committed the code for 2.0.0b2 to
Sourceforge subversion repo.

Since late 2008 python-ngram development has been continued Graham Poulter,
adding features, documentation, performance improvements and Python 3 support.
The repo was first moved to a Mercurial repo on Google Code, but primary
development now takes place here on GitHub.

License
=======

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
USA.

:download:`License Text <../LICENSE>`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
