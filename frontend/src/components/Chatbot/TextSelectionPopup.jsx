import React, { useState, useEffect } from 'react';
import { useTextSelection } from '../../hooks/useTextSelection';
import { useChatbot } from '../../hooks/useChatbot';
import { prepareContext } from '../../utils/contextUtils';
import styles from './styles.module.css';

/**
 * Floating "Ask chatbot" button that appears when text is selected
 */
export default function TextSelectionPopup() {
  const selection = useTextSelection();
  const { openPanel, setContext } = useChatbot();
  const [showTruncationWarning, setShowTruncationWarning] = useState(false);

  // Reset warning when selection changes
  useEffect(() => {
    setShowTruncationWarning(false);
  }, [selection.text]);

  if (!selection.hasSelection) {
    return null;
  }

  const handleAskChatbot = () => {
    // Prepare context with truncation
    const context = prepareContext({
      selectedText: selection.text,
      pageUrl: typeof window !== 'undefined' ? window.location.href : '',
      pageTitle: typeof document !== 'undefined' ? document.title : ''
    });

    // Set context
    setContext(context);

    // Show warning if text was truncated
    if (context.truncationInfo?.wasTruncated) {
      setShowTruncationWarning(true);
      // Auto-hide warning after 5 seconds
      setTimeout(() => setShowTruncationWarning(false), 5000);
    }

    // Open chatbot panel
    openPanel();
  };

  // Position with boundary detection
  const getPosition = () => {
    const { x, y, rect } = selection;
    if (!rect) return {};

    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const buttonWidth = 150; // Approximate button width
    const buttonHeight = 40; // Approximate button height

    let left = x - buttonWidth / 2;
    let top = y;

    // Boundary detection - keep button in viewport
    if (left < 10) left = 10;
    if (left + buttonWidth > viewportWidth - 10) {
      left = viewportWidth - buttonWidth - 10;
    }
    if (top < 10) top = rect.bottom + 10; // Show below if too close to top
    if (top + buttonHeight > viewportHeight - 10) {
      top = rect.top - buttonHeight - 10; // Show above if too close to bottom
    }

    return {
      position: 'fixed',
      left: `${left}px`,
      top: `${top}px`,
      zIndex: 9999
    };
  };

  const isLongSelection = selection.text.length > 2000;

  return (
    <>
      <button
        className={styles.textSelectionPopup}
        onClick={handleAskChatbot}
        style={getPosition()}
        aria-label="Ask chatbot about selected text"
        type="button"
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          style={{ marginRight: '6px' }}
          aria-hidden="true"
          focusable="false"
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        Ask chatbot
        {isLongSelection && (
          <span className={styles.truncationBadge} aria-label="Text will be truncated">
            ✂
          </span>
        )}
      </button>

      {showTruncationWarning && (
        <div
          className={styles.truncationWarning}
          style={{
            position: 'fixed',
            bottom: '100px',
            right: '20px',
            zIndex: 10000
          }}
          role="alert"
          aria-live="polite"
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            style={{ marginRight: '8px', flexShrink: 0 }}
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>Selected text was truncated to 2,000 characters to fit context limits.</span>
        </div>
      )}
    </>
  );
}
