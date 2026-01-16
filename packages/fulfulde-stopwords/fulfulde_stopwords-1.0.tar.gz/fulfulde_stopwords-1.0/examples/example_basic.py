#!/usr/bin/env python3
"""
Basic usage examples for fulfulde-stopwords library.
"""

from fulfulde_stopwords import (
    get_stopwords,
    is_stopword,
    remove_stopwords,
    filter_text,
    get_stats
)


def example_1_get_stopwords():
    """Example 1: Get all stopwords."""
    print("=" * 60)
    print("Example 1: Get all stopwords")
    print("=" * 60)

    stopwords = get_stopwords()
    print(f"Total number of stopwords: {len(stopwords)}")
    print(f"\nFirst 10 stopwords: {list(stopwords)[:10]}")
    print()


def example_2_check_stopword():
    """Example 2: Check if words are stopwords."""
    print("=" * 60)
    print("Example 2: Check if words are stopwords")
    print("=" * 60)

    test_words = ['mi', 'wuro', 'e', 'Kameruun', 'ɗum', 'jimol']

    for word in test_words:
        result = is_stopword(word)
        print(f"'{word}' is stopword: {result}")
    print()


def example_3_remove_stopwords():
    """Example 3: Remove stopwords from token list."""
    print("=" * 60)
    print("Example 3: Remove stopwords from token list")
    print("=" * 60)

    # Example text: "I saw the city in Cameroon"
    tokens = ['mi', 'yii', 'wuro', 'e', 'nder', 'Kameruun']

    print(f"Original tokens: {tokens}")

    filtered = remove_stopwords(tokens)
    print(f"Filtered tokens: {filtered}")
    print()


def example_4_filter_text():
    """Example 4: Filter text directly."""
    print("=" * 60)
    print("Example 4: Filter text directly")
    print("=" * 60)

    # Example: "I came from the village with my family"
    text = "mi ari e wuro bee leɗɗe am"

    print(f"Original text: {text}")

    filtered = filter_text(text)
    print(f"Filtered text: {filtered}")
    print()


def example_5_get_statistics():
    """Example 5: Get stopword statistics."""
    print("=" * 60)
    print("Example 5: Get stopword statistics")
    print("=" * 60)

    # Example sentence
    tokens = ['mi', 'heɓi', 'wuro', 'e', 'nder', 'Kameruun', 'ɗum', 'woni', 'jamanu']

    print(f"Tokens: {tokens}")

    stats = get_stats(tokens)
    print(f"\nStatistics:")
    print(f"  Total tokens: {stats['total_tokens']}")
    print(f"  Stopwords: {stats['stopword_count']}")
    print(f"  Content words: {stats['content_word_count']}")
    print(f"  Stopword ratio: {stats['stopword_ratio']:.2%}")
    print()


def example_6_real_text():
    """Example 6: Process real Fulfulde text."""
    print("=" * 60)
    print("Example 6: Process real Fulfulde text")
    print("=" * 60)

    # Example text: "The man went to the market and bought food"
    text = "gorko arii e luumo o soodii ɲaamdu"
    tokens = text.split()

    print(f"Original text: {text}")
    print(f"Original tokens: {tokens}")

    filtered = remove_stopwords(tokens)
    print(f"Filtered tokens: {filtered}")
    print(f"Filtered text: {' '.join(filtered)}")

    stats = get_stats(tokens)
    print(f"\nStopword ratio: {stats['stopword_ratio']:.2%}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FULFULDE STOPWORDS - USAGE EXAMPLES")
    print("=" * 60 + "\n")

    example_1_get_stopwords()
    example_2_check_stopword()
    example_3_remove_stopwords()
    example_4_filter_text()
    example_5_get_statistics()
    example_6_real_text()

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
