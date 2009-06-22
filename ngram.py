"""
A Python module to index objects and look up similar objects, based
on the N-gram similarity between strings. 

@note: Compatible with Python 2.6

The string-comparison algorithm is based from String::Trigram by Tarek Ahmed:
  http://search.cpan.org/dist/String-Trigram/

@author: Graham Poulter 

Based on "python-ngram" by Michel Albert, and rewritten by Graham Poulter:
 - Generalised the code to index any hashable object. The
   "item_transform" function creates a string from the object for the purpose
   of N-gram indexing. You are no longer limited to indexing and retrieving 
   strings only.
 - Added API documentation in the form of Epydoc docstrings.
 - Refactored the functional decomposition.
 - Replaced several constructor options with a generic "transform" function.
 - Python 2.x updates: e.g. "x in d" instead of "d.has_key(x)", d.setdefault
   instead of conditionals.
 - Identifiers to conform to PEP 8 (style guide), also changed terminology
   to imply indexing of any "item" object, not just strings.
 - Reduced memory usage by eliminating the innermost level of 
   dictionaries. Now storing just the number of shared grams at the lowest 
   level.
 - Made the class inherit from set, since it is effectively a set of items,
   with NGram search capability.
"""

__version__ = (4,0,0)

__license__ = """
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
"""

   
class NGram:
   """Retrieve items by their N-Gram string similarity to the query.  Behaves
   like a set of items, except for the ability to retrieve them by similarity.
   
   @note: Use unicode strings if the data contains multi-byte characters. With
   byte strings (str), the data is split into bytes, while with unicode
   strings (unicode) the data is split into characters.

   @ivar grams: Dictionary from n-gram to collection of items whose string 
   encoding contains the n-gram. Each collection is a dictionary from item 
   containing the n-gram,  to the number of times the n-gram occurs in 
   the string encoding of the item.

   @ivar _seen: Set items that have been indexed.
   
   @ivar _length: Dictionary from original strings (the keys of grams['xyz'])
   to length of the corresponding padded string.

   @ivar _padding: Padding string added before and after the main string.
   """
   

   def __init__(self, items=[], threshold=0.0, warp=1.0, item_transform=lambda x:x,
                N=3, pad_len=None, pad_char='$', query_transform=None):
      """Constructor
      
      @param threshold: Minimum similarity (between 0 and 1) for a string to be
      considered a match.
   
      @param warp: Use warp greater than 1.0 (but less than 3.0) to increase
      the similarity for short strings. 0.0 < warp < 1. 0 reduces the
      similarity of short strings relative to long ones, which is useless.

      @param items: Iteration of items to index for N-gram search.

      @param N: Length of each n-gram, must be at least 2.
   
      @param pad_len: Length of string padding string, between 0 and N-1.
      None means to use the default of N-1.
      
      @param pad_char: Character to use for padding. The default is '$' for
      readability. If '$' occurs in the strings, try using the rare
      non-breaking space character, u'\0xa', instead.
      
      @param item_transform: How to turn items into strings for indexing.
      For example,  lambda x: re.sub(r"[^a-z0-9]+", "", x) indexes only 
      alphanumeric characters for a string item and lambda x:string.lower(x[1]) 
      case-insensitive indexes the second member of a tuple item.
      
      @param query_transform: How to turn query items into strings. The
      default value of None indicates that the item_transform function should
      be used.
      """
      assert 0 <= threshold <= 1
      assert warp >= 0
      assert hasattr(item_transform, "__call__")
      assert N >= 1
      assert pad_len is None or 0 <= pad_len < N
      assert len(pad_char) == 1
      assert query_transform is None or hasattr(query_transform, "__call__")
      self.threshold = threshold
      self.warp = warp
      self._item_transform = item_transform
      self._N = N
      pad_len = pad_len or self._N-1
      self._padding = pad_char * pad_len # derive padding string
      self._query_transform = query_transform or item_transform
      self._seen = set()
      self._grams = {}
      self._length = {}
      self.update(items)
      
   def __contains__(self, item):
      """Whether this item has been indexed"""
      return item in self._seen

   def item_encode(self, item):
      """Encode the item for indexing by transforming it to a string and padding."""
      return self._padding + self._item_transform(item) + self._padding
   
   def query_encode(self, query):
      """Encode the query item for search by transforming it and padding the result."""
      return self._padding + self._query_transform(query) + self._padding
   
   def split(self, string):
      """Iterate over the ngrams in the string."""
      for i in range(len(string) - self._N + 1):
         yield string[i:i+self._N]

   def add(self, item):
      """Add an item to the N-gram index"""
      # Record the length of the padded string for future reference
      encoded_item = self.item_encode(item)
      self._length[item] = len(encoded_item)
      if item not in self:
         self._seen.add(item)
         for ngram in self.split(encoded_item):
            # Add a new n-gram and string to index if necessary
            self._grams.setdefault(ngram, {}).setdefault(item, 0)
            # Increment number of times the n-gram appears in the string
            self._grams[ngram][item] += 1
         
   def update(self, items):
      """Add items to the N-gram index."""
      for item in items:
         self.add(item)

   def candidates(self, query):
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
      for ngram in self.split(self.query_encode(query)):
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

   def candidate_similarities(self, query, candidates):
      """Evaluate similarity of query item to candidate items.
      
      @param query: Item to match against the candidate items.

      @param candidates: Mapping from items to the number of N-grams that they
      share with the query item.
      
      @return: Mapping from candidates to similarity, for candidates above the
      similarity threshold.
      """
      results = {}
      for match, samegrams in candidates.items():
         allgrams = len(self.query_encode(query)) + self._length[match] - 2 * self._N - samegrams + 2
         similarity = self.ngram_similarity(samegrams, allgrams, self.warp)
         if similarity > self.threshold:
            results[match] = similarity
      return results

   def similar_items(self, query):
      """Get similar items to the query item.
      @return: Mapping from matched items to similarity {'abc': 1.0, 'abcd': 0.8}
      """
      return self.candidate_similarities(query, self.candidates(query))

   def best_matches(self, query, count=None):
      """Returns the best matches for the given item.

      @param query: The item to search for.
      @param count: Maximum number of results to return.  None to return all results.
      @return: List of pairs of (item,similarity) by decreasing similarity.
      """
      results = sorted(self.similar_items(query).items(), key=lambda x:x[1], reverse=True)
      if count is not None:
         results = results[:count]
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
      """Static method compares two strings directly and return the similarity.
      For example, ngram.compare('sfewefsf', 'sdfafwgah').  Passes additional
      keyword arguments to the ngram constructor.

      @param s1: First string
      @param s2: Second string
      @return: Similarity between 0.0 and 1.0.
      """
      if s1 is None or s2 is None:
         if s1 == s2:
            return 1.0
         return 0.0
      try:
         return NGram([s1], **kwargs).similar_items(s2)[s1]
      except KeyError:
         return 0.0
