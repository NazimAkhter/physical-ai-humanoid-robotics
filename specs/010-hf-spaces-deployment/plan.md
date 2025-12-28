# Implementation Plan: Hugging Face Spaces Production Deployment

**Branch**: `010-hf-spaces-deployment` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/010-hf-spaces-deployment/spec.md`

## Summary

Deploy the existing FastAPI RAG chatbot backend (009-fastapi-backend) to Hugging Face Spaces using Docker SDK. The deployment will make the backend publicly accessible to the Vercel-hosted frontend, with production-grade error handling, logging, health checks, and CORS configuration. The primary technical challenge is adapting the existing `backend/` codebase for Hugging Face Spaces' Docker environment (UID 1000, port 7860, stdout logging) while implementing robust error handling for external service failures (Cohere, OpenAI, Qdrant).

## Technical Context

**Language/Version**: Python 3.11+ (existing backend), Python 3.10+ (Hugging Face Spaces Docker requirement)
**Primary Dependencies**: FastAPI 0.104+, Uvicorn 0.24+, OpenAI SDK (openai-agents 0.0.7), Cohere 5.0+, Qdrant-client 1.7+, Python-dotenv 1.0+
**Storage**: N/A (stateless API - uses external Qdrant Cloud for vector storage, in-memory for conversation sessions)
**Testing**: pytest 7.4+ (existing), manual endpoint testing, CORS verification from Vercel frontend
**Target Platform**: Hugging Face Spaces (Docker SDK), free tier (cpu-basic: 2 vCPU, 16GB RAM, 50GB disk, 48-hour sleep mode)
**Project Type**: Web application (existing `backend/` directory with FastAPI application)
**Performance Goals**: Health check < 2s response time, API requests < 5s error detection, startup < 60s
**Constraints**: Port 7860 (HF Spaces standard), user UID 1000 (Docker requirement), stdout logging only, 48-hour inactivity sleep mode on free tier
**Scale/Scope**: MVP deployment for single backend service, ~5-10 API endpoints, designed for cold start tolerance

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Code Quality ✅ PASS
- **Spec-Driven Development**: Following Spec-Kit Plus workflow (spec → plan → tasks → implementation)
- **Reproducibility**: All configuration files (README.md, Dockerfile, requirements.txt) are version-controlled and deterministic
- **Educational Efficacy**: N/A (infrastructure deployment, not educational content)

### Integration & Coupling ✅ PASS
- **Seamless Integration**: Deployment enables frontend-backend integration via public API endpoint
- **Tight Coupling**: Frontend (Vercel) couples to backend (HF Spaces) via CORS-configured REST API

### Tooling & Standards ✅ PASS
- **Claude Code**: Using Claude Code for specification, planning, and implementation
- **Spec-Kit Plus**: Following /sp.plan workflow for planning phase
- **FastAPI**: Already using FastAPI as specified in constitution (Chatbot Backend standard)

### Data Persistence ✅ PASS
- **Qdrant Cloud**: Already using Qdrant Cloud Free Tier for vector search (per constitution)
- **Neon Postgres**: Not used for this feature (deployment only, no persistence changes)
- **Stateless API**: Session management is in-memory (no database changes required)

### Content & Curriculum ⚠️ NOT APPLICABLE
- This is an infrastructure/deployment feature, not educational content
- Does not modify or add to the 4-module curriculum structure
- Does not affect book content on GitHub Pages

### Deployment ✅ PASS
- **GitHub Pages**: Book remains on GitHub Pages (no changes)
- **Backend Hosting**: Deploying to Hugging Face Spaces (production hosting for backend)

**Gate Status**: ✅ PASS - All applicable constitution principles satisfied. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/010-hf-spaces-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: HF Spaces deployment research
├── data-model.md        # Phase 1 output: N/A (no new domain entities)
├── quickstart.md        # Phase 1 output: Deployment instructions
├── contracts/           # Phase 1 output: OpenAPI schema for health check endpoint
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/                          # Existing backend directory (009-fastapi-backend)
├── agent.py                      # Existing: OpenAI Agent + RAG implementation
├── api.py                        # Existing: FastAPI application with /chat endpoint
├── main.py                       # Existing: Entry point (imports, unused for HF Spaces)
├── pyproject.toml                # Existing: uv dependency management
├── uv.lock                       # Existing: locked dependencies
├── .env.example                  # Existing: environment variable template
├── README.md                     # MODIFIED: Add HF Spaces YAML frontmatter
├── Dockerfile                    # NEW: Docker configuration for HF Spaces
├── requirements.txt              # NEW: pip requirements (generated from pyproject.toml)
├── app.py                        # NEW: HF Spaces entry point (imports/runs FastAPI from api.py)
├── .dockerignore                 # NEW: Exclude .venv, __pycache__, .env from build
└── deployment.md                 # NEW: Deployment instructions and secrets documentation

backend/config/                   # Existing configuration (if applicable)
└── logging.py                    # NEW: Production logging configuration

history/prompts/010-hf-spaces-deployment/  # This feature's prompt history
└── [PHR files]
```

