import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# English stopwords
stop_words = set(stopwords.words("english"))

# Lemmatizer
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    """
    Basic cleaning of article text.
    """

    # Convert text to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove non-alphabetic characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def preprocess_text(text):
    """
    Complete preprocessing pipeline.
    """

    # 1. Clean the text
    text = clean_text(text)

    # 2. Tokenization
    words = text.split()

    # 3. Remove stopwords
    words = [
        word for word in words
        if word not in stop_words
    ]

    # 4. Lemmatization
    words = [
        lemmatizer.lemmatize(word)
        for word in words
    ]

    # 5. Convert words back into text
    processed_text = " ".join(words)

    return processed_text