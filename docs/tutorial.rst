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

By default, non-string items are indexed using their str() representation, but this
can be overridden with a `key` function - just like the `key` parameter to the `sorted`
builtin.

Here we define a key function to index the lower-case version of a string.  Use
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
    >>> H1 = ngram.NGram(['AbC'], key=string.lower)
    >>> text = pickle.dumps(H1)
    >>> H2 = pickle.loads(text)
    >>> list(H1)
    ['AbC']
    >>> list(H2)
    ['AbC']

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
    >>> list(G)
    ['john', 'joseph', 'joe', 'jonathan', 'sally', 'jon']
    >>> G.discard('sally')
    >>> list(G)
    ['john', 'joseph', 'joe', 'jonathan', 'jon']
    >>> G.difference_update(ngram.NGram(['joe']))
    >>> list(G)
    ['john', 'joseph', 'jonathan', 'jon']
    >>> G.intersection_update(['james', 'joseph', 'joe', 'jon'])
    >>> list(G)
    ['joseph', 'jon']
    >>> G.symmetric_difference_update(ngram.NGram(['jimmy', 'jon']))
    >>> list(G)
    ['jimmy', 'joseph']


Multi-byte characters
=====================

Rule Of Thumb: Use Unicode strings with NGram unless you are
certain that your encoded strings will have exactly one byte per character.

When used with byte-strings, NGram will split on byte boundaries which is
incorrect if one character uses more than one byte.

NGram works works fine with ASCII byte strings

.. doctest::

    >>> index = ngram.NGram(N=3)
    >>> list(index.ngrams(index.pad("abc")))
    ['$$a', '$ab', 'abc', 'bc$', 'c$$']

But the unicode character é (code-point \xe9) would be utf-8 encoded
as the byte-string ``'\xc3\xa9'`` (2 bytes), and thus would be split
as a 2-byte string. The unicode string ``u'\xe9'`` will be handled
correctly as a single character.

.. doctest::

    >>> index = ngram.NGram(pad_len=1, N=3)
    >>> list(index.split('é'))
    ['$\xc3\xa9', '\xc3\xa9$']
    >>> list(index.split(u'\xe9'))
    [u'$\xe9$']
