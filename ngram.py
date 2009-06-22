"""

A Python module to compute the similarity between strings.

This code was largely inspired by String::Trigram by Tarek Ahmed. Actually
I just translated it to python ;)
   
You can find the original Perl-Module at
http://search.cpan.org/dist/String-Trigram/

@author: Michel Albert

@author: Graham Poulter

@copyright: Copyright (C) 2005 Michel Albert

Modifications by Graham Poulter
 - Added Epydoc docstrings for API documentation.
 - Factored out functions like pad() and split()
 - Replaced ignore_case and other options with generic transform.
 - Python 2.x updates: e.g. "x in d" instead of "d.has_key(x)", d.setdefault
   instead of conditionals.
 - Renamed identifiers to conform to PEP 8 (style guide)
 - Reduced memory usage by eliminating the innermost layer of 
   dictionaries (now storing only number of shared grams).

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
"""

   
class ngram:
   """Computes similiarity between strings based on n-gram composition.  Dictionary
   function finds most similar strings.
   
   @note: Do not modify private variables after initialisation.

   @note: Use unicode strings if multi-byte characters may occur.  Using
   base strings or bytes will assume that 1 byte = 1 character.

   @ivar threshold: Minimum similarity score for a string to be considered
   worthy, between 0 and 1.
                       
   @ivar warp: warp > 1 means short strings are getting away better, if
   warp < 1 they are getting away worse.

   @ivar grams: Dictionary from n-gram to collection of strings containing the
   n-gram. Each collection is a dictionary from string containing the n-gram,
   to the number of times the n-gram occurs in the string.

   @ivar _seen: Set of unique padded strings that have been indexed - because
   such string must be indexed only once.
   
   @ivar _length: Dictionary from original strings (the keys of grams['xyz'])
   to length of the corresponding padded string.
   
   @ivar _transform: Transformation function to simplify input strings for
   indexing and matching. For example, pass string.lower to obtain
   case-insensitive comparison, or pass lambda x: re.sub(r"[^a-z0-9]+", "",
   x) to index only alphanumeric characters. Defaults to identity function
   (no transformation).
         
   @ivar _ngram_len: Length of n-gram, must be at least 2.

   @ivar _padding: Padding string added before and after the main string.
   """
   

   def __init__(self, haystack=[], threshold=0.0, warp=1.0, transform=lambda x:x,
                ngram_len=3, pad_len=None, pad_char='$'):
      """Constructor
      
      @param haystack: Iteration over strings in which to look for matches.

      @param pad_len: Length of padding string, between 0 and ngram_len-1.
      Defaults to ngram_len-1.
      
      @param pad_char: character to use for padding. Defaults to '$'.  One
      may for example use u'\0xa' (non-breaking space) instead.
      """
      assert 0 <= threshold <= 1
      self.threshold = threshold
      assert warp >= 0
      self.warp = warp
      assert hasattr(transform, "__call__")
      self._transform = transform
      self._ngram_len = ngram_len
      pad_len = self._ngram_len-1 if pad_len is None else pad_len
      assert 0 <= pad_len < ngram_len
      assert len(pad_char) == 1
      self._padding = pad_char * pad_len # derive padding string
      self._seen = set()
      self._grams = {}
      self._length = {}
      self.index(haystack)

   def index(self, haystack):
      """Takes list of strings and adds them to the N-Gram index"""
      for string in haystack:
         # Record the length of the padded string for future reference
         paddedstring = self.pad(string)
         self._length[string] = len(paddedstring)
         if paddedstring not in self._seen:
            self._seen.add(paddedstring)
            for ngram in self.split(paddedstring, padded=True):
               # Add a new n-gram and string to index if necessary
               self._grams.setdefault(ngram, {}).setdefault(string, 0)
               # Increment number of times the n-gram appears in the string
               self._grams[ngram][string] += 1

   def pad(self, string):
      """Transformed and padded form of the string."""
      return self._padding + self._transform(string) + self._padding

   def split(self, string, padded=False):
      """Iterated over the ngrams in the string.
      @param string: Input string to split.
      @param padded: Whether the input string has already been padded."""
      string = string if padded else self.pad(string)
      for i in range(len(string) - self._ngram_len + 1):
         yield string[i:i+self._ngram_len]

   def similar_strings(self, needle):
      """Return high-scoring matches to the query string, as a dictionary
      mapping matches to their score, such as {'abc': 1.0, 'abcd': 0.8}"""
      return self.similarity(needle, self.candidates(needle))

   def candidates(self, needle):
      """Retrieve strings which have n-grams in common with the query string.
      @param needle: The query string to compare with the search space.
      @return: Dictionary from matched string to the number of shared N-grams.
      """
      # From matched string to number of N-grams shared with query string
      shared = {} 
      # Dictionary mapping n-gram to string to number of occurrences of that 
      # ngram in the string that remain to be matched.
      remaining = {}
      for ngram in self.split(needle):
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

   def similarity(self, string, candidates):
      """Similarity of query string to given candidate strings.
      
      @param string: Unpadded query string to match against the candidates.
      
      @param candidates: Dictionary from matched strings to the number of N-grams 
      they have in common with the query string.
                    
      @return: Dictionary from matched strings to score.
      """
      results = {}
      for match, samegrams in candidates.iteritems():
         allgrams = len(self.pad(string)) + self._length[match] - 2 * self._ngram_len - samegrams + 2
         similarity = self.ngram_similarity_score(samegrams, allgrams, self.warp)
         if similarity > self.threshold:
            results[match] = similarity
      return results

   def best_match(self, needle, count=1):
      """Returns the best matches for the given string

      @param needle: The string to search for.
      @param count: How many results to return.
      @return: Top-ranking strings paired with match score, in decreasing order of score.
      """
      return sorted(self.similar_strings(needle).iteritems(), key=lambda x:x[1], reverse=True)[:count]
      
   @staticmethod
   def ngram_similarity_score(samegrams, allgrams, warp=1):
      """Static method computes the similarity between two sets of n-grams.
      
      Uses the following formula, where a is "all n-grams", d is "different
      n-grams" and e is the warp: (a**e - d**e)/a**e

      @param samegrams: Number of n-grams that were found in both strings.

      @param allgrams: Total number of n-grams in the search space.

      @return: Similarity score between 0.0 and 1.0.
      """
      diffgrams = -1
      if warp == 1:
         similarity = float(samegrams) / allgrams
      else:
         diffgrams = allgrams - samegrams
         similarity = ((allgrams**warp) - (diffgrams**warp)) / (allgrams**warp)
      return similarity

   @staticmethod
   def compare(s1, s2):
      """Static method compares two strings and returns the similarity score, e.g.
      
      ngram.compare('sfewefsf', 'sdfafwgah')

      @param s1: First string
      @param s2: Second string
      
      @return: Float between 0 and 1 with similarity score.
      """
      if s1 is None or s2 is None:
         if s1 == s2:
            return 1.0
         return 0.0
      try:
         return ngram([s1]).similar_strings(s2)[s1]
      except KeyError:
         return 0.0
