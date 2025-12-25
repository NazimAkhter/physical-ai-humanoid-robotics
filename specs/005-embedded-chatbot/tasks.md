# Implementation Tasks: Embedded Chatbot UI for Docusaurus Book

**Feature**: 005-embedded-chatbot  
**Branch**: `005-embedded-chatbot`  
**Date**: 2025-12-22  
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Overview

This document defines the implementation tasks for building an embedded chatbot UI component within a Docusaurus documentation site. Tasks are organized by user story to enable independent implementation and testing.

## Implementation Strategy

**MVP-First Approach**: Implement User Story 1 (Basic Chatbot Interaction) as the complete, shippable MVP. Subsequent stories add enhancements without breaking the core functionality.

**Incremental Delivery**: Each user story phase represents a complete, independently testable increment that can be deployed to production.

## Task Summary

- **Phase 1**: Setup & Project Init (5 tasks)
- **Phase 2**: Foundational Infrastructure (4 tasks)
- **Phase 3**: User Story 1 - Basic Chatbot Interaction [MVP] (8 tasks)
- **Phase 4**: User Story 2 - Context-Aware Questions (4 tasks)
- **Phase 5**: User Story 3 - Responsive Mobile Experience (3 tasks)
- **Phase 6**: User Story 4 - Theme Consistency (3 tasks)
- **Phase 7**: User Story 5 - Keyboard Accessibility (4 tasks)
- **Phase 8**: Polish & Cross-Cutting Concerns (4 tasks)

**Total**: 35 tasks

---

## Phase 1: Setup & Project Initialization

**Goal**: Prepare development environment and project structure

### Tasks

- [x] T001 Swizzle Docusaurus Root component in frontend/src/theme/Root.jsx
- [x] T002 [P] Create chatbot component directory structure at frontend/src/components/Chatbot/
- [x] T003 [P] Create hooks directory at frontend/src/hooks/
- [x] T004 [P] Create chatbot theme CSS file at frontend/src/css/chatbot-theme.css
- [x] T005 [P] Create mock API service at frontend/src/services/mockChatbotAPI.js

**Completion Criteria**: Directory structure matches plan.md; Root.jsx created; mock API functional

---

## Phase 2: Foundational Infrastructure

**Goal**: Build core state management and context infrastructure (blocking for all user stories)

### Tasks

- [x] T006 Implement useChatbot custom hook in frontend/src/hooks/useChatbot.js
- [x] T007 Create ChatbotContext provider in frontend/src/components/Chatbot/ChatbotProvider.jsx
- [x] T008 Implement useDocusaurusTheme hook in frontend/src/hooks/useDocusaurusTheme.js
- [x] T009 Wire ChatbotProvider into Root.jsx theme wrapper

**Completion Criteria**: Context API functional; state management tested; theme hook integrated

**Acceptance Test**: Import useChatbot in a test component; verify state.isOpen toggles correctly

---

## Phase 3: User Story 1 - Basic Chatbot Interaction (Priority: P1) [MVP]

**Story Goal**: Enable readers to open chatbot, send messages, and receive responses

**Independent Test**: Click toggle button to panel opens to type message to press send to response appears to close panel to reopen to history preserved

### Tasks

- [x] T010 [P] [US1] Create ChatbotToggle component in frontend/src/components/Chatbot/ChatbotToggle.jsx
- [x] T011 [P] [US1] Create ChatbotPanel container component in frontend/src/components/Chatbot/ChatbotPanel.jsx
- [x] T012 [P] [US1] Create MessageList component in frontend/src/components/Chatbot/MessageList.jsx
- [x] T013 [P] [US1] Create MessageInput component in frontend/src/components/Chatbot/MessageInput.jsx
- [x] T014 [P] [US1] Create LoadingIndicator component in frontend/src/components/Chatbot/LoadingIndicator.jsx
- [x] T015 [US1] Implement message send/receive logic in useChatbot hook (update frontend/src/hooks/useChatbot.js)
- [x] T016 [US1] Add sessionStorage persistence for conversation history in useChatbot hook
- [x] T017 [US1] Style ChatbotPanel with CSS modules in frontend/src/components/Chatbot/styles.module.css

