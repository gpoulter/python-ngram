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
N-Gram string similarity. It is a full subclass of the built-in `set`
that maintains N-Gram indexing on all set operations. The algorithm is
based from `String::Trigram
<http://search.cpan.org/dist/String-Trigram/>`_ by Tarek Ahmed.

NGram up to version 2.0.0b2 was written by Michel Albert, and since
then has had a major rewrite and been maintained by Graham Poulter:
see `Changes in Version 3`_

Installation
============

Simplest is to install from `PyPI <http://packages.python.org/ngram>`_::

   easy_install ngram

Or download the source tarball from PyPI and install locally::

   python setup.py install --prefix=$HOME/.local

With source you can build documentation in `docs/_build/html`::

   python setup.py build_sphinx

Changes in Version 3
====================

Changes in version 3.1:
 * NEW Support Python 3 via use_2to3 in setup.py
 * NEW Tutorial and docs in Sphinx (http://packages.python.org/ngram)
 * CHANGE Setuptools replaced by Distribute (for Python 3)
 * CHANGE Docstrings in reStructuredText (for Sphinx)
 * CHANGE str_item and str_query are now iconv and qconv
 * FIX Integer division bug (e.g. arises when warp is 2 not 2.0)

Changes in version 3.0:
 * NEW Accepts any hashable item (no longer limited to strings)
 * NEW Re-written as subclass of `set`
 * NEW Docstrings added, using Epydoc API doc generator
 * CHANGE Revised to use Python 2.6 idioms (losing Python 2.2 compatibilit)
 * CHANGE Renamed things to follow PEP 8
 * CHANGE Refactored the NGram class (new method decomposition)
 * FIX Eliminated innermost level of dictionaries, reducing memory usage.

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
