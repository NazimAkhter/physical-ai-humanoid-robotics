import { useContext } from 'react';
import { ChatbotContext } from '../components/Chatbot/ChatbotProvider';

/**
 * Custom hook to access chatbot state and actions
 * @returns {Object} Chatbot state and action methods
 */
export function useChatbot() {
  const context = useContext(ChatbotContext);
  
  if (!context) {
    throw new Error('useChatbot must be used within ChatbotProvider');
  }
  
  return context;
}
