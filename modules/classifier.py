import joblib


# Load trained model
MODEL_PATH = "models/news_classifier.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

classifier = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_category(text):
    """
    Predict the news category of an article.
    """

    # Convert article text into TF-IDF features
    text_tfidf = vectorizer.transform([text])

    # Predict category
    prediction = classifier.predict(text_tfidf)[0]

    # Get prediction probabilities
    probabilities = classifier.predict_proba(text_tfidf)[0]

    # Find highest probability
    confidence = probabilities.max()

    return {
        "category": prediction,
        "confidence": confidence
    }