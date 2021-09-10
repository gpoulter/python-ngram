"""
:mod:`ngram` -- A set class that supports lookup by N-gram string similarity
============================================================================
"""

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import warnings

class NGram(set):
    """A set that supports searching for members by N-gram string similarity.

    In Python 2, items should be `unicode` string or a plain ASCII `str`
    (bytestring) - do not use UTF-8 or other multi-byte encodings, because
    multi-byte characters will be split up.

    :type threshold: float in 0.0 ... 1.0

    :param threshold: minimum similarity for a string to be considered a match.

    :type warp: float in 1.0 ... 3.0

    :param warp: use warp greater than 1.0 to increase the similarity of \
    shorter string pairs.

    :type items: [item, ...]

    :param items: iteration of items to index for N-gram search.

    :type N: int >= 2

    :param N: number of characters per n-gram.

    :type pad_len: int in 0 ... N-1

    :param pad_len: how many characters padding to add (defaults to N-1).

    :type pad_char: str or unicode

    :param pad_char: character to use for padding.  Default is '$', but \
    consider using the\\ non-breaking space character, ``u'\\xa0'`` \
    (``u"\\u00A0"``).

    :type key: function(item) -> str/unicode

    :param key: Function to convert items into string, default is no \
    conversion.  Recommended to use `str` or `unicode` for non-string items. \
    Using anonymous function prevents NGram class from being pickled.

    Instance variables:

    :ivar _grams: For each n-gram, the items containing it and the number of \
    times\\ the n-gram occurs in the item as ``{str:{item:int, ...}, ...}``.

    :ivar length: maps items to length of the padded string representations \
    as ``{item:int, ...}``.
    """

    def __init__(self, items=None, threshold=0.0, warp=1.0, key=None,
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
            pad_len = N - 1
        if not (0 <= pad_len < N):
            raise ValueError("pad_len out of range: " + repr(pad_len))
        if not len(pad_char) == 1:
            raise ValueError(
                "pad_char is not single character: " + repr(pad_char))
        if key is not None and not callable(key):
            raise ValueError("key is not a function: " + repr(key))
        self.threshold = threshold
        self.warp = warp
        self.N = N
        self._pad_len = pad_len
        self._pad_char = pad_char
        self._padding = pad_char * pad_len  # derive a padding string
        # compatibility shim for 3.1 iconv parameter
        if 'iconv' in kwargs:
            self._key = kwargs.pop('iconv')
            warnings.warn('"iconv" parameter deprecated, use "key" instead.', DeprecationWarning)
        # no longer support 3.1 qconv parameter
        if 'qconv' in kwargs:
            raise ValueError('qconv query conversion parameter unsupported. '
            'Please process query to a string before calling .search')
        self._key = key
        self._grams = {}
        self.length = {}
        if items:
            self.update(items)

    def __reduce__(self):
        """Return state information for pickling, no references to this
        instance.  The key function must be None, a builtin function, or
        a named module-level function.

        >>> from ngram import NGram
        >>> n = NGram([0xDEAD, 0xBEEF], key=hex)
        >>> import pickle
        >>> p = pickle.dumps(n)
        >>> m = pickle.loads(p)
        >>> sorted(list(m))
        [48879, 57005]
        """
        return NGram, (list(self), self.threshold, self.warp, self._key,
                       self.N, self._pad_len, self._pad_char)

    def copy(self, items=None):
        """Return a new NGram object with the same settings, and
        referencing the same items.  Copy is shallow in that
        each item is not recursively copied.   Optionally specify
        alternate items to populate the copy.

        >>> from ngram import NGram
        >>> from copy import deepcopy
        >>> n = NGram(['eggs', 'spam'])
        >>> m = n.copy()
        >>> m.add('ham')
        >>> sorted(list(n))
        ['eggs', 'spam']
        >>> sorted(list(m))
        ['eggs', 'ham', 'spam']
        >>> p = n.copy(['foo', 'bar'])
        >>> sorted(list(p))
        ['bar', 'foo']
        """
        return NGram(items if items is not None else self,
                     self.threshold, self.warp, self._key,
                     self.N, self._pad_len, self._pad_char)

    def key(self, item):
        """Get the key string for the item.

        >>> from ngram import NGram
        >>> n = NGram(key=lambda x:x[1])
        >>> n.key((3,"ham"))
        'ham'
        """
        return self._key(item) if self._key else item

    def pad(self, string):
        """Pad a string in preparation for splitting into ngrams.

        >>> from ngram import NGram
        >>> n = NGram()
        >>> n.pad('ham')
        '$$ham$$'
        """
        return self._padding + string + self._padding

    def _split(self, string):
        """Iterates over the ngrams of a string (no padding).

        >>> from ngram import NGram
        >>> n = NGram()
        >>> list(n._split("hamegg"))
        ['ham', 'ame', 'meg', 'egg']
        """
        for i in range(len(string) - self.N + 1):
            yield string[i:i + self.N]

    def split(self, string):
        """Pads a string and iterates over its ngrams.

        >>> from ngram import NGram
        >>> n = NGram()
        >>> list(n.split("ham"))
        ['$$h', '$ha', 'ham', 'am$', 'm$$']
        """
        return self._split(self.pad(string))

    def ngrams(self, string):
        """Alias for 3.1 compatibility, please set pad_len=0 and use split.""" 
        warnings.warn('Method ngram deprecated, use method split with pad_len=0 instead.', DeprecationWarning)
        return self._split(string)

    def ngrams_pad(self, string):
        """Alias for 3.1 compatibility, please use split instead."""
        warnings.warn('Method ngrams_pad deprecated, use method split instead.', DeprecationWarning)
        return self.split(string)

    def splititem(self, item):
        """Pads the string key of an item and iterates over its ngrams.

        >>> from ngram import NGram
        >>> n = NGram(key=lambda x:x[1])
        >>> item = (3,"ham")
        >>> list(n.splititem(item))
        ['$$h', '$ha', 'ham', 'am$', 'm$$']
        """
        return self.split(self.key(item))

    def add(self, item):
        """Add an item to the N-gram index (if it has not already been added).

        >>> from ngram import NGram
        >>> n = NGram()
        >>> n.add("ham")
        >>> list(n)
        ['ham']
        >>> n.add("spam")
        >>> sorted(list(n))
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
        """Remove an item from the set. Inverts the add operation.

        >>> from ngram import NGram
        >>> n = NGram(['spam', 'eggs'])
        >>> n.remove('spam')
        >>> list(n)
        ['eggs']
        """
        if item in self:
            super(NGram, self).remove(item)
            del self.length[item]
            for ngram in set(self.splititem(item)):
                del self._grams[ngram][item]

    def pop(self):
        """Remove and return an arbitrary set element.
        Raises KeyError if the set is empty.

        >>> from ngram import NGram
        >>> n = NGram(['spam', 'eggs'])
        >>> x = n.pop()
        >>> len(n)
        1
        """
        item = super(NGram, self).pop()
        del self.length[item]
        for ngram in set(self.splititem(item)):
            del self._grams[ngram][item]
        return item

    def items_sharing_ngrams(self, query):
        """Retrieve the subset of items that share n-grams the query string.

        :param query: look up items that share N-grams with this string.
        :return: mapping from matched string to the number of shared N-grams.

        >>> from ngram import NGram
        >>> n = NGram(["ham","spam","eggs"])
        >>> sorted(n.items_sharing_ngrams("mam").items())
        [('ham', 2), ('spam', 2)]
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
                    # match as many occurrences as exist in matched string
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
        >>> n = NGram([(0, "SPAM"), (1, "SPAN"), (2, "EG"),
        ... (3, "SPANN")], key=lambda x:x[1])
        >>> sorted(n.searchitem((2, "SPA"), 0.35))
        [((0, 'SPAM'), 0.375), ((1, 'SPAN'), 0.375)]
        """
        return self.search(self.key(item), threshold)

    def search(self, query, threshold=None):
        """Search the index for items whose key exceeds threshold
        similarity to the query string.

        :param query: returned items will have at least `threshold` \
        similarity to the query string.

        :return: list of pairs of (item, similarity) by decreasing similarity.

        >>> from ngram import NGram
        >>> n = NGram([(0, "SPAM"), (1, "SPAN"), (2, "EG")], key=lambda x:x[1])
        >>> sorted(n.search("SPA"))
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
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def finditem(self, item, threshold=None):
        """Return most similar item to the provided one, or None if
        nothing exceeds the threshold.

        >>> from ngram import NGram
        >>> n = NGram([(0, "Spam"), (1, "Ham"), (2, "Eggsy"), (3, "Egggsy")],
        ...     key=lambda x:x[1].lower())
        >>> n.finditem((3, 'Hom'))
        (1, 'Ham')
        >>> n.finditem((4, "Oggsy"))
        (2, 'Eggsy')
        >>> n.finditem((4, "Oggsy"), 0.8)
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
        >>> n.find("Spom", 0.8)
        """
        results = self.search(query, threshold)
        if results:
            return results[0][0]
        else:
            return None

    @staticmethod
    def ngram_similarity(samegrams, allgrams, warp=1.0):
        """Similarity for two sets of n-grams.

        :note: ``similarity = (a**e - d**e)/a**e`` where `a` is \
        "all n-grams", `d` is "different n-grams" and `e` is the warp.

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
        if abs(warp - 1.0) < 1e-9:
            similarity = float(samegrams) / allgrams
        else:
            diffgrams = float(allgrams - samegrams)
            similarity = ((allgrams ** warp - diffgrams ** warp)
                    / (allgrams ** warp))
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

        >>> from ngram import NGram
        >>> n = NGram(["spam"])
        >>> n.update(["eggs"])
        >>> sorted(list(n))
        ['eggs', 'spam']
        """
        for item in items:
            self.add(item)

    def discard(self, item):
        """Remove an element from a set if it is a member.

        If the element is not a member, do nothing.

        >>> from ngram import NGram
        >>> n = NGram(['spam', 'eggs'])
        >>> n.discard('spam')
        >>> n.discard('ham')
        >>> list(n)
        ['eggs']
        """
        if item in self:
            self.remove(item)

    def clear(self):
        """Remove all elements from this set.

        >>> from ngram import NGram
        >>> n = NGram(['spam', 'eggs'])
        >>> sorted(list(n))
        ['eggs', 'spam']
        >>> n.clear()
        >>> list(n)
        []
        """
        super(NGram, self).clear()
        self._grams = {}
        self.length = {}

    def union(self, *others):
        """Return the union of two or more sets as a new set.

        >>> from ngram import NGram
        >>> a = NGram(['spam', 'eggs'])
        >>> b = NGram(['spam', 'ham'])
        >>> sorted(list(a.union(b)))
        ['eggs', 'ham', 'spam']
        """
        return self.copy(super(NGram, self).union(*others))

    def difference(self, *others):
        """Return the difference of two or more sets as a new set.

        >>> from ngram import NGram
        >>> a = NGram(['spam', 'eggs'])
        >>> b = NGram(['spam', 'ham'])
        >>> list(a.difference(b))
        ['eggs']
        """
        return self.copy(super(NGram, self).difference(*others))

    def difference_update(self, other):
        """Remove from this set all elements from `other` set.

        >>> from ngram import NGram
        >>> n = NGram(['spam', 'eggs'])
        >>> other = set(['spam'])
        >>> n.difference_update(other)
        >>> list(n)
        ['eggs']
        """
        for item in other:
            self.discard(item)

    def intersection(self, *others):
        """Return the intersection of two or more sets as a new set.

        >>> from ngram import NGram
        >>> a = NGram(['spam', 'eggs'])
        >>> b = NGram(['spam', 'ham'])
        >>> list(a.intersection(b))
        ['spam']
        """
        return self.copy(super(NGram, self).intersection(*others))

    def intersection_update(self, *others):
        """Update the set with the intersection of itself and other sets.

        >>> from ngram import NGram
        >>> n = NGram(['spam', 'eggs'])
        >>> other = set(['spam', 'ham'])
        >>> n.intersection_update(other)
        >>> list(n)
        ['spam']
        """
        self.difference_update(super(NGram, self).difference(*others))

    def symmetric_difference(self, other):
        """Return the symmetric difference of two sets as a new set.

        >>> from ngram import NGram
        >>> a = NGram(['spam', 'eggs'])
        >>> b = NGram(['spam', 'ham'])
        >>> sorted(list(a.symmetric_difference(b)))
        ['eggs', 'ham']
        """
        return self.copy(super(NGram, self).symmetric_difference(other))

    def symmetric_difference_update(self, other):
        """Update the set with the symmetric difference of itself and `other`.

        >>> from ngram import NGram
        >>> n = NGram(['spam', 'eggs'])
        >>> other = set(['spam', 'ham'])
        >>> n.symmetric_difference_update(other)
        >>> sorted(list(n))
        ['eggs', 'ham']
        """
        intersection = super(NGram, self).intersection(other)
        self.update(other)  # add items present in other
        self.difference_update(intersection)  # remove items present in both
