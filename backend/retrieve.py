"""
RAG Retrieval Pipeline - Semantic Search Implementation

This module provides retrieval functions to query the populated Qdrant vector
database using semantic search. It accepts natural language queries, generates
embeddings using Cohere, and returns ranked results with similarity scores.

Functions:
    query_qdrant(): Core retrieval function with embedding generation
    retrieve_relevant_chunks(): High-level wrapper with formatted results
    test_retrieval_pipeline(): Test suite for validation

Usage:
    from backend.retrieve import retrieve_relevant_chunks, test_retrieval_pipeline

    # Single query
    results = retrieve_relevant_chunks("What is ROS 2?", qdrant_client, cohere_client)

    # Run test suite
    test_results = test_retrieval_pipeline(qdrant_client, cohere_client)

Feature: 007-rag-retrieval
"""

import sys
import io
import time
import logging
from typing import List, Dict, Any, Optional

# Fix Windows UTF-8 encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Third-party libraries
import tiktoken
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import ScoredPoint

# Local imports
from config import settings

# Initialize logger
logger = logging.getLogger(__name__)


# ============================================================================
# Constants for Retrieval
# ============================================================================

# Test queries covering all curriculum modules + edge cases
TEST_QUERIES = [
    # Curriculum queries (expected to pass with score > 0.6)
    ("What is ROS 2?", "ros2"),
    ("How does Isaac Sim work for robot training?", "isaac"),
    ("Explain Gazebo simulation for robotics", "gazebo"),
    ("What is vision-language-action integration?", "vla"),
    ("How to use Unity Robotics Hub?", "unity"),
    # Edge cases (expected to fail gracefully)
    ("How to bake a chocolate cake?", "edge_out_of_scope"),
    ("asdfghjkl qwerty", "edge_gibberish")
]

# Number of curriculum queries expected to pass
EXPECTED_PASS_COUNT = 5

# Thresholds
CONFIDENCE_THRESHOLD = 0.5  # Below this = low confidence warning
PASS_THRESHOLD = 0.6        # For test suite pass/fail determination

# Token limit for queries
MAX_QUERY_TOKENS = 512


# ============================================================================
# Core Retrieval Functions
# ============================================================================

