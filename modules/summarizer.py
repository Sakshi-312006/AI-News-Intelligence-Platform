import os

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Please add it to the .env file."
    )


# Create Groq client
client = Groq(api_key=api_key)


def summarize_article(text):
    """
    Generate a concise summary of a news article
    using the Llama model through Groq.
    """

    prompt = f"""
You are an AI news analyst.

Summarize the following news article in 3 to 5
clear and factual sentences.

Do not add information that is not present
in the article.

Focus on:
- What happened
- Who is involved
- Important actions or decisions
- Main outcome or significance

Article:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=300
    )

    summary = response.choices[0].message.content

    return summary