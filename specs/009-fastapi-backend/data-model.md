# Data Model: FastAPI Backend Integration

**Feature**: 009-fastapi-backend
**Date**: 2025-12-27

## Entities

### ChatRequest

Represents an incoming chat query from the frontend.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| query | string | Yes | 1-2000 chars, non-empty | User's question to the chatbot |

**Validation Rules**:
- Query must not be empty or whitespace-only
- Query must not exceed 2000 characters
- Query must be valid UTF-8 string

---

### ChatResponse

Represents the API response returned to the frontend.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| answer | string | Yes | AI-generated response text |
| sources | array[Source] | Yes | Array of source references (may be empty) |

**Business Rules**:
- Answer is always present (even if error occurred in retrieval)
- Sources array is empty for greetings/off-topic questions
- Sources array contains 1-3 items for curriculum questions

---

### Source

Represents a curriculum source reference.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Page title from the curriculum |
| url | string | Yes | Full URL to the curriculum page |
| score | number | Yes | Relevance score (0.0 - 1.0) |

**Business Rules**:
- Score represents semantic similarity (higher = more relevant)
- Sources are sorted by score descending
- Only sources with score > 0.4 are included

---

### HealthStatus

Represents system health information.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | Yes | "healthy", "degraded", or "unhealthy" |
| dependencies | object | Yes | Status of each dependency |

**Dependencies Object**:
| Field | Type | Values | Description |
|-------|------|--------|-------------|
| qdrant | string | "connected" / "disconnected" | Qdrant vector DB status |
| cohere | string | "connected" / "disconnected" | Cohere embedding API status |
| openrouter | string | "configured" / "not_configured" | OpenRouter API key status |

**Status Logic**:
- "healthy": All dependencies connected/configured
- "degraded": Some non-critical dependencies unavailable
- "unhealthy": Critical dependencies unavailable

---

### ErrorResponse

Represents an error response.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| detail | string | Yes | Human-readable error message |
| error_code | string | No | Machine-readable error code |

**Error Codes**:
- `EMPTY_QUERY`: Query is empty or whitespace
- `QUERY_TOO_LONG`: Query exceeds 2000 characters
- `AGENT_TIMEOUT`: Agent processing exceeded timeout
- `SERVICE_UNAVAILABLE`: Backend service unavailable
- `INTERNAL_ERROR`: Unexpected server error

## State Management

The API is **stateless**:
- No session management required
- No conversation history stored
- Each request is independent
- Agent state is managed internally by agent.py
