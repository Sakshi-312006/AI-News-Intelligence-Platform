from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


def analyze_sentiment(text):

    if not text or not text.strip():
        return {
            "sentiment": "Neutral",
            "sentiment_strength": 0.0,
            "scores": {
                "neg": 0.0,
                "neu": 1.0,
                "pos": 0.0,
                "compound": 0.0
            },
            "compound": 0.0
        }

    scores = sia.polarity_scores(text)

    compound = scores["compound"]

    print("\n===== VADER DEBUG =====")
    print("Positive :", scores["pos"])
    print("Neutral  :", scores["neu"])
    print("Negative :", scores["neg"])
    print("Compound :", compound)

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    sentiment_strength = abs(compound)

    return {
        "sentiment": sentiment,
        "sentiment_strength": sentiment_strength,
        "scores": scores,
        "compound": compound
    }