import { Bot, Plus, MessageSquare, Trash2, X } from 'lucide-react';
import { formatTime } from '../../utils/session';

const SessionSidebar = ({ sessions, currentSessionId, onNewChat, onSelectSession, onDeleteSession, onClose }) => {
    return (
        <aside className="sidebar">
            {}
            <div className="sidebar-header">
                <div className="sidebar-brand">
                    <div className="sidebar-brand-icon">
                        <Bot size={20} color="white" />
                    </div>
                    <h2>OVI AssistAI</h2>
                </div>
                <button className="icon-btn" onClick={onClose} title="Close sidebar" style={{ display: 'none' }}>
                    <X size={18} />
                </button>
            </div>

            {}
            <button className="new-chat-btn" onClick={onNewChat} id="new-chat-button">
                <Plus size={16} />
                New Chat
            </button>

            {}
            <div className="session-list">
                {sessions.length === 0 ? (
                    <div style={{
                        padding: '20px 12px',
                        textAlign: 'center',
                        color: 'var(--text-muted)',
                        fontSize: '13px',
                    }}>
                        No conversations yet
                    </div>
                ) : (
                    sessions.map((session) => (
                        <div
                            key={session.id}
                            className={`session-item ${session.id === currentSessionId ? 'active' : ''}`}
                            onClick={() => onSelectSession(session.id)}
                        >
                            <MessageSquare size={15} color="var(--text-muted)" style={{ flexShrink: 0 }} />
                            <div className="session-item-text">
                                <div className="session-item-title">
                                    {session.title || session.first_message || 'New Chat'}
                                </div>
                                <div className="session-item-date">
                                    {formatTime(session.updated_at)}
                                </div>
                            </div>
                            <button
                                className="session-delete-btn"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    onDeleteSession(session.id);
                                }}
                                title="Delete session"
                            >
                                <Trash2 size={14} />
                            </button>
                        </div>
                    ))
                )}
            </div>
        </aside>
    );
};

export default SessionSidebar;

