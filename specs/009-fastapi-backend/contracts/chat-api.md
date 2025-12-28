# API Contract: Chat Endpoint

**Feature**: 009-fastapi-backend
**Version**: 1.0.0
**Base URL**: http://localhost:8000

## Endpoints

### POST /chat

Send a query to the RAG-powered chatbot and receive an AI-generated response.

**Request**

```http
POST /chat HTTP/1.1
Content-Type: application/json

{
  "query": "What is ROS 2?"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| query | string | Yes | 1-2000 characters, non-empty |

**Response (200 OK)**

```json
{
  "answer": "ROS 2 (Robot Operating System 2) is a middleware framework for robotics...",
  "sources": [
    {
      "title": "Chapter 1: ROS 2 Architecture Overview",
      "url": "https://physical-ai-humanoid-robotics-iota-nine.vercel.app/docs/modules/ros2-nervous-system/architecture-overview",
      "score": 0.85
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| answer | string | AI-generated response text |
| sources | array | Array of source references (may be empty) |
| sources[].title | string | Page title from curriculum |
| sources[].url | string | Full URL to source page |
| sources[].score | number | Relevance score (0.0-1.0) |

**Error Responses**

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | EMPTY_QUERY | Query is empty or whitespace only |
| 400 | QUERY_TOO_LONG | Query exceeds 2000 characters |
| 422 | - | Missing required field (FastAPI validation) |
| 500 | INTERNAL_ERROR | Unexpected server error |
| 503 | SERVICE_UNAVAILABLE | Backend service unavailable |

**Error Response Format**

```json
{
  "detail": "Query cannot be empty",
  "error_code": "EMPTY_QUERY"
}
```

---

### GET /health

Check the health status of the API and its dependencies.

**Request**

```http
GET /health HTTP/1.1
```

**Response (200 OK)**

```json
{
  "status": "healthy",
  "dependencies": {
    "qdrant": "connected",
    "cohere": "connected",
    "openrouter": "configured"
  }
}
```

| Field | Type | Values |
|-------|------|--------|
| status | string | "healthy", "degraded", "unhealthy" |
| dependencies.qdrant | string | "connected", "disconnected" |
| dependencies.cohere | string | "connected", "disconnected" |
| dependencies.openrouter | string | "configured", "not_configured" |

---

### GET /

Root endpoint returning API information.

**Response (200 OK)**

```json
{
  "name": "Physical AI Chatbot API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

## CORS Configuration

**Allowed Origins**:
- `http://localhost:3000` (Docusaurus dev)
- `http://localhost:5173` (Vite dev)
- `http://localhost:8080` (Alternative dev)
- `${FRONTEND_URL}` (Production, from environment)

**Allowed Methods**: GET, POST, OPTIONS
**Allowed Headers**: Content-Type, Authorization
**Max Age**: 600 seconds

## Rate Limiting

No rate limiting implemented in MVP. Future consideration for production.

## Authentication

No authentication required for MVP. All endpoints are public.
