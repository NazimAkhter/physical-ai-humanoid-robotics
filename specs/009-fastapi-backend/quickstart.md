# Quickstart: FastAPI Backend Integration

**Feature**: 009-fastapi-backend
**Date**: 2025-12-27

## Prerequisites

1. **Python 3.11+** installed
2. **uv** package manager installed
3. **Environment variables** configured in `backend/.env`:
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   COHERE_API_KEY=...
   QDRANT_URL=...
   QDRANT_API_KEY=...
   ```

## Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies (already in pyproject.toml)
uv sync
```

## Running the Server

```bash
# Start the FastAPI server
cd backend
uv run python api.py

# Or using uvicorn directly
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Server will start at: http://localhost:8000

## Testing the API

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
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

### Chat Query
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

Expected response:
```json
{
  "answer": "ROS 2 (Robot Operating System 2) is...",
  "sources": [
    {
      "title": "Chapter 1: ROS 2 Architecture Overview",
      "url": "https://...",
      "score": 0.85
    }
  ]
}
```

### Interactive API Docs

Visit http://localhost:8000/docs for Swagger UI documentation.

## Connecting Frontend

Update the Docusaurus chatbot component to use the API:

```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: userMessage })
});
const data = await response.json();
// data.answer contains the response
// data.sources contains source references
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Ensure frontend URL is in allowed origins |
| 503 Service Unavailable | Check Qdrant/Cohere connectivity |
| Empty responses | Verify OPENROUTER_API_KEY is valid |
| Timeout errors | Increase timeout or check network |
