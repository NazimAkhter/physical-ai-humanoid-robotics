"""
Main FastAPI application for the Physical AI & Humanoid Robotics educational platform.
Integrates all modules: RAG chatbot, VLA integration, and educational content management.
"""
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import API routers
from src.api.rag.routes import rag_router
from src.api.vla.routes import vla_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    logger.info("Starting Physical AI & Humanoid Robotics educational platform...")

    # Initialize services
    try:
        # Initialize database
        from src.services.database import init_database
        init_database()
        logger.info("Database initialized successfully")

        # Initialize Qdrant service
        from src.services.qdrant_service import qdrant_service
        logger.info("Qdrant service initialized successfully")

        # Initialize RAG service
        from src.services.rag_service import rag_service
        logger.info("RAG service initialized successfully")

    except Exception as e:
        logger.error(f"Error during application startup: {str(e)}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Physical AI & Humanoid Robotics educational platform...")

# Create FastAPI app with lifespan
app = FastAPI(
    title="Physical AI & Humanoid Robotics Educational Platform",
    description="An educational platform for learning about ROS 2, Digital Twins, Isaac AI, and Vision-Language-Action integration",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(rag_router, prefix="/api")
app.include_router(vla_router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint for the educational platform
    """
    return {
        "message": "Welcome to the Physical AI & Humanoid Robotics Educational Platform",
        "version": "0.1.0",
        "modules": [
            "RAG (Retrieval-Augmented Generation) Chatbot",
            "VLA (Vision-Language-Action) Integration",
            "ROS 2 Nervous System",
            "Digital Twin (Gazebo & Unity)",
            "Isaac AI Brain"
        ],
        "documentation": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for the entire platform
    """
    return {
        "status": "healthy",
        "service": "physical-ai-education-platform",
        "timestamp": "2025-12-07T10:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("RELOAD", "false").lower() == "true"
    )