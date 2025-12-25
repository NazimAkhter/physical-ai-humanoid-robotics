import React, { useRef, useEffect } from 'react';
import LoadingIndicator from './LoadingIndicator';
import styles from './styles.module.css';

/**
 * Scrollable message list displaying conversation history
 */
export default function MessageList({ messages, isLoading }) {
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div 
      className={styles.messageList} 
      role="log" 
      aria-live="polite" 
      aria-atomic="false"
      aria-label="Conversation messages"
    >
      {messages.length === 0 && !isLoading && (
        <div className={styles.emptyState} role="status">
          <p>Ask me anything about this documentation!</p>
        </div>
      )}
      
      {messages.map((message) => (
        <div
          key={message.id}
          className={`${styles.message} ${
            message.sender === 'user' ? styles.messageUser : styles.messageBot
          }`}
          role="article"
          aria-label={`${message.sender === 'user' ? 'You' : 'AI Assistant'} said`}
        >
          <div className={styles.messageContent}>{message.text}</div>
          <div className={styles.messageTimestamp} aria-label="Sent at">
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        </div>
      ))}
      
      {isLoading && <LoadingIndicator />}
      
      <div ref={messagesEndRef} aria-hidden="true" />
    </div>
  );
}
