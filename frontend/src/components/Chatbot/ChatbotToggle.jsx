import React from 'react';
import { useChatbot } from '../../hooks/useChatbot';
import styles from './styles.module.css';

/**
 * Floating toggle button to open/close chatbot
 */
export default function ChatbotToggle() {
  const { state, togglePanel } = useChatbot();

  return (
    <button
      className={`${styles.chatbotToggle} ${state.isOpen ? styles.chatbotToggleOpen : ''}`}
      onClick={togglePanel}
      aria-label={state.isOpen ? "Close chatbot (Escape)" : "Open chatbot (Ctrl+K)"}
      aria-expanded={state.isOpen}
      aria-controls="chatbot-panel"
      title={state.isOpen ? "Close chatbot" : "Open chatbot"}
      type="button"
    >
      {state.isOpen ? (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true" focusable="false">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      ) : (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true" focusable="false">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      )}
    </button>
  );
}
