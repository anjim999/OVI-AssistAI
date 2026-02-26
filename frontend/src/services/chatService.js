/**
 * Chat Service — all API calls to the FastAPI backend.
 */

const API_BASE = import.meta.env.VITE_API_URL || '';

/** Send a chat message (streaming SSE) */
export async function sendMessageStream(sessionId, message) {
    const res = await fetch(`${API_BASE}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, message }),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Failed to send message');
    }

    return res;
}

/** Send a chat message (non-streaming) */
export async function sendMessage(sessionId, message) {
    const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, message }),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Failed to send message');
    }

    return res.json();
}

/** Get conversation messages for a session */
export async function getConversation(sessionId) {
    const res = await fetch(`${API_BASE}/api/conversations/${sessionId}`);
    if (!res.ok) {
        if (res.status === 404) return { messages: [] };
        throw new Error('Failed to load conversation');
    }
    return res.json();
}

/** Get all sessions */
export async function getSessions() {
    const res = await fetch(`${API_BASE}/api/sessions`);
    if (!res.ok) throw new Error('Failed to load sessions');
    return res.json();
}

/** Delete a session */
export async function deleteSession(sessionId) {
    const res = await fetch(`${API_BASE}/api/sessions/${sessionId}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete session');
    return res.json();
}

/** Clear all messages from a session */
export async function clearConversation(sessionId) {
    const res = await fetch(`${API_BASE}/api/conversations/${sessionId}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to clear conversation');
    return res.json();
}
