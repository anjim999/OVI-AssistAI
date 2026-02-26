"""
Chat API Routes — all HTTP endpoint definitions.
"""
import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, field_validator
from services.chat_service import chat_service

router = APIRouter()


# ─── Request / Response Models ────────────────────────────────────

class ChatRequest(BaseModel):
    sessionId: str
    message: str

    @field_validator("sessionId")
    @classmethod
    def validate_session_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Missing or invalid 'sessionId'. Must be a non-empty string.")
        return v.strip()

    @field_validator("message")
    @classmethod
    def validate_message(cls, v):
        if not v or not v.strip():
            raise ValueError("Missing or invalid 'message'. Must be a non-empty string.")
        if len(v.strip()) > 5000:
            raise ValueError("Message is too long. Maximum 5000 characters.")
        return v.strip()


# ─── POST /api/chat — Non-streaming ──────────────────────────────

@router.post("/chat")
async def send_message(body: ChatRequest):
    """Send a chat message and get AI response."""
    try:
        result = await chat_service.process_message(body.sessionId, body.message)
        return {
            "success": True,
            "reply": result["reply"],
            "tokensUsed": result["tokens_used"],
            "retrievedChunks": result["retrieved_chunks"],
            "docsUsed": result["docs_used"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── POST /api/chat/stream — Streaming SSE ───────────────────────

@router.post("/chat/stream")
async def send_message_stream(body: ChatRequest):
    """Send a chat message and get streaming AI response via SSE."""

    async def event_generator():
        try:
            async for event in chat_service.process_message_stream(
                body.sessionId, body.message
            ):
                yield f"data: {json.dumps(event)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            error_event = {"type": "error", "error": str(e)}
            yield f"data: {json.dumps(error_event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ─── GET /api/conversations/:sessionId — Get conversation ────────

@router.get("/conversations/{session_id}")
async def get_conversation(session_id: str):
    """Get all messages for a session."""
    result = chat_service.get_conversation(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "success": True,
        "sessionId": result["session"]["id"],
        "messages": result["messages"],
    }


# ─── GET /api/sessions — List all sessions ───────────────────────

@router.get("/sessions")
async def get_sessions():
    """Get all sessions."""
    sessions = chat_service.get_all_sessions()
    return {"success": True, "sessions": sessions}


# ─── DELETE /api/sessions/:sessionId — Delete session ─────────────

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and all its messages."""
    deleted = chat_service.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True, "message": "Session deleted successfully"}


# ─── DELETE /api/conversations/:sessionId — Clear conversation ────

@router.delete("/conversations/{session_id}")
async def clear_conversation(session_id: str):
    """Clear all messages from a session (keep the session)."""
    cleared = chat_service.clear_conversation(session_id)
    if not cleared:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True, "message": "Conversation cleared successfully"}

