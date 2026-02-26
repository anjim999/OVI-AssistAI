import { Sparkles } from 'lucide-react';

const TypingIndicator = () => {
    return (
        <div className="message-row assistant">
            <div className="message-avatar assistant-avatar">
                <Sparkles size={16} color="#8b5cf6" />
            </div>
            <div className="message-bubble assistant-bubble">
                <div className="typing-indicator">
                    <div className="typing-dot" />
                    <div className="typing-dot" />
                    <div className="typing-dot" />
                </div>
            </div>
        </div>
    );
};

export default TypingIndicator;
