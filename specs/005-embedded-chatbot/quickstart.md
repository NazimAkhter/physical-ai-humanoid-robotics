# Developer Quickstart: Embedded Chatbot UI

**Feature**: 005-embedded-chatbot  
**Date**: 2025-12-22

## Prerequisites

- Node.js 18+ installed
- Existing Docusaurus site running (frontend/ directory)
- Basic knowledge of React and Docusaurus

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Chatbot/               # All chatbot components here
│   │       ├── ChatbotPanel.jsx
│   │       ├── ChatbotToggle.jsx
│   │       ├── MessageList.jsx
│   │       ├── MessageInput.jsx
│   │       ├── TextSelectionPopup.jsx
│   │       └── styles.module.css
│   ├── hooks/
│   │   ├── useChatbot.js
│   │   ├── useTextSelection.js
│   │   └── useDocusaurusTheme.js
│   ├── theme/
│   │   └── Root.jsx                # Swizzled Docusaurus theme wrapper
│   └── css/
│       └── chatbot-theme.css       # Chatbot theme variables
└── package.json                    # No new dependencies needed
```

## Setup Steps

### 1. Swizzle Docusaurus Root Component

```bash
cd frontend
npm run swizzle @docusaurus/theme-classic Root -- --eject
```

This creates `src/theme/Root.jsx` where you'll wrap the app with ChatbotProvider.

### 2. Create Component Directory

```bash
mkdir -p src/components/Chatbot
mkdir -p src/hooks
```

### 3. Development Workflow

Start the Docusaurus dev server:

```bash
cd frontend
npm start
```

Site will be available at http://localhost:3000

### 4. Testing

Run tests (once implemented):

```bash
npm test
```

## Component Development Order

Implement components in this order to minimize dependencies:

1. **useChatbot.js** - State management hook (core logic)
2. **ChatbotToggle.jsx** - Simple button to test state
3. **MessageList.jsx** - Display messages
4. **MessageInput.jsx** - Input and send
5. **ChatbotPanel.jsx** - Assemble all sub-components
6. **TextSelectionPopup.jsx** - Advanced feature
7. **Root.jsx** - Wire everything together

## Key Integration Points

### Root.jsx (Theme Wrapper)

```jsx
import React from 'react';
import ChatbotProvider from '@site/src/components/Chatbot/ChatbotProvider';
import ChatbotToggle from '@site/src/components/Chatbot/ChatbotToggle';
import ChatbotPanel from '@site/src/components/Chatbot/ChatbotPanel';

export default function Root({children}) {
  return (
    <ChatbotProvider>
      {children}
      <ChatbotToggle />
      <ChatbotPanel />
    </ChatbotProvider>
  );
}
```

### Mock API for Development

Create `src/services/mockChatbotAPI.js`:

```javascript
export async function sendMessage(message, context) {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Return mock response
  return {
    message: `Mock response to: ${message}`,
    timestamp: Date.now()
  };
}
```

## Styling Approach

Use Docusaurus CSS variables for theming:

```css
/* src/components/Chatbot/styles.module.css */
.chatbotPanel {
  background: var(--ifm-background-color);
  color: var(--ifm-font-color-base);
  border: 1px solid var(--ifm-color-emphasis-300);
}
```

## Debugging Tips

1. **Panel not opening**: Check console for errors in useChatbot hook
2. **Theme not syncing**: Verify useColorMode import from '@docusaurus/theme-common'
3. **Selection popup not showing**: Check Selection API browser support
4. **Performance issues**: Use React DevTools Profiler to identify re-renders

## Resources

- Docusaurus Docs: https://docusaurus.io/docs
- React Hooks: https://react.dev/reference/react
- Selection API: https://developer.mozilla.org/en-US/docs/Web/API/Selection

## Next Steps

After setup complete, proceed to `/sp.tasks` to generate implementation task list.
