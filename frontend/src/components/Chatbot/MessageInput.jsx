import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

/**
 * Message input field with send button and queue management
 */
export default function MessageInput({ onSendMessage, disabled }) {
  const [value, setValue] = useState('');
  const [messageQueue, setMessageQueue] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const queueRef = useRef([]);

  // Process message queue
  useEffect(() => {
    if (messageQueue.length > 0 && !isProcessing && !disabled) {
      setIsProcessing(true);
      const nextMessage = messageQueue[0];

      // Send the message
      onSendMessage(nextMessage);

      // Remove from queue after sending
      setMessageQueue((prev) => prev.slice(1));

      // Reset processing state after a brief delay
      setTimeout(() => {
        setIsProcessing(false);
      }, 500);
    }
  }, [messageQueue, isProcessing, disabled, onSendMessage]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmedValue = value.trim();

    if (trimmedValue && !disabled) {
      // If currently processing, add to queue
      if (isProcessing || messageQueue.length > 0) {
        setMessageQueue((prev) => [...prev, trimmedValue]);
      } else {
        // Otherwise send immediately
        setIsProcessing(true);
        onSendMessage(trimmedValue);
        setTimeout(() => {
          setIsProcessing(false);
        }, 500);
      }

      setValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form 
      className={styles.messageInputContainer} 
      onSubmit={handleSubmit}
      role="form"
      aria-label="Send message form"
    >
      <input
        type="text"
        className={styles.messageInput}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question..."
        disabled={disabled || isProcessing}
        aria-label="Message input"
        aria-required="false"
        aria-describedby="message-hint"
        maxLength={2000}
      />
      <span id="message-hint" className="sr-only">
        Press Enter to send, Shift+Enter for new line
        {messageQueue.length > 0 && ` (${messageQueue.length} message${messageQueue.length > 1 ? 's' : ''} queued)`}
      </span>
      <button
        type="submit"
        className={styles.sendButton}
        disabled={disabled || !value.trim()}
        aria-label="Send message"
        title="Send message"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true" focusable="false">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </form>
  );
}
