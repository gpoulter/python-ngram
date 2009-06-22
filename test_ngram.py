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

from ngram import NGram

class NgramTests(unittest.TestCase):
    """Tests of the ngram class"""
    
    def test_original(self):
        """Tests from the old __name__=="__main__" stanza of ngram.py to
        check that the logic hasn't changed while upgrading the code"""

        items = ['sdafaf','asfwef','asdfawe','adfwe', 'askfjwehiuasdfji']
        
        tg = NGram(items)

        self.assertEqual(
            tg.similar_items('askfjwehiuasdfji'),
            {'adfwe': 0.041666666666666664,
             'asdfawe': 0.17391304347826086,
             'asfwef': 0.083333333333333329,
             'askfjwehiuasdfji': 1.0} )

        self.assertEqual(tg.best_matches('afadfwe', 2),
                         [('adfwe', 0.59999999999999998), 
                          ('asdfawe', 0.20000000000000001)])

        self.assertEqual(NGram.compare('sdfeff', 'sdfeff'), 1.0)


    def test_split(self):
        """Test the functions that split strings into ngrams"""
        
        abcgrams = ['$$a', '$ab', 'abc', 'bc$', 'c$$']
        
        # Basic splitting into n-grams
        index = NGram()
        self.assertEqual(list(index.split(index.item_encode("abc"))), abcgrams)

        # Transforming string to lowercase first.
        index = NGram(item_transform=string.lower)
        self.assertEqual(list(index.split(index.item_encode("AbC"))), abcgrams)
        
        # Encoded byte strings are split into bytes, not necessarily characters.
        # For example, the utf-8 encoding of é (\xe9) is \xc3\xa9
        index = NGram(pad_len=1)
        self.assertEqual(list(index.split(index.item_encode('é'))), ['$\xc3\xa9', '\xc3\xa9$'])
        
        # Unicode strings are correctly split into characters.
        # Fox example, the unicode character for é is \xe9
        self.assertEqual(list(index.split(index.item_encode(u'é'))), [u'$\xe9$'])


if __name__ == "__main__":
    unittest.main()
