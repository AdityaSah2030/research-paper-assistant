from google import genai

from app.utils.config import GEMINI_API_KEY


def get_gemini_client():
    return genai.Client(
        api_key=GEMINI_API_KEY
    )


def generate_answer(
    question: str,
    context: str
):
    client = get_gemini_client()

    prompt = f"""
You are a research paper assistant.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text