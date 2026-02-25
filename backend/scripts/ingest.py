"""
Ingestion Script — Pre-processes documents into embeddings.

This script:
1. Reads docs.json (raw knowledge base)
2. Chunks each document into ~300-word pieces with overlap
3. Generates embeddings for each chunk using Gemini Embeddings API
4. Saves everything to vector_store.json

Run: python scripts/ingest.py
"""
import json
import os
import sys
import time

# Add parent directory to path so we can import project modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

import google.generativeai as genai
from config import config
from utils.chunker import chunk_all_documents

# Configure Gemini
genai.configure(api_key=config.GEMINI_API_KEY)

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DOCS_PATH = os.path.join(DATA_DIR, "docs.json")
VECTOR_STORE_PATH = os.path.join(DATA_DIR, "vector_store.json")


def load_documents() -> list[dict]:
    """Load raw documents from docs.json."""
    with open(DOCS_PATH, "r") as f:
        docs = json.load(f)
    print(f"📄 Loaded {len(docs)} documents from docs.json")
    return docs


def generate_embedding(text: str) -> list[float]:
    """Generate embedding vector for a text using Gemini Embeddings API."""
    result = genai.embed_content(
        model=config.EMBEDDING_MODEL,
        content=text,
    )
    return result["embedding"]


def main():
    """Main ingestion pipeline."""
    print("=" * 60)
    print("🚀 RAG Ingestion Pipeline")
    print("=" * 60)

    # Validate API key
    config.validate()

    # Step 1: Load documents
    documents = load_documents()

    # Step 2: Chunk documents
    print(f"\n📐 Chunking documents (size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP})...")
    chunks = chunk_all_documents(documents, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

    # Step 3: Generate embeddings for each chunk
    print(f"\n🧠 Generating embeddings for {len(chunks)} chunks...")
    print(f"   Using model: {config.EMBEDDING_MODEL}")

    vector_store = []
    for i, chunk in enumerate(chunks):
        try:
            # Combine title + content for richer embeddings
            embed_text = f"{chunk['title']}: {chunk['content']}"
            embedding = generate_embedding(embed_text)

            vector_entry = {
                "id": chunk["id"],
                "doc_id": chunk["doc_id"],
                "title": chunk["title"],
                "content": chunk["content"],
                "chunk_index": chunk["chunk_index"],
                "total_chunks": chunk["total_chunks"],
                "word_count": chunk["word_count"],
                "embedding": embedding,
            }
            vector_store.append(vector_entry)

            print(f"   ✅ [{i + 1}/{len(chunks)}] {chunk['id']} — {chunk['word_count']} words — {len(embedding)}d vector")

            # Small delay to avoid API rate limits
            time.sleep(0.3)

        except Exception as e:
            print(f"   ❌ [{i + 1}/{len(chunks)}] Failed: {chunk['id']} — {e}")

    # Step 4: Save to vector_store.json
    print(f"\n💾 Saving {len(vector_store)} vectors to vector_store.json...")
    with open(VECTOR_STORE_PATH, "w") as f:
        json.dump(vector_store, f, indent=2)

    # Summary
    print("\n" + "=" * 60)
    print("✅ Ingestion Complete!")
    print(f"   📄 Documents:  {len(documents)}")
    print(f"   📐 Chunks:     {len(chunks)}")
    print(f"   🧠 Embeddings: {len(vector_store)}")
    print(f"   💾 Saved to:   {VECTOR_STORE_PATH}")
    embedding_dim = len(vector_store[0]["embedding"]) if vector_store else 0
    print(f"   📏 Dimensions: {embedding_dim}")
    print("=" * 60)


if __name__ == "__main__":
    main()
