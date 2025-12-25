# Component Interfaces Contract

**Feature**: 005-embedded-chatbot  
**Date**: 2025-12-22

## Overview

This document defines the TypeScript/JSDoc interfaces for all chatbot components.

## Core Types

```typescript
// Message type
type Message = {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: number;
  contextRef?: string;
};

// Context information
type ContextInfo = {
  pageUrl: string;
  pageTitle: string;
  selectedText: string | null;
};

// Chatbot state
type ChatbotState = {
  isOpen: boolean;
  messages: Message[];
  isLoading: boolean;
  currentContext: ContextInfo;
  error: string | null;
};
```

## Component Props

### ChatbotPanel.jsx

```typescript
// No props (uses Context)
export default function ChatbotPanel(): JSX.Element;
```

### ChatbotToggle.jsx

```typescript
// No props (uses Context)
export default function ChatbotToggle(): JSX.Element;
```

### MessageList.jsx

```typescript
type MessageListProps = {
  messages: Message[];
  isLoading: boolean;
};

export default function MessageList(props: MessageListProps): JSX.Element;
```

### MessageInput.jsx

```typescript
type MessageInputProps = {
  onSendMessage: (text: string) => void;
  disabled: boolean;
};

export default function MessageInput(props: MessageInputProps): JSX.Element;
```

### TextSelectionPopup.jsx

```typescript
type TextSelectionPopupProps = {
  selectedText: string;
  position: { top: number; left: number };
  onAskAbout: () => void;
};

export default function TextSelectionPopup(props: TextSelectionPopupProps): JSX.Element;
```

## Custom Hooks

### useChatbot.js

```typescript
type UseChatbotReturn = {
  state: ChatbotState;
  openPanel: () => void;
  closePanel: () => void;
  togglePanel: () => void;
  sendMessage: (text: string) => Promise<void>;
  setContext: (context: Partial<ContextInfo>) => void;
  clearMessages: () => void;
};

export function useChatbot(): UseChatbotReturn;
```

### useTextSelection.js

```typescript
type UseTextSelectionReturn = {
  isVisible: boolean;
  position: { top: number; left: number } | null;
  selectedText: string;
};

export function useTextSelection(): UseTextSelectionReturn;
```

### useDocusaurusTheme.js

```typescript
type UseDocusaurusThemeReturn = {
  colorMode: 'light' | 'dark';
};

export function useDocusaurusTheme(): UseDocusaurusThemeReturn;
```
