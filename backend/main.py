"""
FastAPI Application — main entry point.
Production-Grade RAG Assistant Backend.
"""
import google.generativeai as genai
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from config import config
from db.database import init_db, close_db
from services.rag_service import rag_service
from routes.chat import router as chat_router
from middleware.rate_limiter import limiter, rate_limit_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle events."""
    # ── Startup ──
    print("\n🚀 Starting RAG Assistant Backend...")
    config.validate()
    genai.configure(api_key=config.GEMINI_API_KEY)
    init_db()
    rag_service.load_vector_store()
    print("✅ Server ready!\n")

    yield

    # ── Shutdown ──
    close_db()
    print("👋 Server shut down gracefully")


# ─── Create App ───────────────────────────────────────────────────

app = FastAPI(
    title="OVI AssistAI API",
    description="Production-Grade GenAI Chat Assistant with Retrieval-Augmented Generation",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── Middleware ────────────────────────────────────────────────────

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.CLIENT_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ────────────────────────────────────────────────────────

app.include_router(chat_router, prefix="/api")


# ─── Health Check ──────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "success": True,
        "status": "healthy",
        "service": "OVI AssistAI API",
        "version": "1.0.0",
    }


# ─── Global Error Handler ─────────────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all error handler for unhandled exceptions."""
    print(f"❌ Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error. Please try again later.",
        },
    )


# ─── Run ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=(config.ENV == "development"),
    )
