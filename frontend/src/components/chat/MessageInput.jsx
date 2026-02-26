import { useState, useRef, useEffect } from 'react';
import { SendHorizontal } from 'lucide-react';

const MessageInput = ({ onSend, isLoading }) => {
    const [text, setText] = useState('');
    const textareaRef = useRef(null);

    // Auto-resize textarea
    useEffect(() => {
        const ta = textareaRef.current;
        if (ta) {
            ta.style.height = 'auto';
            ta.style.height = Math.min(ta.scrollHeight, 150) + 'px';
        }
    }, [text]);

    const handleSubmit = () => {
        const trimmed = text.trim();
        if (!trimmed || isLoading) return;
        onSend(trimmed);
        setText('');
        // Reset textarea height
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <div className="input-area">
            <div className="input-container">
                <div className="input-wrapper">
                    <textarea
                        ref={textareaRef}
                        className="message-input"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask a question about our platform..."
                        disabled={isLoading}
                        rows={1}
                        id="chat-message-input"
                    />
                </div>
                <button
                    className="send-btn"
                    onClick={handleSubmit}
                    disabled={!text.trim() || isLoading}
                    title="Send message"
                    id="chat-send-button"
                >
                    <SendHorizontal size={20} />
                </button>
            </div>
            <p className="input-hint">
                Press Enter to send • Shift+Enter for new line
            </p>
        </div>
    );
};

export default MessageInput;

