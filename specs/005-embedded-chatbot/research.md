# Research & Best Practices: Embedded Chatbot UI for Docusaurus

**Feature**: 005-embedded-chatbot  
**Date**: 2025-12-22  
**Phase**: 0 (Research & Unknowns Resolution)

## Overview

This document captures research findings, best practices, and design decisions for implementing an embedded chatbot UI within a Docusaurus documentation site.

## Key Research Areas

### 1. Docusaurus Theme Integration Patterns

**Decision**: Use Docusaurus theme swizzling with Root component wrapper

**Rationale**:
- Docusaurus provides official swizzle mechanism for customizing theme components
- Root.jsx wrapper pattern allows global component injection
- Maintains upgrade compatibility with future Docusaurus versions

**Alternatives Considered**:
- Direct DOM manipulation: Rejected due to poor React integration
- Docusaurus plugin: Rejected as unnecessarily complex
- Custom HTML injection: Rejected due to limited React control

### 2. React State Management

**Decision**: Use React Context API + useReducer for chatbot state

**Rationale**:
- No external state libraries allowed per spec
- Context API sufficient for component-level state
- useReducer provides predictable state transitions

### 3. Text Selection Detection

**Decision**: Use Selection API + absolute positioning

**Rationale**:
- Standard browser API, well-supported
- Absolute positioning for floating button
- Boundary detection keeps button visible

### 4. Responsive Layout

**Decision**: CSS media queries + conditional rendering

**Breakpoints**:
- Desktop: >768px (sidebar overlay)
- Mobile: <=768px (full-screen overlay)

### 5. Theme Synchronization

**Decision**: Use Docusaurus useColorMode hook + CSS variables

**Rationale**:
- Built-in Docusaurus hook for theme state
- CSS variables for dynamic theming

### 6. Accessibility

**Decision**: Semantic HTML + ARIA + keyboard navigation

**Requirements**:
- Focus trap in panel
- Keyboard shortcuts (Ctrl+K, Escape)
- ARIA live regions
- WCAG AA contrast (4.5:1)

### 7. Performance

**Decision**: Lazy loading + React.memo

**Targets**:
- Initial load: <100ms
- Panel open: <1s
- Message render: <0.5s

### 8. Storage

**Decision**: sessionStorage for per-page conversation state

**Rationale**:
- Resets on page navigation per clarification
- Persists during page session

## Summary

All research complete. Ready for Phase 1: Design & Contracts.
