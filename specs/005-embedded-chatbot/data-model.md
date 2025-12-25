# Data Model: Embedded Chatbot UI

**Feature**: 005-embedded-chatbot  
**Date**: 2025-12-22  
**Phase**: 1 (Design & Contracts)

## Overview

This document defines the data structures and state management for the embedded chatbot UI component. Since this is a frontend-only feature with no backend persistence, the data model focuses on client-side state and component interfaces.

## State Management Architecture

### ChatbotContext (Global State)

Managed via React Context API + useReducer

```typescript
interface ChatbotState {
  isOpen: boolean;              // Panel visibility
  messages: Message[];          // Conversation history
  isLoading: boolean;           // API call in progress
  currentContext: ContextInfo;  // Page/selection context
  error: string | null;         // Error message if any
}

interface Message {
  id: string;                   // Unique message ID (UUID)
  text: string;                 // Message content
  sender: 'user' | 'bot';       // Message sender type
  timestamp: number;            // Unix timestamp (Date.now())
  contextRef?: string;          // Optional reference to context used
}

interface ContextInfo {
  pageUrl: string;              // Current documentation page URL
  pageTitle: string;            // Current page title
  selectedText: string | null;  // User-selected text (if any)
}
```

### State Actions (Reducer)

```typescript
type ChatbotAction =
  | { type: 'OPEN_PANEL' }
  | { type: 'CLOSE_PANEL' }
  | { type: 'TOGGLE_PANEL' }
  | { type: 'ADD_MESSAGE'; payload: { text: string; sender: 'user' | 'bot' } }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_CONTEXT'; payload: Partial<ContextInfo> }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CLEAR_MESSAGES' }
  | { type: 'RESTORE_FROM_STORAGE'; payload: ChatbotState };
```

---

## Component Prop Interfaces

### ChatbotPanel

Main container component

```typescript
interface ChatbotPanelProps {
  // No props needed; uses ChatbotContext
}
```

### ChatbotToggle

Floating toggle button

```typescript
interface ChatbotToggleProps {
  // No props needed; uses ChatbotContext
}
```

### MessageList

Scrollable message display

```typescript
interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}
```

### MessageInput

Text input and send button

```typescript
interface MessageInputProps {
  onSendMessage: (text: string) => void;
  disabled: boolean;  // Disabled while loading
}
```

### TextSelectionPopup

Floating button for text selection

```typescript
interface TextSelectionPopupProps {
  selectedText: string;
  position: { top: number; left: number };
  onAskAbout: () => void;
}
```

---

## Session Storage Schema

Data persisted in browser sessionStorage (cleared on page navigation)

```typescript
// Key: 'chatbot-state'
interface StoredState {
  messages: Message[];
  currentContext: ContextInfo;
  timestamp: number;  // When state was saved
}
```

---

## Component State (Local)

### TextSelectionPopup Component

```typescript
interface SelectionState {
  isVisible: boolean;
  position: { top: number; left: number };
  selectedText: string;
}
```

### MessageInput Component

```typescript
interface InputState {
  value: string;  // Current input text
}
```

---

## Validation Rules

### Message

- `text`: Min 1 character, max 2000 characters
- `sender`: Must be 'user' or 'bot'
- `timestamp`: Must be valid Unix timestamp

### ContextInfo

- `selectedText`: If not null, max 2000 characters (enforced by FR-016)
- `pageUrl`: Must be valid URL format
- `pageTitle`: Min 1 character, max 200 characters

---

## Entity Relationships

```
ChatbotContext (1) ──> (*) Message
ChatbotContext (1) ──> (1) ContextInfo
TextSelectionPopup (1) ──> (1) SelectionState (local)
MessageInput (1) ──> (1) InputState (local)
```

---

## State Transitions

```
Initial State:
  isOpen: false
  messages: []
  isLoading: false
  currentContext: { pageUrl, pageTitle, selectedText: null }
  error: null

User opens panel:
  OPEN_PANEL -> isOpen: true

User sends message:
  1. ADD_MESSAGE (user) -> messages: [...messages, userMessage]
  2. SET_LOADING (true) -> isLoading: true
  3. [API call happens]
  4. ADD_MESSAGE (bot) -> messages: [...messages, botMessage]
  5. SET_LOADING (false) -> isLoading: false

User closes panel:
  CLOSE_PANEL -> isOpen: false (messages retained)

Page navigation:
  CLEAR_MESSAGES -> messages: [], context reset
```

---

## Next Steps

- Define component contracts in contracts/ directory
- Create quickstart.md with developer setup instructions
