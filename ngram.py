#!/usr/bin/env python
"""
A Python module implementing a set-like object which has facilities to
retrieve similar objects from the set based on N-gram similarity
between strings.

@note: Compatible with Python 2.6

The string-comparison algorithm is based from String::Trigram by Tarek Ahmed:
  http://search.cpan.org/dist/String-Trigram/

@author: Michel Albert, Graham Poulter 

Changes in version 3 by Graham:
 
 1. Eliminated innermost level of dictionaries to reduce memory
 usage. Now stores innermost dict is just to look up the number of
 times the n-grams occurs in the item.

 2. New functional decomposition, Python 2.6 idioms, PEP 8 naming
 conventions, and Epydoc API documentation.

 3. Generalised the code to index any hashable object by means of a
 str_item function to generate an appropriate string from the item
 NGram indexing. No longer limited to indexing and retrieving strings.

 4. Refactored as a subclass the of built-in set, since it is really
 a set of things with fuzzy NGram lookup ability.
"""

__version__ = (3,0,0)

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

import copy

class NGram(set):
   """Retrieve items by their N-Gram string similarity to the query.  Behaves
   like a set of items, except for the ability to retrieve them by similarity.
   
   @note: Use unicode strings if the data contains multi-byte characters. With
   byte strings (str), the data is split into bytes, while with unicode
   strings (unicode) the data is split into characters.

   @note: Implements set update operations. Copy-creating set operations
   (union, intersection, difference, symmetric_difference) return instances of
   the built-in set. Use the NGram.copy operation to index
   a built-in set as an NGram instance of the desired parametrisation.

   @ivar grams: Dictionary from n-gram to collection of items whose string 
   encoding contains the n-gram. Each collection is a dictionary from item 
   containing the n-gram,  to the number of times the n-gram occurs in 
   the string encoding of the item.
   
   @ivar _length: Dictionary from items (the keys of each dictionary in grams)
   to length of the corresponding transformed and padded string.

   @ivar _padding: Padding string added before and after the main string.
   """
   

   def __init__(self, items=[], threshold=0.0, warp=1.0, str_item=lambda x:x,
                N=3, pad_len=None, pad_char='$', str_query=None):
      """Constructor
      
      @param threshold: Minimum similarity (between 0 and 1) for a string to be
      considered a match.
   
      @param warp: Use warp greater than 1.0 (but less than 3.0) to increase
      the similarity assigned to short string pairs to imrpove recall. 0.0 <
      warp < 1. 0 is disallowed, because it reduces the similarity of short
      strings relative to long strings, which is not what you want (trust me).

      @param items: Iteration of items to index for N-gram search.

      @param N: Length of each n-gram, must be at least 2.
   
      @param pad_len: Length of string padding string, between 0 and N-1.
      None means to use the default of N-1.
      
      @param pad_char: Character to use for padding. The default is '$' for
      readability. If '$' occurs in the strings, try using the rare
      non-breaking space character, u'\0xa', instead.
      
      @param str_item: Function to convert items into strings, defaulting to
      lambda x:x. For example, lambda x: re.sub(r"[^a-z0-9]+", "", x) will index
      only alphanumeric characters for a string item and lambda
      x:string.lower(x[1]) case-insensitive indexes the second member of a
      tuple item.
      
      @param str_query: Function to convert query items into strings. Default
      of None indicates that str_item should be used. Set to lambda x:x for
      example if the items are tuples but you wish to query by string.
      """
      assert 0 <= threshold <= 1
      assert 1.0 <= warp <= 3.0
      assert hasattr(str_item, "__call__")
      assert N >= 1
      if pad_len is None:
         pad_len = N-1
      assert 0 <= pad_len < N
      assert len(pad_char) == 1
      assert str_query is None or hasattr(str_query, "__call__")
      self.threshold = threshold
      self.warp = warp
      self._N = N
      self._pad_len = pad_len
      self._pad_char = pad_char
      self._padding = pad_char * pad_len # derive a padding string
      self._str_item = str_item
      self._str_query = str_query or str_item
      self._grams = {}
      self._length = {}
      self.update(items)
      
   def copy(self, items=None):
      """Epensive copy of NGram instance: reindexes everything. Although
      referencing the same items (shallow copy of items). 
      @param items: Index these items instead of those in the original.
      """
      items = items or self # Index different items if provided
      return NGram(items, self.threshold, self.warp, self._str_item,
               self._N, self._pad_len, self._pad_char, self._str_query)
   
   def pad(self, string):
      """Pad a string in preparation for splitting into ngrams."""
      return self._padding + string + self._padding
         
   def ngrams(self, string):
      """Iterate over the ngrams of a string.  No padding is performed."""
      for i in range(len(string) - self._N + 1):
         yield string[i:i+self._N]
         
   def ngrams_pad(self, string):
      """Iterate over ngrams of a string, padding the string before processing."""
      return self.ngrams(self.pad(string))

   def add(self, item):
      """Add an item to the N-gram index (only if it has not already been added)."""
      if item not in self:
         # Add the item to the base set
         super(NGram, self).add(item)
         # Record length of padded string
         padded_item = self.pad(self._str_item(item))
         self._length[item] = len(padded_item)
         for ngram in self.ngrams(padded_item):
            # Add a new n-gram and string to index if necessary
            self._grams.setdefault(ngram, {}).setdefault(item, 0)
            # Increment number of times the n-gram appears in the string
            self._grams[ngram][item] += 1

   def remove(self, item):
      """Remove an item from the index. Inverts the add operation."""
      if item in self:
         super(NGram, self).remove(item)
         del self._length[item]
         for ngram in self.ngrams_pad(self._str_item(item)):
            del self._grams[ngram][item]
         
   def items_sharing_ngrams(self, query):
      """Retrieve the subset of items that share n-grams the query item.
   
      @param query: Query item, for which indexed items that share N-grams
      will be retrieved.

      @return: Dictionary from matched string to the number of shared N-grams.
      """
      # From matched string to number of N-grams shared with query string
      shared = {} 
      # Dictionary mapping n-gram to string to number of occurrences of that 
      # ngram in the string that remain to be matched.
      remaining = {}
      for ngram in self.ngrams_pad(self._str_query(query)):
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

   def search(self, query):
      """Get items from the index that share some N-grams with the
      query and meet the similaroty threshold.
      
      @param query: Item to match against the candidate items.

      @param items_sharing_ngrams: Mapping from items to the number of N-grams that they
      share with the query item.
      
      @return: List of pairs of (item,similarity) by decreasing similarity.
      """
      results = []
      # Identify possible results
      for match, samegrams in self.items_sharing_ngrams(query).iteritems():
         allgrams = (len(self.pad(self._str_query(query))) 
                     + self._length[match] - (2 * self._N) - samegrams + 2)
         similarity = self.ngram_similarity(samegrams, allgrams, self.warp)
         if similarity >= self.threshold:
            results.append((match, similarity))
      # Sort results by decreasing similarity
      results.sort(key=lambda x:x[1], reverse=True)
      return results

   @staticmethod
   def ngram_similarity(samegrams, allgrams, warp=1):
      """Static method computes the similarity between two sets of n-grams.
      
      @note: similarity = (a**e - d**e)/a**e where a is "all n-grams", 
      d is "different n-grams" and e is the warp.

      @param samegrams: Number of n-grams that were found in both strings.
      @param allgrams: Total number ofn-grams in both strings.
      @return: Similarity in the range 0.0 to 1.0.
      """
      if warp == 1:
         similarity = float(samegrams) / allgrams
      else:
         diffgrams = allgrams - samegrams
         similarity = ((allgrams**warp) - (diffgrams**warp)) / (allgrams**warp)
      return similarity

   @staticmethod
   def compare(s1, s2, **kwargs):
      """Compares two strings and return their similarity.  For example, 
      ngram.compare('sfewefsf', 'sdfafwgah').  Additional keyword arguments
      passed to __init__.

      @param s1: First string
      @param s2: Second string
      @return: Similarity between 0.0 and 1.0.
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
      """Merge iteration of items into the index."""
      for item in items:
         self.add(item)
            
   def discard(self, item):
      """Remove an element from a set if it is a member.
      If the element is not a member, do nothing."""
      if item in self:
         self.remove(item)
   
   def difference_update(self, other):
      """Remove all elements of another set from this set."""
      for x in other:
         self.discard(x)
   
   def intersection_update(self, other):
      """Update a set with the intersection of itself and another."""
      self.difference_update([x for x in self if x not in other])
      
   def symmetric_difference_update(self, other):
      """Update a set with the symmetric difference of itself and another."""
      intersection = self.intersection(other) # record intersection of sets
      self.update(other) # add items present in other
      self.difference_update(self, intersection) # remove items present in both
         
if __name__ == "__main__":
   import sys
   print NGram.compare(sys.argv[1], sys.argv[2])
