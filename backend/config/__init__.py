"""Configuration package for Physical AI Chatbot Backend."""

from .settings import (
    COHERE_API_KEY,
    QDRANT_URL,
    QDRANT_API_KEY,
    BASE_URL,
    COLLECTION_NAME,
    CHUNK_SIZE,
    OVERLAP_SIZE,
    BATCH_SIZE,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSIONS,
    LOG_LEVEL,
    LOG_FORMAT,
    validate_settings
)

# Create settings object for backward compatibility
class Settings:
    COHERE_API_KEY = COHERE_API_KEY
    QDRANT_URL = QDRANT_URL
    QDRANT_API_KEY = QDRANT_API_KEY
    BASE_URL = BASE_URL
    COLLECTION_NAME = COLLECTION_NAME
    CHUNK_SIZE = CHUNK_SIZE
    OVERLAP_SIZE = OVERLAP_SIZE
    BATCH_SIZE = BATCH_SIZE
    EMBEDDING_MODEL = EMBEDDING_MODEL
    EMBEDDING_DIMENSIONS = EMBEDDING_DIMENSIONS
    LOG_LEVEL = LOG_LEVEL
    LOG_FORMAT = LOG_FORMAT

    @staticmethod
    def validate_settings():
        """Validate that required environment variables are set."""
        return validate_settings()

settings = Settings()

__all__ = [
    'settings',
    'COHERE_API_KEY',
    'QDRANT_URL',
    'QDRANT_API_KEY',
    'BASE_URL',
    'COLLECTION_NAME',
    'CHUNK_SIZE',
    'OVERLAP_SIZE',
    'BATCH_SIZE',
    'EMBEDDING_MODEL',
    'EMBEDDING_DIMENSIONS',
    'LOG_LEVEL',
    'LOG_FORMAT',
    'validate_settings'
]
