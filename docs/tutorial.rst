==========
 Tutorial
==========

Comparing and searching strings
===============================

The static :meth:`~ngram.NGram.compare` compares two strings.

.. doctest::

   >>> import ngram
   >>> ngram.NGram.compare('Boo','Bar',N=1)
   0.20000000000000001

The :class:`~ngram.NGram` is an ordinary set augmented by the ability
to search for members by n-gram similarity.  Below we use
:meth:`~ngram.NGram.search` returns matching strings ranked by
decreasing similarity.

   >>> G = ngram.NGram(['joe','joseph','jon','john','sally'])
   >>> G.search('jon')
   [('jon', 1.0), ('john', 0.375), ('joe', 0.25), ('joseph', 0.18181818181818182)]
   >>> G.search('jon', threshold=0.3)
   [('jon', 1.0), ('john', 0.375)]

Transforming items
==================

:class:`~ngram.NGram` supports transforming items prior to indexing.

For example, index the lower-case version of a string.

.. doctest::

   >>> G = ngram.NGram(iconv=lambda x:x.lower())
   >>> G.iconv('AbC')
   'abc'
   >>> G.pad(_)
   '$$abc$$'
   >>> list(G.ngrams(_))
   ['$$a', '$ab', 'abc', 'bc$', 'c$$']
   >>> G.add('AbC')
   >>> G.search('abcd')
   [('AbC', 0.375)]
   >>> # not found, query is not lowercase
   >>> G.search('AbCD') 
   []
   >>> # now lower-case both the items and the queries
   >>> lower = lambda x: x.lower()
   >>> G = ngram.NGram(iconv=lower, qconv=lower)
   >>> G.add('AbC')
   >>> G.search('AbCD')
   [('AbC', 0.375)]

We can use the transform to index complex objects by a custom string
representation.

.. doctest::

   >>> G = ngram.NGram(iconv=lambda x:(" ".join(x)).lower())
   >>> G.add(("Joe","Bloggs"))
   >>> G.search("jeo blogger")
   [(('Joe', 'Bloggs'), 0.25)]
   

Multi-byte characters
=====================

In general, use unicode strings with NGram unless you are certain that
your encoded strings will have exactly one byte per character.  When
used with byte-strings, NGram will split on byte boundaries which is
incorrect if one character uses more than one byte.

So, n-gram splitting works fine with ASCII byte strings

.. doctest::

   >>> index = ngram.NGram(N=3)
   >>> list(index.ngrams(index.pad("abc")))
   ['$$a', '$ab', 'abc', 'bc$', 'c$$']

But the unicode character é (code-point \xe9) would be utf-8 encoded
as the byte-string ``'\xc3\xa9'`` (2 bytes), and thus would be split
as a 2-byte string. The unicode string ``u'\xe9'`` will be handled
correctly as a single character.

.. doctest::

   >>> index = ngram.NGram(pad_len=1,N=3)
   >>> list(index.ngrams_pad('é'))
   ['$\xc3\xa9', '\xc3\xa9$']
   >>> list(index.ngrams_pad(u'é'))
   [u'$\xe9$']
