"""
PhishGuard Pro - Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from app.api import health, verdict, url_features, live, graph, policies, auth, audit, review, demo, model, render, sandbox
from app.core.config import settings
from app.core.logging import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    yield
    # Shutdown

# Create FastAPI app
app = FastAPI(
    title="PhishGuard Pro API",
    description="AI-Powered Phishing Detection & Response Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0", "testserver"]
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(verdict.router, prefix="/api", tags=["verdict"])
app.include_router(url_features.router, prefix="/api", tags=["url"])
app.include_router(live.router, prefix="/api", tags=["live"])
app.include_router(graph.router, prefix="/api", tags=["graph"])
app.include_router(policies.router, prefix="/api", tags=["policies"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(audit.router, prefix="/api", tags=["audit"])
app.include_router(review.router, prefix="/api", tags=["review"])
app.include_router(demo.router, prefix="/api", tags=["demo"])
app.include_router(model.router, prefix="/api", tags=["model"])
app.include_router(render.router, prefix="/api", tags=["render"])
app.include_router(sandbox.router, prefix="/api", tags=["sandbox"])

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )