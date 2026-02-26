"""
Vector Math Utility
Cosine similarity computation using NumPy for embedding-based retrieval.
"""
import numpy as np


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Cosine similarity = (A · B) / (||A|| * ||B||)

    Args:
        vec_a: First embedding vector
        vec_b: Second embedding vector

    Returns:
        Similarity score between -1 and 1 (higher = more similar)
    """
    a = np.array(vec_a, dtype=np.float64)
    b = np.array(vec_b, dtype=np.float64)

    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    # Avoid division by zero
    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def find_top_k_similar(
    query_vector: list[float],
    document_vectors: list[dict],
    top_k: int = 3,
    threshold: float = 0.65,
) -> list[dict]:
    """
    Find the top-K most similar document chunks to the query.

    Args:
        query_vector: Embedding vector of the user query
        document_vectors: List of dicts with 'embedding' and chunk metadata
        top_k: Number of top results to return
        threshold: Minimum similarity score to include

    Returns:
        List of matching chunks with their similarity scores, sorted by score
    """
    scored = []

    for doc in document_vectors:
        score = cosine_similarity(query_vector, doc["embedding"])
        scored.append({
            "id": doc["id"],
            "doc_id": doc["doc_id"],
            "title": doc["title"],
            "content": doc["content"],
            "chunk_index": doc["chunk_index"],
            "score": round(score, 4),
        })

    # Filter by threshold, sort descending, take top K
    relevant = [s for s in scored if s["score"] >= threshold]
    relevant.sort(key=lambda x: x["score"], reverse=True)

    return relevant[:top_k]

