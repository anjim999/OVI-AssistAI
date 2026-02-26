import { useState } from 'react';
import { PanelLeftOpen, PanelLeftClose, Eraser, Trash2 } from 'lucide-react';

const ChatHeader = ({ title, sidebarOpen, onToggleSidebar, onClearChat, onDeleteChat, hasMessages }) => {
    const [showModal, setShowModal] = useState(null); // 'clear' | 'delete' | null

    const handleConfirm = () => {
        if (showModal === 'clear') onClearChat();
        if (showModal === 'delete') onDeleteChat();
        setShowModal(null);
    };

    return (
        <>
            <header className="chat-header">
                <div className="chat-header-left">
                    <button
                        className="icon-btn"
                        onClick={onToggleSidebar}
                        title={sidebarOpen ? 'Close sidebar' : 'Open sidebar'}
                    >
                        {sidebarOpen ? <PanelLeftClose size={20} /> : <PanelLeftOpen size={20} />}
                    </button>
                    <span className="chat-header-title">
                        {title || 'New Conversation'}
                    </span>
                </div>

                <div className="chat-header-right">
                    {hasMessages && (
                        <>
                            <button
                                className="icon-btn"
                                onClick={() => setShowModal('clear')}
                                title="Clear chat"
                            >
                                <Eraser size={18} />
                            </button>
                            <button
                                className="icon-btn danger"
                                onClick={() => setShowModal('delete')}
                                title="Delete chat"
                            >
                                <Trash2 size={18} />
                            </button>
                        </>
                    )}
                </div>
            </header>

            {}
            {showModal && (
                <div className="modal-overlay" onClick={() => setShowModal(null)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <h3 className="modal-title">
                            {showModal === 'clear' ? 'Clear Chat?' : 'Delete Chat?'}
                        </h3>
                        <p className="modal-message">
                            {showModal === 'clear'
                                ? 'This will remove all messages but keep the session. This action cannot be undone.'
                                : 'This will permanently delete this conversation and all its messages. This action cannot be undone.'}
                        </p>
                        <div className="modal-actions">
                            <button className="modal-btn cancel" onClick={() => setShowModal(null)}>
                                Cancel
                            </button>
                            <button className="modal-btn confirm" onClick={handleConfirm}>
                                {showModal === 'clear' ? 'Clear' : 'Delete'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

export default ChatHeader;

