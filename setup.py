#!/usr/bin/python
"""Set that retrieves members by N-Gram similarity to a query string.

The NGram class is a set that supports searching for its members by
N-Gram string similarity. It is a full subclass of the built-in `set`
that maintains N-Gram indexing on all set operations. The algorithm is
based from `String::Trigram
<http://search.cpan.org/dist/String-Trigram/>`_ by Tarek Ahmed.

Here is the `documentation home page
<http://packages.python.org/ngram/>`_ and the `tutorial
<http://packages.python.org/ngram/tutorial.html>`_.
"""

import sys
try:
    from setuptools import setup
except ImportError:
    try:
        from distribute_setup import use_setuptools
        use_setuptools()
        from setuptools import setup
    except ImportError:
        from distutils.core import setup


classifiers = """
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Topic :: Text Processing :: Linguistic
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 3
Programming Language :: Python :: 3.1
"""

params = dict(
    description = __doc__.split("\n")[0],
    long_description = "\n".join(__doc__.split("\n")[2:]),
    classifiers = [c.strip() for c in classifiers.split('\n') if c.strip()],
)

if sys.version_info >= (3,):
    params.update(
        use_2to3 = True,
        convert_2to3_doctests = ['doc/tutorial.rst'],
    )

setup(
    name = 'ngram',
    version = '3.2',
    py_modules = ['ngram'],
    zip_safe = True,
    author = 'Graham Poulter, Michael Albert',
    maintainer = 'Graham Poulter',
    author_email = 'http://www.grahampoulter.com',
    license = 'http://www.gnu.org/copyleft/lesser.html',
    url = 'http://packages.python.org/ngram',
    download_url = 'http://pypi.python.org/pypi/ngram',
    keywords = "ngram string similarity",
    test_suite = 'test_ngram',
    scripts = ['scripts/csvjoin.py'],
    platforms = ['any'],
    **params
)
