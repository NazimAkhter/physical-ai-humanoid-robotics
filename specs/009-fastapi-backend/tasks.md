# Tasks: FastAPI Backend Integration

**Input**: Design documents from `/specs/009-fastapi-backend/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/chat-api.md

**Tests**: Manual curl/Postman testing (no automated tests requested)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/api.py` (single file per spec constraints)
- Existing files: `backend/agent.py`, `backend/retrieve.py`, `backend/config.py`

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure verification

- [x] T001 Verify FastAPI and Uvicorn dependencies exist in backend/pyproject.toml
- [x] T002 Create backend/api.py file with basic structure (imports, app instance)
- [x] T003 Add FRONTEND_URL to backend/.env.example for CORS configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user story implementation

- [x] T004 [P] Define Pydantic models in backend/api.py: ChatRequest, Source, ChatResponse
- [x] T005 [P] Define Pydantic models in backend/api.py: HealthStatus, ErrorResponse
- [x] T006 Create FastAPI app instance with metadata in backend/api.py
- [x] T007 Import agent functions (create_agent, run_query, initialize_clients) in backend/api.py
- [x] T008 Add startup event handler to initialize agent and clients in backend/api.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Basic Chat Query (Priority: P1) MVP

**Goal**: Frontend can send queries and receive AI responses with source citations

**Independent Test**: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"query\": \"What is ROS 2?\"}"` returns answer and sources

### Implementation for User Story 1

- [x] T009 [US1] Implement POST /chat endpoint in backend/api.py
- [x] T010 [US1] Add query validation (non-empty, max 2000 chars) in POST /chat endpoint
- [x] T011 [US1] Integrate run_query() from agent.py to process queries in backend/api.py
- [x] T012 [US1] Map agent response to ChatResponse format with sources in backend/api.py
- [x] T013 [US1] Add logging for chat requests and responses in backend/api.py
- [x] T014 [US1] Implement GET / root endpoint returning API info in backend/api.py
- [x] T015 [US1] Add uvicorn.run() in __main__ block for direct execution in backend/api.py
- [x] T016 [US1] Test POST /chat with curl: curriculum question (expect sources)
- [x] T017 [US1] Test POST /chat with curl: greeting (expect no sources)

**Checkpoint**: User Story 1 complete - basic chat functionality works

---

## Phase 4: User Story 2 - Cross-Origin Frontend Integration (Priority: P2)

**Goal**: Frontend apps on different origins can communicate with the API

**Independent Test**: Make request from browser at localhost:3000 to API at localhost:8000, verify no CORS errors

### Implementation for User Story 2

- [x] T018 [US2] Add CORSMiddleware import in backend/api.py
- [x] T019 [US2] Configure allowed origins list (localhost:3000, 5173, 8080, FRONTEND_URL env) in backend/api.py
- [x] T020 [US2] Add CORSMiddleware to FastAPI app with configured origins in backend/api.py
- [x] T021 [US2] Set CORS allowed methods (GET, POST, OPTIONS) in backend/api.py
- [x] T022 [US2] Set CORS allowed headers (Content-Type, Authorization) in backend/api.py
- [x] T023 [US2] Test CORS with browser request from different origin

**Checkpoint**: User Story 2 complete - cross-origin requests work

---

## Phase 5: User Story 3 - Error Handling for Invalid Requests (Priority: P3)

**Goal**: API returns clear, structured error messages for invalid requests

**Independent Test**: Send invalid requests and verify appropriate HTTP status codes and error messages

### Implementation for User Story 3

- [x] T024 [US3] Add HTTPException import for error handling in backend/api.py
- [x] T025 [US3] Implement empty query validation with 400 EMPTY_QUERY error in backend/api.py
- [x] T026 [US3] Implement query length validation with 400 QUERY_TOO_LONG error in backend/api.py
- [x] T027 [US3] Add try/except wrapper in /chat for agent errors with 500 response in backend/api.py
- [x] T028 [US3] Add timeout handling (30s) for agent calls with 503 response in backend/api.py
- [x] T029 [US3] Test error: empty query (expect 400)
- [x] T030 [US3] Test error: query too long (expect 400)
- [x] T031 [US3] Test error: missing query field (expect 422)

**Checkpoint**: User Story 3 complete - error handling works correctly

---

## Phase 6: User Story 4 - Health Check Endpoint (Priority: P4)

**Goal**: Operations teams can verify API and dependency health

**Independent Test**: `curl http://localhost:8000/health` returns status and dependency info

### Implementation for User Story 4

- [x] T032 [US4] Implement GET /health endpoint in backend/api.py
- [x] T033 [US4] Add Qdrant connection status check in health endpoint
- [x] T034 [US4] Add Cohere client status check in health endpoint
- [x] T035 [US4] Add OpenRouter API key configuration check in health endpoint
- [x] T036 [US4] Implement status logic (healthy/degraded/unhealthy) based on dependencies
- [x] T037 [US4] Test health endpoint with all dependencies available
- [x] T038 [US4] Test health endpoint response format matches contract

**Checkpoint**: User Story 4 complete - health monitoring works

---

## Phase 7: Polish and Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T039 [P] Add docstrings to all endpoints in backend/api.py
- [x] T040 Run 10+ consecutive test requests to verify SC-003 (API stability)
- [x] T041 Verify server startup time under 5 seconds (SC-001)
- [x] T042 Update backend/README.md with API documentation
- [x] T043 Run quickstart.md validation steps

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after US1 - CORS middleware adds to existing app
- **User Story 3 (P3)**: Can start after US1 - Error handling enhances existing endpoint
- **User Story 4 (P4)**: Can start after Foundational - Independent health endpoint

### Parallel Opportunities

- T004 and T005 (Pydantic models) can run in parallel
- T039 (docstrings) can run in parallel with other polish tasks

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test chat endpoint with curl
5. Deploy/demo if ready - basic chat API works!

### Incremental Delivery

1. Complete Setup + Foundational - Foundation ready
2. Add User Story 1 - Test with curl - MVP ready!
3. Add User Story 2 - Test CORS - Cross-origin ready
4. Add User Story 3 - Test errors - Production-ready errors
5. Add User Story 4 - Test health - Monitoring ready

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 43 |
| Phase 1 (Setup) | 3 tasks |
| Phase 2 (Foundational) | 5 tasks |
| Phase 3 (US1 - Chat) | 9 tasks |
| Phase 4 (US2 - CORS) | 6 tasks |
| Phase 5 (US3 - Errors) | 8 tasks |
| Phase 6 (US4 - Health) | 7 tasks |
| Phase 7 (Polish) | 5 tasks |
| Parallel Opportunities | 4 tasks marked [P] |

**MVP Scope**: Complete through Phase 3 (User Story 1) - 17 tasks
**Full Implementation**: All 43 tasks

---

## Notes

- All implementation in single file: backend/api.py
- Testing via manual curl commands (no automated test framework)
- [P] tasks = can run in parallel with other [P] tasks in same phase
- [US#] label maps task to specific user story
- Commit after each phase or logical group
- Stop at any checkpoint to validate story independently