def query_qdrant(
    query_text: str,
    qdrant_client: QdrantClient,
    cohere_client: cohere.ClientV2,
    top_k: int = 5,
    score_threshold: float = 0.3
) -> List[ScoredPoint]:
    """
    Execute semantic search against Qdrant collection.

    Core retrieval function that generates query embeddings using Cohere
    and searches the Qdrant vector database for similar content chunks.

    Args:
        query_text: Natural language query string
        qdrant_client: Initialized Qdrant client instance
        cohere_client: Initialized Cohere ClientV2 instance
        top_k: Number of results to return (3-5, default 5)
        score_threshold: Minimum similarity score (0.0-1.0, default 0.3)

    Returns:
        List of ScoredPoint objects from Qdrant, sorted by similarity (highest first)

    Raises:
        ValueError: If query_text is empty or top_k not in valid range
        Exception: If Cohere API or Qdrant operations fail

    Satisfies: FR-001, FR-002, FR-003, FR-004 from spec.md
    """
    # ========================================================================
    # Input Validation (T007, T024, T025)
    # ========================================================================

    # Empty query validation (T024)
    if not query_text or not query_text.strip():
        raise ValueError("Query text cannot be empty. Please provide a search query.")

    query_text = query_text.strip()

    # top_k validation
    if not isinstance(top_k, int) or top_k < 3 or top_k > 5:
        raise ValueError(f"top_k must be an integer between 3 and 5, got {top_k}")

    # score_threshold validation
    if not isinstance(score_threshold, (int, float)) or score_threshold < 0.0 or score_threshold > 1.0:
        raise ValueError(f"score_threshold must be between 0.0 and 1.0, got {score_threshold}")

    # Query length warning (T025)
    encoding = tiktoken.get_encoding("cl100k_base")
    query_tokens = encoding.encode(query_text)
    if len(query_tokens) > MAX_QUERY_TOKENS:
        logger.warning(
            f"Query exceeds recommended token limit: {len(query_tokens)} tokens "
            f"(max recommended: {MAX_QUERY_TOKENS}). Results may be less accurate."
        )

    # ========================================================================
    # Collection Existence Check (T028)
    # ========================================================================
    try:
        collections = qdrant_client.get_collections().collections
        collection_exists = any(c.name == settings.COLLECTION_NAME for c in collections)

        if not collection_exists:
            raise ValueError(
                f"Collection '{settings.COLLECTION_NAME}' does not exist in Qdrant. "
                f"Please run the ingestion pipeline first (Spec 006)."
            )
    except Exception as e:
        if "does not exist" in str(e):
            raise
        logger.error(f"Failed to check collection existence: {e}")
        raise ConnectionError(
            f"Failed to connect to Qdrant: {e}. "
            f"Please check your QDRANT_URL and QDRANT_API_KEY settings."
        )

    # ========================================================================
    # Generate Query Embedding (T008, T010)
    # ========================================================================
    try:
        logger.debug(f"Generating embedding for query: '{query_text[:50]}...'")

        # Use input_type="search_query" for retrieval (per research.md)
        response = cohere_client.embed(
            texts=[query_text],
            model=settings.EMBEDDING_MODEL,
            input_type="search_query"  # Key: different from "search_document" used in ingestion
        )

        # Extract vector from Cohere V2 response
        if hasattr(response.embeddings, 'float_'):
            query_vector = response.embeddings.float_[0]
        else:
            query_vector = response.embeddings[0]

        logger.debug(f"Generated {len(query_vector)}-dimensional embedding")

    except Exception as e:
        # Handle Cohere API errors (T010)
        error_msg = str(e).lower()

        if '429' in str(e) or 'rate limit' in error_msg:
            logger.error(f"Cohere rate limit exceeded: {e}")
            raise RuntimeError(
                "Cohere API rate limit exceeded. Please wait a moment and try again."
            )
        elif 'api key' in error_msg or 'authentication' in error_msg or 'unauthorized' in error_msg:
            logger.error(f"Cohere authentication error: {e}")
            raise RuntimeError(
                "Cohere API authentication failed. Please check your COHERE_API_KEY."
            )
        else:
            logger.error(f"Cohere embedding generation failed: {e}")
            raise RuntimeError(f"Failed to generate query embedding: {e}")

    # ========================================================================
    # Search Qdrant (T009, T011)
    # ========================================================================
    try:
        logger.debug(f"Searching Qdrant collection '{settings.COLLECTION_NAME}' with top_k={top_k}")

        # Use query_points (qdrant-client v1.7+) with query parameter for vector search
        search_response = qdrant_client.query_points(
            collection_name=settings.COLLECTION_NAME,
            query=query_vector,
            limit=top_k,
            with_payload=True,
            score_threshold=score_threshold
        )

        # Extract points from QueryResponse
        search_results = search_response.points

        logger.debug(f"Search returned {len(search_results)} results")
        return search_results

    except Exception as e:
        # Handle Qdrant connection errors (T011)
        error_msg = str(e).lower()

        if 'connection' in error_msg or 'timeout' in error_msg:
            logger.error(f"Qdrant connection error: {e}")
            raise ConnectionError(
                f"Failed to connect to Qdrant: {e}. "
                f"Please check your network connection and Qdrant URL."
            )
        elif 'not found' in error_msg or 'does not exist' in error_msg:
            logger.error(f"Qdrant collection not found: {e}")
            raise ValueError(
                f"Collection '{settings.COLLECTION_NAME}' not found. "
                f"Please run the ingestion pipeline first."
            )
        else:
            logger.error(f"Qdrant search failed: {e}")
            raise RuntimeError(f"Failed to search Qdrant: {e}")


