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


def answer_question(article, question):
    """
    Answer a question using the provided news article
    as the context.
    """

    prompt = f"""
You are an AI news analysis assistant.

Answer the user's question using ONLY the information
provided in the article below.

If the article does not contain enough information to
answer the question, clearly say that the information
is not available in the article.

Do not invent facts.
Do not use outside information.

ARTICLE:
{article}

QUESTION:
{question}

Provide a clear and concise answer.
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

    answer = response.choices[0].message.content

    return answer