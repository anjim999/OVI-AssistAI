import { useState, useEffect, useCallback } from 'react';
import toast from 'react-hot-toast';
import { Bot, Sparkles } from 'lucide-react';

import ChatHeader from '../components/chat/ChatHeader';
import MessageList from '../components/chat/MessageList';
import MessageInput from '../components/chat/MessageInput';
import SuggestionChips from '../components/chat/SuggestionChips';
import SessionSidebar from '../components/sidebar/SessionSidebar';

import { getSessionId, createNewSession, setSessionId } from '../utils/session';
import {
    sendMessageStream,
    getConversation,
    getSessions,
    deleteSession,
    clearConversation,
} from '../services/chatService';

const ChatPage = () => {
    const [sessionId, setCurrentSessionId] = useState(getSessionId());
    const [messages, setMessages] = useState([]);
    const [sessions, setSessions] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [streamingMessage, setStreamingMessage] = useState('');
    const [statusStages, setStatusStages] = useState([]);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [chatTitle, setChatTitle] = useState('');

    // Load sessions on mount
    useEffect(() => {
        loadSessions();
        loadConversation(sessionId);
    }, []);

    const loadSessions = async () => {
        try {
            const data = await getSessions();
            setSessions(data.sessions || []);
        } catch {
            // No sessions yet
        }
    };

    const loadConversation = async (sid) => {
        try {
            const data = await getConversation(sid);
            setMessages(data.messages || []);
            const session = sessions.find((s) => s.id === sid);
            if (session?.title) {
                setChatTitle(session.title);
            } else if (data.messages?.length > 0) {
                setChatTitle(data.messages[0].content.substring(0, 40));
            }
        } catch {
            setMessages([]);
            setChatTitle('');
        }
    };

    // Send message with streaming
    const handleSend = useCallback(
        async (messageText) => {
            if (isLoading) return;

            const userMsg = {
                id: Date.now(),
                role: 'user',
                content: messageText,
                created_at: new Date().toISOString(),
            };
            setMessages((prev) => [...prev, userMsg]);
            setIsLoading(true);
            setStreamingMessage('');
            setStatusStages([]);

            try {
                const response = await sendMessageStream(sessionId, messageText);
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let fullMessage = '';

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\n');

                    for (const line of lines) {
                        if (!line.startsWith('data: ')) continue;
                        const rawData = line.slice(6);
                        if (rawData === '[DONE]') continue;

                        try {
                            const data = JSON.parse(rawData);

                            if (data.type === 'status') {
                                setStatusStages((prev) => [...prev, data]);
                            } else if (data.type === 'chunk') {
                                setStatusStages([]);
                                fullMessage += data.content;
                                setStreamingMessage(fullMessage);
                            } else if (data.type === 'complete') {
                                const assistantMsg = {
                                    id: Date.now() + 1,
                                    role: 'assistant',
                                    content: fullMessage,
                                    created_at: new Date().toISOString(),
                                };
                                setMessages((prev) => [...prev, assistantMsg]);
                                setStreamingMessage('');
                                setStatusStages([]);
                                if (data.title) setChatTitle(data.title);
                            } else if (data.type === 'error') {
                                toast.error(data.error || 'Failed to get response');
                            }
                        } catch {
                            // Skip invalid JSON
                        }
                    }
                }

                loadSessions();
            } catch (error) {
                toast.error(error.message || 'Failed to send message. Is the backend running?');
            } finally {
                setIsLoading(false);
                setStreamingMessage('');
                setStatusStages([]);
            }
        },
        [sessionId, isLoading]
    );

    // New chat
    const handleNewChat = useCallback(() => {
        const newId = createNewSession();
        setCurrentSessionId(newId);
        setMessages([]);
        setChatTitle('');
        setStreamingMessage('');
        setStatusStages([]);
        toast.success('New conversation started');
        loadSessions();
        if (window.innerWidth < 768) setSidebarOpen(false);
    }, []);

    // Select session
    const handleSelectSession = useCallback(async (sid) => {
        setSessionId(sid);
        setCurrentSessionId(sid);
        setStreamingMessage('');
        setStatusStages([]);
        await loadConversation(sid);
        if (window.innerWidth < 768) setSidebarOpen(false);
    }, []);

    // Delete session
    const handleDeleteSession = useCallback(
        async (sid) => {
            try {
                await deleteSession(sid);
                setSessions((prev) => prev.filter((s) => s.id !== sid));
                if (sid === sessionId) {
                    const newId = createNewSession();
                    setCurrentSessionId(newId);
                    setMessages([]);
                    setChatTitle('');
                }
                toast.success('Session deleted');
            } catch {
                toast.error('Failed to delete session');
            }
        },
        [sessionId]
    );

    // Suggestion click
    const handleSuggestion = useCallback(
        (text) => {
            handleSend(text);
        },
        [handleSend]
    );

    // Clear chat
    const handleClearChat = useCallback(async () => {
        try {
            await clearConversation(sessionId);
            setMessages([]);
            setChatTitle('');
            setStreamingMessage('');
            setStatusStages([]);
            toast.success('Chat cleared');
        } catch {
            toast.error('Failed to clear chat');
        }
    }, [sessionId]);

    // Delete chat
    const handleDeleteChat = useCallback(async () => {
        try {
            await deleteSession(sessionId);
            setSessions((prev) => prev.filter((s) => s.id !== sessionId));
            const newId = createNewSession();
            setCurrentSessionId(newId);
            setMessages([]);
            setChatTitle('');
            setStreamingMessage('');
            setStatusStages([]);
            toast.success('Chat deleted');
            loadSessions();
        } catch {
            toast.error('Failed to delete chat');
        }
    }, [sessionId]);

    return (
        <div style={{ height: '100vh', display: 'flex', overflow: 'hidden' }}>
            {}
            {sidebarOpen && (
                <>
                    <SessionSidebar
                        sessions={sessions}
                        currentSessionId={sessionId}
                        onNewChat={handleNewChat}
                        onSelectSession={handleSelectSession}
                        onDeleteSession={handleDeleteSession}
                        onClose={() => setSidebarOpen(false)}
                    />
                    <div
                        className="sidebar-overlay"
                        onClick={() => setSidebarOpen(false)}
                        style={{ display: 'none' }}
                    />
                </>
            )}

            {}
            <main
                style={{
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%',
                    minWidth: 0,
                    marginLeft: sidebarOpen ? '280px' : '0',
                    transition: 'margin-left 0.3s ease',
                }}
            >
                <ChatHeader
                    title={chatTitle}
                    sidebarOpen={sidebarOpen}
                    onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
                    onClearChat={handleClearChat}
                    onDeleteChat={handleDeleteChat}
                    hasMessages={messages.length > 0}
                />

                {}
                {messages.length === 0 && !isLoading ? (
                    <div className="empty-state">
                        <div className="empty-icon">
                            <Bot style={{ width: '40px', height: '40px', color: 'white' }} />
                        </div>
                        <h1 className="empty-title gradient-text">
                            How can I help you today?
                            <Sparkles style={{ width: '22px', height: '22px', color: '#818cf8' }} />
                        </h1>
                        <p className="empty-subtitle">
                            I&apos;m your AI support assistant powered by RAG. I answer questions
                            accurately using our knowledge base documentation.
                        </p>
                        <SuggestionChips onSelect={handleSuggestion} />
                    </div>
                ) : (
                    <MessageList
                        messages={messages}
                        isLoading={isLoading}
                        streamingMessage={streamingMessage}
                        statusStages={statusStages}
                    />
                )}

                <MessageInput onSend={handleSend} isLoading={isLoading} />
            </main>
        </div>
    );
};

export default ChatPage;

