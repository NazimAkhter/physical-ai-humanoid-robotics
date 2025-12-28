"""
Configuration settings for RAG Content Pipeline.

Loads environment variables using python-dotenv and provides
centralized access to configuration values.
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://physical-ai-humanoid-robotics-iota-nine.vercel.app")

# Pipeline Configuration
COLLECTION_NAME = "physical_ai_book"
CHUNK_SIZE = 512  # tokens
OVERLAP_SIZE = 50  # tokens
BATCH_SIZE = 90  # embeddings per batch (Cohere trial limit: 96, using 90 for safety)
EMBEDDING_MODEL = "embed-english-v3.0"
EMBEDDING_DIMENSIONS = 1024

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
    ]
)

def validate_settings():
    """Validate that required environment variables are set."""
    required_vars = {
        "COHERE_API_KEY": COHERE_API_KEY,
        "QDRANT_URL": QDRANT_URL,
        "QDRANT_API_KEY": QDRANT_API_KEY,
    }

    missing = [var for var, value in required_vars.items() if not value]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Please check your .env file."
        )

    return True