**Structure Decision**:
- **Extend existing `backend/` directory** with Hugging Face Spaces deployment files
- **No restructuring** of existing code (api.py, agent.py remain unchanged except for error handling enhancements)
- **New entry point** (`app.py`) created for Hugging Face Spaces compatibility (replaces `main.py` usage)
- **Docker-specific files** (Dockerfile, .dockerignore) added to backend root
- **Requirements.txt** generated from existing pyproject.toml for Docker build compatibility

## Complexity Tracking

> **No constitution violations detected - this section is not applicable**

## Phase 0: Research Findings

### Research Summary

Comprehensive research completed on Hugging Face Spaces deployment requirements for FastAPI applications. Key findings documented in research.md include:

1. **README.md YAML Frontmatter**: Required fields (title, emoji, colorFrom, colorTo, sdk: docker, app_port: 7860)
2. **Port Configuration**: Standard port 7860 with uvicorn binding to 0.0.0.0:7860
3. **Docker SDK Requirements**: User UID 1000, --chown=user for all COPY operations, non-root execution
4. **Environment Secrets**: Accessed via os.getenv() at runtime, configured in Space Settings
5. **Logging**: stdout/stderr automatically captured in Container logs
6. **Free Tier Behavior**: 48-hour inactivity sleep, 10-60s cold start time
7. **CORS Configuration**: Explicit allow_origins required for Vercel frontend access

### Technology Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| **Docker SDK** | Required for FastAPI deployment on HF Spaces | Gradio SDK (not compatible with FastAPI) |
| **Python 3.10 base image** | Balance of compatibility and stability for HF Spaces | Python 3.11 (newer but less tested on HF), Python 3.9 (older) |
| **Port 7860** | HF Spaces standard, widely documented | Custom port (not supported on free tier) |
| **requirements.txt** | Docker build compatibility (standard pip) | pyproject.toml only (not standard in Docker ecosystem) |
| **app.py entry point** | Clear HF Spaces convention | Reuse main.py (confusing for multi-entry-point scenarios) |
| **Explicit CORS origins** | Security best practice (whitelist known frontend) | Wildcard CORS (less secure, allows any origin) |
| **Structured logging to stdout** | HF Spaces best practice (captured automatically) | File logging (lost on restart, not visible in Container logs) |
| **Health check endpoint** | Standard production monitoring practice | No health check (harder to debug deployment issues) |

### Integration Points

1. **Existing FastAPI Application** (backend/api.py):
   - Import and mount in app.py
   - Add health check endpoint
   - Enhance error handling for external services

2. **External Services** (Cohere, OpenAI, Qdrant):
   - Wrap API calls with try-except for timeout/rate limit handling
   - Return user-friendly error messages (HTTP 503/429)
   - Log errors with sufficient detail for debugging

3. **Vercel Frontend** (https://physical-ai-humanoid-robotics-iota-nine.vercel.app):
   - Configure CORS allow_origins
   - Support preflight OPTIONS requests
   - Enable credentials if needed for future auth

4. **Hugging Face Spaces Platform**:
   - Read environment variables for API keys
   - Log to stdout for visibility
   - Handle 48-hour sleep/wake cycle gracefully

## Phase 1: Design & Contracts

### Data Model

**N/A** - This is an infrastructure/deployment feature. No new domain entities are introduced. The existing data model from previous features (008-openai-agent-rag: RAGAgent, ConversationSession; 006-rag-pipeline: EmbeddedChunk) remains unchanged.

### API Contracts

#### Existing Endpoints (from 009-fastapi-backend)

**POST /chat** - Send chat query to RAG agent
```json
Request:
{
  "query": "string (1-2000 chars)"
}

Response (200 OK):
{
  "answer": "string",
  "sources": [
    {
      "title": "string",
      "url": "string",
      "score": 0.0-1.0
    }
  ],
  "session_id": "string"
}

Error Responses:
- 400 Bad Request: Invalid query (empty, too long)
- 503 Service Unavailable: External service failure (Cohere, OpenAI, Qdrant)
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Unexpected error
```

#### New Endpoint (for deployment feature)

**GET /health** - Health check endpoint for monitoring
```json
Response (200 OK):
{
  "status": "healthy",
  "timestamp": "2025-12-28T10:30:00Z",
  "services": {
    "cohere": "reachable",
    "openai": "reachable",
    "qdrant": "reachable"
  }
}

Response (503 Service Unavailable):
{
  "status": "degraded",
  "timestamp": "2025-12-28T10:30:00Z",
  "services": {
    "cohere": "unreachable",
    "openai": "reachable",
    "qdrant": "reachable"
  },
  "error": "Cohere API connection failed"
}
```

**GET /** - Root endpoint (redirect or info)
```json
Response (200 OK):
{
  "service": "Physical AI Chatbot Backend",
  "version": "1.0.0",
  "status": "running",
  "endpoints": ["/chat", "/health"]
}
```

### Error Handling Strategy

#### External Service Error Mapping

| Service | Error Type | HTTP Status | User Message | Log Detail |
|---------|-----------|-------------|--------------|------------|
| Cohere | Timeout | 503 | "Embedding service temporarily unavailable, please try again" | Full exception stack trace |
| Cohere | Rate Limit | 429 | "Service is experiencing high demand, please try again in a moment" | Rate limit details |
| Cohere | Auth Failure | 503 | "Configuration error, please contact support" | API key validation error |
| OpenAI | Timeout | 503 | "AI service temporarily unavailable, please try again" | Full exception stack trace |
| OpenAI | Rate Limit | 429 | "Service is experiencing high demand, please try again in a moment" | Rate limit details |
| OpenAI | Auth Failure | 503 | "Configuration error, please contact support" | API key validation error |
| Qdrant | Connection | 503 | "Vector database temporarily unavailable, please try again" | Connection error details |
| Qdrant | Timeout | 503 | "Vector database temporarily unavailable, please try again" | Timeout duration |
| Qdrant | Auth Failure | 503 | "Configuration error, please contact support" | Auth error details |
| Internal | Unexpected | 500 | "An unexpected error occurred, please contact support" | Full stack trace (sanitized) |

#### Error Handling Implementation Pattern

```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def safe_api_call(service_name: str, api_function, *args, **kwargs):
    """Wrapper for external API calls with error handling."""
    try:
        return await api_function(*args, **kwargs)
    except TimeoutError as e:
        logger.error(f"{service_name} timeout: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail=f"{service_name} temporarily unavailable, please try again"
        )
    except RateLimitError as e:
        logger.warning(f"{service_name} rate limit: {str(e)}")
        raise HTTPException(
            status_code=429,
            detail="Service is experiencing high demand, please try again in a moment"
        )
    except AuthenticationError as e:
        logger.error(f"{service_name} auth failure: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail="Configuration error, please contact support"
        )
    except Exception as e:
        logger.error(f"{service_name} unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred, please contact support"
        )
```

### Deployment Configuration

#### README.md Frontmatter (YAML)

```yaml
---
title: Physical AI Chatbot Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Physical AI Chatbot Backend

Production FastAPI backend for the Physical AI & Humanoid Robotics curriculum RAG chatbot.

## Features
- RAG-powered Q&A using Qdrant vector search
- OpenAI Agents for intelligent responses
- Real-time streaming responses
- Production logging and error handling
- Health check monitoring

## Documentation
See [deployment.md](./deployment.md) for setup instructions.
```

#### Dockerfile

```dockerfile
# Use Python 3.10 for compatibility with HF Spaces
FROM python:3.10

# Create non-root user with UID 1000 (required by HF Spaces)
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies (as root, with proper ownership)
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code (with proper ownership)
COPY --chown=user:user . .

# Switch to non-root user
USER user

# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Expose port 7860 (documentation only)
EXPOSE 7860

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

#### .dockerignore

```text
# Virtual environments
.venv/
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Environment files (secrets should be in HF Spaces settings)
.env
.env.local

# Development files
.git/
.gitignore
*.md
!README.md
!deployment.md

# Testing
tests/
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log

# Build artifacts
dist/
build/
*.egg-info/

# OS files
.DS_Store
Thumbs.db

# UV lock file (use requirements.txt in Docker)
uv.lock
pyproject.toml
```

#### requirements.txt Generation

Convert from pyproject.toml to requirements.txt for Docker build:

```bash
# Generate requirements.txt from pyproject.toml
pip install uv
uv pip compile pyproject.toml -o requirements.txt
```

Or manually create from dependencies:

```text
fastapi>=0.104.0
uvicorn>=0.24.0
openai-agents>=0.0.7
cohere>=5.0.0
qdrant-client>=1.7.0
tiktoken>=0.5.0
python-dotenv>=1.0.0
beautifulsoup4>=4.12.0
requests>=2.31.0
lxml>=6.0.2
```

#### app.py Entry Point

```python
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
    "OPENAI_API_KEY",
    "QDRANT_URL",
    "QDRANT_API_KEY"
]

missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    logger.error("Please configure these secrets in Hugging Face Spaces settings")
    sys.exit(1)

logger.info("All required environment variables are configured")

# Import FastAPI application from existing api.py
from api import app

# Add health check endpoint (if not already in api.py)
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        dict: Health status with timestamp and service availability
    """
    # TODO: In tasks phase, implement actual service health checks
    # For now, return basic health status
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": {
            "cohere": "unknown",
            "openai": "unknown",
            "qdrant": "unknown"
        }
    }

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
```

#### deployment.md

```markdown
# Deployment Instructions: Hugging Face Spaces

This document provides instructions for deploying the Physical AI Chatbot Backend to Hugging Face Spaces.

## Prerequisites

- Hugging Face account with Spaces access
- API keys for:
  - Cohere (embeddings)
  - OpenAI (GPT-4)
  - Qdrant Cloud (vector database)

## Required Secrets

Configure these in **Space Settings → Variables and secrets**:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `COHERE_API_KEY` | Cohere API key for embeddings | `co_xxxxxxxxxxxxx` |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | `sk-xxxxxxxxxxxxx` |
| `QDRANT_URL` | Qdrant Cloud cluster URL | `https://xxxxx.qdrant.io` |
| `QDRANT_API_KEY` | Qdrant API key | `xxxxxxxxxxxxx` |

### Setting Secrets

1. Navigate to your Space: `https://huggingface.co/spaces/USERNAME/SPACE_NAME/settings`
2. Scroll to **Variables and secrets** section
3. Click **New secret**
4. Enter **Name** and **Value**
5. Click **Save**
6. Repeat for all required secrets

## Local Testing

Test the Docker build locally before deploying:

```bash
# Generate requirements.txt from pyproject.toml
uv pip compile pyproject.toml -o requirements.txt

# Build Docker image
docker build -t physical-ai-backend .

# Run container (with environment variables)
docker run -p 7860:7860 \
  -e COHERE_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  -e QDRANT_URL=your_url \
  -e QDRANT_API_KEY=your_key \
  physical-ai-backend

# Test health endpoint
curl http://localhost:7860/health

# Test chat endpoint
curl -X POST http://localhost:7860/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

## Deployment Steps

### 1. Create Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Enter Space name: `physical-ai-chatbot-backend`
3. Select **Docker** SDK
4. Choose **Public** or **Private** visibility
5. Click **Create Space**

### 2. Push Code to Space

```bash
# Clone the Space repository
git clone https://huggingface.co/spaces/USERNAME/physical-ai-chatbot-backend
cd physical-ai-chatbot-backend

# Copy backend files
cp -r /path/to/physical_ai_book/backend/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### 3. Configure Secrets

Follow the steps in **Required Secrets** section above.

### 4. Monitor Build

1. Go to your Space page
2. Click **Open Logs** button
3. Monitor **Build** tab for Docker build progress
4. Monitor **Container** tab for application logs

### 5. Verify Deployment

Once the Space shows **Running** status:

```bash
# Test health endpoint
curl https://USERNAME-physical-ai-chatbot-backend.hf.space/health

# Test chat endpoint from frontend origin
# (Should work without CORS errors)
```

## Troubleshooting

### Space shows "Runtime error"

**Check Container logs:**
1. Click **Open Logs**
2. Check **Container** tab for error messages
3. Common issues:
   - Missing environment variables (see error log for specific variable)
   - API key authentication failures
   - Network connectivity to external services

**Solution:** Verify all secrets are configured correctly in Space Settings.

### CORS errors from frontend

**Symptom:** Browser console shows CORS policy errors

**Solution:** Verify `allow_origins` in api.py includes your Vercel URL:
```python
allow_origins=[
    "https://physical-ai-humanoid-robotics-iota-nine.vercel.app",
    "http://localhost:3000",
]
```

### Health check returns 503

**Symptom:** `/health` endpoint returns "degraded" status

**Solution:** Check which service is failing in the response body, then:
1. Verify the corresponding API key is set correctly
2. Check the service's status page (Cohere, OpenAI, Qdrant)
3. Review Container logs for detailed error messages

### Space goes to sleep

**Symptom:** First request after inactivity takes 30-60 seconds

**Explanation:** Free tier Spaces sleep after 48 hours of inactivity

**Solutions:**
1. **Accept cold starts**: Design frontend to show loading indicator
2. **Periodic pings**: Set up cron job to ping `/health` every 24 hours
3. **Upgrade to paid tier**: Eliminates sleep mode

## Monitoring

### Health Checks

Monitor endpoint availability:

```bash
# Manual check
curl https://USERNAME-physical-ai-chatbot-backend.hf.space/health

# Automated monitoring (using UptimeRobot or similar)
# Configure to ping /health every 5 minutes
```

### Logs

View application logs:

1. Navigate to Space page
2. Click **Open Logs**
3. Select **Container** tab
4. Monitor for errors and performance issues

### Performance

Key metrics to monitor:
- Health check response time (target: < 2s)
- Chat endpoint response time (target: < 5s for errors, variable for responses)
- Startup time after sleep (target: < 60s)

## Updating the Deployment

To deploy updates:

```bash
# Make changes to backend code
git add .
git commit -m "Description of changes"
git push

# Space will automatically rebuild and redeploy
# Monitor in Open Logs → Build tab
```

## Rollback

If deployment fails:

```bash
# Revert to previous commit
git log  # Find last working commit hash
git revert <commit-hash>
git push
```

## Security Considerations

1. **Never commit secrets**: Always use Hugging Face Spaces secrets management
2. **Review logs**: Ensure no secrets appear in stdout/stderr
3. **CORS configuration**: Only allow trusted frontend origins
4. **Rate limiting**: Consider adding rate limiting if abuse occurs

## Support

For issues:
1. Check Container logs first
2. Verify secrets configuration
3. Test locally with Docker
4. Review [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces)
```

### CORS Configuration

Update `backend/api.py` to include explicit CORS configuration:

```python
# Add or update CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://physical-ai-humanoid-robotics-iota-nine.vercel.app",
        "http://localhost:3000",  # For local development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

## Phase 1 Completion Summary

### Artifacts Generated

1. ✅ **plan.md** (this file): Complete implementation plan with technical context, research findings, and design decisions
2. ✅ **research.md**: Comprehensive Hugging Face Spaces deployment research (linked via research agent)
3. ❌ **data-model.md**: N/A (no new domain entities for infrastructure feature)
4. ✅ **quickstart.md**: Deployment instructions (integrated into plan as deployment.md content)
5. ✅ **contracts/**: API contract specifications (embedded in plan as OpenAPI-style documentation)

### Key Design Decisions

1. **Docker SDK**: Required for FastAPI deployment on Hugging Face Spaces
2. **app.py Entry Point**: New entry point for HF Spaces (imports from api.py)
3. **Explicit CORS**: Whitelist Vercel frontend origin for security
4. **Structured Error Handling**: Map external service errors to user-friendly messages
5. **Health Check Endpoint**: Implement /health for monitoring with service status details
6. **Requirements.txt**: Generate from pyproject.toml for Docker compatibility
7. **Production Logging**: Configure stdout logging for HF Spaces visibility

### Ready for Phase 2 (Tasks Generation)

Next step: Run `/sp.tasks` to generate actionable implementation tasks from this plan.

## Constitution Check (Post-Design) ✅ PASS

Re-evaluation after Phase 1 design confirms all constitution principles remain satisfied:

- **Spec-Driven Development**: ✅ Following full workflow (spec → plan → tasks)
- **Seamless Integration**: ✅ Deployment enables frontend-backend integration
- **Reproducibility**: ✅ All deployment artifacts are deterministic and version-controlled
- **Tooling Constraint**: ✅ Using Claude Code and Spec-Kit Plus exclusively
- **Backend Standard**: ✅ Using FastAPI as specified in constitution
- **Qdrant Cloud**: ✅ Using existing Qdrant deployment (no changes)

**No design changes required based on constitution check.**
