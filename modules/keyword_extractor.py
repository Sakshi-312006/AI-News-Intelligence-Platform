from sklearn.feature_extraction.text import TfidfVectorizer


def extract_keywords(text, top_n=10):
    """
    Extract the most important keywords from an article
    using TF-IDF.
    """

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=1000
    )

    # Convert article into TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform([text])

    # Get all terms
    terms = vectorizer.get_feature_names_out()

    # Get TF-IDF scores
    scores = tfidf_matrix.toarray()[0]

    # Pair each term with its score
    keyword_scores = list(zip(terms, scores))

    # Sort by score, highest first
    keyword_scores = sorted(
        keyword_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Return top keywords
    keywords = keyword_scores[:top_n]

    return keywords