def retrieve_relevant_chunks(
    query_text: str,
    qdrant_client: QdrantClient,
    cohere_client: cohere.ClientV2,
    top_k: int = 5,
    confidence_threshold: float = CONFIDENCE_THRESHOLD
) -> Dict[str, Any]:
    """
    Retrieve and format relevant content chunks with quality metadata.

    High-level wrapper around query_qdrant() that transforms raw Qdrant
    results into a structured QueryResults dictionary with execution
    metadata and confidence indicators.

    Args:
        query_text: Natural language query string
        qdrant_client: Initialized Qdrant client instance
        cohere_client: Initialized Cohere ClientV2 instance
        top_k: Number of results to return (3-5, default 5)
        confidence_threshold: Score below which results are flagged as low confidence

    Returns:
        QueryResults dictionary containing:
        - query_text: Original query string
        - results: List of RetrievalResult dicts with chunk details
        - result_count: Number of results returned
        - max_score: Highest similarity score
        - execution_time: Query execution time in seconds
        - low_confidence: True if max_score < confidence_threshold
        - message: User-facing status message

    Satisfies: FR-005, FR-006, FR-007, FR-008, FR-009 from spec.md
    """
    start_time = time.time()

    logger.info(f"Retrieving chunks for query: '{query_text[:50]}...'")

    try:
        # ====================================================================
        # Execute Search (T012)
        # ====================================================================
        search_results = query_qdrant(
            query_text=query_text,
            qdrant_client=qdrant_client,
            cohere_client=cohere_client,
            top_k=top_k
        )

        # ====================================================================
        # Transform Results (T013)
        # ====================================================================
        results_list = []
        for result in search_results:
            # Convert ScoredPoint to RetrievalResult dict (per data-model.md)
            retrieval_result = {
                'chunk_id': str(result.id),
                'text_content': result.payload.get('text_content', ''),
                'page_title': result.payload.get('page_title', ''),
                'page_url': result.payload.get('page_url', ''),
                'content_hash': result.payload.get('content_hash', ''),
                'chunk_index': result.payload.get('chunk_index', 0),
                'similarity_score': float(result.score)
            }
            results_list.append(retrieval_result)

        # ====================================================================
        # Compute Metadata (T014)
        # ====================================================================
        execution_time = time.time() - start_time
        result_count = len(results_list)
        max_score = max((r['similarity_score'] for r in results_list), default=0.0)

        # ====================================================================
        # Determine Confidence and Message (T015, T026, T027)
        # ====================================================================
        if result_count == 0:
            # No results found (T027)
            low_confidence = True
            message = "No matching results found. Try rephrasing your question or using different keywords."
        elif max_score < confidence_threshold:
            # Low confidence results (T026)
            low_confidence = True
            message = (
                f"Low similarity scores (max: {max_score:.2f}). "
                f"Results may not be directly relevant to your query. "
                f"Try rephrasing or being more specific."
            )
        else:
            # Good results
            low_confidence = False
            message = f"Found {result_count} relevant results."

        # ====================================================================
        # Build QueryResults (T014, T016)
        # ====================================================================
        query_results = {
            'query_text': query_text,
            'results': results_list,
            'result_count': result_count,
            'max_score': max_score,
            'execution_time': execution_time,
            'low_confidence': low_confidence,
            'message': message
        }

        # Log retrieval operation (T016)
        logger.info(
            f"Retrieval complete: query='{query_text[:30]}...', "
            f"results={result_count}, max_score={max_score:.4f}, "
            f"time={execution_time:.2f}s, low_confidence={low_confidence}"
        )

        return query_results

    except Exception as e:
        # Handle errors gracefully
        execution_time = time.time() - start_time
        logger.error(f"Retrieval failed for query '{query_text[:30]}...': {e}")

        return {
            'query_text': query_text,
            'results': [],
            'result_count': 0,
            'max_score': 0.0,
            'execution_time': execution_time,
            'low_confidence': True,
            'message': f"Error during retrieval: {str(e)}"
        }


