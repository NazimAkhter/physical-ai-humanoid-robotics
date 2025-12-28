import React, { createContext, useReducer, useEffect, useCallback } from 'react';
import { sendMessage as sendMessageAPI } from '../../services/chatbotAPI';

export const ChatbotContext = createContext(null);

// Initial state
const initialState = {
  isOpen: false,
  messages: [],
  isLoading: false,
  currentContext: {
    pageUrl: typeof window !== 'undefined' ? window.location.href : '',
    pageTitle: typeof document !== 'undefined' ? document.title : '',
    selectedText: null
  },
  error: null
};

// Reducer
function chatbotReducer(state, action) {
  switch (action.type) {
    case 'OPEN_PANEL':
      return { ...state, isOpen: true };
    case 'CLOSE_PANEL':
      return { ...state, isOpen: false };
    case 'TOGGLE_PANEL':
      return { ...state, isOpen: !state.isOpen };
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, {
          id: Date.now().toString() + Math.random(),
          text: action.payload.text,
          sender: action.payload.sender,
          timestamp: Date.now(),
          contextRef: action.payload.contextRef
        }]
      };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_CONTEXT':
      return {
        ...state,
        currentContext: { ...state.currentContext, ...action.payload }
      };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'CLEAR_MESSAGES':
      return { ...state, messages: [] };
    case 'RESTORE_FROM_STORAGE':
      return { ...state, ...action.payload };
    default:
      return state;
  }
}

export default function ChatbotProvider({ children }) {
  const [state, dispatch] = useReducer(chatbotReducer, initialState);

  // Load from sessionStorage on mount
  useEffect(() => {
    const stored = sessionStorage.getItem('chatbot-state');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        dispatch({ type: 'RESTORE_FROM_STORAGE', payload: parsed });
      } catch (e) {
        console.error('Failed to restore chatbot state:', e);
      }
    }
  }, []);

  // Save to sessionStorage on state change
  useEffect(() => {
    sessionStorage.setItem('chatbot-state', JSON.stringify({
      messages: state.messages,
      currentContext: state.currentContext
    }));
  }, [state.messages, state.currentContext]);

  // Actions
  const openPanel = useCallback(() => dispatch({ type: 'OPEN_PANEL' }), []);
  const closePanel = useCallback(() => dispatch({ type: 'CLOSE_PANEL' }), []);
  const togglePanel = useCallback(() => dispatch({ type: 'TOGGLE_PANEL' }), []);
  
  const sendMessage = useCallback(async (text) => {
    if (!text.trim()) return;
    
    // Add user message
    dispatch({ type: 'ADD_MESSAGE', payload: { text, sender: 'user' } });
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });
    
    try {
      const response = await sendMessageAPI(text, state.currentContext);
      dispatch({ type: 'ADD_MESSAGE', payload: { text: response.message, sender: 'bot' } });
    } catch (error) {
      // Enhanced error handling with user-friendly messages
      let errorMessage = 'Failed to send message. Please try again.';
      
      if (error.message) {
        errorMessage = error.message;
      }
      
      if (error.name === 'NetworkError' || error.message.includes('network')) {
        errorMessage = 'Network error. Please check your internet connection and try again.';
      } else if (error.name === 'TimeoutError' || error.message.includes('timeout')) {
        errorMessage = 'Request timed out. The server took too long to respond. Please try again.';
      } else if (error.status === 429) {
        errorMessage = 'Too many requests. Please wait a moment before trying again.';
      } else if (error.status === 500 || error.status === 503) {
        errorMessage = 'Server error. The service is temporarily unavailable. Please try again later.';
      } else if (error.status === 404) {
        errorMessage = 'Service not found. Please contact support if this persists.';
      }
      
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      
      // Log error for debugging (only in development)
      if (typeof process !== 'undefined' && process.env.NODE_ENV === 'development') {
        console.error('Chatbot API Error:', error);
      }
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, [state.currentContext]);
  
  const setContext = useCallback((context) => {
    dispatch({ type: 'SET_CONTEXT', payload: context });
  }, []);
  
  const clearMessages = useCallback(() => {
    dispatch({ type: 'CLEAR_MESSAGES' });
  }, []);

  // Keyboard shortcut listener (Ctrl/Cmd + K to toggle chatbot)
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleKeyDown = (event) => {
      // Ctrl+K or Cmd+K to toggle chatbot
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        togglePanel();
      }
      
      // Escape to close chatbot
      if (event.key === 'Escape' && state.isOpen) {
        event.preventDefault();
        closePanel();
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [state.isOpen, togglePanel, closePanel]);

  const value = {
    state,
    openPanel,
    closePanel,
    togglePanel,
    sendMessage,
    setContext,
    clearMessages
  };

  return (
    <ChatbotContext.Provider value={value}>
      {children}
    </ChatbotContext.Provider>
  );
}
