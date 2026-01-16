"""
Fulfulde Stopwords
==================

A Python library providing stopwords for the Fulfulde language (Adamawa variant).

This library provides a curated list of stopwords for Natural Language Processing
tasks in Fulfulde, including text classification, information retrieval, clustering,
and topic modeling.

Usage:
    >>> from fulfulde_stopwords import get_stopwords
    >>> stopwords = get_stopwords()
    >>> print(len(stopwords))

    >>> from fulfulde_stopwords import remove_stopwords
    >>> tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder']
    >>> filtered = remove_stopwords(tokens)
    >>> print(filtered)
    ['heɓi', 'wuro']

Author: Research Team
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Research Team"
__license__ = "MIT"

from .core import (
    get_stopwords,
    remove_stopwords,
    is_stopword,
    filter_text,
    get_stopword_count,
    get_stopword_ratio,
    get_stats,
    STOPWORDS
)

__all__ = [
    "get_stopwords",
    "remove_stopwords",
    "is_stopword",
    "filter_text",
    "get_stopword_count",
    "get_stopword_ratio",
    "get_stats",
    "STOPWORDS",
]
