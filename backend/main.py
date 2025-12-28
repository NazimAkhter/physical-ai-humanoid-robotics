"""
RAG Content Pipeline - Main Implementation

This script orchestrates the RAG content ingestion pipeline:
1. Scrapes all pages from deployed Docusaurus site
2. Chunks text into 512-token segments with overlap
3. Generates embeddings using Cohere API
4. Stores embeddings in Qdrant Cloud vector database

Usage:
    uv run python main.py
"""

import sys
import io

# Fix Windows UTF-8 encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import hashlib
import uuid
import logging
import time
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Standard library
import requests
from bs4 import BeautifulSoup

# Third-party libraries
import tiktoken
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Local imports
from config import settings

# Initialize logger
logger = logging.getLogger(__name__)


# ============================================================================
# Helper Functions
# ============================================================================

def retry_with_exponential_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (will be exponentially increased)

    Returns:
        Decorated function with retry logic
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (requests.ConnectionError, requests.Timeout) as e:
                    last_exception = e
                    if attempt < max_retries:
                        delay = base_delay * (2 ** attempt)
                        logger.warning(f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        logger.error(f"{func.__name__} failed after {max_retries + 1} attempts: {e}")
                        raise
                except requests.HTTPError as e:
                    # Retry on 500, 502, 503, 504
                    if e.response and e.response.status_code in [500, 502, 503, 504]:
                        last_exception = e
                        if attempt < max_retries:
                            delay = base_delay * (2 ** attempt)
                            logger.warning(f"{func.__name__} HTTP {e.response.status_code} (attempt {attempt + 1}/{max_retries + 1}). Retrying in {delay}s...")
                            time.sleep(delay)
                        else:
                            logger.error(f"{func.__name__} failed after {max_retries + 1} attempts: HTTP {e.response.status_code}")
                            raise
                    else:
                        # Don't retry on other HTTP errors (like 404)
                        raise

            # Should never reach here, but raise last exception if we do
            if last_exception:
                raise last_exception

        return wrapper
    return decorator


def compute_content_hash(text: str) -> str:
    """
    Compute SHA-256 hash of text content for change detection.

    Args:
        text: Input text to hash

    Returns:
        Hex string representation of SHA-256 hash
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def generate_chunk_id() -> str:
    """
    Generate unique UUID for a chunk.

    Returns:
        String representation of UUID v4
    """
    return str(uuid.uuid4())


# ============================================================================
# Pipeline Functions - To be implemented
# ============================================================================

@retry_with_exponential_backoff(max_retries=3, base_delay=1.0)
def fetch_sitemap(base_url: str) -> List[str]:
    """
    Fetch all page URLs from sitemap.xml.

    Args:
        base_url: Base URL of the deployed site

    Returns:
        List of absolute URLs found in sitemap.xml
    """
    sitemap_url = f"{base_url}/sitemap.xml"
    logger.info(f"Fetching sitemap from {sitemap_url}")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(sitemap_url, headers=headers, timeout=10)
    response.raise_for_status()

    # Parse sitemap XML
    sitemap = BeautifulSoup(response.content, 'xml')
    urls = [loc.text for loc in sitemap.find_all('loc')]

    logger.info(f"Found {len(urls)} URLs in sitemap")
    return urls


@retry_with_exponential_backoff(max_retries=3, base_delay=1.0)
def scrape_page(url: str) -> Dict[str, Any]:
    """
    Scrape single page and extract structured content.

    Args:
        url: Absolute URL of the page to scrape

    Returns:
        Dict containing page metadata and content

    Raises:
        requests.HTTPError: For 404 errors (not retried)
        ConnectionError: For network errors after retries exhausted
    """
    logger.debug(f"Scraping page: {url}")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers, timeout=10)

    # Handle 404 separately - don't retry, just skip
    if response.status_code == 404:
        logger.warning(f"Page not found (HTTP 404), skipping: {url}")
        raise requests.HTTPError(f"HTTP 404: {url}", response=response)

    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title
    title = None
    if soup.find('h1'):
        title = soup.find('h1').get_text(strip=True)
    elif soup.find('title'):
        title = soup.find('title').get_text(strip=True)
    else:
        title = url.split('/')[-1]

    # Extract main content (skip navigation, footer, aside)
    for tag in soup(['nav', 'footer', 'aside', 'script', 'style']):
        tag.decompose()

    # Get main content
    main = soup.find(['main', 'article']) or soup.body
    if main:
        extracted_text = main.get_text(separator='\n', strip=True)
    else:
        extracted_text = soup.get_text(separator='\n', strip=True)

    # Validate content length
    if len(extracted_text) < 50:
        logger.warning(f"Page has minimal content (<50 chars): {url}")

    # Create page entity
    page = {
        'url': url,
        'title': title,
        'html_content': str(soup),
        'extracted_text': extracted_text,
        'content_hash': compute_content_hash(extracted_text),
        'last_scraped': datetime.utcnow().isoformat() + 'Z',
        'section_type': None  # Will be enhanced later
    }

    return page


def detect_changed_pages(new_pages: List[Dict], qdrant_client: QdrantClient) -> Tuple[List, List]:
    """
    Detect which pages have changed by comparing content hashes.

    Args:
        new_pages: List of newly scraped Page entities with content_hash
        qdrant_client: Initialized Qdrant client

    Returns:
        Tuple of (changed_pages, unchanged_pages) lists
    """
    changed_pages = []
    unchanged_pages = []

    logger.info(f"Detecting changed pages among {len(new_pages)} scraped pages")

    try:
        # Check if collection exists
        collections = qdrant_client.get_collections().collections
        collection_exists = any(c.name == settings.COLLECTION_NAME for c in collections)

        if not collection_exists:
            # No existing collection - all pages are new
            logger.info("Collection does not exist - all pages are new")
            return (new_pages, [])

    except Exception as e:
        logger.warning(f"Could not check collection existence: {e}. Treating all pages as new.")
        return (new_pages, [])

    # Query Qdrant for each page to check if it exists and get content_hash
    for page in new_pages:
        page_url = page['url']
        new_hash = page['content_hash']

        try:
            # Search for chunks with this page_url in payload
            # We'll use scroll to get all points with matching page_url
            scroll_result = qdrant_client.scroll(
                collection_name=settings.COLLECTION_NAME,
                scroll_filter={
                    "must": [
                        {
                            "key": "page_url",
                            "match": {"value": page_url}
                        }
                    ]
                },
                limit=1,  # We only need one chunk to get the hash
                with_payload=True,
                with_vectors=False
            )

            points = scroll_result[0]  # scroll returns (points, next_page_offset)

            if not points:
                # Page doesn't exist in Qdrant - it's new/changed
                logger.debug(f"Page not found in Qdrant (new): {page_url}")
                changed_pages.append(page)
            else:
                # Page exists - compare content_hash
                stored_hash = points[0].payload.get('content_hash')

                if stored_hash == new_hash:
                    # Content unchanged
                    logger.debug(f"Page unchanged: {page_url}")
                    unchanged_pages.append(page)
                else:
                    # Content changed
                    logger.debug(f"Page changed (hash mismatch): {page_url}")
                    changed_pages.append(page)

        except Exception as e:
            # On error, assume page needs reprocessing
            logger.warning(f"Error checking page {page_url}: {e}. Marking as changed.")
            changed_pages.append(page)

    logger.info(f"Change detection complete: {len(changed_pages)} changed, {len(unchanged_pages)} unchanged")
    return (changed_pages, unchanged_pages)


def chunk_text(text: str, page_metadata: Dict) -> List[Dict]:
    """
    Split text into 512-token chunks with 50-token overlap.

    Args:
        text: Extracted text from a page
        page_metadata: Page metadata (url, title, etc.)

    Returns:
        List of Chunk entities
    """
    if not text or len(text.strip()) == 0:
        raise ValueError(f"Text content is empty for page: {page_metadata.get('url', 'unknown')}")

    if len(text.strip()) < 50:
        raise ValueError(f"Text content too short (<50 chars) for page: {page_metadata.get('url', 'unknown')}")

    # Initialize tiktoken encoder
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    total_tokens = len(tokens)

    logger.debug(f"Chunking text with {total_tokens} tokens from {page_metadata.get('url', 'unknown')}")

    # Warn if text is very short
    if total_tokens < 100:
        logger.warning(f"Text has less than 100 tokens ({total_tokens} tokens) for page: {page_metadata.get('url', 'unknown')}")

    # If text is short, create single chunk
    if total_tokens <= settings.CHUNK_SIZE:
        chunk_text_content = encoding.decode(tokens)
        return [{
            'chunk_id': generate_chunk_id(),
            'parent_page_url': page_metadata['url'],
            'page_title': page_metadata.get('title', ''),
            'content_hash': page_metadata.get('content_hash', ''),
            'text_content': chunk_text_content,
            'token_count': total_tokens,
            'chunk_index': 0,
            'section_heading': None,
            'overlap_offset': 0
        }]

    # Create overlapping chunks
    chunks = []
    chunk_index = 0
    i = 0

    while i < total_tokens:
        # Take up to CHUNK_SIZE tokens
        end = min(i + settings.CHUNK_SIZE, total_tokens)
        chunk_tokens = tokens[i:end]
        chunk_text_content = encoding.decode(chunk_tokens)

        # Validate token count doesn't exceed limit
        if len(chunk_tokens) > settings.CHUNK_SIZE:
            logger.error(f"Chunk {chunk_index} exceeds token limit: {len(chunk_tokens)} > {settings.CHUNK_SIZE}")
            raise ValueError(f"Chunk token count ({len(chunk_tokens)}) exceeds limit ({settings.CHUNK_SIZE})")

        chunk = {
            'chunk_id': generate_chunk_id(),
            'parent_page_url': page_metadata['url'],
            'page_title': page_metadata.get('title', ''),
            'content_hash': page_metadata.get('content_hash', ''),
            'text_content': chunk_text_content,
            'token_count': len(chunk_tokens),
            'chunk_index': chunk_index,
            'section_heading': None,  # Will be enhanced later
            'overlap_offset': settings.OVERLAP_SIZE if chunk_index > 0 else 0
        }

        chunks.append(chunk)

        # Advance by (CHUNK_SIZE - OVERLAP_SIZE) to create overlap
        i += settings.CHUNK_SIZE - settings.OVERLAP_SIZE
        chunk_index += 1

    logger.debug(f"Created {len(chunks)} chunks from {total_tokens} tokens")
    return chunks


def generate_embeddings(chunks: List[Dict]) -> List[Dict]:
    """
    Generate Cohere embeddings for chunk batch.

    Args:
        chunks: List of Chunk entities from chunk_text()

    Returns:
        List of Embedding entities
    """
    if not chunks:
        return []

    logger.info(f"Generating embeddings for {len(chunks)} chunks")

    # Initialize Cohere client
    co = cohere.ClientV2(api_key=settings.COHERE_API_KEY)

    embeddings_list = []
    texts = [chunk['text_content'] for chunk in chunks]

    # Process in batches
    for i in range(0, len(texts), settings.BATCH_SIZE):
        batch = texts[i:i + settings.BATCH_SIZE]
        logger.debug(f"Processing embedding batch {i // settings.BATCH_SIZE + 1} ({len(batch)} texts)")

        # Retry logic for rate limiting
        max_retries = 3
        for attempt in range(max_retries + 1):
            try:
                response = co.embed(
                    texts=batch,
                    model=settings.EMBEDDING_MODEL,
                    input_type="search_document"
                )

                # Create embedding entities
                # Note: Cohere V2 SDK returns embeddings as EmbedByTypeResponseEmbeddings object
                # Extract the embeddings list - in Cohere V2, it's in the .float_ attribute
                if hasattr(response.embeddings, 'float_'):
                    embeddings_vectors = response.embeddings.float_
                else:
                    embeddings_vectors = response.embeddings

                for j, embedding_vector in enumerate(embeddings_vectors):
                    chunk_idx = i + j
                    chunk = chunks[chunk_idx]

                    # Validate embedding dimensions
                    if len(embedding_vector) != settings.EMBEDDING_DIMENSIONS:
                        error_msg = f"Embedding dimension mismatch: expected {settings.EMBEDDING_DIMENSIONS}, got {len(embedding_vector)}"
                        logger.error(error_msg)
                        raise ValueError(error_msg)

                    embeddings_list.append({
                        'embedding_id': chunk['chunk_id'],
                        'chunk_id': chunk['chunk_id'],
                        'vector': embedding_vector,
                        'model_version': settings.EMBEDDING_MODEL,
                        'generation_timestamp': datetime.utcnow().isoformat() + 'Z',
                        'page_url': chunk['parent_page_url'],
                        'page_title': chunk['page_title'],
                        'content_hash': chunk['content_hash'],
                        'text_content': chunk['text_content'],
                        'chunk_index': chunk['chunk_index']
                    })

                # Success - break out of retry loop
                break

            except Exception as e:
                # Check if it's a rate limit error (HTTP 429)
                is_rate_limit = False
                if hasattr(e, 'status_code') and e.status_code == 429:
                    is_rate_limit = True
                elif hasattr(e, 'response') and hasattr(e.response, 'status_code') and e.response.status_code == 429:
                    is_rate_limit = True
                elif '429' in str(e) or 'rate limit' in str(e).lower():
                    is_rate_limit = True

                if is_rate_limit and attempt < max_retries:
                    delay = 1.0 * (2 ** attempt)  # 1s, 2s, 4s
                    logger.warning(f"Rate limit hit (attempt {attempt + 1}/{max_retries + 1}). Waiting {delay}s before retry...")
                    time.sleep(delay)
                else:
                    # Not a rate limit error, or retries exhausted
                    logger.error(f"Failed to generate embeddings for batch {i // settings.BATCH_SIZE + 1}: {e}")
                    raise

        # Add delay between batches to avoid hitting rate limits
        # Cohere trial: 100k tokens/minute limit
        # With ~46k tokens/batch, we can safely do 2 batches/minute
        # Add 30s delay between batches to stay under limit
        if i + settings.BATCH_SIZE < len(texts):  # Not the last batch
            logger.info("Waiting 30s between batches to avoid rate limits...")
            time.sleep(30)

    logger.info(f"Successfully generated {len(embeddings_list)} embeddings")
    return embeddings_list


def store_in_qdrant(embeddings: List[Dict], client: QdrantClient) -> Dict:
    """
    Store embeddings in Qdrant collection.

    Args:
        embeddings: List of Embedding entities
        client: Initialized Qdrant client

    Returns:
        Summary dict with total_stored, failed, collection_name
    """
    if not embeddings:
        return {'total_stored': 0, 'failed': 0, 'collection_name': settings.COLLECTION_NAME}

    logger.info(f"Storing {len(embeddings)} embeddings in Qdrant collection '{settings.COLLECTION_NAME}'")

    # Check if collection exists, create if not
    try:
        collections = client.get_collections().collections
        collection_exists = any(c.name == settings.COLLECTION_NAME for c in collections)

        if not collection_exists:
            logger.info(f"Creating collection '{settings.COLLECTION_NAME}'")
            client.create_collection(
                collection_name=settings.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSIONS,
                    distance=Distance.COSINE
                )
            )
    except Exception as e:
        logger.error(f"Failed to create/check collection: {e}")
        raise

    # Prepare points for upsert
    points = []
    for embedding in embeddings:
        # Generate deterministic ID from chunk_id
        point_id = str(uuid.UUID(embedding['chunk_id']))

        point = PointStruct(
            id=point_id,
            vector=embedding['vector'],
            payload={
                'chunk_id': embedding['chunk_id'],
                'model_version': embedding['model_version'],
                'generation_timestamp': embedding['generation_timestamp'],
                'page_url': embedding['page_url'],
                'page_title': embedding['page_title'],
                'content_hash': embedding['content_hash'],
                'text_content': embedding['text_content'],
                'chunk_index': embedding['chunk_index']
            }
        )
        points.append(point)

    # Upsert points in batches for better error handling
    total_stored = 0
    failed = 0
    batch_size = 100

    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(points) + batch_size - 1) // batch_size

        try:
            client.upsert(
                collection_name=settings.COLLECTION_NAME,
                points=batch,
                wait=True
            )
            total_stored += len(batch)
            logger.debug(f"Stored batch {batch_num}/{total_batches} ({len(batch)} embeddings)")

        except Exception as e:
            failed += len(batch)
            # Log error with page URLs from this batch
            page_urls = set(p.payload.get('page_url', 'unknown') for p in batch[:5])  # Show first 5 URLs
            logger.error(f"Failed to store batch {batch_num}/{total_batches} ({len(batch)} embeddings): {type(e).__name__}: {e}")
            logger.error(f"Affected pages (first 5): {', '.join(page_urls)}")
            # Continue processing remaining batches instead of raising
            continue

    if failed > 0:
        logger.warning(f"Completed with errors: {total_stored} stored, {failed} failed")
    else:
        logger.info(f"Successfully stored all {total_stored} embeddings")

    return {
        'total_stored': total_stored,
        'failed': failed,
        'collection_name': settings.COLLECTION_NAME
    }


def validate_embeddings(client: QdrantClient, test_query: str) -> float:
    """
    Run test query to validate embedding quality.

    Args:
        client: Initialized Qdrant client
        test_query: Test query text (e.g., "What is ROS 2?")

    Returns:
        Maximum similarity score from top-5 results
    """
    logger.info(f"Validating embeddings with test query: '{test_query}'")

    try:
        # Generate query embedding
        co = cohere.ClientV2(api_key=settings.COHERE_API_KEY)
        response = co.embed(
            texts=[test_query],
            model=settings.EMBEDDING_MODEL,
            input_type="search_query"
        )
        # Extract vector from Cohere V2 response
        if hasattr(response.embeddings, 'float_'):
            query_vector = response.embeddings.float_[0]
        else:
            query_vector = response.embeddings[0]

        # Search Qdrant
        search_results = client.search(
            collection_name=settings.COLLECTION_NAME,
            query_vector=query_vector,
            limit=5
        )

        if not search_results:
            logger.warning("No search results returned for test query")
            return 0.0

        # Get max similarity score
        max_score = max(result.score for result in search_results)
        logger.info(f"Validation query max similarity score: {max_score:.4f}")

        return max_score

    except Exception as e:
        logger.error(f"Failed to validate embeddings: {e}")
        raise


def main(base_url: str, qdrant_url: str, qdrant_api_key: str, cohere_key: str) -> None:
    """
    Execute full pipeline orchestration.

    Args:
        base_url: Deployed Docusaurus site URL
        qdrant_url: Qdrant Cloud cluster URL
        qdrant_api_key: Qdrant API key
        cohere_key: Cohere API key
    """
    start_time = time.time()

    print("\n" + "=" * 80)
    print("RAG Content Pipeline - Physical AI & Humanoid Robotics Book")
    print("=" * 80 + "\n")

    # Initialize Qdrant client
    print(f"📊 Initializing Qdrant client...")
    qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    logger.info(f"Connected to Qdrant at {qdrant_url}")

    # Step 1: Fetch sitemap
    print(f"\n🌐 Fetching sitemap from {base_url}...")
    urls = fetch_sitemap(base_url)
    print(f"✓ Found {len(urls)} URLs in sitemap")

    # Error tracking
    scrape_failures = 0
    chunk_failures = 0
    embedding_failures = 0
    storage_failures = 0

    # Performance tracking
    phase_times = {}

    # Step 2: Scrape all pages
    print(f"\n📄 Scraping pages...")
    scrape_start = time.time()
    all_pages = []
    scraped_count = 0

    for idx, url in enumerate(urls, 1):
        try:
            print(f"  [{idx}/{len(urls)}] Scraping: {url}")

            # Scrape page
            page = scrape_page(url)
            all_pages.append(page)
            scraped_count += 1

            # Add small delay to respect server
            time.sleep(1.5)

        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"Scrape failed for {url}: {error_type}: {e}")
            scrape_failures += 1
            continue

    phase_times['scraping'] = time.time() - scrape_start
    print(f"\n✓ Scraped {scraped_count} pages successfully ({phase_times['scraping']:.1f}s)")
    if scrape_failures > 0:
        print(f"⚠ Failed to scrape {scrape_failures} pages")
        logger.warning(f"Scraping completed with {scrape_failures} failures")

    # Step 3: Detect changed pages
    print(f"\n🔍 Detecting changed pages...")
    detect_start = time.time()
    changed_pages, unchanged_pages = detect_changed_pages(all_pages, qdrant_client)
    phase_times['change_detection'] = time.time() - detect_start

    new_pages = [p for p in changed_pages if p not in unchanged_pages]

    print(f"✓ Change detection complete:")
    print(f"  • Changed pages: {len(changed_pages)}")
    print(f"  • Unchanged pages: {len(unchanged_pages)}")
    logger.info(f"{len(changed_pages)} pages changed, {len(unchanged_pages)} pages unchanged")

    # Step 4: Process only changed pages
    print(f"\n📝 Processing changed pages...")
    chunk_start = time.time()
    all_chunks = []
    processed_count = 0

    for idx, page in enumerate(changed_pages, 1):
        try:
            print(f"  [{idx}/{len(changed_pages)}] Chunking: {page['url']}")

            # Chunk text
            chunks = chunk_text(page['extracted_text'], page)

            # Track chunks
            all_chunks.extend(chunks)
            processed_count += 1

        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"Chunking failed for {page['url']}: {error_type}: {e}")
            chunk_failures += 1
            continue

    phase_times['chunking'] = time.time() - chunk_start
    print(f"\n✓ Processed {processed_count} changed pages ({phase_times['chunking']:.1f}s)")
    print(f"✓ Created {len(all_chunks)} chunks")
    if chunk_failures > 0:
        print(f"⚠ Failed to chunk {chunk_failures} pages")
    if len(unchanged_pages) > 0:
        print(f"✓ Skipped {len(unchanged_pages)} unchanged pages")

    # Step 5: Generate embeddings
    if all_chunks:
        try:
            print(f"\n🔮 Generating embeddings...")
            embed_start = time.time()
            embeddings = generate_embeddings(all_chunks)
            phase_times['embedding'] = time.time() - embed_start
            print(f"✓ Generated {len(embeddings)} embeddings ({phase_times['embedding']:.1f}s)")
        except Exception as e:
            logger.error(f"Embedding generation failed: {type(e).__name__}: {e}")
            embedding_failures = len(all_chunks)
            embeddings = []
            summary = {'total_stored': 0, 'failed': 0, 'collection_name': settings.COLLECTION_NAME}
            phase_times['embedding'] = 0
            phase_times['storage'] = 0
        else:
            # Step 6: Store in Qdrant
            print(f"\n💾 Storing embeddings in Qdrant...")
            storage_start = time.time()
            summary = store_in_qdrant(embeddings, qdrant_client)
            phase_times['storage'] = time.time() - storage_start
            storage_failures = summary['failed']
            print(f"✓ Stored {summary['total_stored']} embeddings in collection '{summary['collection_name']}' ({phase_times['storage']:.1f}s)")
            if storage_failures > 0:
                print(f"⚠ Failed to store {storage_failures} embeddings")

            # Step 7: Validate
            print(f"\n✅ Validating embeddings...")
            try:
                test_score = validate_embeddings(qdrant_client, "What is ROS 2?")
                print(f"✓ Validation query similarity score: {test_score:.4f}")

                if test_score > 0.7:
                    print(f"✓ Validation PASSED (score > 0.7)")
                else:
                    print(f"⚠ Validation score below threshold (0.7)")
            except Exception as e:
                logger.error(f"Validation failed: {type(e).__name__}: {e}")
                print(f"⚠ Validation failed - skipping")
    else:
        print(f"\n✓ No changed pages - database is up to date!")
        embeddings = []
        summary = {'total_stored': 0, 'failed': 0, 'collection_name': settings.COLLECTION_NAME}
        phase_times['chunking'] = 0
        phase_times['embedding'] = 0
        phase_times['storage'] = 0

    # Pipeline complete
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    total_errors = scrape_failures + chunk_failures + embedding_failures + storage_failures
    success = total_errors == 0

    print(f"\n" + "=" * 80)
    if success:
        print(f"✓ Pipeline complete - All operations successful!")
    else:
        print(f"⚠ Pipeline complete - Completed with errors")
    print(f"=" * 80)
    print(f"📊 Summary:")
    print(f"  • Pages scraped: {scraped_count}/{len(urls)}")
    print(f"  • Pages changed: {len(changed_pages)}")
    print(f"  • Pages unchanged: {len(unchanged_pages)}")
    print(f"  • Pages processed: {processed_count}")
    print(f"  • Chunks created: {len(all_chunks)}")
    print(f"  • Embeddings generated: {len(embeddings)}")
    print(f"  • Embeddings stored: {summary['total_stored']}")
    print(f"\n📉 Errors:")
    print(f"  • Total errors: {total_errors}")
    print(f"  • Scrape failures: {scrape_failures}")
    print(f"  • Chunk failures: {chunk_failures}")
    print(f"  • Embedding failures: {embedding_failures}")
    print(f"  • Storage failures: {storage_failures}")
    print(f"\n⏱️  Performance:")
    print(f"  • Scraping: {phase_times.get('scraping', 0):.1f}s")
    print(f"  • Change detection: {phase_times.get('change_detection', 0):.1f}s")
    print(f"  • Chunking: {phase_times.get('chunking', 0):.1f}s")
    print(f"  • Embedding: {phase_times.get('embedding', 0):.1f}s")
    print(f"  • Storage: {phase_times.get('storage', 0):.1f}s")
    print(f"  • Total: {minutes}m {seconds}s")
    print(f"=" * 80 + "\n")

    logger.info(f"Pipeline completed: {scraped_count} pages scraped, {processed_count} processed, {total_errors} total errors")


if __name__ == "__main__":
    # Load and validate settings
    settings.validate_settings()

    # Run pipeline
    main(
        base_url=settings.BASE_URL,
        qdrant_url=settings.QDRANT_URL,
        qdrant_api_key=settings.QDRANT_API_KEY,
        cohere_key=settings.COHERE_API_KEY
    )
