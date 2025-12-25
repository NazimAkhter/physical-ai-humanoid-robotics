# Implementation Plan: Embedded Chatbot UI for Docusaurus Book

**Branch**: `005-embedded-chatbot` | **Date**: 2025-12-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-embedded-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an embedded chatbot UI component for the Docusaurus-based Physical AI & Humanoid Robotics documentation site. The component will enable readers to interact with an AI assistant directly within the documentation, supporting context-aware questions based on the current page or selected text. The UI must be responsive (desktop sidebar overlay, mobile full-screen), theme-aware (light/dark modes), accessible (keyboard navigation, screen readers), and performant (minimal page load impact). Conversation state resets on page navigation, and the chatbot integrates seamlessly with existing Docusaurus theme styling using CSS variables.

## Technical Context

**Language/Version**: JavaScript/TypeScript (ES2020+), React 18.x (already in Docusaurus)  
**Primary Dependencies**:
- @docusaurus/core: ^3.1.0 (existing)
- @docusaurus/preset-classic: ^3.1.0 (existing)
- react: ^18.0.0 (existing)
- react-dom: ^18.0.0 (existing)
- No additional external dependencies (per FR constraint)

**Storage**: Browser sessionStorage for conversation state (in-memory during page session); no persistent storage required  
**Testing**: Jest + React Testing Library (standard Docusaurus testing setup)  
**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)  
**Project Type**: Web application (frontend-only, embedded within existing Docusaurus site)  
**Performance Goals**:
- Chatbot panel opens in <1s (SC-001)
- Message submission responds within 0.5s for UI feedback (SC-002)
- Page load increase <100ms due to chatbot initialization (SC-010)
- Theme switching <0.5s (SC-006)

**Constraints**:
- Must use only Docusaurus CSS variables and theme tokens (no external UI libraries)
- Must not introduce new npm dependencies beyond existing Docusaurus packages
- Must work without page reloads (client-side state management only)
- Must be accessible (WCAG AA contrast ratios, keyboard navigation, screen readers)
- Timeline: Complete within 1-2 weeks

**Scale/Scope**:
- Single chatbot component (1 primary React component + 3-5 sub-components)
- Responsive layouts (2 breakpoints: desktop >768px, mobile <768px)
- ~500-800 lines of React/JSX + ~200-300 lines of CSS
- 5-7 functional requirements mapped to component features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Alignment with Core Principles

✅ **Spec-Driven Development**: This plan strictly follows Spec-Kit Plus workflow (spec → clarify → plan → tasks)

✅ **Seamless Integration**: Chatbot UI integrates tightly with existing Docusaurus site; uses theme CSS variables for consistency

✅ **Reproducibility**: Component will be built with standard React patterns; all code testable and deployable

✅ **Tooling Constraint**: Using Claude Code and Spec-Kit Plus exclusively for generation (this planning session)

### Alignment with Key Standards

✅ **Frontend/Book**: Component built for Docusaurus (latest stable: 3.1.0); will deploy to GitHub Pages with rest of book

✅ **Content Structure**: Feature enhances user experience across all 4 modules + capstone (no content changes required)

✅ **Feature Requirement**: Implements context-aware queries based on user-selected text (FR-007: floating button near selection)

### Alignment with Constraints

✅ **Tooling**: Using Claude Code and Spec-Kit Plus for generation

✅ **Hosting**: Component will be part of GitHub Pages deployment

N/A **Database Limits**: No database involved (frontend-only, sessionStorage)

✅ **Curriculum Alignment**: Feature enhances existing content without altering curriculum structure

### Constitution Gate Status

**PASS** ✅ - All constitution requirements met. No violations detected.


## Project Structure

### Documentation (this feature)

```text
specs/005-embedded-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── Chatbot/
│   │   │   ├── ChatbotPanel.jsx          # Main chatbot container component
│   │   │   ├── ChatbotToggle.jsx         # Floating toggle button
│   │   │   ├── ChatbotHeader.jsx         # Panel header with title and close button
│   │   │   ├── MessageList.jsx           # Scrollable conversation display
│   │   │   ├── MessageInput.jsx          # Text input + send button
│   │   │   ├── TextSelectionPopup.jsx    # Floating "Ask chatbot" button for selected text
│   │   │   ├── LoadingIndicator.jsx      # Loading spinner for API calls
│   │   │   └── styles.module.css         # Component-specific styles using CSS modules
│   │   └── [other existing components]/
│   ├── hooks/
│   │   ├── useChatbot.js                 # Custom hook for chatbot state management
│   │   ├── useTextSelection.js           # Custom hook for text selection detection
│   │   └── useDocusaurusTheme.js         # Custom hook for theme synchronization
│   ├── theme/
│   │   └── Root.jsx                      # Docusaurus theme wrapper (swizzled component)
│   ├── pages/
│   │   └── [existing pages]/
│   └── css/
│       ├── custom.css                    # Global styles (existing)
│       └── chatbot-theme.css             # Chatbot theme variables and overrides
├── static/
│   └── [existing static assets]/
├── docusaurus.config.js                  # No changes required (uses existing config)
├── package.json                          # No new dependencies
└── sidebars.js                           # No changes required

tests/
└── chatbot/
    ├── ChatbotPanel.test.jsx
    ├── MessageList.test.jsx
    ├── TextSelectionPopup.test.jsx
    └── useChatbot.test.js
```

**Structure Decision**: Web application (Option 2) with frontend-only changes. All code lives under `frontend/src/components/Chatbot/`. No backend changes required as per spec (chatbot backend/RAG logic is out of scope). Component integrates with existing Docusaurus site structure via theme swizzling (Root.jsx wrapper pattern).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. Constitution Check passed all gates.

