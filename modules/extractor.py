from newspaper import Article
from bs4 import BeautifulSoup
import requests


def extract_with_newspaper(url):
    """
    Extract news article using Newspaper3k.
    """

    try:
        article = Article(url)

        article.download()
        article.parse()

        return {
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "publish_date": article.publish_date,
            "url": url
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def extract_with_beautifulsoup(url):
    """
    Fallback extraction using BeautifulSoup.
    """

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Extract title
        title = ""

        if soup.title:
            title = soup.title.get_text(strip=True)

        # Extract paragraphs
        paragraphs = soup.find_all("p")

        text = "\n".join(
            paragraph.get_text(strip=True)
            for paragraph in paragraphs
            if paragraph.get_text(strip=True)
        )

        return {
            "title": title,
            "text": text,
            "authors": [],
            "publish_date": None,
            "url": url
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def extract_article(url):
    """
    Main extraction function.

    Newspaper3k is tried first.
    BeautifulSoup is used as a fallback.
    """

    result = extract_with_newspaper(url)

    if (
        "error" not in result
        and result.get("text")
        and len(result["text"].strip()) > 50
    ):
        return result

    return extract_with_beautifulsoup(url)