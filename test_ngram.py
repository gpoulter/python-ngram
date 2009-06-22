#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for the ngram module.

@author: Graham Poulter

"""

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

from pprint import pprint as pp
import unittest
import string

from ngram import ngram

class NgramTests(unittest.TestCase):
    """Tests of the ngram class"""
    
    def test_original(self):
        """Tests from the old __name__=="__main__" stanza of ngram.py to
        check that the logic hasn't changed while upgrading the code"""

        haystack = ['sdafaf','asfwef','asdfawe','adfwe', 'askfjwehiuasdfji']
        
        tg = ngram(haystack, threshold=0.0)

        self.assertEqual(
            tg.similar_strings('askfjwehiuasdfji'),
            {'adfwe': 0.041666666666666664,
             'asdfawe': 0.17391304347826086,
             'asfwef': 0.083333333333333329,
             'askfjwehiuasdfji': 1.0} ) 

        self.assertEqual(tg.best_match('afadfwe', 2),
                         [('adfwe', 0.59999999999999998), 
                          ('asdfawe', 0.20000000000000001)])

        self.assertEqual(ngram.compare('sdfeff', 'sdfeff'), 1.0)


    def test_split(self):
        """Test the functions that split strings into ngrams"""
        
        abcgrams = ['$$a', '$ab', 'abc', 'bc$', 'c$$']
        
        # Basic splitting into n-grams
        self.assertEqual(list(ngram().split("abc")), abcgrams)

        # Test transforming to lowercase
        self.assertEqual(list(ngram(transform=string.lower).split("AbC")), abcgrams)
        
        # Demonstrate that multi-byte characters fall prey to the 1 char == 1 byte assumption
        # Note: utf-8 encoding of é is \xc3\xa9
        self.assertEqual(list(ngram(pad_len=1).split('é')), ['$\xc3\xa9', '\xc3\xa9$'])
        
        # Unicode strings don't have this problem.
        # Note: unicode character for é is \xe9
        self.assertEqual(list(ngram(pad_len=1).split(u'é')), [u'$\xe9$'])


if __name__ == "__main__":
    unittest.main()
