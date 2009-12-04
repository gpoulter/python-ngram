"""
:mod:`ngram` -- Provides a set that supports lookup by string similarity
========================================================================

.. moduleauthor:: Michel Albert (to version 2)
.. moduleauthor:: Graham Poulter (version 3+)

"""

from __future__ import division

__version__ = (3, 0, 0)

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

   :type threshold: float between 0.0 and 1.0
   :param threshold: minimum similarity for a string to be considered a match.

   :type warp: float, 1.0 <= warp <= 3.0
   :param warp: use warp greater than 1.0 to increase the similarity of shorter string pairs.

   :type items: [item,...]
   :param items: iteration of items to index for N-gram search.

   :type N: int, N >= 2
   :param N: number of characters per n-gram
   
   :type pad_len: int, 0 <= pad_len <= N-1
   :param pad_len: how many characters padding to add (default N-1)
   
   :type pad_char: str or unicode
   :param pad_char: character to use for padding.  Default is '$', but consider using the\
   non-breaking space character, ``u'\0xa'``.
   
   :type iconv: function(item) -> str/unicode 
   :param iconv: Function to convert items into string, default is no conversion.
 
   :type qconv: function(query) -> str/unicode
   :param qconv: Function to convert query into string, default is no conversion.

   And some instance variables:

   :type grams: {ngram:{item:int,...},...],...}
   :ivar grams: For each n-gram, the items containing it and the number of times\
   the n-gram occurs in the item.
   
   :type length: {item:int,...}
   :ivar length: lengths of padded string representations of each item.
   """
   

   def __init__(self, items=[], threshold=0.0, warp=1.0, iconv=None,
                N=3, pad_len=None, pad_char='$', qconv=None):
      super(set, self).__init__()
      if not (0 <= threshold <= 1):
         raise ValueError("Threshold %s outside 0.0 to 1.0 range" % threshold)
      if not(1.0 <= warp <= 3.0):
         raise ValueError("Warp %s outside 1.0 to 3.0 range" % warp)
      if not N >= 1:
         raise ValueError("N of %s needs to be >= 1" % N)
      if pad_len is None:
         pad_len = N-1
      if not (0 <= pad_len < N):
         raise ValueError("pad_len of %s is outside 0 to %d range" % (pad_len,N))
      if not (isinstance(pad_char,basestring) and len(pad_char)==1):
         raise ValueError("pad_char %s is not a single-character string." % pad_char)
      if not (iconv is None or hasattr(iconv, "__call__")):
         raise ValueError("iconv %s is not a function." % pad_char)
      if not (qconv is None or hasattr(qconv, "__call__")):
         raise ValueError("qconv %s is not a function." % pad_char)
      self.threshold = threshold
      self.warp = warp
      self.N = N
      self._pad_len = pad_len
      self._pad_char = pad_char
      self._padding = pad_char * pad_len # derive a padding string
      def identity(x):
         return x
      self.iconv = iconv or identity
      self.qconv = qconv or identity
      self._grams = {}
      self.length = {}
      self.update(items)
      
   def copy(self, items=None):
      """Create a deep copy of the current instance by using the same items and
      constructor parameters.

      :type items: [item,...]
      :param items: Index these items instead of those in the original.
      """
      items = items or self # Index different items if provided
      return NGram(items, self.threshold, self.warp, self.iconv,
               self.N, self._pad_len, self._pad_char, self.qconv)
   
   def pad(self, string):
      """Pad a string in preparation for splitting into ngrams."""
      return self._padding + string + self._padding
         
   def ngrams(self, string):
      """Iterate over the ngrams of a string.  No padding is performed."""
      for i in range(len(string) - self.N + 1):
         yield string[i:i+self.N]
         
   def ngrams_pad(self, string):
      """Iterate over ngrams of a string, padding the string before processing."""
      return self.ngrams(self.pad(string))

   def add(self, item):
      """Add an item to the N-gram index (only if it has not already been added)."""
      if item not in self:
         # Add the item to the base set
         super(NGram, self).add(item)
         # Record length of padded string
         padded_item = self.pad(self.iconv(item))
         self.length[item] = len(padded_item)
         for ngram in self.ngrams(padded_item):
            # Add a new n-gram and string to index if necessary
            self._grams.setdefault(ngram, {}).setdefault(item, 0)
            # Increment number of times the n-gram appears in the string
            self._grams[ngram][item] += 1

   def remove(self, item):
      """Remove an item from the index. Inverts the add operation."""
      if item in self:
         super(NGram, self).remove(item)
         del self.length[item]
         for ngram in self.ngrams_pad(self.iconv(item)):
            del self._grams[ngram][item]
         
   def items_sharing_ngrams(self, query):
      """Retrieve the subset of items that share n-grams the query item.
   
      :param query: look up items that share N-grams with the `query`.
      :return: dictionary from matched string to the number of shared N-grams.
      """
      # From matched string to number of N-grams shared with query string
      shared = {} 
      # Dictionary mapping n-gram to string to number of occurrences of that 
      # ngram in the string that remain to be matched.
      remaining = {}
      for ngram in self.ngrams_pad(self.qconv(query)):
         try:
            for match, count in self._grams[ngram].iteritems():
               remaining.setdefault(ngram, {}).setdefault(match, count)
               # match up to as many occurrences of ngram as exist in the matched string
               if remaining[ngram][match] > 0:
                  remaining[ngram][match] -= 1
                  shared.setdefault(match, 0)
                  shared[match] += 1
         except KeyError:
            pass
      return shared

   def search(self, query, threshold=None):
      """Search the index for items that have similarity to the query.
      
      :param query: returned items will have at least `threshold` similarity to the query.
      :param threshold: override the threshold specified in the constructor.
      :return: list of pairs of (item,similarity) by decreasing similarity.
      """
      threshold = threshold if threshold is not None else self.threshold
      results = []
      # Identify possible results
      for match, samegrams in self.items_sharing_ngrams(query).iteritems():
         allgrams = (len(self.pad(self.qconv(query))) 
                     + self.length[match] - (2 * self.N) - samegrams + 2)
         similarity = self.ngram_similarity(samegrams, allgrams, self.warp)
         if similarity >= threshold:
            results.append((match, similarity))
      # Sort results by decreasing similarity
      results.sort(key=lambda x:x[1], reverse=True)
      return results

   @staticmethod
   def ngram_similarity(samegrams, allgrams, warp=1.0):
      """Similarity for two sets of n-grams.
      
      :note: ``similarity = (a**e - d**e)/a**e`` where `a` is "all n-grams", 
      `d` is "different n-grams" and `e` is the warp.

      :param samegrams: number of n-grams that were found in both strings.
      :param allgrams: total number ofn-grams in both strings.
      :return: similarity in the range 0.0 to 1.0.

      >>> from ngram import NGram
      >>> NGram.ngram_similarity(5,10)
      0.5
      >>> NGram.ngram_similarity(5,10,warp=2)
      0.75
      >>> NGram.ngram_similarity(5,10,warp=3)
      0.875
      >>> NGram.ngram_similarity(2,4,warp=2)
      0.75
      >>> NGram.ngram_similarity(3,4)
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
      """Compares two strings and return their similarity.  

      :param s1: first string
      :param s2: second string
      :param kwargs: additional keyword arguments passed to __init__.
      :return: similarity between 0.0 and 1.0.

      >>> from ngram import NGram
      >>> NGram.compare('foo', 'foobar')
      0.29999999999999999
      >>> NGram.compare('foo', 'boo')
      0.25
      >>> NGram.compare('abcd', 'bcd') #N=2
      0.375
      >>> NGram.compare('abc', 'bcd', N=1)
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

   ### Reimplement updating set operations on top of NGram add/remove
      
   def update(self, items):
      """Update the set with new items."""
      for item in items:
         self.add(item)
            
   def discard(self, item):
      """If `item` is a member of the set, remove it."""
      if item in self:
         self.remove(item)
   
   def difference_update(self, other):
      """Remove from this set all elements from `other` set."""
      for x in other:
         self.discard(x)
   
   def intersection_update(self, other):
      """Update the set with the intersection of itself and `other`."""
      self.difference_update([x for x in self if x not in other])
      
   def symmetric_difference_update(self, other):
      """Update the set with the symmetric difference of itself and `other`."""
      intersection = self.intersection(other) # record intersection of sets
      self.update(other) # add items present in other
      self.difference_update(self, intersection) # remove items present in both
