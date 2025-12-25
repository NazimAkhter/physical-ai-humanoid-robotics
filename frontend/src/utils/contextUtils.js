/**
 * Context Management Utilities
 * Handles context length truncation and validation
 */

const MAX_CONTEXT_LENGTH = 2000; // FR-016: Maximum context length

/**
 * Truncates context to maximum allowed length
 * @param {string} text - The text to truncate
 * @param {number} maxLength - Maximum length (default: 2000)
 * @returns {Object} { text: string, wasTruncated: boolean, originalLength: number }
 */
export function truncateContext(text, maxLength = MAX_CONTEXT_LENGTH) {
  if (!text || typeof text !== 'string') {
    return {
      text: '',
      wasTruncated: false,
      originalLength: 0
    };
  }

  const trimmed = text.trim();
  const originalLength = trimmed.length;

  if (originalLength <= maxLength) {
    return {
      text: trimmed,
      wasTruncated: false,
      originalLength
    };
  }

  // Truncate at word boundary if possible
  let truncated = trimmed.substring(0, maxLength);
  const lastSpace = truncated.lastIndexOf(' ');

  if (lastSpace > maxLength * 0.8) {
    // Only break at word if we're at least 80% of max length
    truncated = truncated.substring(0, lastSpace);
  }

  return {
    text: truncated,
    wasTruncated: true,
    originalLength
  };
}

/**
 * Gets a user-friendly truncation message
 * @param {number} originalLength - Original text length
 * @param {number} maxLength - Maximum allowed length
 * @returns {string} Truncation notification message
 */
export function getTruncationMessage(originalLength, maxLength = MAX_CONTEXT_LENGTH) {
  const truncatedChars = originalLength - maxLength;
  return `Text was truncated from ${originalLength.toLocaleString()} to ${maxLength.toLocaleString()} characters (${truncatedChars.toLocaleString()} characters removed) to fit context limits.`;
}

/**
 * Validates and prepares context object for chatbot
 * @param {Object} context - Context object { pageUrl, pageTitle, selectedText }
 * @returns {Object} Validated and truncated context
 */
export function prepareContext(context) {
  const prepared = {
    pageUrl: context.pageUrl || '',
    pageTitle: context.pageTitle || '',
    selectedText: null,
    truncationInfo: null
  };

  if (context.selectedText) {
    const result = truncateContext(context.selectedText);
    prepared.selectedText = result.text;

    if (result.wasTruncated) {
      prepared.truncationInfo = {
        wasTruncated: true,
        originalLength: result.originalLength,
        message: getTruncationMessage(result.originalLength)
      };
    }
  }

  return prepared;
}
