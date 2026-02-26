import { useEffect, useRef } from 'react';
import MessageItem from './MessageItem';
import TypingIndicator from './TypingIndicator';
import StatusIndicator from './StatusIndicator';

const MessageList = ({ messages, isLoading, streamingMessage, statusStages }) => {
    const bottomRef = useRef(null);

    // Auto-scroll to bottom on new messages
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, streamingMessage, statusStages]);

    return (
        <div className="message-area">
            {messages.map((msg) => (
                <MessageItem key={msg.id} message={msg} />
            ))}

            {/* Status stages */}
            {statusStages.length > 0 && (
                <StatusIndicator stages={statusStages} />
            )}

            {/* Streaming message being received */}
            {streamingMessage && (
                <MessageItem
                    message={{
                        id: 'streaming',
                        role: 'assistant',
                        content: streamingMessage,
                        created_at: new Date().toISOString(),
                    }}
                    isStreaming
                />
            )}

            {/* Typing indicator */}
            {isLoading && !streamingMessage && statusStages.length === 0 && (
                <TypingIndicator />
            )}

            <div ref={bottomRef} />
        </div>
    );
};

export default MessageList;
