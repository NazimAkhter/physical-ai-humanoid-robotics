---
description: "Task list for Hugging Face Spaces Production Deployment"
---

# Tasks: Hugging Face Spaces Production Deployment

**Input**: Design documents from `/specs/010-hf-spaces-deployment/`
**Prerequisites**: plan.md (complete), spec.md (complete with user stories)

**Tests**: Tests are NOT explicitly requested in the spec, so test tasks are excluded. Focus is on deployment configuration and production readiness.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with existing `backend/` directory. All deployment files are added to `backend/` root per plan.md structure.

---

## Phase 1: Setup (Deployment Infrastructure)

**Purpose**: Create deployment configuration files for Hugging Face Spaces

- [X] T001 [P] Create Dockerfile for HF Spaces in backend/Dockerfile following plan.md template (Python 3.10, user UID 1000, port 7860)
- [X] T002 [P] Create .dockerignore file in backend/.dockerignore to exclude .venv, __pycache__, .env, tests
- [X] T003 [P] Create deployment documentation in backend/deployment.md with HF Spaces setup instructions and troubleshooting guide
- [X] T004 Generate requirements.txt from pyproject.toml in backend/requirements.txt using uv pip compile

**Checkpoint**: Deployment infrastructure files created, ready for application entry point

---

## Phase 2: Foundational (Application Entry Point & Configuration)

