"""
Centralized configuration — loads and validates environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration from environment variables."""

    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    CLIENT_URL: str = os.getenv("CLIENT_URL", "http://localhost:5173")
    ENV: str = os.getenv("ENV", "development")

    # Model settings
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    CHAT_MODEL: str = "gemini-2.5-flash"
    TEMPERATURE: float = 0.2
    MAX_OUTPUT_TOKENS: int = 1024

    # RAG settings
    SIMILARITY_THRESHOLD: float = 0.65
    TOP_K_CHUNKS: int = 3
    CHUNK_SIZE: int = 300       # words per chunk
    CHUNK_OVERLAP: int = 50     # overlap words

    # Context settings
    MAX_HISTORY_PAIRS: int = 5

    @classmethod
    def validate(cls):
        """Validate required config values exist."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "❌ GEMINI_API_KEY is required. "
                "Get one free at https://aistudio.google.com/apikey"
            )
        print(f"✅ Config loaded — ENV={cls.ENV}, MODEL={cls.CHAT_MODEL}")


config = Config()

