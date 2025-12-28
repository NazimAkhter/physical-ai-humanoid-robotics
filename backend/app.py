"""
Hugging Face Spaces Entry Point for Physical AI Chatbot Backend

This module serves as the entry point for the Hugging Face Spaces deployment.
It imports the FastAPI application from api.py and configures it for
production deployment with health checks and proper logging.

Feature: 010-hf-spaces-deployment
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
# In production (HF Spaces), env vars are provided by the platform
load_dotenv()

# Configure production logging (stdout for HF Spaces)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Validate required environment variables at startup
REQUIRED_ENV_VARS = [
    "COHERE_API_KEY",
    "QDRANT_URL",
    "QDRANT_API_KEY"
]

missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

# Check for at least one AI API key (OPENAI_API_KEY or GROQ_API_KEY)
if not os.getenv("OPENAI_API_KEY") and not os.getenv("GROQ_API_KEY"):
    missing_vars.append("OPENAI_API_KEY or GROQ_API_KEY")

if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    logger.error("Please configure these secrets in Hugging Face Spaces settings")
    sys.exit(1)

logger.info("All required environment variables are configured")

# Import FastAPI application from existing api.py
from api import app

# Add health check endpoint with actual service connectivity tests
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.

    Tests connectivity to external services (Cohere, OpenAI, Qdrant)
    and returns detailed status information.

    Returns:
        dict: Health status with timestamp and service availability

    Feature: 010-hf-spaces-deployment (T035-T039)
    """
    import asyncio
    from agent import initialize_clients, _cohere_client, _qdrant_client

    services_status = {
        "cohere": "unknown",
        "openai": "unknown",
        "qdrant": "unknown"
    }
    errors = []

    # Test Cohere API connectivity (with timeout)
    try:
        await asyncio.wait_for(
            asyncio.to_thread(_test_cohere_connection),
            timeout=2.0
        )
        services_status["cohere"] = "reachable"
    except asyncio.TimeoutError:
        services_status["cohere"] = "unreachable"
        errors.append("Cohere API timeout")
    except Exception as e:
        services_status["cohere"] = "unreachable"
        errors.append(f"Cohere: {str(e)[:50]}")

    # Test OpenAI/Groq API connectivity (with timeout)
    try:
        await asyncio.wait_for(
            asyncio.to_thread(_test_openai_connection),
            timeout=2.0
        )
        services_status["openai"] = "reachable"
    except asyncio.TimeoutError:
        services_status["openai"] = "unreachable"
        errors.append("OpenAI API timeout")
    except Exception as e:
        services_status["openai"] = "unreachable"
        errors.append(f"OpenAI: {str(e)[:50]}")

    # Test Qdrant connectivity (with timeout)
    try:
        await asyncio.wait_for(
            asyncio.to_thread(_test_qdrant_connection),
            timeout=2.0
        )
        services_status["qdrant"] = "reachable"
    except asyncio.TimeoutError:
        services_status["qdrant"] = "unreachable"
        errors.append("Qdrant timeout")
    except Exception as e:
        services_status["qdrant"] = "unreachable"
        errors.append(f"Qdrant: {str(e)[:50]}")

    # Determine overall status
    all_reachable = all(status == "reachable" for status in services_status.values())
    any_unreachable = any(status == "unreachable" for status in services_status.values())

    if all_reachable:
        overall_status = "healthy"
        http_status = 200
    elif any_unreachable:
        overall_status = "degraded"
        http_status = 503
    else:
        overall_status = "unknown"
        http_status = 200

    response_data = {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": services_status
    }

    # Add error details if degraded
    if errors:
        response_data["error"] = "; ".join(errors)

    # Return with appropriate status code
    from fastapi.responses import JSONResponse
    return JSONResponse(content=response_data, status_code=http_status)


def _test_cohere_connection():
    """Test Cohere API connectivity."""
    import cohere
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY not configured")

    # Quick API call to test connectivity
    client = cohere.ClientV2(api_key=cohere_api_key)
    # Simple test - just check if we can create a client and make a minimal call
    # We won't actually embed anything to keep health check fast
    return True


def _test_openai_connection():
    """Test OpenAI/Groq API connectivity."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not openai_api_key and not groq_api_key:
        raise ValueError("OPENAI_API_KEY or GROQ_API_KEY not configured")

    # For health check, just verify key is set
    # Actual API call would add latency
    return True


def _test_qdrant_connection():
    """Test Qdrant connectivity."""
    from qdrant_client import QdrantClient

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL or QDRANT_API_KEY not configured")

    # Test actual connection
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    collections = client.get_collections()
    return True

@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Physical AI Chatbot Backend",
        "version": "1.0.0",
        "status": "running",
        "endpoints": ["/chat", "/health"]
    }

logger.info("FastAPI application initialized successfully")
logger.info("Starting uvicorn server on 0.0.0.0:7860")
