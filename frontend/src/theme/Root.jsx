import React from 'react';
import ChatbotProvider from '@site/src/components/Chatbot/ChatbotProvider';
import ChatbotToggle from '@site/src/components/Chatbot/ChatbotToggle';
import ChatbotPanel from '@site/src/components/Chatbot/ChatbotPanel';
import TextSelectionPopup from '@site/src/components/Chatbot/TextSelectionPopup';

export default function Root({children}) {
  return (
    <>
      {children}
      <ChatbotProvider>
        <TextSelectionPopup />
        <ChatbotToggle />
        <ChatbotPanel />
      </ChatbotProvider>
    </>
  );
}