**Completion Criteria**: 
- Toggle button visible on all pages
- Panel opens/closes without page reload
- Messages display with sender distinction and timestamps
- Conversation persists on panel close/reopen (same page session)
- Loading indicator shows during API calls

**Acceptance Scenarios** (from spec.md):
1. Click toggle to panel opens without reload
2. Type message + send to message appears with timestamp
3. After send to bot response appears below user message
4. Click close to panel closes, conversation preserved
5. Reopen panel to previous conversation displayed


---

## Phase 4: User Story 2 - Context-Aware Questions from Page Content (Priority: P2)

**Story Goal**: Enable readers to select text and ask questions with that text as context

**Independent Test**: Select text on page, floating Ask chatbot button appears, click button, chatbot opens with selected text as context

### Tasks

- [x] T018 [P] [US2] Implement useTextSelection custom hook in frontend/src/hooks/useTextSelection.js
- [x] T019 [P] [US2] Create TextSelectionPopup component in frontend/src/components/Chatbot/TextSelectionPopup.jsx
- [x] T020 [US2] Add context detection logic to useChatbot hook (page URL, title, selected text)
- [x] T021 [US2] Integrate TextSelectionPopup into Root.jsx

**Completion Criteria**:
- Floating button appears when text selected
- Button positioned near selection with boundary detection
- Clicking button opens chatbot with text as context

---

## Phase 5: User Story 3 - Responsive Mobile Experience (Priority: P2)

**Story Goal**: Ensure chatbot works on mobile devices with optimized layout

### Tasks

- [x] T022 [P] [US3] Add mobile layout styles to frontend/src/components/Chatbot/styles.module.css
- [x] T023 [P] [US3] Implement conditional rendering for desktop vs mobile layout in ChatbotPanel.jsx
- [x] T024 [US3] Add viewport scroll position preservation on panel close/open

---

## Phase 6: User Story 4 - Theme Consistency (Priority: P3)

**Story Goal**: Automatically match chatbot UI to Docusaurus theme

### Tasks

- [x] T025 [P] [US4] Define CSS variables for light/dark themes in frontend/src/css/chatbot-theme.css
- [x] T026 [P] [US4] Apply theme-aware styles using useDocusaurusTheme hook in ChatbotPanel.jsx
- [x] T027 [US4] Test and adjust contrast ratios to meet WCAG AA standard

---

## Phase 7: User Story 5 - Keyboard Accessibility (Priority: P3)

**Story Goal**: Enable full keyboard control

### Tasks

- [x] T028 [P] [US5] Add keyboard shortcut listener in ChatbotProvider.jsx
- [x] T029 [P] [US5] Implement focus trap in ChatbotPanel.jsx
- [x] T030 [P] [US5] Add ARIA labels and semantic HTML to all chatbot components
- [x] T031 [US5] Add visible focus indicators to all interactive elements

---

## Phase 8: Polish & Cross-Cutting Concerns

### Tasks

- [x] T032 [P] Add error handling for API failures in useChatbot hook
- [x] T033 [P] Implement context length truncation (2000 char limit)
- [x] T034 [P] Add message queue management in MessageInput.jsx
- [x] T035 Verify page load performance impact using Lighthouse

**Completion Criteria**:
- Enhanced error handling with user-friendly messages for network, timeout, and HTTP errors
- Context truncation utility with word-boundary preservation and user notifications
- Message queue prevents double-sends and manages rapid submissions
- Build successful with all components compiling correctly

---

## Suggested MVP Scope

**Minimum Shippable Product**: Phase 1 + Phase 2 + Phase 3 (US1)

**Total MVP Tasks**: 17 tasks (T001-T017)
