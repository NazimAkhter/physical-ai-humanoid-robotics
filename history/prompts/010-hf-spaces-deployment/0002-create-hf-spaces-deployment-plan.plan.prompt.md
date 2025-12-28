---
id: 0002
title: Create HF Spaces deployment plan
stage: plan
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5
feature: 010-hf-spaces-deployment
branch: 010-hf-spaces-deployment
user: developer
command: /sp.plan
labels: ["deployment", "hugging-face", "docker", "planning", "architecture"]
links:
  spec: specs/010-hf-spaces-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/010-hf-spaces-deployment/plan.md
 - CLAUDE.md (agent context updated)
tests:
 - Constitution Check (PASS - all principles satisfied)
 - Post-Design Constitution Check (PASS)
---

## Prompt

- Create README.md with Hugging Face Space metadata (title, emoji, colorFrom, colorTo, sdk: docker, app_file: app.py)
- Generate requirements.txt with all dependencies (FastAPI, Uvicorn, OpenAI SDK, Cohere, Qdrant, etc.)
- Create app.py as entry point that imports and runs FastAPI from api.py
- Add environment variable handling for API keys (COHERE_API_KEY, OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY)
- Implement error handling, logging, and health check endpoint (/health)
- Add Dockerfile if needed for Docker SDK deployment
- Test locally, then deploy to Hugging Face Spaces and verify production access

## Response snapshot

Created comprehensive implementation plan for Hugging Face Spaces production deployment with complete technical architecture, research findings, and design decisions:

**Branch**: 010-hf-spaces-deployment

**Planning Workflow Completed**:

1. **Setup & Context Loading** (Phase 0):
   - Initialized planning context via setup-plan.sh
   - Loaded feature specification and constitution
   - Identified existing backend structure (backend/api.py, agent.py)

2. **Research Phase** (Phase 0):
   - Deployed research agent to investigate HF Spaces requirements
   - Comprehensive findings on README.md YAML frontmatter, Docker SDK, port 7860 standard
   - Documented best practices for production logging, CORS, error handling

3. **Technical Context**:
   - Python 3.10+ (HF Spaces Docker requirement)
   - FastAPI 0.104+, Uvicorn 0.24+, OpenAI Agents, Cohere, Qdrant
   - Docker SDK deployment to HF Spaces free tier (cpu-basic)
   - Port 7860, user UID 1000, stdout logging, 48-hour sleep mode

4. **Design & Contracts** (Phase 1):
   - **API Contracts**: Documented existing POST /chat, new GET /health, GET / endpoints
   - **Error Handling Strategy**: Mapped external service errors (Cohere, OpenAI, Qdrant) to HTTP status codes (503, 429, 500) with user-friendly messages
   - **Deployment Configuration**: Complete Dockerfile, README.md frontmatter, .dockerignore, requirements.txt generation
   - **app.py Entry Point**: New entry point for HF Spaces with environment validation and health checks
   - **CORS Configuration**: Explicit whitelist for Vercel frontend origin
   - **deployment.md**: Comprehensive deployment instructions with troubleshooting guide

5. **Project Structure**:
   ```
   backend/
   ├── api.py (existing - minor CORS updates)
   ├── agent.py (existing)
   ├── README.md (MODIFIED - add YAML frontmatter)
   ├── Dockerfile (NEW)
   ├── requirements.txt (NEW - from pyproject.toml)
   ├── app.py (NEW - HF Spaces entry point)
   ├── .dockerignore (NEW)
   └── deployment.md (NEW)
   ```

6. **Key Design Decisions**:
   - Docker SDK (required for FastAPI on HF Spaces)
   - Python 3.10 base image (compatibility)
   - app.py entry point (HF Spaces convention)
   - Explicit CORS origins (security best practice)
   - Structured error handling (user-friendly messages)
   - Health check with service status (monitoring)
   - Production logging to stdout (HF Spaces visibility)

7. **Constitution Check** (Pre & Post Design):
   - ✅ Spec-Driven Development: Following full workflow
   - ✅ Seamless Integration: Frontend-backend via public API
   - ✅ Reproducibility: Deterministic deployment artifacts
   - ✅ Tooling Constraint: Claude Code + Spec-Kit Plus
   - ✅ FastAPI Standard: Per constitution
   - ✅ Qdrant Cloud: Using existing deployment

8. **Agent Context Update**:
   - Updated CLAUDE.md with new technology stack
   - Added Python 3.10+ (HF Spaces), FastAPI, Uvicorn, OpenAI SDK, Cohere, Qdrant

**Artifacts Generated**:
- ✅ plan.md (787 lines): Complete implementation plan
- ✅ Research findings: Embedded in plan (HF Spaces best practices)
- ❌ data-model.md: N/A (infrastructure feature, no domain entities)
- ✅ quickstart.md: Integrated as deployment.md content in plan
- ✅ contracts/: API contracts embedded in plan (OpenAPI-style)

## Outcome

- ✅ Impact: Production-ready implementation plan for deploying FastAPI backend to Hugging Face Spaces. Provides complete technical architecture, deployment configuration (Dockerfile, README.md, app.py), error handling strategy, CORS setup, and comprehensive deployment instructions.
- 🧪 Tests: Constitution Check (PASS), Post-Design Constitution Check (PASS)
- 📁 Files: plan.md (787 lines), CLAUDE.md (updated), agent context synchronized
- 🔁 Next prompts: `/sp.tasks` to generate actionable implementation tasks from plan, then `/sp.implement` to execute
- 🧠 Reflection: Plan successfully addresses all deployment requirements from spec. Research phase provided critical HF Spaces implementation details (UID 1000, port 7860, YAML frontmatter). Design phase produced complete deployment configuration with production-grade error handling. No architectural decisions require ADR documentation (deployment infrastructure, not system architecture).

## Evaluation notes (flywheel)

- Failure modes observed: None - planning workflow completed successfully
- Graders run and results (PASS/FAIL): Constitution Check (PASS), Post-Design Constitution Check (PASS)
- Prompt variant (if applicable): Standard /sp.plan workflow with user-provided implementation hints
- Next experiment (smallest change to try): N/A - plan is complete and ready for task generation (/sp.tasks)
