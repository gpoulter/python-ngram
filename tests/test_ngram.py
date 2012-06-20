#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for the ngram module."""

import unittest
from ngram import NGram


class NgramTests(unittest.TestCase):
    """Tests of the ngram class"""

    items = ['sdafaf', 'asfwef', 'asdfawe', 'adfwe', 'askfjwehiuasdfji']

    def test_ngram_search(self):
        """Tests from the original ngram.py, to check that the
        rewrite still uses the same underlying algorithm"""

        # Basic searching of the index
        idx = NGram(self.items)
        self.assertEqual(idx.search('askfjwehiuasdfji'), [
            ('askfjwehiuasdfji', 1.0),
            ('asdfawe', 0.17391304347826086),
            ('asfwef', 0.083333333333333329),
            ('adfwe', 0.041666666666666664)])
        self.assertEqual(idx.search('afadfwe')[:2],
                [('adfwe', 0.59999999999999998),
                 ('asdfawe', 0.20000000000000001)])

        # Pairwise comparison of strings
        self.assertEqual(NGram.compare('sdfeff', 'sdfeff'), 1.0)
        self.assertEqual(NGram.compare('sdfeff', 'zzzzzz'), 0.0)

    def test_set_operations(self):
        """Test advanced set operations"""
        items1 = set(["abcde", "cdefg", "fghijk", "ijklm"])
        items2 = set(["cdefg", "lmnop"])
        idx1 = NGram(items1)
        idx2 = NGram(items2)
        results = lambda L: sorted(x[0] for x in L)
        # Item removal
        self.assertEqual(results(idx1.search('cde')), ["abcde", "cdefg"])
        idx1.remove('abcde')
        self.assertEqual(results(idx1.search('cde')), ["cdefg"])
        # Set intersection operation
        items1.remove('abcde')
        idx1.intersection_update(idx2)
        self.assertEqual(idx1, items1.intersection(items2))
        self.assertEqual(results(idx1.search('lmn')), [])
        self.assertEqual(results(idx1.search('ijk')), [])
        self.assertEqual(results(idx1.search('def')), ['cdefg'])


if __name__ == "__main__":
    unittest.main()
