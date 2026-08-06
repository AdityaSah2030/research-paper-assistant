from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.utils.config import GEMINI_API_KEY


def get_embedding_model():
    """
    Returns Gemini embedding model.
    """

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key=GEMINI_API_KEY
    )