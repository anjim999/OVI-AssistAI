# OVI-AssistAI

OVI-AssistAI is an intelligent, context-aware chatbot assistant application. It consists of a robust Python/FastAPI backend that handles natural language processing, vector similarity search, and conversation management, coupled with a responsive, modern React frontend built with Vite.

## 🚀 Features

*   **Intelligent Chat Interface**: A modern, responsive chat UI with message history, typing indicators, and seamless interactions.
*   **Vector Search & RAG**: Utilizes Retrieval-Augmented Generation (RAG) with local vector databases to provide context-aware responses based on ingested documents.
*   **Session Management**: Keeps track of multiple chat sessions, allowing users to switch between different conversational contexts.
*   **FastAPI Backend**: High-performance, asynchronous REST API powered by FastAPI.
*   **React + Vite Frontend**: Lightning-fast frontend development and optimized production builds.
*   **Docker Support**: Easily deployable with containerized environments using Docker and Docker Compose.

## 🛠️ Technology Stack

**Frontend:**
*   React
*   Vite
*   Tailwind CSS (or custom CSS for styling)
*   Lucide React (Icons)

**Backend:**
*   Python 3.9+
*   FastAPI
*   LangChain / LlamaIndex (for RAG/Vector operations)
*   SQLite / ChromaDB (for local vector storage)
*   Uvicorn

## 📦 Project Structure

```text
rest-agent/
├── backend/            # FastAPI application
│   ├── data/           # Stored documents and vector DB
│   ├── routes/         # API endpoint definitions
│   ├── services/       # Core business logic and LLM orchestration
│   ├── scripts/        # Data ingestion and utility scripts
│   ├── main.py         # Application entry point
│   ├── config.py       # Configuration management
│   └── requirements.txt# Python dependencies
├── frontend/           # React application
│   ├── src/            # Components, pages, and utilities
│   ├── package.json    # Node.js dependencies
│   ├── vite.config.js  # Vite configuration
│   └── vercel.json     # Vercel deployment configuration
├── docker-compose.yml  # Multi-container orchestration
└── .github/workflows/  # CI/CD pipelines
```

## 🚦 Getting Started

### Prerequisites
*   Node.js (v18+)
*   Python (v3.9+)
*   Docker (optional, for containerized setup)

### Local Development Setup

#### 1. Clone the repository
```bash
git clone https://github.com/anjim999/OVI-AssistAI.git
cd OVI-AssistAI
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Configure your environment variables
python main.py
```
*The backend API will be running on `http://localhost:8000`*

#### 3. Frontend Setup
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
*The frontend application will be running on `http://localhost:5173`*

### Docker Setup

To run the entire stack using Docker Compose:
```bash
docker-compose up --build
```

## 🚀 Deployment

*   **Frontend**: Ready to be deployed on Vercel. Push to the `main` branch or connect your repository to Vercel. The included `vercel.json` will handle the build and routing.
*   **Backend**: Can be deployed on Render, Heroku, or any virtual private server (VPS). Keep your environment variables secure.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.
