# RAG Content Pipeline

Automated pipeline for ingesting content from the Physical AI & Humanoid Robotics book website into a vector database for RAG (Retrieval Augmented Generation) chatbot functionality.

## Features

- **Automated Scraping**: Fetches all pages from sitemap.xml
- **Smart Chunking**: Splits content into 512-token chunks with 50-token overlap
- **Vector Embeddings**: Generates 1024-dimensional embeddings using Cohere API
- **Vector Storage**: Stores embeddings in Qdrant Cloud with full metadata
- **Incremental Updates**: Detects changed content and skips unchanged pages
- **Error Recovery**: Automatic retry with exponential backoff for transient failures
- **Comprehensive Logging**: Detailed error tracking and performance metrics

## Prerequisites

Before running the pipeline, you need:

1. **Python 3.11+**
2. **UV Package Manager**: [Install UV](https://github.com/astral-sh/uv)
3. **Cohere API Key**: [Sign up for Cohere](https://cohere.com/)
4. **Qdrant Cloud Account**: [Sign up for Qdrant](https://qdrant.tech/)

## Setup

### 1. Install Dependencies

```bash
cd backend
uv sync
```

This will install all required dependencies:
- beautifulsoup4 (HTML parsing)
- requests (HTTP client)
- cohere (Embedding generation)
- qdrant-client (Vector database)
- tiktoken (Token counting)
- python-dotenv (Environment variables)

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your_qdrant_api_key_here

# Docusaurus Deployment URL
BASE_URL=https://physical-ai-humanoid-robotics-iota-nine.vercel.app
```

### 3. Get API Keys

#### Cohere API Key

1. Visit https://cohere.com/
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key to `.env`

#### Qdrant Cloud

1. Visit https://qdrant.tech/
2. Sign up for a free account
3. Create a new cluster
4. Copy the cluster URL and API key to `.env`

## Usage

### Run the Pipeline

```bash
uv run python main.py
```

### What the Pipeline Does

1. **Fetches Sitemap**: Retrieves all URLs from sitemap.xml
2. **Scrapes Pages**: Downloads and parses each page's HTML
3. **Detects Changes**: Compares content hashes to skip unchanged pages
4. **Chunks Content**: Splits text into 512-token chunks with 50-token overlap
5. **Generates Embeddings**: Creates vector embeddings using Cohere
6. **Stores Vectors**: Uploads embeddings to Qdrant Cloud
7. **Validates**: Runs test query to verify embedding quality

### Example Output

```
================================================================================
RAG Content Pipeline - Physical AI & Humanoid Robotics Book
================================================================================

📊 Initializing Qdrant client...

🌐 Fetching sitemap from https://physical-ai-humanoid-robotics-iota-nine.vercel.app/sitemap.xml...
✓ Found 50 URLs in sitemap

📄 Scraping pages...
  [1/50] Scraping: https://physical-ai-humanoid-robotics-iota-nine.vercel.app/
  [2/50] Scraping: https://physical-ai-humanoid-robotics-iota-nine.vercel.app/docs/intro
  ...
✓ Scraped 50 pages successfully (120.5s)

🔍 Detecting changed pages...
✓ Change detection complete:
  • Changed pages: 5
  • Unchanged pages: 45

📝 Processing changed pages...
✓ Processed 5 changed pages (2.3s)
✓ Created 125 chunks
✓ Skipped 45 unchanged pages

🔮 Generating embeddings...
✓ Generated 125 embeddings (15.2s)

💾 Storing embeddings in Qdrant...
✓ Stored 125 embeddings in collection 'physical_ai_book' (3.1s)

✅ Validating embeddings...
✓ Validation query similarity score: 0.8234
✓ Validation PASSED (score > 0.7)

================================================================================
✓ Pipeline complete - All operations successful!
================================================================================
📊 Summary:
  • Pages scraped: 50/50
  • Pages changed: 5
  • Pages unchanged: 45
  • Pages processed: 5
  • Chunks created: 125
  • Embeddings generated: 125
  • Embeddings stored: 125

📉 Errors:
  • Total errors: 0
  • Scrape failures: 0
  • Chunk failures: 0
  • Embedding failures: 0
  • Storage failures: 0

⏱️  Performance:
  • Scraping: 120.5s
  • Change detection: 1.8s
  • Chunking: 2.3s
  • Embedding: 15.2s
  • Storage: 3.1s
  • Total: 2m 25s
================================================================================
```

## Configuration

All configuration is managed in `config/settings.py`:

```python
# Pipeline Configuration
COLLECTION_NAME = "physical_ai_book"     # Qdrant collection name
CHUNK_SIZE = 512                          # Tokens per chunk
OVERLAP_SIZE = 50                         # Token overlap between chunks
BATCH_SIZE = 100                          # Embeddings per API batch
EMBEDDING_MODEL = "embed-english-v3.0"   # Cohere model
EMBEDDING_DIMENSIONS = 1024               # Vector dimensions
```

## Error Handling

The pipeline includes robust error handling:

- **Network Errors**: Automatic retry with exponential backoff (1s, 2s, 4s)
- **Rate Limits**: Detects HTTP 429 and waits before retrying
- **Invalid Content**: Validates text length and token counts
- **Partial Failures**: Continues processing even if some pages fail
- **Detailed Logging**: All errors logged with timestamps and context

## Incremental Updates

On subsequent runs, the pipeline:

1. Scrapes all pages to check for changes
2. Compares SHA-256 hashes of content
3. Only processes pages with changed content
4. Skips unchanged pages (no reprocessing)
5. Updates only modified embeddings in Qdrant

This dramatically reduces runtime when only a few pages have changed.

## Troubleshooting

### "Missing required environment variables"

Make sure your `.env` file exists and contains all required keys:
- COHERE_API_KEY
- QDRANT_URL
- QDRANT_API_KEY

### "Failed to fetch sitemap"

Check that BASE_URL is correct and the sitemap.xml is accessible:
```bash
curl https://your-site.vercel.app/sitemap.xml
```

### "Rate limit hit"

The pipeline automatically handles rate limits with exponential backoff. If you consistently hit rate limits, consider:
- Reducing BATCH_SIZE in settings.py
- Upgrading your Cohere API plan

### "Embedding dimension mismatch"

Ensure `EMBEDDING_MODEL` and `EMBEDDING_DIMENSIONS` match:
- embed-english-v3.0 → 1024 dimensions
- embed-english-light-v3.0 → 384 dimensions

## Performance

Expected runtime for initial ingestion of 100 pages:

- Scraping: ~2-3 minutes (with 1.5s delay between requests)
- Change detection: ~2-5 seconds
- Chunking: ~5-10 seconds
- Embedding: ~30-60 seconds (100 embeddings/batch)
- Storage: ~10-15 seconds

Total: **~3-5 minutes for 100 pages**

Subsequent runs (with no changes): **~2-3 minutes** (scraping + change detection only)

## License

Part of the Physical AI & Humanoid Robotics Book project.

## Retrieval Pipeline (Spec 007)

The retrieval module (`retrieve.py`) provides semantic search functionality to query the populated Qdrant vector database.

### Quick Start

```bash
# Run a single query
uv run python retrieve.py --query "What is ROS 2?"

# Run the full test suite (7 queries)
uv run python retrieve.py --test

# Specify number of results (3-5)
uv run python retrieve.py --query "Isaac Sim robot training" --top-k 3
```

### Functions

#### `retrieve_relevant_chunks(query_text, qdrant_client, cohere_client, top_k=5)`

High-level wrapper that returns formatted results with metadata.

```python
from retrieve import retrieve_relevant_chunks, create_clients

qdrant_client, cohere_client = create_clients()
results = retrieve_relevant_chunks(
    query_text="How does Isaac Sim work?",
    qdrant_client=qdrant_client,
    cohere_client=cohere_client,
    top_k=5
)

print(f"Found {results['result_count']} results")
print(f"Max score: {results['max_score']:.4f}")
for r in results['results']:
    print(f"[{r['similarity_score']:.4f}] {r['page_title']}")
```

#### Convenience Functions

```python
from retrieve import run_single_query, run_test_suite

# Quick query (auto-creates clients)
results = run_single_query("What is VLA integration?")

# Quick test suite
test_results = run_test_suite()
```


## OpenAI Agent RAG Chat (Spec 008)

The agent module (`agent.py`) provides a FastAPI-based chat endpoint that uses OpenAI Agent SDK with function calling to integrate with the retrieval functions.

### Quick Start

```bash
# Start the chat server
uv run python -m uvicorn agent:app --reload --host 0.0.0.0 --port 8000

# Or run directly
uv run python agent.py
```

### API Endpoints

#### POST /chat

Send a chat message and receive an AI-generated response with optional RAG context.

```bash
# Basic chat (curriculum query)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ROS 2?"}'

# Chat with session continuity
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are its main features?", "session_id": "your-session-id"}'
```

#### GET /health

Check service connectivity.

```bash
curl http://localhost:8000/health
```

### Features

- **Intelligent Tool Calling**: Agent decides when to search curriculum vs respond directly
- **Conversation History**: Maintains context across multiple messages per session
- **Source Citations**: Returns source documents with similarity scores
- **Error Handling**: Graceful degradation with user-friendly error messages
- **CORS Support**: Ready for frontend integration

### Configuration

Add to `.env`:

```bash
# OpenAI Agent SDK
OPENAI_API_KEY=sk-your-openai-api-key
```

## FastAPI Backend API (Spec 009)

The API module (`api.py`) provides a REST API that exposes the RAG-powered agent to frontend applications.

### Quick Start

```bash
# Start the API server
uv run python api.py

# Or with uvicorn directly
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints

#### GET /

Root endpoint returning API information.

```bash
curl http://localhost:8000/
# Returns: {"name": "Physical AI Chatbot API", "version": "1.0.0", "docs": "/docs"}
```

#### GET /health

Health check endpoint for monitoring.

```bash
curl http://localhost:8000/health
# Returns: {"status": "healthy", "dependencies": {"qdrant": "connected", "cohere": "connected", "openrouter": "configured"}}
```

#### POST /chat

Send a query and receive an AI-generated response with source citations.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

**Response:**
```json
{
  "answer": "ROS 2 (Robot Operating System 2) is a middleware framework...",
  "sources": [
    {
      "title": "Chapter 1: ROS 2 Architecture Overview",
      "url": "https://physical-ai-humanoid-robotics-iota-nine.vercel.app/docs/modules/ros2-nervous-system/architecture-overview",
      "score": 0.85
    }
  ]
}
```

### Features

- **CORS Support**: Configured for cross-origin requests from frontend
- **Request Validation**: Query length limits (1-2000 chars)
- **Error Handling**: Structured error responses with error codes
- **Health Monitoring**: Dependency status checks
- **Auto Documentation**: OpenAPI docs at /docs

### Configuration

Add to `.env`:

```bash
# FastAPI Backend
FRONTEND_URL=https://your-frontend-domain.com
API_HOST=0.0.0.0
API_PORT=8000
```