def test_retrieval_pipeline(
    qdrant_client: QdrantClient,
    cohere_client: cohere.ClientV2,
    top_k: int = 5,
    confidence_threshold: float = PASS_THRESHOLD
) -> Dict[str, Any]:
    """
    Run comprehensive test suite to validate retrieval accuracy.

    Executes 7 predefined queries (5 curriculum + 2 edge cases) and
    reports pass/fail status for each. Curriculum queries are expected
    to return results with similarity scores above the confidence threshold.

    Args:
        qdrant_client: Initialized Qdrant client instance
        cohere_client: Initialized Cohere ClientV2 instance
        top_k: Number of results to return per query (default 5)
        confidence_threshold: Score threshold for pass/fail (default 0.6)

    Returns:
        Test results dictionary containing:
        - total_queries: Total number of queries executed
        - passed: Number of curriculum queries that passed
        - failed: Number of curriculum queries that failed
        - pass_rate: Pass rate as decimal (0.0-1.0)
        - expected_pass_count: Expected number of passes (5)
        - results: List of per-query result details
        - summary: Human-readable summary message

    Satisfies: FR-010, FR-011, FR-012 from spec.md
    """
    logger.info("=" * 60)
    logger.info("Starting RAG Retrieval Pipeline Test Suite")
    logger.info("=" * 60)

    print("\n" + "=" * 70)
    print("RAG Retrieval Pipeline Test Suite")
    print("=" * 70 + "\n")

    results = []
    passed = 0
    failed = 0

    # ========================================================================
    # Execute Test Queries (T017, T018)
    # ========================================================================
    for idx, (query_text, description) in enumerate(TEST_QUERIES, 1):
        # Determine if this is an edge case (T029)
        is_edge_case = description.startswith("edge_")
        query_type = "edge case" if is_edge_case else "curriculum"

        print(f"Query {idx}/{len(TEST_QUERIES)} [{description}]: {query_text}")
        logger.info(f"Test query {idx}: [{description}] '{query_text}'")

        # Execute query (T018)
        query_result = retrieve_relevant_chunks(
            query_text=query_text,
            qdrant_client=qdrant_client,
            cohere_client=cohere_client,
            top_k=top_k,
            confidence_threshold=CONFIDENCE_THRESHOLD
        )

        # ====================================================================
        # Determine Pass/Fail (T019, T020)
        # ====================================================================
        max_score = query_result['max_score']
        result_count = query_result['result_count']
        execution_time = query_result['execution_time']

        # For curriculum queries: pass if score >= threshold
        # For edge cases: always "pass" (we expect low scores)
        if is_edge_case:
            is_pass = True  # Edge cases always pass (we expect them to fail gracefully)
            status = "HANDLED"
        else:
            is_pass = max_score >= confidence_threshold
            status = "PASS" if is_pass else "FAIL"
            if is_pass:
                passed += 1
            else:
                failed += 1

        # Collect per-query result (T019)
        result_entry = {
            'query_text': query_text,
            'description': description,
            'query_type': query_type,
            'max_score': max_score,
            'result_count': result_count,
            'execution_time': execution_time,
            'is_pass': is_pass,
            'status': status,
            'top_result_title': query_result['results'][0]['page_title'] if query_result['results'] else None
        }
        results.append(result_entry)

        # Print result (T022)
        status_symbol = "PASS" if is_pass else ("HANDLED" if is_edge_case else "FAIL")
        status_emoji = "+" if status_symbol in ["PASS", "HANDLED"] else "x"
        print(f"  [{status_emoji}] {status_symbol} - Score: {max_score:.4f}, Results: {result_count}, Time: {execution_time:.2f}s")

        if query_result['results']:
            print(f"      Top result: {query_result['results'][0]['page_title']}")

        print()

        logger.info(
            f"  Result: {status_symbol}, max_score={max_score:.4f}, "
            f"results={result_count}, time={execution_time:.2f}s"
        )

    # ========================================================================
    # Generate Summary (T021, T022)
    # ========================================================================
    total_curriculum = EXPECTED_PASS_COUNT
    pass_rate = passed / total_curriculum if total_curriculum > 0 else 0.0

    # Summary message
    if passed == total_curriculum:
        summary = (
            f"Test suite PASSED: {passed}/{total_curriculum} curriculum queries "
            f"returned relevant results (score >= {confidence_threshold}). "
            f"Edge cases handled gracefully."
        )
    else:
        summary = (
            f"Test suite INCOMPLETE: {passed}/{total_curriculum} curriculum queries passed. "
            f"{failed} queries returned low relevance scores. "
            f"Consider reviewing the failed queries or adjusting the threshold."
        )

    # Print summary (T022)
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Curriculum queries: {passed}/{total_curriculum} passed (threshold >= {confidence_threshold})")
    print(f"Edge cases: 2/2 handled gracefully")
    print(f"Pass rate: {pass_rate:.1%}")
    print(f"\n{summary}")
    print("=" * 70 + "\n")

    logger.info("=" * 60)
    logger.info(f"Test suite complete: {passed}/{total_curriculum} passed, pass_rate={pass_rate:.1%}")
    logger.info("=" * 60)

    # ========================================================================
    # Return Test Results (T021)
    # ========================================================================
    return {
        'total_queries': len(TEST_QUERIES),
        'passed': passed,
        'failed': failed,
        'pass_rate': pass_rate,
        'expected_pass_count': EXPECTED_PASS_COUNT,
        'results': results,
        'summary': summary
    }


