"""
FastAPI Backend for Physical AI Chatbot

This module provides a REST API that exposes the RAG-powered OpenAI Agent
to frontend applications. Implements POST /chat for queries, GET /health
for monitoring, and CORS support for cross-origin requests.

Feature: 009-fastapi-backend
"""

import os
import sys
import asyncio
import logging
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import agent functions from existing agent.py (Spec 008)
from agent import create_agent, run_query, initialize_clients

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# Pydantic Models
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str = Field(..., min_length=1, max_length=2000, description="User question")


class Source(BaseModel):
    """Source citation from curriculum."""
    title: str = Field(..., description="Page title from curriculum")
    url: str = Field(..., description="Full URL to source page")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str = Field(..., description="AI-generated response")
    sources: List[Source] = Field(default_factory=list, description="Source citations")


class DependencyStatus(BaseModel):
    """Status of individual dependency."""
    qdrant: str = Field(..., description="Qdrant connection status")
    cohere: str = Field(..., description="Cohere API status")
    openrouter: str = Field(..., description="OpenRouter API key status")


class HealthStatus(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Overall health status")
    dependencies: DependencyStatus = Field(..., description="Dependency statuses")


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Machine-readable error code")


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Physical AI Chatbot API",
    description="RAG-powered chatbot API for Physical AI & Humanoid Robotics curriculum",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",     # Docusaurus dev
    "http://localhost:5173",     # Vite dev
    "http://localhost:8080",     # Alternative dev
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

# Add production frontend URL from environment
frontend_url = os.getenv("FRONTEND_URL", "")
if frontend_url:
    ALLOWED_ORIGINS.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,
)


# ============================================================================
# Global State
# ============================================================================

_agent = None
_qdrant_client = None
_cohere_client = None


# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
async def startup():
    """Initialize agent and clients on startup."""
    global _agent, _qdrant_client, _cohere_client

    logger.info("Initializing API server...")

    try:
        # Initialize Qdrant and Cohere clients
        initialize_clients()
        logger.info("Clients initialized successfully")

        # Create agent
        _agent = create_agent()
        logger.info("Agent created successfully")

    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        # Don't raise - allow server to start but health will report degraded


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/", response_model=dict)
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Physical AI Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Health check endpoint for monitoring."""
    global _agent

    # Check dependencies
    qdrant_status = "disconnected"
    cohere_status = "disconnected"
    openrouter_status = "not_configured"

    try:
        # Check Qdrant
        from agent import _qdrant_client as qdrant
        if qdrant is not None:
            qdrant_status = "connected"
    except Exception:
        pass

    try:
        # Check Cohere
        from agent import _cohere_client as cohere
        if cohere is not None:
            cohere_status = "connected"
    except Exception:
        pass

    # Check OpenRouter API key
    if os.getenv("OPENROUTER_API_KEY"):
        openrouter_status = "configured"

    # Determine overall status
    if qdrant_status == "connected" and cohere_status == "connected" and openrouter_status == "configured":
        overall_status = "healthy"
    elif qdrant_status == "disconnected" or cohere_status == "disconnected":
        overall_status = "unhealthy"
    else:
        overall_status = "degraded"

    return HealthStatus(
        status=overall_status,
        dependencies=DependencyStatus(
            qdrant=qdrant_status,
            cohere=cohere_status,
            openrouter=openrouter_status
        )
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat query and return AI-generated response with sources.

    - **query**: User's question (1-2000 characters)

    Returns answer with source citations from the Physical AI curriculum.
    """
    global _agent

    # Validate query
    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail={"detail": "Query cannot be empty", "error_code": "EMPTY_QUERY"}
        )

    if len(query) > 2000:
        raise HTTPException(
            status_code=400,
            detail={"detail": "Query exceeds maximum length of 2000 characters", "error_code": "QUERY_TOO_LONG"}
        )

    logger.info(f"Processing chat request: '{query[:50]}...'")

    # Ensure agent is initialized
    if _agent is None:
        try:
            initialize_clients()
            _agent = create_agent()
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise HTTPException(
                status_code=503,
                detail={"detail": "Service temporarily unavailable", "error_code": "SERVICE_UNAVAILABLE"}
            )

    try:
        # Process query with timeout
        result = await asyncio.wait_for(
            run_query(_agent, query),
            timeout=30.0
        )

        if not result.get('success', False):
            error_msg = result.get('error', 'Unknown error')
            logger.error(f"Agent query failed: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail={"detail": "An error occurred processing your request", "error_code": "INTERNAL_ERROR"}
            )

        # Map response to ChatResponse
        sources = [
            Source(
                title=src.get('title', 'Unknown'),
                url=src.get('url', ''),
                score=src.get('score', 0.0)
            )
            for src in result.get('sources', [])
        ]

        logger.info(f"Chat response generated: {len(result.get('response', ''))} chars, {len(sources)} sources")

        return ChatResponse(
            answer=result.get('response', ''),
            sources=sources
        )

    except asyncio.TimeoutError:
        logger.error("Agent query timed out after 30 seconds")
        raise HTTPException(
            status_code=503,
            detail={"detail": "Request timed out. Please try again.", "error_code": "AGENT_TIMEOUT"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail={"detail": "An unexpected error occurred", "error_code": "INTERNAL_ERROR"}
        )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))

    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
