==========
 Tutorial
==========

Comparing and searching strings
===============================

Compare two strings using :meth:`~ngram.NGram.compare`:

.. doctest::

    >>> import ngram
    >>> ngram.NGram.compare('Ham','Spam',N=1)
    0.4

The :class:`~ngram.NGram` class extends the builtin `set` class with the
ability to search for members by n-gram similarity.

Use :meth:`~ngram.NGram.search` to return similar items in a set,
and :meth:`~ngram.NGram.find` to only return the most similar item:

.. doctest::

    >>> G = ngram.NGram(['joe','joseph','jon','john','sally'])
    >>> G.search('jon')
    [('jon', 1.0), ('john', 0.375), ('joe', 0.25), ('joseph', 0.18181818181818182)]
    >>> G.search('jon', threshold=0.3)
    [('jon', 1.0), ('john', 0.375)]
    >>> G.find('jose')
    'joseph'

Transforming items
==================

By default no transformation is done, so items must be strings. By passing a `key` function,
similar to the `key` parameter of the `sorted` builtin, arbitrary items can be indexed.
For non-string items, generally pass `str` or `unicode` as the key function.

Below, we define a key function to index the lower-case version of a string, and use
the key, pad and ngrams methods to examine the internal representations:

.. doctest::

    >>> def lower(s):
    ...     return s.lower()
    >>> G = ngram.NGram(key=lower)
    >>> G.key('AbC')
    'abc'
    >>> G.pad('abc')
    '$$abc$$'
    >>> list(G.split('abc'))
    ['$$a', '$ab', 'abc', 'bc$', 'c$$']

Searching with a lowercase query returns results, but there is no match if the
query contains capitals:

.. doctest::

    >>> G.add('AbC')
    >>> G.search('abcd')
    [('AbC', 0.375)]
    >>> G.find('abcd')
    'AbC'
    >>> G.search('AbC') == []
    True
    >>> G.find('AbC') == None
    True

We can either lowercase the query, or use the "searchitem" or "finditem"
methods that apply the key function to the query before searching:

.. doctest::

    >>> G.search('AbCD'.lower())
    [('AbC', 0.375)]
    >>> G.find(lower('AbCD'))
    'AbC'
    >>> G.searchitem('AbCD')
    [('AbC', 0.375)]
    >>> G.finditem('AbCD')
    'AbC'

So long as the function can be found in `__main__` or imported, NGram instances can be pickled:

.. doctest::

    >>> import pickle
    >>> pickle.dumps(G)  #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    PicklingError: Can't pickle <function lower at ...>: it's not found as __main__.lower
    >>> import string
    >>> H1 = ngram.NGram(['ab cd'], key=string.capwords)
    >>> text = pickle.dumps(H1)
    >>> H2 = pickle.loads(text)
    >>> list(H1)
    ['ab cd']
    >>> list(H2)
    ['ab cd']

The key function can perform complex transformations:

.. doctest::

    >>> G = ngram.NGram(key=lambda x:(" ".join(x)).lower())
    >>> G.add(("Joe","Bloggs"))
    >>> G.search("jeo blogger")
    [(('Joe', 'Bloggs'), 0.25)]
    >>> G.searchitem(("Jeo", "Blogger"))
    [(('Joe', 'Bloggs'), 0.25)]


Set Operations
==============

The `update`, `discard`, `difference_update`, `intersection_update` and `symmetric_difference` update
methods from the builtin `set` class have been overridden to maintain the integrity of the
NGram index when performing them.  These take any iterable as argument, including another
NGram instance.

.. doctest::

    >>> G = ngram.NGram(['joe','joseph','jon','john','sally'])
    >>> G.update(['jonathan'])
    >>> sorted(list(G))
    ['joe', 'john', 'jon', 'jonathan', 'joseph', 'sally']
    >>> G.discard('sally')
    >>> sorted(list(G))
    ['joe', 'john', 'jon', 'jonathan', 'joseph']
    >>> G.difference_update(ngram.NGram(['joe']))
    >>> sorted(list(G))
    ['john', 'jon', 'jonathan', 'joseph']
    >>> G.intersection_update(['james', 'joseph', 'joe', 'jon'])
    >>> sorted(list(G))
    ['jon', 'joseph']
    >>> G.symmetric_difference_update(ngram.NGram(['jimmy', 'jon']))
    >>> sorted(list(G))
    ['jimmy', 'joseph']


Multi-byte characters
=====================

When used with byte-strings, NGram will split on byte boundaries which is
incorrect if one character uses more than one byte.  This is mainly a problem
in Python 2 where you often handle encoded byte strings.  In Python 3, you will
generally be handed a unicode string.

Rule Of Thumb: Use Unicode strings with NGram unless you are certain that your
encoded strings are plain ASCII.

In Python 2.x, NGram does work fine with ASCII byte-strings:

.. doctest::

    >>> index = ngram.NGram(N=3)
    >>> list(index.ngrams(index.pad("abc")))
    ['$$a', '$ab', 'abc', 'bc$', 'c$$']

But, take é (code point 0xE9) for example.  As a UTF-8 byte-string this
takes up 2-bytes (``'\xc3\xa9'``) and so will be split into 2 characters.

But as a Unicode strings, it is simply ``u'\xe9'`` (``'\xe9'`` in Py3)
and will be handled correctly as a single character.

.. doctest::

    >>> index = ngram.NGram(pad_len=1, N=3)
    >>> import sys
    >>> # Fails in Python 3 (non-ASCII forbidden in literal bytestrings)
    >>> # list(index.split('é')) == ['$\xc3\xa9', '\xc3\xa9$']
    >>> # Fails in Python 3 (the u'' syntax is removed)
    >>> # list(index.split(u'\xe9')) == [u'$\xe9$']