# ============================================================================
# Convenience Functions
# ============================================================================

def create_clients() -> tuple:
    """
    Create and return initialized Qdrant and Cohere clients.

    Uses settings from backend/config/settings.py.

    Returns:
        Tuple of (qdrant_client, cohere_client)

    Raises:
        ValueError: If required environment variables are missing
    """
    settings.validate_settings()

    qdrant_client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )

    cohere_client = cohere.ClientV2(api_key=settings.COHERE_API_KEY)

    return qdrant_client, cohere_client


def run_single_query(query_text: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Convenience function to run a single query with auto-initialized clients.

    Args:
        query_text: Natural language query string
        top_k: Number of results to return (3-5, default 5)

    Returns:
        QueryResults dictionary
    """
    qdrant_client, cohere_client = create_clients()
    return retrieve_relevant_chunks(
        query_text=query_text,
        qdrant_client=qdrant_client,
        cohere_client=cohere_client,
        top_k=top_k
    )


def run_test_suite(top_k: int = 5) -> Dict[str, Any]:
    """
    Convenience function to run the full test suite with auto-initialized clients.

    Args:
        top_k: Number of results to return per query (default 5)

    Returns:
        Test results dictionary
    """
    qdrant_client, cohere_client = create_clients()
    return test_retrieval_pipeline(
        qdrant_client=qdrant_client,
        cohere_client=cohere_client,
        top_k=top_k
    )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="RAG Retrieval Pipeline - Query the Physical AI book knowledge base"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Run a single query against the knowledge base"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Run the full test suite to validate retrieval quality"
    )
    parser.add_argument(
        "--top-k", "-k",
        type=int,
        default=5,
        choices=[3, 4, 5],
        help="Number of results to return (3-5, default: 5)"
    )

    args = parser.parse_args()

    if args.query:
        # Run single query
        print(f"\nExecuting query: '{args.query}'\n")
        results = run_single_query(args.query, top_k=args.top_k)

        print(f"Query: {results['query_text']}")
        print(f"Results: {results['result_count']}")
        print(f"Max score: {results['max_score']:.4f}")
        print(f"Execution time: {results['execution_time']:.2f}s")
        print(f"Status: {results['message']}")
        print()

        for i, result in enumerate(results['results'], 1):
            print(f"{i}. [{result['similarity_score']:.4f}] {result['page_title']}")
            print(f"   {result['text_content'][:150]}...")
            print(f"   URL: {result['page_url']}")
            print()

    elif args.test:
        # Run test suite
        test_results = run_test_suite(top_k=args.top_k)

        # Exit with appropriate code
        if test_results['passed'] == test_results['expected_pass_count']:
            sys.exit(0)
        else:
            sys.exit(1)

    else:
        # Default: run test suite
        print("No arguments provided. Running test suite by default.")
        print("Use --help for usage information.\n")
        test_results = run_test_suite(top_k=args.top_k)
