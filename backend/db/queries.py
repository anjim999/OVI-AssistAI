"""
Database Query Functions — all SQL operations for sessions and messages.
"""
from db.database import get_db


# ─── Session Queries ──────────────────────────────────────────────

def create_session(session_id: str) -> None:
    """Create a new session if it doesn't exist."""
    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO sessions (id) VALUES (?)",
        (session_id,)
    )
    db.commit()


def get_session_by_id(session_id: str) -> dict | None:
    """Get a single session by ID."""
    db = get_db()
    row = db.execute(
        "SELECT id, title, created_at, updated_at FROM sessions WHERE id = ?",
        (session_id,)
    ).fetchone()
    return dict(row) if row else None


def get_all_sessions() -> list[dict]:
    """Get all sessions ordered by most recently updated."""
    db = get_db()
    rows = db.execute("""
        SELECT 
            s.id, s.title, s.created_at, s.updated_at,
            COUNT(m.id) as message_count,
            (SELECT content FROM messages WHERE session_id = s.id AND role = 'user' 
             ORDER BY created_at ASC LIMIT 1) as first_message
        FROM sessions s
        LEFT JOIN messages m ON m.session_id = s.id
        GROUP BY s.id
        ORDER BY s.updated_at DESC
    """).fetchall()
    return [dict(row) for row in rows]


def update_session_title(session_id: str, title: str) -> None:
    """Update session title."""
    db = get_db()
    db.execute(
        "UPDATE sessions SET title = ? WHERE id = ?",
        (title, session_id)
    )
    db.commit()


def has_title(session_id: str) -> bool:
    """Check if session already has a title."""
    db = get_db()
    row = db.execute(
        "SELECT title FROM sessions WHERE id = ?",
        (session_id,)
    ).fetchone()
    return row is not None and row["title"] is not None


def delete_session(session_id: str) -> None:
    """Delete a session and all its messages (CASCADE)."""
    db = get_db()
    db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    db.commit()


# ─── Message Queries ──────────────────────────────────────────────

def insert_message(session_id: str, role: str, content: str, tokens_used: int = 0) -> None:
    """Insert a new message and update session timestamp."""
    db = get_db()
    db.execute(
        "INSERT INTO messages (session_id, role, content, tokens_used) VALUES (?, ?, ?, ?)",
        (session_id, role, content, tokens_used)
    )
    db.execute(
        "UPDATE sessions SET updated_at = datetime('now') WHERE id = ?",
        (session_id,)
    )
    db.commit()


def get_messages_by_session(session_id: str) -> list[dict]:
    """Get all messages for a session in chronological order."""
    db = get_db()
    rows = db.execute(
        "SELECT id, session_id, role, content, tokens_used, created_at "
        "FROM messages WHERE session_id = ? ORDER BY created_at ASC",
        (session_id,)
    ).fetchall()
    return [dict(row) for row in rows]


def get_recent_message_pairs(session_id: str, limit: int = 5) -> list[dict]:
    """
    Get the last N message pairs (user + assistant) for context.
    Returns up to limit*2 messages (limit pairs).
    """
    db = get_db()
    rows = db.execute(
        "SELECT role, content FROM messages "
        "WHERE session_id = ? ORDER BY created_at DESC LIMIT ?",
        (session_id, limit * 2)
    ).fetchall()
    # Reverse to get chronological order
    return [dict(row) for row in reversed(rows)]


def clear_messages(session_id: str) -> None:
    """Clear all messages from a session (keep the session)."""
    db = get_db()
    db.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    db.execute(
        "UPDATE sessions SET title = NULL, updated_at = datetime('now') WHERE id = ?",
        (session_id,)
    )
    db.commit()

