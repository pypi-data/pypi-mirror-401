#!/usr/bin/env python3
"""
Examples of integrating fulfulde-stopwords with popular NLP libraries.
"""

from fulfulde_stopwords import get_stopwords


def example_sklearn():
    """Example: Integration with scikit-learn."""
    print("=" * 60)
    print("Example: scikit-learn Integration")
    print("=" * 60)

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

        stopwords = list(get_stopwords())

        # Sample Fulfulde documents
        documents = [
            "mi heɓi wuro e nder Kameruun",
            "gorko arii e luumo o soodii ɲaamdu",
            "mi yii jimol bee debbo",
            "wuro ɗum woni jamanu haa mbaɗa"
        ]

        print("Documents:")
        for i, doc in enumerate(documents, 1):
            print(f"  {i}. {doc}")

        # TF-IDF with stopwords removed
        print("\nTF-IDF Vectorization (with stopword removal):")
        vectorizer = TfidfVectorizer(stop_words=stopwords)
        tfidf_matrix = vectorizer.fit_transform(documents)

        print(f"  Feature names: {vectorizer.get_feature_names_out()}")
        print(f"  Matrix shape: {tfidf_matrix.shape}")

        # Count Vectorizer
        print("\nCount Vectorization (with stopword removal):")
        count_vec = CountVectorizer(stop_words=stopwords)
        count_matrix = count_vec.fit_transform(documents)
        print(f"  Feature names: {count_vec.get_feature_names_out()}")
        print(f"  Matrix shape: {count_matrix.shape}")

    except ImportError:
        print("scikit-learn not installed. Install with: pip install scikit-learn")

    print()


def example_nltk():
    """Example: Integration with NLTK."""
    print("=" * 60)
    print("Example: NLTK Integration")
    print("=" * 60)

    try:
        from nltk.tokenize import word_tokenize

        stopwords = get_stopwords()

        text = "mi heɓi wuro e nder Kameruun ɗum woni jamanu"

        print(f"Original text: {text}")

        # Tokenize and filter
        tokens = word_tokenize(text)
        print(f"Tokens: {tokens}")

        filtered = [w for w in tokens if w.lower() not in stopwords]
        print(f"Filtered: {filtered}")

    except ImportError:
        print("NLTK not installed. Install with: pip install nltk")
    except LookupError:
        print("NLTK punkt tokenizer not found. Download with:")
        print("  import nltk; nltk.download('punkt')")

    print()


def example_spacy():
    """Example: Integration with spaCy."""
    print("=" * 60)
    print("Example: spaCy Integration")
    print("=" * 60)

    try:
        import spacy

        # Create a blank model for multi-language
        nlp = spacy.blank("xx")

        # Add Fulfulde stopwords
        stopwords = get_stopwords()
        for word in stopwords:
            nlp.vocab[word].is_stop = True

        text = "mi heɓi wuro e nder Kameruun"
        doc = nlp(text)

        print(f"Original text: {text}")
        print(f"Tokens: {[token.text for token in doc]}")
        print(f"Stopwords: {[token.text for token in doc if token.is_stop]}")
        print(f"Content words: {[token.text for token in doc if not token.is_stop]}")

    except ImportError:
        print("spaCy not installed. Install with: pip install spacy")

    print()


def example_custom_tokenizer():
    """Example: Using custom tokenizer with filter_text."""
    print("=" * 60)
    print("Example: Custom Tokenizer")
    print("=" * 60)

    from fulfulde_stopwords import filter_text

    def custom_tokenizer(text):
        """Custom tokenizer that handles Fulfulde-specific characters."""
        # Simple whitespace tokenizer, but could be more sophisticated
        return text.lower().split()

    text = "Mi heɓi wuro e nder Kameruun ɗum woni jamanu"

    print(f"Original text: {text}")

    filtered = filter_text(text, tokenizer=custom_tokenizer)
    print(f"Filtered text: {filtered}")

    print()


def example_text_preprocessing_pipeline():
    """Example: Complete text preprocessing pipeline."""
    print("=" * 60)
    print("Example: Text Preprocessing Pipeline")
    print("=" * 60)

    from fulfulde_stopwords import remove_stopwords, get_stats

    def preprocess_fulfulde_text(text):
        """Complete preprocessing pipeline for Fulfulde text."""
        # Step 1: Lowercase
        text = text.lower()

        # Step 2: Tokenize (simple whitespace split)
        tokens = text.split()

        # Step 3: Get statistics before filtering
        stats_before = get_stats(tokens)

        # Step 4: Remove stopwords
        filtered_tokens = remove_stopwords(tokens)

        # Step 5: Get statistics after filtering
        stats_after = {
            'total_tokens': len(filtered_tokens),
            'stopword_count': 0,
            'content_word_count': len(filtered_tokens),
            'stopword_ratio': 0.0
        }

        return {
            'original_text': text,
            'original_tokens': tokens,
            'filtered_tokens': filtered_tokens,
            'filtered_text': ' '.join(filtered_tokens),
            'stats_before': stats_before,
            'stats_after': stats_after
        }

    text = "Mi yii gorko arii e luumo o soodii ɲaamdu bee mi heɓi wuro"

    print(f"Input text: {text}\n")

    result = preprocess_fulfulde_text(text)

    print(f"Original tokens ({len(result['original_tokens'])}): {result['original_tokens']}")
    print(f"Filtered tokens ({len(result['filtered_tokens'])}): {result['filtered_tokens']}")
    print(f"Filtered text: {result['filtered_text']}")
    print(f"\nStatistics:")
    print(f"  Stopwords removed: {result['stats_before']['stopword_count']}")
    print(f"  Content words kept: {result['stats_after']['content_word_count']}")
    print(f"  Reduction: {(1 - len(result['filtered_tokens'])/len(result['original_tokens'])):.2%}")

    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FULFULDE STOPWORDS - NLP INTEGRATION EXAMPLES")
    print("=" * 60 + "\n")

    example_sklearn()
    example_nltk()
    example_spacy()
    example_custom_tokenizer()
    example_text_preprocessing_pipeline()

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
