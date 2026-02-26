# 🤖 AI-Powered Support Assistant

A full-stack AI-powered support assistant built with React, Python/FastAPI, SQLite, and Google Gemini AI. The assistant answers user questions strictly based on product documentation using RAG (Retrieval-Augmented Generation) with TF-IDF similarity search, maintains session-wise conversation context, and provides real-time streaming responses with live status updates.

**Python FastAPI** | **React** | **SQLite** | **Gemini**

## ✨ Features

### Core Features
*   **💬 AI Chat Interface** — Beautiful chat UI with user/assistant message bubbles
*   **📄 Document-Grounded Answering** — AI only answers from docs.json, refuses unknown questions
*   **🔍 RAG with Vector Search** — Finds relevant docs instead of sending full knowledge base
*   **🧠 Conversation Memory** — Last 5 message pairs as context from SQLite
*   **📁 Session Management** — UUID-based sessions stored in localStorage
*   **💾 SQLite Persistence** — All messages and sessions stored in SQLite database

### Bonus Features
*   **⚡ Real-time Streaming** — Word-by-word responses via Server-Sent Events (SSE)
*   **🔄 Live Status Updates** — Shows "Searching docs..." → "Analyzing context..." → "Generating..." stages
*   **📝 Markdown Rendering** — AI responses rendered with proper formatting
*   **🐳 Docker Support** — Full Dockerfiles + docker-compose.yml
*   **🛡️ Rate Limiting** — Per-IP rate limiting on all endpoints

### UI Features
*   **🎨 Premium Glassmorphic Dark UI** — Stunning dark theme with glass effects
*   **✨ Smooth Animations** — Message entry animations, typing indicator, status pulses
*   **📱 Fully Responsive** — Works on desktop, tablet, and mobile
*   **💡 Suggestion Chips** — Pre-built questions for easy onboarding
*   **📋 Session Sidebar** — Browse, switch, and delete past conversations
*   **🆕 New Chat Button** — Start fresh conversations anytime

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 18, Vite, TailwindCSS v4, Lucide Icons, React Markdown, Framer Motion |
| **Backend** | Python, FastAPI |
| **Database** | SQLite (via ChromaDB/local vector store) |
| **AI/LLM** | Google Gemini 2.0 Flash / Langchain |
| **Containerization**| Docker + docker-compose |

## � Project Structure

```text
OVI-AssistAI/
├── frontend/                        # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   │   ├── ChatHeader.jsx      # Header with branding
│   │   │   │   ├── MessageList.jsx     # Renders all messages
│   │   │   │   ├── MessageItem.jsx     # Individual message bubble
│   │   │   │   ├── MessageInput.jsx    # Input + send button
│   │   │   │   ├── TypingIndicator.jsx # Animated typing dots
│   │   │   │   ├── StatusIndicator.jsx # Live status stages
│   │   │   │   └── SuggestionChips.jsx # Quick question suggestions
│   │   │   └── sidebar/
│   │   │       └── SessionSidebar.jsx  # Session list + controls
│   │   ├── pages/
│   │   │   └── ChatPage.jsx           # Main page (orchestrates everything)
│   │   ├── services/
│   │   │   └── chatService.js         # API calls (axios + fetch for SSE)
│   │   ├── utils/
│   │   │   └── session.js             # Session ID + timestamp utils
│   │   ├── App.jsx                    # Root component
│   │   ├── main.jsx                   # Entry point
│   │   └── index.css                  # Design system (Tailwind v4)
│   ├── Dockerfile
│   ├── package.json
│   └── vercel.json                    # Vercel rules
│
├── backend/                          # FastAPI Backend
│   ├── data/                           # Stored documents and vector DB
│   ├── routes/                         # API endpoint definitions
│   ├── services/                       # Core business logic and LLM orchestration
│   ├── scripts/                        # Data ingestion and utility scripts
│   ├── main.py                         # Application entry point
│   ├── config.py                       # Configuration management
│   ├── requirements.txt                # Python dependencies
│   └── Dockerfile
│
├── docker-compose.yml                # Container orchestration
└── README.md                         # This file
```

## � Quick Start

### Prerequisites
*   Node.js 20+ (check: `node --version`)
*   Python 3.9+ (check: `python --version`)
*   Google Gemini API key — Get free at `aistudio.google.com/apikey`

### 1. Clone & Install
```bash
# Clone the repository
git clone https://github.com/anjim999/OVI-AssistAI.git
cd OVI-AssistAI

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Configure Environment

**Backend environment**
```bash
cd backend
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

**Frontend environment**
```bash
cd frontend
cp .env.example .env
# Edit .env and add:
# VITE_API_R_URL=http://localhost:8000
```

### 3. Run Development Servers

```bash
# Terminal 1 — Backend (port 8000)
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend (port 5173)
cd frontend
npm run dev
```

### 4. Open Browser
Visit `http://localhost:5173`

## 🔑 API Documentation

Base URL: `http://localhost:8000/api`

### ✅ POST `/api/chat` — Send Message
Send a user message and receive an AI response.

**Request:**
```json
{
    "sessionId": "550e8400-e29b-41d4-a716-446655440000",
    "message": "How can I reset my password?"
}
```

### ✅ POST `/api/chat/stream` — Send Message (Streaming)
Same as `/api/chat` but returns Server-Sent Events with live status updates.

### ✅ GET `/api/conversations/:sessionId` — Get Conversation
Returns all messages for a session in chronological order.

### ✅ GET `/api/sessions` — List All Sessions

### ✅ DELETE `/api/sessions/:sessionId` — Delete Session
Deletes a session and all its messages.

### ✅ GET `/health` — Health Check

## 🐳 Docker Deployment
```bash
# Build and run both services
docker-compose up --build

# Frontend: http://localhost:80
# Backend:  http://localhost:8000
```

## 🚀 Deployment (Vercel + Render)

### Frontend → Vercel
1. Push your code to GitHub
2. Go to vercel.com → Import Project
3. Select the `frontend` folder as the root directory
4. Set Framework: Vite
5. Add Environment Variable:
   * `VITE_API_R_URL = https://ovi-assistai.onrender.com`
6. Deploy!

### Backend → Render
1. Go to render.com → New Web Service
2. Connect your GitHub repo
3. Configure:
   * Root Directory: `backend`
   * Build Command: `pip install -r requirements.txt`
   * Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   * Environment: Python
4. Add Environment Variables:
   * `GEMINI_API_KEY = your Gemini API key`
5. Deploy!

## 🌐 Live Demo

Built with ❤️ for the OVI Assist AI Assignment

**Frontend:** https://ovi-assist-ai.vercel.app/

**Backend:** https://ovi-assistai.onrender.com
