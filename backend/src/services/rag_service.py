"""
RAG (Retrieval-Augmented Generation) service implementation.
Coordinates the retrieval and generation components for the educational chatbot.
"""
from typing import List, Dict, Any
from .qdrant_service import qdrant_service
from .database import get_db, Conversation, Message
from sqlalchemy.orm import Session
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.qdrant = qdrant_service

    def retrieve_context(self, query: str, module: str = "vla-integration", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from the knowledge base using Qdrant
        """
        try:
            # Search for relevant documents
            search_results = self.qdrant.search_documents(query, limit=limit)

            # Filter results by module if specified
            if module:
                filtered_results = [
                    result for result in search_results
                    if result.get("metadata", {}).get("module") == module
                ]
                if not filtered_results:
                    # If no results for specific module, return all results
                    filtered_results = search_results
            else:
                filtered_results = search_results

            return filtered_results

        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise

    def generate_response(self, query: str, context: List[Dict[str, Any]], conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response using OpenAI GPT with retrieved context
        """
        try:
            import openai
            from openai import OpenAI
            client = OpenAI()

            # Format the context for the prompt
            context_str = "\n\n".join([f"Source: {ctx['doc_id']}\nContent: {ctx['content']}" for ctx in context])

            # Prepare the conversation history for the prompt
            history_str = ""
            if conversation_history:
                history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-5:]])  # Last 5 messages

            # Create the prompt with context
            prompt = f"""
You are an AI assistant for the Physical AI & Humanoid Robotics educational platform.
Your role is to help students learn about robotics, AI, and the integration of vision, language, and action systems.

Use the following context to answer the question:
{context_str}

Previous conversation history:
{history_str}

Question: {query}

Please provide an educational response that helps the student understand the concepts related to their question.
If the context doesn't contain relevant information, provide a general educational response based on your knowledge of robotics and AI.
Always maintain a helpful and educational tone appropriate for students learning about these advanced topics.
"""

            # Generate response using OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant for the Physical AI & Humanoid Robotics educational platform. Provide helpful, accurate, and educational responses to student questions about robotics, AI, and the integration of vision, language, and action systems."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def query_knowledge_base(self, query: str, module: str = "vla-integration", conversation_id: int = None) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve context and generate response
        """
        try:
            # Retrieve relevant context
            context = self.retrieve_context(query, module)

            # Get conversation history if conversation_id is provided
            conversation_history = []
            if conversation_id:
                db: Session = next(get_db())
                try:
                    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
                    if conv:
                        messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
                        conversation_history = [
                            {"role": msg.role, "content": msg.content}
                            for msg in messages
                        ]
                finally:
                    db.close()

            # Generate response with context
            response = self.generate_response(query, context, conversation_history)

            # Prepare the result
            result = {
                "query": query,
                "module": module,
                "response": response,
                "sources": [ctx["doc_id"] for ctx in context],
                "context_relevance_scores": [ctx["score"] for ctx in context],
                "timestamp": datetime.utcnow().isoformat()
            }

            return result

        except Exception as e:
            logger.error(f"Error in RAG query: {str(e)}")
            raise

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Add a document to the knowledge base
        """
        try:
            # Set default metadata if not provided
            if metadata is None:
                metadata = {}

            # Ensure module is specified in metadata
            if "module" not in metadata:
                metadata["module"] = "general"

            # Store in Qdrant
            result = self.qdrant.store_document(doc_id, content, metadata)
            return result

        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            raise

# Global instance for the service
rag_service = RAGService()