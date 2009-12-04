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

The NGram class is a set that supports searching for its members by
N-Gram string similarity.

It is a full subclass of the built-in `set` that maintains N-Gram
indexing on all set operations.

The algorithm is based from `String::Trigram
<http://search.cpan.org/dist/String-Trigram/>`_ by Tarek Ahmed.

NGram up to version 2.0.0b2 was written by Michel Alberst. Version 3
is a major re-write and refactoring by Graham Poulter.  See `Changes
in Version 3`_

Installation
============

From the source code::

   python setup.py install --prefix=$HOME/.local

From `ngram on PyPI <http://packages.python.org/ngram>`_::

   easy_install ngram

Build documentation in `docs/_build/html`::

   python setup.py build_sphinx

Python compatibility
====================

The :mod:`ngram` module is compatible with Python 2.6 and above, and a Python
3.x version will be available as a 2to3 conversion.

NGram has no dependencies and should run on any platform supported by
Python 2.6

Changes in Version 3
====================

Fixes and additions in version 3:
 * Eliminated inner level of dictionaries to reduce memory usage.
 * Accepts any hashable, not just strings (function parameter for converting to string)

Breaking changes in version 3:
 * Re-written as subclass of built-in set object
 * Python 2.6 updates
 * PEP 8 method naming
 * Epydoc documenation in 3.0 (Sphinx documentation in 3.1)
 * New functional decomposition (refactored methods)

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

