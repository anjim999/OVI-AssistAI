"""
RAG Service — Embedding-based Retrieval-Augmented Generation.
Loads pre-computed embeddings from vector_store.json and performs
real cosine similarity search against user queries.
"""
import json
import os
import google.generativeai as genai
from config import config
from utils.vector_math import find_top_k_similar

# Path to vector store
VECTOR_STORE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "vector_store.json"
)


class RAGService:
    """Embedding-based RAG retrieval engine."""

    def __init__(self):
        self.chunks: list[dict] = []
        self._loaded = False

    def load_vector_store(self):
        """Load pre-computed embeddings from vector_store.json."""
        try:
            if not os.path.exists(VECTOR_STORE_PATH):
                print("⚠️  vector_store.json not found. Run 'python scripts/ingest.py' first.")
                return

            with open(VECTOR_STORE_PATH, "r") as f:
                self.chunks = json.load(f)

            self._loaded = True
            print(f"📚 RAG Service loaded {len(self.chunks)} chunks from vector store")
        except Exception as e:
            print(f"❌ Failed to load vector store: {e}")
            self.chunks = []

    async def get_query_embedding(self, query: str) -> list[float]:
        """
        Generate embedding vector for a user query using Gemini Embeddings API.
        """
        try:
            result = genai.embed_content(
                model=config.EMBEDDING_MODEL,
                content=query,
            )
            return result["embedding"]
        except Exception as e:
            print(f"❌ Embedding generation error: {e}")
            raise Exception("Failed to generate query embedding")

    async def search(self, query: str) -> dict:
        """
        Perform embedding-based similarity search.

        1. Convert user query to embedding vector
        2. Compare against all stored chunk embeddings using cosine similarity
        3. Return top-K chunks above threshold

        Args:
            query: User's question text

        Returns:
            Dict with context string, docs_used list, and has_relevant_docs flag
        """
        if not self._loaded or len(self.chunks) == 0:
            return {
                "context": "",
                "docs_used": [],
                "has_relevant_docs": False,
            }

        # Step 1: Get query embedding
        query_vector = await self.get_query_embedding(query)

        # Step 2: Find top-K similar chunks via cosine similarity
        top_chunks = find_top_k_similar(
            query_vector=query_vector,
            document_vectors=self.chunks,
            top_k=config.TOP_K_CHUNKS,
            threshold=config.SIMILARITY_THRESHOLD,
        )

        if not top_chunks:
            print(f"🔍 No chunks above threshold ({config.SIMILARITY_THRESHOLD}) for: {query[:60]}...")
            return {
                "context": "",
                "docs_used": [],
                "has_relevant_docs": False,
            }

        # Step 3: Build context from retrieved chunks
        context = "\n\n".join(
            f"[{chunk['title']}]: {chunk['content']}" for chunk in top_chunks
        )

        docs_used = [
            {"title": c["title"], "score": str(c["score"]), "chunk_id": c["id"]}
            for c in top_chunks
        ]

        # Log similarity scores
        print(f"🔍 Query: \"{query[:50]}...\"")
        for doc in docs_used:
            print(f"   📄 {doc['title']} — score: {doc['score']}")

        return {
            "context": context,
            "docs_used": docs_used,
            "has_relevant_docs": True,
        }


# Singleton instance
rag_service = RAGService()
