from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.datasets import router as datasets_router
from app.api.ai import router as ai_router


app = FastAPI(
    title="InsightFlow AI API",
    description="Agentic RAG-Based Data Analytics Platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "InsightFlow AI backend is running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(datasets_router)
app.include_router(ai_router)