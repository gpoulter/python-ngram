Release Notes
=============

Version 4.0.1
-------------
Released 2021-09-10

* Switched documentation host to ReadTheDocs because sphinx_upload stopped working.

Version 4.0.0
-------------
Released 2021-09-10

* Removed Python 2.7 support since 2to3 support is removed from recent setuptools.

Version 3.3.2
-------------
Released 2017-06-20

* Fixed bug in remove and pop attempting to delete an ngram multiple times.
* Add DeprecationWarning for use of iconv param, ngrams method, ngrams_pad method.
* Fixed csvjoin_test to run on Windows.
* Fixed doctests to support dictionary random iteration order.

Version 3.3.0
-------------
Released 2012-06-29

NEW FEATURES
    * Correct support for remaining set methods: `pop`, `clear`, `union`, `intersection`, `difference`, `symmetric_difference`
    * Can provide alternate `items` to the `copy` method

IMPROVEMENTS
    * Update license from LGPL to LGPL version 3
    * Revised readme to work with GitHub, PyPI and generated docs.
    * Tox to run all doctests, pass under 2.7 and 3.2

BUG FIXES
    * Fix unused threshold param in `searchitem` method
    * Fix intersection_update to accept multiple other iterables

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


