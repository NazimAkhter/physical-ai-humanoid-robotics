# Implementation Plan: FastAPI Backend Integration

**Branch**: `009-fastapi-backend` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/009-fastapi-backend/spec.md`

## Summary

Build a FastAPI REST API that exposes the existing OpenAI Agent RAG functionality to frontend applications. The API provides a `/chat` endpoint that accepts user queries, processes them through the agent, and returns structured JSON responses with AI-generated answers and source citations. Includes CORS support for cross-origin frontend integration and health monitoring endpoint.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.104+, Uvicorn 0.24+, Pydantic (built-in with FastAPI)
**Storage**: N/A (stateless API, uses existing Qdrant via agent.py)
**Testing**: Manual curl/Postman testing (10+ requests per success criteria)
**Target Platform**: Local development server (localhost:8000)
**Project Type**: Web application (backend API only, frontend exists)
**Performance Goals**: <30s response time for 95% of queries (per SC-002)
**Constraints**: Single file implementation (backend/api.py)
**Scale/Scope**: MVP for local testing, connects to existing Docusaurus frontend

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Spec-Driven Development | PASS | Following Spec-Kit Plus workflow |
| Educational Efficacy | N/A | API layer, not content |
| Seamless Integration | PASS | Connects Docusaurus to RAG agent |
| Reproducibility | PASS | Single file, clear setup |
| Tooling Constraint | PASS | Using Claude Code |
| Curriculum Alignment | N/A | API layer, not content |

**Key Standards Check**:
- Chatbot Backend: FastAPI service ✓ (per constitution)
- Vector Search: Uses existing Qdrant via agent.py ✓

## Project Structure

### Documentation (this feature)

```text
specs/009-fastapi-backend/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── chat-api.md      # API contract
└── tasks.md             # Phase 2 output (via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── api.py               # NEW: FastAPI application (this feature)
├── agent.py             # EXISTING: OpenAI Agent RAG (Spec 008)
├── retrieve.py          # EXISTING: Qdrant retrieval (Spec 007)
├── config.py            # EXISTING: Configuration
├── pyproject.toml       # EXISTING: Dependencies (FastAPI already included)
└── .env                 # EXISTING: Environment variables

frontend/
├── src/
│   └── components/
│       └── Chatbot/     # EXISTING: Chatbot UI (Spec 005)
└── ...
```

**Structure Decision**: Single file addition (backend/api.py) integrating with existing backend modules.

## Complexity Tracking

No constitution violations. Implementation is minimal:
- Single new file (api.py)
- Imports existing agent.py functions
- Standard FastAPI patterns

## Phase 0: Research Summary

See [research.md](./research.md) for full details.

**Key Decisions**:
1. Import `run_query()`, `create_agent()`, `initialize_clients()` from agent.py
2. Use FastAPI CORSMiddleware with configurable origins
3. Pydantic models for request/response validation
4. HTTPException for structured error handling
5. Health endpoint checks Qdrant, Cohere, OpenRouter status

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](./data-model.md) for full entity definitions.

**Entities**:
- ChatRequest: `{ query: str }`
- ChatResponse: `{ answer: str, sources: List[Source] }`
- Source: `{ title: str, url: str, score: float }`
- HealthStatus: `{ status: str, dependencies: dict }`

### API Contract

See [contracts/chat-api.md](./contracts/chat-api.md) for full API specification.

**Endpoints**:
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat | Send query, receive AI response with sources |
| GET | /health | Check API and dependency health |
| GET | / | API info and docs link |

### Quickstart

See [quickstart.md](./quickstart.md) for setup and testing instructions.

## Implementation Approach

### api.py Structure

```python
# 1. Imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from agent import create_agent, run_query, initialize_clients

# 2. Pydantic Models
class ChatRequest(BaseModel): ...
class Source(BaseModel): ...
class ChatResponse(BaseModel): ...
class HealthStatus(BaseModel): ...

# 3. FastAPI App & CORS
app = FastAPI(title="Physical AI Chatbot API")
app.add_middleware(CORSMiddleware, ...)

# 4. Startup Event
@app.on_event("startup")
async def startup(): ...

# 5. Endpoints
@app.get("/")
@app.get("/health")
@app.post("/chat")

# 6. Main
if __name__ == "__main__":
    uvicorn.run(app, ...)
```

## Ready for Next Phase

Run `/sp.tasks` to generate implementation tasks.
