"""
Chat Service — orchestrates session management, RAG retrieval, and LLM calls.
"""
import asyncio
from db import queries
from services.rag_service import rag_service
from services.llm_service import llm_service
from config import config


class ChatService:
    """Business logic orchestrator for the chat pipeline."""

    async def process_message(self, session_id: str, user_message: str) -> dict:
        """
        Process a chat message (non-streaming).

        Pipeline:
        1. Ensure session exists
        2. Store user message
        3. RAG similarity search
        4. Get conversation history
        5. Generate LLM response
        6. Store assistant response
        7. Generate session title (first message only)
        """
        # Session + store user message
        queries.create_session(session_id)
        queries.insert_message(session_id, "user", user_message)

        # RAG retrieval
        rag_result = await rag_service.search(user_message)

        # Conversation history
        history = queries.get_recent_message_pairs(session_id, config.MAX_HISTORY_PAIRS)

        # LLM generation
        llm_result = await llm_service.generate_response(
            user_message, rag_result["context"], history
        )

        # Store response
        queries.insert_message(session_id, "assistant", llm_result["reply"], llm_result["tokens_used"])

        # Generate title for first message
        title = None
        if not queries.has_title(session_id):
            title = await llm_service.generate_title(user_message, llm_result["reply"])
            queries.update_session_title(session_id, title)

        return {
            "reply": llm_result["reply"],
            "tokens_used": llm_result["tokens_used"],
            "docs_used": rag_result["docs_used"],
            "has_relevant_docs": rag_result["has_relevant_docs"],
            "retrieved_chunks": len(rag_result["docs_used"]),
            "title": title,
        }

    async def process_message_stream(self, session_id: str, user_message: str):
        """
        Process a chat message with streaming + live status updates.

        Yields SSE events:
        - status: Pipeline stage updates
        - chunk: Response text chunks
        - complete: Final metadata
        - error: Error information
        """
        # Stage 1: Initialize session
        yield {"type": "status", "stage": "session", "message": "Initializing session..."}
        queries.create_session(session_id)
        queries.insert_message(session_id, "user", user_message)

        # Stage 2: RAG search
        yield {"type": "status", "stage": "searching", "message": "🔍 Searching documentation..."}
        await asyncio.sleep(0.3)

        rag_result = await rag_service.search(user_message)

        if rag_result["has_relevant_docs"]:
            yield {
                "type": "status",
                "stage": "docs_found",
                "message": f"📄 Found {len(rag_result['docs_used'])} relevant document(s)",
            }
        else:
            yield {
                "type": "status",
                "stage": "docs_found",
                "message": "📄 No specific documentation match found",
            }

        # Stage 3: Context analysis
        yield {"type": "status", "stage": "analyzing", "message": "🧠 Analyzing conversation context..."}
        await asyncio.sleep(0.2)
        history = queries.get_recent_message_pairs(session_id, config.MAX_HISTORY_PAIRS)

        # Stage 4: Generate streaming response
        yield {"type": "status", "stage": "generating", "message": "✍️ Generating response..."}
        await asyncio.sleep(0.15)

        full_response = ""
        tokens_used = 0

        async for event in llm_service.generate_stream_response(
            user_message, rag_result["context"], history
        ):
            if event["type"] == "chunk":
                full_response += event["content"]
                yield {"type": "chunk", "content": event["content"]}
            elif event["type"] == "complete":
                tokens_used = event.get("tokens_used", 0)
            elif event["type"] == "error":
                yield {"type": "error", "error": event["error"]}
                return

        # Store response in DB
        queries.insert_message(session_id, "assistant", full_response, tokens_used)

        # Generate title (first message only)
        title = None
        if not queries.has_title(session_id):
            try:
                title = await llm_service.generate_title(user_message, full_response)
                queries.update_session_title(session_id, title)
            except Exception:
                pass  # Non-critical

        yield {
            "type": "complete",
            "tokens_used": tokens_used,
            "docs_used": rag_result["docs_used"],
            "has_relevant_docs": rag_result["has_relevant_docs"],
            "retrieved_chunks": len(rag_result["docs_used"]),
            "title": title,
        }

    def get_conversation(self, session_id: str) -> dict | None:
        """Get all messages for a session."""
        session = queries.get_session_by_id(session_id)
        if not session:
            return None
        messages = queries.get_messages_by_session(session_id)
        return {"session": session, "messages": messages}

    def get_all_sessions(self) -> list[dict]:
        """Get all sessions."""
        return queries.get_all_sessions()

    def delete_session(self, session_id: str) -> bool:
        """Delete a session and all its messages."""
        session = queries.get_session_by_id(session_id)
        if not session:
            return False
        queries.delete_session(session_id)
        return True

    def clear_conversation(self, session_id: str) -> bool:
        """Clear all messages from a session (keep the session)."""
        session = queries.get_session_by_id(session_id)
        if not session:
            return False
        queries.clear_messages(session_id)
        return True


# Singleton instance
chat_service = ChatService()
