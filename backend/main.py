"""Teaching Agent — FastAPI Application Entry Point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from backend.api.auth_routes import router as auth_router
from backend.api.chat_routes import router as chat_router
from backend.api.progress_routes import router as progress_router
from backend.admin.routes import router as admin_router
from backend.api.tutorial_routes import router as tutorial_router
from backend.auth.middleware import JWTAuthMiddleware

app = FastAPI(
    title="Teaching Agent API",
    description="Agentic AI Course Companion — Student Q&A with RAG + Guardrails",
    version="0.1.0",
)

# CORS — restrict to frontend domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server; override via env in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Authentication middleware
app.add_middleware(JWTAuthMiddleware)

# Routes
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(progress_router, prefix="/api/progress", tags=["progress"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(tutorial_router, prefix="/api/tutorial", tags=["tutorial"])


@app.get("/health")
async def health():
    """Health check — unauthenticated."""
    return {"status": "healthy", "service": "teaching-agent"}


# Lambda handler (via Mangum)
handler = Mangum(app, lifespan="off")
