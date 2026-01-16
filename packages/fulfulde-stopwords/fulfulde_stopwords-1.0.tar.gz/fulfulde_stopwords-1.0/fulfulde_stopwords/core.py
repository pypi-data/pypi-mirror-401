"""
Core functionality for the Fulfulde stopwords library.

This module provides the main functions for working with Fulfulde stopwords,
including loading stopwords from file, checking if words are stopwords, and
removing stopwords from text.
"""

import os
from typing import Set, List, Union


def _load_stopwords() -> Set[str]:
    """
    Load stopwords from the bundled stopwords.txt file.

    Returns:
        Set[str]: A set of Fulfulde stopwords.

    Raises:
        FileNotFoundError: If the stopwords.txt file cannot be found.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stopwords_file = os.path.join(current_dir, 'stopwords.txt')

    if not os.path.exists(stopwords_file):
        raise FileNotFoundError(
            f"Stopwords file not found at {stopwords_file}. "
            "Please ensure the package is properly installed."
        )

    stopwords = set()

    with open(stopwords_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Strip whitespace and ignore comments and empty lines
            line = line.strip()
            if line and not line.startswith('#'):
                stopwords.add(line.lower())

    return stopwords


# Load stopwords once at module import
STOPWORDS = _load_stopwords()


def get_stopwords(case_sensitive: bool = False) -> Set[str]:
    """
    Get the set of Fulfulde stopwords.

    Args:
        case_sensitive (bool): If False (default), returns lowercase stopwords.
                              If True, preserves original casing.

    Returns:
        Set[str]: A set containing all Fulfulde stopwords.

    Example:
        >>> stopwords = get_stopwords()
        >>> 'mi' in stopwords
        True
        >>> len(stopwords) > 100
        True
    """
    if case_sensitive:
        return STOPWORDS.copy()
    return {word.lower() for word in STOPWORDS}


def is_stopword(word: str, case_sensitive: bool = False) -> bool:
    """
    Check if a word is a Fulfulde stopword.

    Args:
        word (str): The word to check.
        case_sensitive (bool): If False (default), comparison is case-insensitive.

    Returns:
        bool: True if the word is a stopword, False otherwise.

    Example:
        >>> is_stopword('mi')
        True
        >>> is_stopword('wuro')
        False
        >>> is_stopword('MI')
        True
        >>> is_stopword('MI', case_sensitive=True)
        False
    """
    check_word = word if case_sensitive else word.lower()
    return check_word in STOPWORDS


def remove_stopwords(
    tokens: List[str],
    case_sensitive: bool = False,
    preserve_order: bool = True
) -> List[str]:
    """
    Remove stopwords from a list of tokens.

    Args:
        tokens (List[str]): List of tokens (words) to filter.
        case_sensitive (bool): If False (default), comparison is case-insensitive.
        preserve_order (bool): If True (default), preserves original token order.

    Returns:
        List[str]: List of tokens with stopwords removed.

    Example:
        >>> tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder', 'Kameruun']
        >>> remove_stopwords(tokens)
        ['heɓi', 'wuro', 'Kameruun']
    """
    if preserve_order:
        return [
            token for token in tokens
            if not is_stopword(token, case_sensitive)
        ]
    else:
        return list({
            token for token in tokens
            if not is_stopword(token, case_sensitive)
        })


def filter_text(
    text: str,
    tokenizer=None,
    case_sensitive: bool = False
) -> str:
    """
    Remove stopwords from a text string.

    Args:
        text (str): The text to filter.
        tokenizer (callable, optional): A function to tokenize the text.
                                       If None, uses simple whitespace splitting.
        case_sensitive (bool): If False (default), comparison is case-insensitive.

    Returns:
        str: The filtered text with stopwords removed.

    Example:
        >>> text = "mi heɓi wuro e nder Kameruun"
        >>> filter_text(text)
        'heɓi wuro Kameruun'
    """
    # Use provided tokenizer or default to whitespace split
    if tokenizer is None:
        tokens = text.split()
    else:
        tokens = tokenizer(text)

    # Remove stopwords
    filtered_tokens = remove_stopwords(tokens, case_sensitive)

    # Rejoin tokens
    return ' '.join(filtered_tokens)


def get_stopword_count(tokens: List[str], case_sensitive: bool = False) -> int:
    """
    Count the number of stopwords in a list of tokens.

    Args:
        tokens (List[str]): List of tokens to analyze.
        case_sensitive (bool): If False (default), comparison is case-insensitive.

    Returns:
        int: The number of stopwords found.

    Example:
        >>> tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder']
        >>> get_stopword_count(tokens)
        3
    """
    return sum(1 for token in tokens if is_stopword(token, case_sensitive))


def get_stopword_ratio(tokens: List[str], case_sensitive: bool = False) -> float:
    """
    Calculate the ratio of stopwords to total tokens.

    Args:
        tokens (List[str]): List of tokens to analyze.
        case_sensitive (bool): If False (default), comparison is case-insensitive.

    Returns:
        float: The ratio of stopwords (between 0 and 1).
               Returns 0.0 if tokens list is empty.

    Example:
        >>> tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder']
        >>> round(get_stopword_ratio(tokens), 2)
        0.6
    """
    if not tokens:
        return 0.0

    stopword_count = get_stopword_count(tokens, case_sensitive)
    return stopword_count / len(tokens)


def get_stats(tokens: List[str], case_sensitive: bool = False) -> dict:
    """
    Get statistics about stopwords in a list of tokens.

    Args:
        tokens (List[str]): List of tokens to analyze.
        case_sensitive (bool): If False (default), comparison is case-insensitive.

    Returns:
        dict: A dictionary containing:
            - total_tokens: Total number of tokens
            - stopword_count: Number of stopwords
            - content_word_count: Number of content words (non-stopwords)
            - stopword_ratio: Ratio of stopwords to total tokens

    Example:
        >>> tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder']
        >>> stats = get_stats(tokens)
        >>> stats['stopword_count']
        3
    """
    total = len(tokens)
    sw_count = get_stopword_count(tokens, case_sensitive)

    return {
        'total_tokens': total,
        'stopword_count': sw_count,
        'content_word_count': total - sw_count,
        'stopword_ratio': sw_count / total if total > 0 else 0.0
    }
