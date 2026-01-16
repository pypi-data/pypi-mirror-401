#!/usr/bin/env python3
"""
Unit tests for the fulfulde_stopwords library.
"""

import unittest
from fulfulde_stopwords import (
    get_stopwords,
    is_stopword,
    remove_stopwords,
    filter_text,
    get_stopword_count,
    get_stopword_ratio,
    get_stats,
    STOPWORDS
)


class TestGetStopwords(unittest.TestCase):
    """Test the get_stopwords function."""

    def test_returns_set(self):
        """Test that get_stopwords returns a set."""
        stopwords = get_stopwords()
        self.assertIsInstance(stopwords, set)

    def test_not_empty(self):
        """Test that stopword list is not empty."""
        stopwords = get_stopwords()
        self.assertGreater(len(stopwords), 0)

    def test_expected_size(self):
        """Test that stopword list has expected size."""
        stopwords = get_stopwords()
        self.assertGreater(len(stopwords), 100)
        self.assertLess(len(stopwords), 300)

    def test_contains_common_stopwords(self):
        """Test that common stopwords are present."""
        stopwords = get_stopwords()
        common = ['mi', 'e', 'o', 'ɗum', 'nder', 'a']
        for word in common:
            self.assertIn(word, stopwords)


class TestIsStopword(unittest.TestCase):
    """Test the is_stopword function."""

    def test_known_stopwords(self):
        """Test known stopwords return True."""
        self.assertTrue(is_stopword('mi'))
        self.assertTrue(is_stopword('e'))
        self.assertTrue(is_stopword('o'))
        self.assertTrue(is_stopword('ɗum'))

    def test_known_content_words(self):
        """Test known content words return False."""
        self.assertFalse(is_stopword('wuro'))
        self.assertFalse(is_stopword('gorko'))
        self.assertFalse(is_stopword('jimol'))

    def test_case_insensitive_default(self):
        """Test case insensitive matching by default."""
        self.assertTrue(is_stopword('MI'))
        self.assertTrue(is_stopword('Mi'))
        self.assertTrue(is_stopword('mI'))

    def test_case_sensitive_mode(self):
        """Test case sensitive mode."""
        self.assertTrue(is_stopword('mi', case_sensitive=True))
        self.assertFalse(is_stopword('MI', case_sensitive=True))


class TestRemoveStopwords(unittest.TestCase):
    """Test the remove_stopwords function."""

    def test_removes_stopwords(self):
        """Test that stopwords are removed."""
        tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder']
        filtered = remove_stopwords(tokens)
        self.assertEqual(filtered, ['heɓi', 'wuro'])

    def test_preserves_order(self):
        """Test that token order is preserved."""
        tokens = ['wuro', 'mi', 'heɓi', 'e', 'jimol']
        filtered = remove_stopwords(tokens)
        self.assertEqual(filtered, ['wuro', 'heɓi', 'jimol'])

    def test_empty_input(self):
        """Test empty token list."""
        tokens = []
        filtered = remove_stopwords(tokens)
        self.assertEqual(filtered, [])

    def test_all_stopwords(self):
        """Test list with only stopwords."""
        tokens = ['mi', 'e', 'o', 'nder']
        filtered = remove_stopwords(tokens)
        self.assertEqual(filtered, [])

    def test_no_stopwords(self):
        """Test list with no stopwords."""
        tokens = ['wuro', 'gorko', 'jimol']
        filtered = remove_stopwords(tokens)
        self.assertEqual(tokens, filtered)


class TestFilterText(unittest.TestCase):
    """Test the filter_text function."""

    def test_basic_filtering(self):
        """Test basic text filtering."""
        text = "mi heɓi wuro e nder Kameruun"
        filtered = filter_text(text)
        self.assertEqual(filtered, "heɓi wuro Kameruun")

    def test_empty_text(self):
        """Test empty text."""
        text = ""
        filtered = filter_text(text)
        self.assertEqual(filtered, "")

    def test_only_stopwords(self):
        """Test text with only stopwords."""
        text = "mi e o nder"
        filtered = filter_text(text)
        self.assertEqual(filtered, "")


class TestGetStopwordCount(unittest.TestCase):
    """Test the get_stopword_count function."""

    def test_count_stopwords(self):
        """Test counting stopwords."""
        tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder']
        count = get_stopword_count(tokens)
        self.assertEqual(count, 3)

    def test_no_stopwords(self):
        """Test count with no stopwords."""
        tokens = ['wuro', 'gorko', 'jimol']
        count = get_stopword_count(tokens)
        self.assertEqual(count, 0)

    def test_all_stopwords(self):
        """Test count with all stopwords."""
        tokens = ['mi', 'e', 'o']
        count = get_stopword_count(tokens)
        self.assertEqual(count, 3)

    def test_empty_list(self):
        """Test count with empty list."""
        tokens = []
        count = get_stopword_count(tokens)
        self.assertEqual(count, 0)


class TestGetStopwordRatio(unittest.TestCase):
    """Test the get_stopword_ratio function."""

    def test_ratio_calculation(self):
        """Test ratio calculation."""
        tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder']
        ratio = get_stopword_ratio(tokens)
        self.assertAlmostEqual(ratio, 0.6)

    def test_no_stopwords_ratio(self):
        """Test ratio with no stopwords."""
        tokens = ['wuro', 'gorko', 'jimol']
        ratio = get_stopword_ratio(tokens)
        self.assertEqual(ratio, 0.0)

    def test_all_stopwords_ratio(self):
        """Test ratio with all stopwords."""
        tokens = ['mi', 'e', 'o']
        ratio = get_stopword_ratio(tokens)
        self.assertEqual(ratio, 1.0)

    def test_empty_list_ratio(self):
        """Test ratio with empty list."""
        tokens = []
        ratio = get_stopword_ratio(tokens)
        self.assertEqual(ratio, 0.0)


class TestGetStats(unittest.TestCase):
    """Test the get_stats function."""

    def test_stats_structure(self):
        """Test that stats returns correct structure."""
        tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder']
        stats = get_stats(tokens)

        self.assertIn('total_tokens', stats)
        self.assertIn('stopword_count', stats)
        self.assertIn('content_word_count', stats)
        self.assertIn('stopword_ratio', stats)

    def test_stats_values(self):
        """Test that stats returns correct values."""
        tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder']
        stats = get_stats(tokens)

        self.assertEqual(stats['total_tokens'], 5)
        self.assertEqual(stats['stopword_count'], 3)
        self.assertEqual(stats['content_word_count'], 2)
        self.assertAlmostEqual(stats['stopword_ratio'], 0.6)

    def test_stats_empty_list(self):
        """Test stats with empty list."""
        tokens = []
        stats = get_stats(tokens)

        self.assertEqual(stats['total_tokens'], 0)
        self.assertEqual(stats['stopword_count'], 0)
        self.assertEqual(stats['content_word_count'], 0)
        self.assertEqual(stats['stopword_ratio'], 0.0)


class TestModuleConstants(unittest.TestCase):
    """Test module-level constants."""

    def test_stopwords_constant(self):
        """Test that STOPWORDS constant exists and is valid."""
        self.assertIsInstance(STOPWORDS, set)
        self.assertGreater(len(STOPWORDS), 0)

    def test_stopwords_constant_matches_function(self):
        """Test that STOPWORDS matches get_stopwords()."""
        self.assertEqual(STOPWORDS, get_stopwords())


if __name__ == '__main__':
    unittest.main()
