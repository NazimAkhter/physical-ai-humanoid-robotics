/**
 * Mock Chatbot API Service
 * Simulates backend API for development and testing
 */

export async function sendMessage(message, context) {
  // Simulate network delay (500ms - 1500ms)
  const delay = Math.random() * 1000 + 500;
  await new Promise(resolve => setTimeout(resolve, delay));
  
  // Simulate occasional errors (10% chance)
  if (Math.random() < 0.1) {
    throw new Error('Mock API error: Service temporarily unavailable');
  }
  
  // Generate mock response based on context
  let response = `Thanks for your question about "${context.pageTitle}".`;
  
  if (context.selectedText) {
    response += ` Regarding "${context.selectedText.substring(0, 50)}..."`;
  }
  
  response += ` This is a mock response. The actual chatbot backend will provide real answers based on the book content.`;
  
  return {
    message: response,
    timestamp: Date.now()
  };
}
