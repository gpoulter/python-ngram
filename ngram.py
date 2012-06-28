"""
:mod:`ngram` -- Provides a set that supports lookup by string similarity
========================================================================

.. moduleauthor:: Graham Poulter (version 3.0+)
.. moduleauthor:: Michel Albert (version 2.0.0b2)
"""

from __future__ import division

__license__ = """
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

See LICENSE file or http://www.gnu.org/licenses/lgpl-2.1.html
"""

class NGram(set):
    """A set that supports lookup by NGram string similarity.

    Accepts `unicode` string or an encoded `str` of bytes. With encoded `str` the
    splitting is on byte boundaries, which will be incorrect if the encoding uses
    multiple bytes per character.  You must provide NGram with unicode strings if
    the encoding would have multi-byte characters.

    :type threshold: float in 0.0 ... 1.0

    :param threshold: minimum similarity for a string to be considered a match.

    :type warp: float in 1.0 ... 3.0

    :param warp: use warp greater than 1.0 to increase the similarity of shorter string pairs.

    :type items: [item, ...]

    :param items: iteration of items to index for N-gram search.

    :type N: int >= 2

    :param N: number of characters per n-gram.

    :type pad_len: int in 0 ... N-1

    :param pad_len: how many characters padding to add (defaults to N-1).

    :type pad_char: str or unicode

    :param pad_char: character to use for padding.  Default is '$', but consider using the\
    non-breaking space character, ``u'\\xa0'`` (``u"\\u00A0"``).

    :type key: function(item) -> str/unicode

    :param key: Function to convert items into string, default is no conversion.

    Instance variables:

    :ivar _grams: For each n-gram, the items containing it and the number of times\
    the n-gram occurs in the item as ``{str:{item:int, ...}, ...}``.

    :ivar length: maps items to length of the padded string representations as
    ``{item:int, ...}``.
    """

    def __init__(self, items=[], threshold=0.0, warp=1.0, key=None,
                    N=3, pad_len=None, pad_char='$', **kwargs):
        super(NGram, self).__init__()
        if not (0 <= threshold <= 1):
            raise ValueError("threshold out of range 0.0 to 1.0: "
                             + repr(threshold))
        if not (1.0 <= warp <= 3.0):
            raise ValueError(
                "warp out of range 1.0 to 3.0: " + repr(warp))
        if not N >= 1:
            raise ValueError("N out of range (should be N >= 1): " + repr(N))
        if pad_len is None:
            pad_len = N-1
        if not (0 <= pad_len < N):
            raise ValueError("pad_len out of range: " + repr(pad_len))
        if not len(pad_char)==1:
            raise ValueError(
                "pad_char is not single character: " + repr(pad_char))
        if key is not None and not callable(key):
            raise ValueError("key is not a function: " + repr(key))
        self.threshold = threshold
        self.warp = warp
        self.N = N
        self._pad_len = pad_len
        self._pad_char = pad_char
        self._padding = pad_char * pad_len # derive a padding string
        # compatibility shim for 3.1 iconv parameter
        if 'iconv' in kwargs:
            self._key = kwargs.pop('iconv')
        # no longer support 3.1 qconv parameter
        if 'qconv' in kwargs:
            raise ValueError('qconv query conversion parameter unsupported. '
            'Please process query to a string before calling .search')
        self._key = key
        self._grams = {}
        self.length = {}
        self.update(items)

    def __reduce__(self):
        """Return state information for pickling, no references to this instance.
        The key function must be None, a builtin function, or a named
        module-level function.

        >>> n = NGram([0xDEADBEEF, 0xBEEF], key=hex)
        >>> import pickle
        >>> p = pickle.dumps(n)
        >>> m = pickle.loads(p)
        >>> list(m)
        [3735928559, 48879]
        """
        return NGram, (list(self), self.threshold, self.warp, self._key,
                       self.N, self._pad_len, self._pad_char)

    def copy(self):
        """Return a shallow copy of the NGram object.  That is, instantiate
        a new NGram from references to items stored in this one.

        >>> from copy import deepcopy
        >>> n = NGram(['eggs', 'spam'])
        >>> m = n.copy()
        >>> m.add('ham')
        >>> list(n)
        ['eggs', 'spam']
        >>> list(m)
        ['eggs', 'ham', 'spam']
        """
        return NGram(self, self.threshold, self.warp, self._key,
                     self.N, self._pad_len, self._pad_char)

    def key(self, item):
        """Get the key string for the item.

        >>> n = NGram(key=lambda x:x[1])
        >>> n.key((3,"ham"))
        'ham'
        """
        return self._key(item) if self._key else item

    def pad(self, string):
        """Pad a string in preparation for splitting into ngrams.

        >>> n = NGram()
        >>> n.pad('ham')
        '$$ham$$'
        """
        return self._padding + string + self._padding

    def _split(self, string):
        """Iterates over the ngrams of a string (no padding).

        >>> n = NGram()
        >>> list(n._split("hamegg"))
        ['ham', 'ame', 'meg', 'egg']
        """
        for i in range(len(string) - self.N + 1):
            yield string[i:i+self.N]

    # compatibility with 3.1
    ngrams = _split

    def split(self, string):
        """Pads a string and iterates over its ngrams.

        >>> n = NGram()
        >>> list(n.split("ham"))
        ['$$h', '$ha', 'ham', 'am$', 'm$$']
        """
        return self._split(self.pad(string))

    # compatibility with 3.1
    ngrams_pad = split

    def splititem(self, item):
        """Pads the string key of an item and iterates over its ngrams.

        >>> n = NGram(key=lambda x:x[1])
        >>> item = (3,"ham")
        >>> list(n.splititem(item))
        ['$$h', '$ha', 'ham', 'am$', 'm$$']
        """
        return self.split(self.key(item))

    def add(self, item):
        """Add an item to the N-gram index (only if it has not already been added).

        >>> n = NGram()
        >>> n.add("ham")
        >>> list(n)
        ['ham']
        >>> n.add("spam")
        >>> list(n)
        ['ham', 'spam']
        """
        if item not in self:
            # Add the item to the base set
            super(NGram, self).add(item)
            # Record length of padded string
            padded_item = self.pad(self.key(item))
            self.length[item] = len(padded_item)
            for ngram in self._split(padded_item):
                # Add a new n-gram and string to index if necessary
                self._grams.setdefault(ngram, {}).setdefault(item, 0)
                # Increment number of times the n-gram appears in the string
                self._grams[ngram][item] += 1

    def remove(self, item):
        """Remove an item from the index. Inverts the add operation.

        >>> n = NGram(['spam', 'eggs'])
        >>> n.remove('spam')
        >>> list(n)
        ['eggs']
        """
        if item in self:
            super(NGram, self).remove(item)
            del self.length[item]
            for ngram in self.splititem(item):
                del self._grams[ngram][item]

    def items_sharing_ngrams(self, query):
        """Retrieve the subset of items that share n-grams the query string.

        :param query: look up items that share N-grams with this string.
        :return: dictionary from matched string to the number of shared N-grams.

        >>> n = NGram(["ham","spam","eggs"])
        >>> n.items_sharing_ngrams("mam")
        {'ham': 2, 'spam': 2}
        """
        # From matched string to number of N-grams shared with query string
        shared = {}
        # Dictionary mapping n-gram to string to number of occurrences of that
        # ngram in the string that remain to be matched.
        remaining = {}
        for ngram in self.split(query):
            try:
                for match, count in self._grams[ngram].items():
                    remaining.setdefault(ngram, {}).setdefault(match, count)
                    # match up to as many occurrences of ngram as exist in the matched string
                    if remaining[ngram][match] > 0:
                        remaining[ngram][match] -= 1
                        shared.setdefault(match, 0)
                        shared[match] += 1
            except KeyError:
                pass
        return shared

    def searchitem(self, item, threshold=None):
        """Search the index for items whose key exceeds the threshold
        similarity to the key of the given item.

        :return: list of pairs of (item, similarity) by decreasing similarity.

        >>> from ngram import NGram
        >>> n = NGram([(0, "SPAM"), (1, "SPAN"), (2, "EG")], key=lambda x:x[1])
        >>> n.searchitem((2, "SPA"))
        [((0, 'SPAM'), 0.375), ((1, 'SPAN'), 0.375)]
        """
        return self.search(self.key(item))

    def search(self, query, threshold=None):
        """Search the index for items whose key exceeds threshold
        similarity to the query string.

        :param query: returned items will have at least `threshold` similarity to
        the query string.

        :return: list of pairs of (item, similarity) by decreasing similarity.

        >>> from ngram import NGram
        >>> n = NGram([(0, "SPAM"), (1, "SPAN"), (2, "EG")], key=lambda x:x[1])
        >>> n.search("SPA")
        [((0, 'SPAM'), 0.375), ((1, 'SPAN'), 0.375)]
        >>> n.search("M")
        [((0, 'SPAM'), 0.125)]
        >>> n.search("EG")
        [((2, 'EG'), 1.0)]
        """
        threshold = threshold if threshold is not None else self.threshold
        results = []
        # Identify possible results
        for match, samegrams in self.items_sharing_ngrams(query).items():
            allgrams = (len(self.pad(query))
                        + self.length[match] - (2 * self.N) - samegrams + 2)
            similarity = self.ngram_similarity(samegrams, allgrams, self.warp)
            if similarity >= threshold:
                results.append((match, similarity))
        # Sort results by decreasing similarity
        results.sort(key=lambda x:x[1], reverse=True)
        return results

    def finditem(self, item, threshold=None):
        """Return most similar item to the provided one, or None if
        nothing exceeds the threshold.

        >>> from ngram import NGram
        >>> n = NGram([(0, "Spam"), (1, "Ham"), (2, "Eggsy")], key=lambda x:x[1].lower())
        >>> n.finditem((3, 'Hom'))
        (1, 'Ham')
        >>> n.finditem((4, "Oggsy"))
        (2, 'Eggsy')
        """
        results = self.searchitem(item, threshold)
        if results:
            return results[0][0]
        else:
            return None

    def find(self, query, threshold=None):
        """Simply return the best match to the query, None on no match.

        >>> from ngram import NGram
        >>> n = NGram(["Spam","Eggs","Ham"], key=lambda x:x.lower(), N=1)
        >>> n.find('Hom')
        'Ham'
        >>> n.find("Spom")
        'Spam'
        """
        results = self.search(query, threshold)
        if results:
            return results[0][0]
        else:
            return None

    @staticmethod
    def ngram_similarity(samegrams, allgrams, warp=1.0):
        """Similarity for two sets of n-grams.

        :note: ``similarity = (a**e - d**e)/a**e`` where `a` is "all n-grams",
        `d` is "different n-grams" and `e` is the warp.

        :param samegrams: number of n-grams shared by the two strings.

        :param allgrams: total of the distinct n-grams across the two strings.
        :return: similarity in the range 0.0 to 1.0.

        >>> from ngram import NGram
        >>> NGram.ngram_similarity(5, 10)
        0.5
        >>> NGram.ngram_similarity(5, 10, warp=2)
        0.75
        >>> NGram.ngram_similarity(5, 10, warp=3)
        0.875
        >>> NGram.ngram_similarity(2, 4, warp=2)
        0.75
        >>> NGram.ngram_similarity(3, 4)
        0.75
        """
        if abs(warp-1.0) < 1e-9:
            similarity = float(samegrams) / allgrams
        else:
            diffgrams = float(allgrams - samegrams)
            similarity = (allgrams**warp - diffgrams**warp) / (allgrams**warp)
        return similarity

    @staticmethod
    def compare(s1, s2, **kwargs):
        """Compares two strings and returns their similarity.

        :param s1: first string
        :param s2: second string
        :param kwargs: additional keyword arguments passed to __init__.
        :return: similarity between 0.0 and 1.0.

        >>> from ngram import NGram
        >>> NGram.compare('spa', 'spam')
        0.375
        >>> NGram.compare('ham', 'bam')
        0.25
        >>> NGram.compare('spam', 'pam') #N=2
        0.375
        >>> NGram.compare('ham', 'ams', N=1)
        0.5
        """
        if s1 is None or s2 is None:
            if s1 == s2:
                return 1.0
            return 0.0
        try:
            return NGram([s1], **kwargs).search(s2)[0][1]
        except IndexError:
            return 0.0

    ### Set operations implemented on top of NGram add/remove

    def update(self, items):
        """Update the set with new items.

        >>> n = NGram(["spam"])
        >>> n.update(["eggs"])
        >>> list(n)
        ['eggs', 'spam']
        """
        for item in items:
            self.add(item)

    def discard(self, item):
        """If `item` is a member of the set, remove it.

        >>> n = NGram(['spam', 'eggs'])
        >>> n.discard('spam')
        >>> n.discard('ham')
        >>> list(n)
        ['eggs']
        """
        if item in self:
            self.remove(item)

    def difference_update(self, other):
        """Remove from this set all elements from `other` set.

        >>> n = NGram(['spam', 'eggs'])
        >>> other = set(['spam'])
        >>> n.difference_update(other)
        >>> list(n)
        ['eggs']
        """
        for x in other:
            self.discard(x)

    def intersection_update(self, other):
        """Update the set with the intersection of itself and `other`.

        >>> n = NGram(['spam', 'eggs'])
        >>> other = set(['spam', 'ham'])
        >>> n.intersection_update(other)
        >>> list(n)
        ['spam']
        """
        self.difference_update([x for x in self if x not in other])

    def symmetric_difference_update(self, other):
        """Update the set with the symmetric difference of itself and `other`.

        >>> n = NGram(['spam', 'eggs'])
        >>> other = set(['spam', 'ham'])
        >>> n.symmetric_difference_update(other)
        >>> list(n)
        ['eggs', 'ham']
        """
        intersection = self.intersection(other) # record intersection of sets
        self.update(other) # add items present in other
        self.difference_update(intersection) # remove items present in both
