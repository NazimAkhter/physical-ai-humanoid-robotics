"""
Qdrant client configuration for RAG (Retrieval-Augmented Generation) functionality.
Handles vector storage and similarity search for the educational platform's knowledge base.
"""
import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import logging

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        # Initialize Qdrant client with environment variables
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if self.qdrant_api_key:
            self.client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                prefer_grpc=False  # Set to True for production if gRPC is available
            )
        else:
            self.client = QdrantClient(url=self.qdrant_url)

        # Collection name for the educational platform
        self.collection_name = "educational_knowledge_base"

        # Initialize the collection if it doesn't exist
        self._initialize_collection()

    def _initialize_collection(self):
        """
        Initialize the Qdrant collection for storing educational content vectors
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection with vector configuration
                # Using 1536 dimensions for OpenAI embeddings (text-embedding-ada-002)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )

                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection already exists: {self.collection_name}")

        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {str(e)}")
            raise

    def store_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None):
        """
        Store a document in the Qdrant collection
        """
        try:
            from openai import OpenAI
            client = OpenAI()

            # Generate embedding for the content
            response = client.embeddings.create(
                input=content,
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding

            # Prepare the point for Qdrant
            point = models.PointStruct(
                id=doc_id,
                vector=embedding,
                payload={
                    "content": content,
                    "metadata": metadata or {},
                    "doc_id": doc_id
                }
            )

            # Store in Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            return {"status": "success", "doc_id": doc_id}

        except Exception as e:
            logger.error(f"Error storing document in Qdrant: {str(e)}")
            raise

    def search_documents(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents based on the query
        """
        try:
            from openai import OpenAI
            client = OpenAI()

            # Generate embedding for the query
            response = client.embeddings.create(
                input=query,
                model="text-embedding-ada-002"
            )
            query_embedding = response.data[0].embedding

            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )

            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "doc_id": hit.payload.get("doc_id"),
                    "content": hit.payload.get("content"),
                    "metadata": hit.payload.get("metadata", {}),
                    "score": hit.score
                })

            return results

        except Exception as e:
            logger.error(f"Error searching documents in Qdrant: {str(e)}")
            raise

    def delete_document(self, doc_id: str):
        """
        Delete a document from the Qdrant collection
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[doc_id]
                )
            )
            return {"status": "success", "doc_id": doc_id}

        except Exception as e:
            logger.error(f"Error deleting document from Qdrant: {str(e)}")
            raise

# Global instance for the service
qdrant_service = QdrantService()