/**
 * Chat Service — all API calls to the FastAPI backend.
 */
import axiosClient from '../api/axiosClient';

const API_BASE = import.meta.env.VITE_API_R_URL;

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
    try {
        const res = await axiosClient.post('/api/chat', { sessionId, message });
        return res.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to send message');
    }
}

/** Get conversation messages for a session */
export async function getConversation(sessionId) {
    try {
        const res = await axiosClient.get(`/api/conversations/${sessionId}`);
        return res.data;
    } catch (error) {
        if (error.response?.status === 404) return { messages: [] };
        throw new Error('Failed to load conversation');
    }
}

/** Get all sessions */
export async function getSessions() {
    try {
        const res = await axiosClient.get('/api/sessions');
        return res.data;
    } catch (error) {
        throw new Error('Failed to load sessions');
    }
}

/** Delete a session */
export async function deleteSession(sessionId) {
    try {
        const res = await axiosClient.delete(`/api/sessions/${sessionId}`);
        return res.data;
    } catch (error) {
        throw new Error('Failed to delete session');
    }
}

/** Clear all messages from a session */
export async function clearConversation(sessionId) {
    try {
        const res = await axiosClient.delete(`/api/conversations/${sessionId}`);
        return res.data;
    } catch (error) {
        throw new Error('Failed to clear conversation');
    }
}
