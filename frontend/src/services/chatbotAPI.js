/**
 * Real Chatbot API Service
 * Connects to FastAPI backend for RAG-powered responses
 */

// Use hardcoded URL for now - works in both dev and production
const API_BASE_URL = 'http://127.0.0.1:3001';

/**
 * Send a message to the chatbot backend
 * @param {string} message - User's query
 * @param {Object} context - Page context (url, title, selectedText)
 * @returns {Promise<Object>} Response with message, sources, and timestamp
 */
export async function sendMessage(message, context) {
  try {
    // Call the FastAPI backend
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: message
      })
    });

    // Handle non-200 responses
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));

      if (response.status === 400) {
        throw new Error(errorData.detail?.detail || 'Invalid request');
      } else if (response.status === 422) {
        throw new Error('Query validation failed. Please check your input.');
      } else if (response.status === 429) {
        const error = new Error('Rate limit exceeded. Please wait a moment before trying again.');
        error.status = 429;
        throw error;
      } else if (response.status === 500) {
        throw new Error('Server error. Please try again later.');
      } else if (response.status === 503) {
        throw new Error('Service temporarily unavailable. Please try again in a moment.');
      } else {
        throw new Error('Failed to get response from chatbot');
      }
    }

    const data = await response.json();

    // Format the response with sources
    let formattedMessage = data.answer;

    // Append source citations if available
    if (data.sources && data.sources.length > 0) {
      formattedMessage += '\n\n📚 Sources:\n';
      data.sources.forEach((source, index) => {
        formattedMessage += `${index + 1}. [${source.title}](${source.url}) (score: ${source.score.toFixed(2)})\n`;
      });
    }

    return {
      message: formattedMessage,
      sources: data.sources || [],
      timestamp: Date.now()
    };

  } catch (error) {
    // Network errors
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      const netError = new Error('Cannot connect to chatbot service. Please ensure the backend is running.');
      netError.name = 'NetworkError';
      throw netError;
    }

    // Re-throw other errors
    throw error;
  }
}

/**
 * Check if the chatbot backend is healthy
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return await response.json();
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'unhealthy', error: error.message };
  }
}
