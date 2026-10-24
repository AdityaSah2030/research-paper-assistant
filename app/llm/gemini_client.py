from google import genai
from app.utils.config import GEMINI_API_KEY


def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(question: str, context: str):
    client = get_gemini_client()

    prompt = f"""
You are ResearchAI, a specialized Research Paper Assistant.

Answer questions ONLY using the provided research paper context.

RULES:
1. Do not use external knowledge, assumptions, or guesses.
2. If the answer is not present in the context, respond exactly:
The provided research paper does not contain enough information to answer this question.
3. If the question is unrelated to the uploaded research paper, respond exactly:
I am a research paper assistant. I can only answer questions related to the uploaded research paper and its contents.
4. Prefer concise but complete academic answers.
5. Use plain text. Do not use Markdown headings or bold formatting.
6. Cite factual claims using the source labels supplied in the context, in this format: [filename, p. X].
7. Only cite a page when the provided context supports the claim from that page. Never invent a filename, page number, quotation, or citation.
8. If sources from multiple papers are relevant, distinguish them by filename.
9. If the context does not support a claim, say that the provided research paper does not contain enough information.

RESEARCH PAPER CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    answer = response.text
    if not answer or not answer.strip():
        raise RuntimeError("Gemini returned an empty response.")

    return answer.strip()
