import { Toaster } from 'react-hot-toast';
import ChatPage from './pages/ChatPage';

const App = () => {
    return (
        <>
            <Toaster
                position="top-right"
                toastOptions={{
                    duration: 3000,
                    style: {
                        background: 'rgba(30, 30, 50, 0.95)',
                        color: '#e2e8f0',
                        border: '1px solid rgba(139, 92, 246, 0.3)',
                        backdropFilter: 'blur(12px)',
                        fontSize: '14px',
                        borderRadius: '12px',
                    },
                    success: { iconTheme: { primary: '#8b5cf6', secondary: '#fff' } },
                    error: { iconTheme: { primary: '#ef4444', secondary: '#fff' } },
                }}
            />
            <ChatPage />
        </>
    );
};

export default App;

