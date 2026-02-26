"""
Document Chunking Utility
Splits long documents into smaller chunks with word overlap 
to preserve context across chunk boundaries.
"""


def chunk_document(doc: dict, chunk_size: int = 300, overlap: int = 50) -> list[dict]:
    """
    Split a document into chunks of approximately `chunk_size` words,
    with `overlap` words shared between consecutive chunks.

    Args:
        doc: Document dict with 'id', 'title', 'content'
        chunk_size: Target words per chunk
        overlap: Number of overlapping words between chunks

    Returns:
        List of chunk dicts with metadata
    """
    words = doc["content"].split()
    total_words = len(words)

    # If document is short enough, return as single chunk
    if total_words <= chunk_size:
        return [{
            "id": f"doc_{doc['id']}_chunk_0",
            "doc_id": doc["id"],
            "title": doc["title"],
            "content": doc["content"],
            "chunk_index": 0,
            "total_chunks": 1,
            "word_count": total_words,
        }]

    chunks = []
    start = 0
    chunk_index = 0
    step = chunk_size - overlap  # How far to advance for each new chunk

    while start < total_words:
        end = min(start + chunk_size, total_words)
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunks.append({
            "id": f"doc_{doc['id']}_chunk_{chunk_index}",
            "doc_id": doc["id"],
            "title": doc["title"],
            "content": chunk_text,
            "chunk_index": chunk_index,
            "total_chunks": -1,  # Will be updated after loop
            "word_count": len(chunk_words),
        })

        chunk_index += 1
        start += step

        # Avoid creating tiny trailing chunks (< 30% of chunk_size)
        if start < total_words and (total_words - start) < (chunk_size * 0.3):
            # Extend previous chunk to include remaining words
            remaining = " ".join(words[start:])
            chunks[-1]["content"] += " " + remaining
            chunks[-1]["word_count"] += (total_words - start)
            break

    # Update total_chunks count
    for chunk in chunks:
        chunk["total_chunks"] = len(chunks)

    return chunks


def chunk_all_documents(documents: list[dict], chunk_size: int = 300, overlap: int = 50) -> list[dict]:
    """
    Chunk all documents in the knowledge base.

    Args:
        documents: List of document dicts
        chunk_size: Target words per chunk
        overlap: Overlap words between chunks

    Returns:
        List of all chunks across all documents
    """
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc, chunk_size, overlap)
        all_chunks.extend(chunks)

    print(f"📄 Chunked {len(documents)} documents into {len(all_chunks)} chunks")
    return all_chunks

