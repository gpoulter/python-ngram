Welcome to NGram's documentation!
=================================

Contents:

.. toctree::
   :maxdepth: 2

   tutorial
   ngram

Introduction
============

.. include:: ../README

Release Notes
=============

Version 3.2.1
-------------
Released 2012-06-28

    * Fix bug in symmetric_difference_update method
    * Update release notes / changelog
    * Update tutorial


Version 3.2.0
-------------
Released 2012-06-25

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
Released 2009-12-07

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
Released 2009-07-03.

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
Released 2007-10-23.

This was the code committed to Subversion by Exhuma.

License
=======

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

:download:`GPL <../COPYING>`
:download:`LGPL <../COPYING.LESSER>`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
