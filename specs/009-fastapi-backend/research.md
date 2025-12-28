# Research: FastAPI Backend Integration

**Feature**: 009-fastapi-backend
**Date**: 2025-12-27

## Technical Decisions

### 1. FastAPI Integration with Existing Agent

**Decision**: Import and use `run_query()` function from agent.py directly

**Rationale**:
- agent.py already provides a well-structured async `run_query(agent, query)` function
- Returns a standardized dict with `response`, `sources`, `tool_used`, `success`, `error`
- No need to re-implement agent logic in api.py

**Alternatives Considered**:
- Create new agent instance per request (rejected: unnecessary overhead)
- Duplicate agent code in api.py (rejected: violates DRY)

### 2. CORS Configuration

**Decision**: Use FastAPI CORSMiddleware with configurable origins

**Rationale**:
- Standard FastAPI pattern for CORS handling
- Allow localhost origins for development (3000, 5173, 8080)
- Allow production Vercel URL from environment variable

**Configuration**:
```python
origins = [
    "http://localhost:3000",      # Docusaurus dev
    "http://localhost:5173",      # Vite dev
    "http://localhost:8080",      # Alternative dev
    os.getenv("FRONTEND_URL", ""),  # Production URL
]
```

### 3. Response Model Structure

**Decision**: Use Pydantic models for request/response validation

**Rationale**:
- FastAPI's native approach for data validation
- Automatic OpenAPI documentation generation
- Type safety and clear contracts

**Models**:
- `ChatRequest`: `{ query: str }`
- `ChatResponse`: `{ answer: str, sources: List[Source] }`
- `Source`: `{ title: str, url: str, score: float }`

### 4. Error Handling Strategy

**Decision**: Use FastAPI HTTPException with structured error responses

**Rationale**:
- Consistent HTTP status codes (400, 422, 500, 503)
- JSON error format: `{ detail: str, error_code: str }`
- Hide internal errors from clients (500 returns generic message)

### 5. Health Check Implementation

**Decision**: Implement GET /health with dependency status checks

**Rationale**:
- Essential for monitoring and deployment validation
- Check Qdrant connection status
- Check Cohere client initialization
- Check OpenRouter API key configuration

### 6. Server Configuration

**Decision**: Use Uvicorn with configurable host/port

**Rationale**:
- Standard ASGI server for FastAPI
- Environment variable configuration (HOST, PORT)
- Default to 0.0.0.0:8000 for container compatibility

## Dependencies

All dependencies already exist in pyproject.toml from Spec 008:
- `fastapi>=0.104.0`
- `uvicorn>=0.24.0`
- `openai-agents>=0.0.7`
- `qdrant-client`
- `cohere`
- `python-dotenv`

## Integration Points

| Component | Integration Method |
|-----------|-------------------|
| agent.py | Import `create_agent()`, `run_query()`, `initialize_clients()` |
| Qdrant | Via agent.py (uses retrieve.py internally) |
| Cohere | Via agent.py (uses retrieve.py internally) |
| OpenRouter | Via agent.py (configured at module level) |
