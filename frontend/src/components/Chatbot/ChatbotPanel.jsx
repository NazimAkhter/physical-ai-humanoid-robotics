import React, { useEffect, useRef } from 'react';
import { useChatbot } from '../../hooks/useChatbot';
import { useDocusaurusTheme } from '../../hooks/useDocusaurusTheme';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import styles from './styles.module.css';

/**
 * Main chatbot panel container
 */
export default function ChatbotPanel() {
  const { state, closePanel, sendMessage } = useChatbot();
  const { colorMode } = useDocusaurusTheme();
  const scrollPositionRef = useRef(0);
  const panelRef = useRef(null);
  const firstFocusableRef = useRef(null);
  const lastFocusableRef = useRef(null);

  // Preserve scroll position on mount/unmount
  useEffect(() => {
    if (typeof window === 'undefined') return;

    if (state.isOpen) {
      // Save current scroll position
      scrollPositionRef.current = window.scrollY;

      // Prevent body scroll on mobile when chatbot is open
      document.body.style.overflow = 'hidden';
      document.body.style.position = 'fixed';
      document.body.style.top = `-${scrollPositionRef.current}px`;
      document.body.style.width = '100%';
    } else {
      // Restore body scroll
      document.body.style.overflow = '';
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';

      // Restore scroll position
      window.scrollTo(0, scrollPositionRef.current);
    }

    return () => {
      // Cleanup on unmount
      document.body.style.overflow = '';
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
    };
  }, [state.isOpen]);

  // Focus management and focus trap
  useEffect(() => {
    if (!state.isOpen || !panelRef.current) return;

    // Get all focusable elements
    const focusableElements = panelRef.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    if (focusableElements.length === 0) return;

    firstFocusableRef.current = focusableElements[0];
    lastFocusableRef.current = focusableElements[focusableElements.length - 1];

    // Focus first element when panel opens
    firstFocusableRef.current?.focus();

    // Handle Tab key for focus trap
    const handleKeyDown = (event) => {
      if (event.key !== 'Tab') return;

      // Shift+Tab on first element: go to last
      if (event.shiftKey && document.activeElement === firstFocusableRef.current) {
        event.preventDefault();
        lastFocusableRef.current?.focus();
      }
      // Tab on last element: go to first
      else if (!event.shiftKey && document.activeElement === lastFocusableRef.current) {
        event.preventDefault();
        firstFocusableRef.current?.focus();
      }
    };

    panelRef.current.addEventListener('keydown', handleKeyDown);
    const currentPanel = panelRef.current;

    return () => {
      currentPanel?.removeEventListener('keydown', handleKeyDown);
    };
  }, [state.isOpen]);

  if (!state.isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div 
        className={styles.chatbotBackdrop}
        onClick={closePanel}
        aria-hidden="true"
      />
      
      {/* Panel */}
      <div 
        ref={panelRef}
        className={`${styles.chatbotPanel} chatbot-panel--${colorMode}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="chatbot-title"
      >
        {/* Header */}
        <div className={styles.chatbotHeader}>
          <h3 id="chatbot-title" className={styles.chatbotTitle}>
            AI Assistant
          </h3>
          <button
            className={styles.chatbotCloseButton}
            onClick={closePanel}
            aria-label="Close chatbot"
            type="button"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        {/* Context Info */}
        {state.currentContext.selectedText && (
          <div className={styles.chatbotContext} role="status" aria-live="polite">
            <small>Context: {state.currentContext.selectedText.substring(0, 100)}...</small>
          </div>
        )}

        {/* Messages */}
        <MessageList messages={state.messages} isLoading={state.isLoading} />

        {/* Error */}
        {state.error && (
          <div className={styles.chatbotError} role="alert" aria-live="assertive">
            {state.error}
          </div>
        )}

        {/* Input */}
        <MessageInput onSendMessage={sendMessage} disabled={state.isLoading} />
      </div>
    </>
  );
}
