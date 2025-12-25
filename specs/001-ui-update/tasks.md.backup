---
description: "Task list for UI Update for Physical AI Book Website"
---

# Tasks: UI Update for Physical AI Book Website

**Input**: Design documents from `/specs/001-ui-update/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` at repository root
- **Docusaurus**: Configuration in `frontend/docusaurus.config.js`, components in `frontend/src/`, CSS in `frontend/src/css/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Verify frontend project structure exists per implementation plan
- [ ] T002 [P] Install required dependencies if not already present
- [ ] T003 [P] Verify Docusaurus development server can start successfully

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Verify current navigation structure in docusaurus.config.js
- [ ] T005 [P] Identify all 6 module navigation links to be removed
- [ ] T006 [P] Create backup of current docusaurus.config.js file

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Improved Navigation Experience (Priority: P1) 🎯 MVP

**Goal**: Remove 6 module navigation links from the Header navbar, Resources, and Community menus to reduce clutter and improve user experience

**Independent Test**: Can be fully tested by verifying that the 6 module navigation links are removed from the Header navbar, Resources, and Community menus while maintaining access to essential navigation.

### Implementation for User Story 1

- [ ] T007 [US1] Remove 6 module navigation links from Header navbar in frontend/docusaurus.config.js
- [ ] T008 [US1] Remove 6 module navigation links from Resources menu in frontend/docusaurus.config.js
- [ ] T009 [US1] Remove 6 module navigation links from Community menu in frontend/docusaurus.config.js
- [ ] T010 [US1] Verify remaining navigation links function correctly after removal

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Updated Visual Branding (Priority: P2)

**Goal**: Update the navbar logo and hero section image to better represent the AI/robotics theme, creating a more engaging and relevant user experience

**Independent Test**: Can be fully tested by verifying that the navbar logo and hero section image have been updated to the specified images while maintaining proper display across different devices.

### Implementation for User Story 2

- [ ] T011 [US2] Download new navbar logo image from https://png.pngtree.com/png-vector/20240531/ourlarge/pngtree-3d-a-robot-is-on-transparent-background-png-image_12549806.png
- [ ] T012 [US2] Add new logo image to frontend/static/img/ directory
- [ ] T013 [US2] Update navbar logo configuration in frontend/docusaurus.config.js to use new image
- [ ] T014 [US2] Download new hero section image from https://img.freepik.com/free-psd/futuristic-robot-using-laptop_191095-85585.jpg?semt=ais_hybrid&w=740&q=80
- [ ] T015 [US2] Add new hero image to frontend/static/img/ directory
- [ ] T016 [US2] Update hero section component to use new image in frontend/src/components/
- [ ] T017 [US2] Verify new images display correctly across different screen sizes

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Enhanced Visual Theme (Priority: P3)

**Goal**: Apply a cohesive color theme that matches the reference design, improving the overall aesthetic appeal

**Independent Test**: Can be fully tested by comparing the website's color theme with the reference image and ensuring all UI elements use the updated color palette.

### Implementation for User Story 3

- [ ] T018 [US3] Extract color values from reference image https://colorlib.com/wp/wp-content/uploads/sites/2/videograph-free-template-408x322.jpg.avif
- [ ] T019 [US3] Update primary color variables in frontend/src/css/custom.css
- [ ] T020 [US3] Update secondary color variables in frontend/src/css/custom.css
- [ ] T021 [US3] Update background color variables in frontend/src/css/custom.css
- [ ] T022 [US3] Update text color variables in frontend/src/css/custom.css
- [ ] T023 [US3] Update accent color variables in frontend/src/css/custom.css
- [ ] T024 [US3] Apply new color theme to navigation elements
- [ ] T025 [US3] Apply new color theme to buttons and interactive elements
- [ ] T026 [US3] Verify all UI elements reflect the new color theme consistently

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Fixed Navigation Links (Priority: P1)

**Goal**: Validate and fix all navigation links across the site to ensure they work correctly without encountering broken links or 404 errors

**Independent Test**: Can be fully tested by validating all navigation links across the site to ensure they work correctly and don't return 404 errors.

### Implementation for User Story 4

- [ ] T027 [US4] Create list of all current navigation links on the website
- [ ] T028 [US4] Use link validation tool to scan for broken links (404 errors)
- [ ] T029 [US4] Fix broken navigation links in docusaurus.config.js
- [ ] T030 [US4] Fix broken navigation links in MDX content files
- [ ] T031 [US4] Update any incorrect internal links to proper destinations
- [ ] T032 [US4] Verify all navigation links return 200 status codes

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T033 [P] Test mobile responsiveness on various screen sizes (320px, 768px, 1024px)
- [ ] T034 [P] Verify no regressions were introduced to layout, sidebar, or MDX content
- [ ] T035 [P] Run quickstart.md validation to confirm all features work together
- [ ] T036 [P] Update documentation if needed to reflect UI changes
- [ ] T037 [P] Final validation that all success criteria from spec are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all navigation removal tasks for User Story 1 together:
Task: "Remove 6 module navigation links from Header navbar in frontend/docusaurus.config.js"
Task: "Remove 6 module navigation links from Resources menu in frontend/docusaurus.config.js"
Task: "Remove 6 module navigation links from Community menu in frontend/docusaurus.config.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 4 → Test independently → Deploy/Demo
4. Add User Story 2 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Navigation cleanup)
   - Developer B: User Story 2 (Visual branding)
   - Developer C: User Story 3 (Color theme)
   - Developer D: User Story 4 (Link validation)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence