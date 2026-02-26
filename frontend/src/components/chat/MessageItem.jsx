import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Bot, User, Copy, Check } from 'lucide-react';
import { formatFullTime } from '../../utils/session';

const MessageItem = ({ message, isStreaming = false }) => {
    const [copied, setCopied] = useState(false);
    const isUser = message.role === 'user';

    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(message.content);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch {
            // Fallback
        }
    };

    return (
        <div className={`message-row ${isUser ? 'user' : 'assistant'}`}>
            {/* Avatar */}
            <div className={`message-avatar ${isUser ? 'user-avatar' : 'assistant-avatar'}`}>
                {isUser ? <User size={16} color="white" /> : <Bot size={16} color="#8b5cf6" />}
            </div>

            {/* Bubble */}
            <div>
                <div className={`message-bubble ${isUser ? 'user-bubble' : 'assistant-bubble'}`}>
                    {isUser ? (
                        <span>{message.content}</span>
                    ) : (
                        <>
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {message.content}
                            </ReactMarkdown>

                            {/* Copy button (assistant only) */}
                            {!isStreaming && (
                                <button className="copy-btn" onClick={handleCopy}>
                                    {copied ? <Check size={12} /> : <Copy size={12} />}
                                    {copied ? 'Copied' : 'Copy'}
                                </button>
                            )}
                        </>
                    )}
                </div>

                {/* Timestamp */}
                <div className="message-timestamp">
                    {formatFullTime(message.created_at)}
                    {isStreaming && ' • typing...'}
                </div>
            </div>
        </div>
    );
};

export default MessageItem;
