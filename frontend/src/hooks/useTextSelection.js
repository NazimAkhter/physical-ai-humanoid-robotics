import { useState, useEffect } from 'react';

/**
 * Custom hook to detect text selection on the page
 * @returns {Object} Selection state with text and position
 */
export function useTextSelection() {
  const [selection, setSelection] = useState({
    text: '',
    hasSelection: false,
    x: 0,
    y: 0,
    rect: null
  });

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleSelectionChange = () => {
      const sel = window.getSelection();
      const text = sel?.toString().trim() || '';

      if (text.length > 0) {
        const range = sel.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        setSelection({
          text,
          hasSelection: true,
          x: rect.left + rect.width / 2,
          y: rect.top - 10, // Position above selection
          rect: {
            top: rect.top,
            left: rect.left,
            bottom: rect.bottom,
            right: rect.right,
            width: rect.width,
            height: rect.height
          }
        });
      } else {
        setSelection({
          text: '',
          hasSelection: false,
          x: 0,
          y: 0,
          rect: null
        });
      }
    };

    // Listen for mouseup events (selection complete)
    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('selectionchange', handleSelectionChange);

    return () => {
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('selectionchange', handleSelectionChange);
    };
  }, []);

  return selection;
}