**Purpose**: Core application entry point that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create app.py entry point in backend/app.py that imports FastAPI app from api.py, validates environment variables, and configures production logging
- [X] T006 Add YAML frontmatter to backend/README.md with HF Spaces metadata (title: Physical AI Chatbot Backend, emoji: 🤖, sdk: docker, app_port: 7860)
- [X] T007 Update CORS configuration in backend/api.py to explicitly allow Vercel frontend origin (https://physical-ai-humanoid-robotics-iota-nine.vercel.app)

**Checkpoint**: Foundation ready - app.py can start FastAPI, environment validation works, CORS configured

---

## Phase 3: User Story 1 - Deploy Backend Successfully (Priority: P1) 🎯 MVP

**Goal**: Deploy the RAG chatbot backend to Hugging Face Spaces so that the public-facing frontend can access the API endpoints without errors

**Independent Test**: Deploy to HF Spaces, configure environment secrets (COHERE_API_KEY, OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY), verify health check endpoint returns 200 and backend responds to requests

### Implementation for User Story 1

- [X] T008 [US1] Implement GET /health endpoint in backend/app.py that returns basic health status with timestamp and placeholder service status
- [X] T009 [US1] Implement GET / root endpoint in backend/app.py that returns service information (name, version, status, endpoints list)
- [X] T010 [US1] Add environment variable validation on startup in backend/app.py to check all required vars (COHERE_API_KEY, OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY) and exit with clear error if missing
- [X] T011 [US1] Configure production logging to stdout in backend/app.py using logging.basicConfig with INFO level and structured format
- [ ] T012 [US1] Test Docker build locally: docker build -t physical-ai-backend backend/ and verify no errors
- [ ] T013 [US1] Test Docker run locally: docker run -p 7860:7860 --env-file backend/.env physical-ai-backend and verify /health endpoint responds
- [ ] T014 [US1] Create HF Space at https://huggingface.co/spaces (Docker SDK, public/private visibility)
- [ ] T015 [US1] Push backend code to HF Space repository and monitor Build logs for successful Docker build
- [ ] T016 [US1] Configure environment secrets in HF Space Settings (COHERE_API_KEY, OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY)
- [ ] T017 [US1] Verify Space shows "Running" status and test /health endpoint returns HTTP 200 from deployed URL
- [ ] T018 [US1] Test /chat endpoint from deployed HF Space URL with sample query and verify response

**Checkpoint**: Backend is deployed to HF Spaces, health check works, chat endpoint responds, CORS allows frontend access

---

## Phase 4: User Story 2 - Handle Production Errors Gracefully (Priority: P2)

**Goal**: Deployed API handles external service failures (Cohere timeouts, OpenAI rate limits, Qdrant connection errors) gracefully so users receive informative error messages instead of cryptic 500 errors

**Independent Test**: Simulate failures (invalid API keys, disconnect network) and verify appropriate HTTP status codes (503, 429, 500) with user-friendly error messages instead of stack traces

### Implementation for User Story 2

- [X] T019 [P] [US2] Create error handling wrapper function safe_api_call in backend/app.py or backend/api.py for external service calls with try-except for TimeoutError, RateLimitError, AuthenticationError
- [X] T020 [US2] Wrap Cohere API calls in backend/agent.py with error handling to return HTTP 503 for timeouts/connection errors and HTTP 429 for rate limits with user message "Embedding service temporarily unavailable, please try again"
- [X] T021 [US2] Wrap OpenAI API calls in backend/agent.py with error handling to return HTTP 503 for timeouts and HTTP 429 for rate limits with user message "Service is experiencing high demand, please try again in a moment"
- [X] T022 [US2] Wrap Qdrant client calls in backend/agent.py with error handling to return HTTP 503 for connection failures/timeouts with user message "Vector database temporarily unavailable, please try again"
- [X] T023 [US2] Add global exception handler in backend/api.py to catch unexpected errors and return HTTP 500 with generic message "An unexpected error occurred, please contact support" while logging full stack trace
- [X] T024 [US2] Update logging in error handlers to log full exception details (exc_info=True) for debugging while returning sanitized messages to users
- [ ] T025 [US2] Test error scenarios locally: invalid API keys, simulated timeouts, rate limit responses, verify appropriate HTTP status codes and user messages
- [ ] T026 [US2] Deploy updated code to HF Space and verify error handling in production by testing with invalid secrets temporarily

**Checkpoint**: All external service errors return appropriate status codes and user-friendly messages, logs contain debugging details

---

## Phase 5: User Story 3 - Enable Frontend Cross-Origin Access (Priority: P2)

**Goal**: Backend API accepts requests from the public Vercel-hosted frontend so users can interact with the chatbot from the website without CORS errors

**Independent Test**: Make a fetch request from Vercel frontend URL to HF Spaces API endpoint and verify request succeeds without CORS errors in browser console

### Implementation for User Story 3

- [X] T027 [US3] Verify CORSMiddleware configuration in backend/api.py includes explicit allow_origins list with Vercel URL (https://physical-ai-humanoid-robotics-iota-nine.vercel.app) and localhost:3000
- [X] T028 [US3] Ensure CORS allow_credentials is set to True in backend/api.py for session support if needed in future
- [X] T029 [US3] Verify CORS allow_methods includes GET, POST, OPTIONS for preflight requests in backend/api.py
- [X] T030 [US3] Verify CORS allow_headers includes Content-Type and Authorization in backend/api.py
- [ ] T031 [US3] Test CORS preflight request locally using curl with OPTIONS method and Origin header, verify Access-Control-Allow-Origin header in response
- [ ] T032 [US3] Deploy CORS configuration to HF Space
- [ ] T033 [US3] Test CORS from Vercel frontend: open frontend in browser, send chat request, verify no CORS errors in console and request succeeds
- [ ] T034 [US3] Test CORS from different origins (not in whitelist) to confirm requests are blocked as expected

**Checkpoint**: Frontend can successfully communicate with backend API without CORS errors, OPTIONS preflight requests work correctly

---

## Phase 6: User Story 4 - Monitor Deployment Health (Priority: P3)

**Goal**: Operations team can quickly verify backend is healthy and responding correctly to detect and respond to outages or degraded performance

**Independent Test**: Set up external monitoring service (UptimeRobot) to ping health endpoint every 5 minutes and verify 200 responses, automated alerts trigger on failures

### Implementation for User Story 4

- [X] T035 [US4] Enhance GET /health endpoint in backend/app.py to check actual service connectivity: test Cohere API reachability, OpenAI API reachability, Qdrant connection
- [X] T036 [US4] Update /health response to return HTTP 200 with "healthy" status when all services are reachable, or HTTP 503 with "degraded" status and details when any service is unreachable
- [X] T037 [US4] Add timeout limits to health check service tests (1-2 seconds max) to ensure health endpoint responds quickly without impacting main API performance
- [X] T038 [US4] Update /health response to include timestamp in ISO 8601 format and individual service status (cohere: reachable/unreachable, openai: reachable/unreachable, qdrant: reachable/unreachable)
- [X] T039 [US4] Add health check error details to response body when status is degraded (e.g., "error": "Cohere API connection failed")
- [ ] T040 [US4] Test health check locally with valid API keys (should return 200 healthy) and invalid keys (should return 503 degraded)
- [ ] T041 [US4] Deploy enhanced health check to HF Space and verify it returns correct status based on actual service availability
- [ ] T042 [US4] Set up external monitoring service (UptimeRobot, Pingdom, or similar) to ping /health endpoint every 5 minutes
- [ ] T043 [US4] Configure monitoring alerts to notify on health check failures (email, Slack, etc.)
- [ ] T044 [US4] Document health check monitoring setup in backend/deployment.md under "Monitoring" section

**Checkpoint**: Health check endpoint provides detailed service status, external monitoring configured with alerts

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and production readiness

- [X] T045 [P] Review and update backend/README.md with complete HF Space description, features list, and link to deployment.md
- [ ] T046 [P] Review Container logs in HF Space for any warnings or errors and address them
- [ ] T047 [P] Verify all secrets are properly configured in HF Space Settings and not exposed in logs
- [ ] T048 [P] Test cold start behavior after 48 hours: verify application wakes gracefully and establishes service connections
- [X] T049 [P] Document known limitations in backend/deployment.md (free tier sleep mode, cold start time, resource limits)
- [X] T050 [P] Add troubleshooting section to backend/deployment.md with common issues (runtime errors, CORS errors, health check 503, sleep mode)
- [X] T051 Review backend/deployment.md for completeness and accuracy, ensure all setup steps are clear
- [ ] T052 Create a quickstart validation checklist: test all deployment steps from scratch on a new HF Space to ensure reproducibility
- [ ] T053 Update main project README.md at repository root with link to deployed HF Space backend URL
- [ ] T054 Verify frontend in production (Vercel) successfully communicates with deployed backend (end-to-end test)

**Checkpoint**: All user stories complete, deployment documented, production-ready

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion (T001-T004) - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion (T005-T007)
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories (foundational for deployment)
  - User Story 2 (P2): Can start after US1 deployment complete (T018) - needs working deployment to test error handling
  - User Story 3 (P2): Can start in parallel with US2 after Foundational - independent CORS configuration
  - User Story 4 (P3): Can start after US2 complete (T026) - needs error handling for health check service tests
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Foundational deployment - can start after Phase 2 complete
- **User Story 2 (P2)**: Depends on US1 deployment (T018) - needs working backend to add error handling
- **User Story 3 (P2)**: Depends on Foundational (T007 CORS config in Phase 2) - independent from US1/US2
- **User Story 4 (P3)**: Depends on US2 error handling (T026) - health check needs error handling patterns

### Within Each User Story

- **US1**: T008-T011 (endpoint/logging setup) → T012-T013 (local testing) → T014-T017 (HF deployment) → T018 (verification)
- **US2**: T019 (error wrapper) can be parallel with T020-T022 (service-specific error handling) → T023-T024 (global handler) → T025-T026 (testing)
- **US3**: T027-T030 (CORS verification/config) in parallel → T031 (local test) → T032-T034 (deployment test)
- **US4**: T035-T039 (health check enhancement) in parallel → T040 (local test) → T041 (deploy) → T042-T044 (monitoring setup)

### Parallel Opportunities

**Within Setup (Phase 1)**:
- T001, T002, T003 can run in parallel (different files)
- T004 depends on pyproject.toml being readable

**Within Foundational (Phase 2)**:
- T005, T006, T007 are sequential (T005 creates app.py, T007 modifies api.py)

**Within User Story 1**:
- T008, T009 can run in parallel (different functions in app.py)
- T010, T011 can run in parallel (different functions in app.py)

**Within User Story 2**:
- T020, T021, T022 can run in parallel (different error handling for different services)
- T019 should be done first (creates reusable wrapper)

**Within User Story 3**:
- T027, T028, T029, T030 can run in parallel (different CORS config checks)

**Within User Story 4**:
- T035, T036, T037, T038, T039 can be done together (all modify /health endpoint)

**Within Polish (Phase 7)**:
- T045, T046, T047, T048, T049, T050 can all run in parallel (different files/concerns)

---

## Parallel Example: User Story 1

```bash
# Launch basic endpoint implementations together:
Task: "Implement GET /health endpoint in backend/app.py"
Task: "Implement GET / root endpoint in backend/app.py"

# Launch configuration tasks together:
Task: "Add environment variable validation on startup in backend/app.py"
Task: "Configure production logging to stdout in backend/app.py"
```

## Parallel Example: User Story 2

```bash
# Launch service-specific error handling together:
Task: "Wrap Cohere API calls in backend/agent.py with error handling"
Task: "Wrap OpenAI API calls in backend/agent.py with error handling"
Task: "Wrap Qdrant client calls in backend/agent.py with error handling"
```

## Parallel Example: User Story 3

```bash
# Launch CORS configuration verification together:
Task: "Verify CORSMiddleware configuration includes Vercel URL"
Task: "Ensure CORS allow_credentials is set to True"
Task: "Verify CORS allow_methods includes GET, POST, OPTIONS"
Task: "Verify CORS allow_headers includes Content-Type and Authorization"
```

## Parallel Example: Polish Phase

```bash
# Launch documentation and review tasks together:
Task: "Review and update backend/README.md"
Task: "Review Container logs in HF Space"
Task: "Verify all secrets properly configured"
Task: "Document known limitations"
Task: "Add troubleshooting section"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004) - ~1 hour
2. Complete Phase 2: Foundational (T005-T007) - ~1 hour
3. Complete Phase 3: User Story 1 (T008-T018) - ~3 hours
4. **STOP and VALIDATE**: Test deployed backend independently
   - Health check returns 200
   - Chat endpoint works from HF Space URL
   - CORS allows frontend access
5. Deploy/demo MVP backend

**Total MVP Time**: ~5 hours to working deployment

### Incremental Delivery

1. **Foundation** (Phases 1-2): Setup + app.py entry point → ~2 hours → Backend can start
2. **Add US1** (Phase 3): Deploy to HF Spaces → Test independently → ~3 hours → **MVP deployed!**
3. **Add US2** (Phase 4): Error handling → Test independently → ~2 hours → Production-ready error handling
4. **Add US3** (Phase 5): CORS verification → Test independently → ~1 hour → Frontend integration confirmed
5. **Add US4** (Phase 6): Health monitoring → Test independently → ~2 hours → Monitoring configured
6. **Polish** (Phase 7): Documentation and final validation → ~2 hours → Production-ready

**Total Time**: ~12 hours for complete production deployment

### Parallel Team Strategy

With 2 developers:

1. **Together**: Complete Setup + Foundational (Phases 1-2) - ~2 hours
2. **Once Foundational is done**:
   - Developer A: User Story 1 (P1) - deploy to HF Spaces - ~3 hours
   - Developer B: Prepare User Story 2 error handling patterns - ~2 hours
3. **After US1 deployed**:
   - Developer A: User Story 3 (CORS) + User Story 4 (monitoring) - ~3 hours
   - Developer B: User Story 2 (error handling in deployed backend) - ~2 hours
4. **Together**: Polish phase final validation - ~1 hour

**Total Time with 2 developers**: ~7-8 hours

---

## Notes

- **[P] tasks**: Different files or independent concerns, no dependencies
- **[Story] label**: Maps task to specific user story for traceability (US1, US2, US3, US4)
- **Each user story**: Independently completable and testable
- **Tests excluded**: Spec does not request tests, focus is on deployment configuration
- **Deployment-first**: US1 gets backend deployed, then incrementally add production features
- **Stop at any checkpoint**: Validate story independently before moving on
- **Error handling is critical**: US2 addresses production reliability before monitoring (US4)
- **CORS validated early**: US3 ensures frontend can communicate immediately after US1 deployment
- **Avoid**: Hardcoding secrets, skipping local Docker testing, deploying without health check
- **Commit strategy**: Commit after each task or logical group (e.g., T001-T004 together, T008-T011 together)
- **Dockerfile testing**: Always test Docker build and run locally before pushing to HF Space
- **Environment secrets**: Configure in HF Space Settings, never commit to repository
- **Cold start ready**: Free tier sleeps after 48 hours, design for graceful wake-up
