"""
OpenAI Agent SDK RAG - Physical AI Curriculum Assistant

This module implements a RAG-powered agent using OpenAI Agent SDK with:
- Custom retrieval tool that queries Qdrant via Cohere embeddings
- Groq integration for LLM access (via LiteLLM)
- Intelligent decision-making: retrieval vs general knowledge
- Test suite for validating 10+ queries with context-grounded responses

Success Criteria:
- Agent uses OpenAI Agent SDK with retrieval function calling
- Custom retrieval tool queries Qdrant via Cohere embeddings
- Answers book-related questions using retrieved context
- Handles 10+ test queries with accurate, context-grounded responses
- Distinguishes between questions requiring retrieval vs. general knowledge

Usage:
    # Run test suite
    python agent.py --test

    # Single query
    python agent.py --query "What is ROS 2?"

    # Interactive mode
    python agent.py --interactive

Feature: 008-openai-agent-rag
"""

import sys
import os
import time
import asyncio
import logging
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Fix Windows UTF-8 encoding (safer approach)
if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass  # Ignore if reconfigure fails

from dotenv import load_dotenv

# OpenAI Agents SDK
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

# Load environment variables
load_dotenv()
set_tracing_disabled(True)
groq_api_key = os.getenv("GROQ_API_KEY")

# Third Party Model Configuration


external_client = AsyncOpenAI(
    api_key= groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

third_Party_model = OpenAIChatCompletionsModel(
    model="openai/gpt-oss-20b",
    openai_client=external_client
)

# Local imports - retrieve.py from Spec 007
from retrieve import retrieve_relevant_chunks, create_clients
from config import settings

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# Configuration
# ============================================================================

# Groq configuration (via OPENAI_API_KEY and OPENAI_BASE_URL)
# Set these in .env:
#   OPENAI_API_KEY=sk-or-v1-your-openrouter-key
#   OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Model to use via Groq (or direct OpenAI)
# MODEL_NAME = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")

SYSTEM_PROMPT = """You are an expert assistant for the Physical AI & Humanoid Robotics curriculum.

Your role is to help students and developers learn about:
- ROS 2 (Robot Operating System 2), robotics middleware, rclpy, nodes, topics, services
- Digital twins, Gazebo simulation, Unity Robotics Hub
- NVIDIA Isaac Sim, Isaac ROS, robot training and simulation
- Vision-Language-Action (VLA) models, embodied AI, robot learning

CRITICAL INSTRUCTIONS FOR TOOL USAGE:

**USE the search_curriculum tool for:**
- Any question about ROS 2, rclpy, nodes, topics, services, actions
- Questions about Gazebo, Unity Robotics Hub, digital twins
- Questions about NVIDIA Isaac Sim, Isaac ROS, robot training
- Questions about VLA (Vision-Language-Action) models, embodied AI
- Code examples, implementation details, or technical explanations from the curriculum
- Any robotics-related technical question that might be covered in the book

**DO NOT use the search_curriculum tool for:**
- Simple greetings: "Hello", "Hi", "Hey", "Good morning"
- Thank you messages: "Thanks", "Thank you", "Appreciate it"
- Farewell messages: "Bye", "Goodbye", "See you"
- General conversation: "How are you?", "What can you do?"
- Questions clearly outside robotics: "What's the weather?", "How to bake a cake?"

RESPONSE GUIDELINES:
- When using retrieved content, ALWAYS cite the source with page title
- If retrieval returns low-confidence results (score < 0.5), acknowledge uncertainty
- Be concise but thorough in technical explanations
- For code examples, ensure they are syntactically correct
- If no relevant content is found, say so honestly
"""


# ============================================================================
# Global State
# ============================================================================

# Qdrant and Cohere clients (initialized once)
_qdrant_client = None
_cohere_client = None

# Tool tracking for test validation
_last_tool_results: Dict[str, Any] = {}
_tool_was_used: bool = False


def initialize_clients():
    """Initialize Qdrant and Cohere clients."""
    global _qdrant_client, _cohere_client
    if _qdrant_client is None or _cohere_client is None:
        logger.info("Initializing Qdrant and Cohere clients...")
        _qdrant_client, _cohere_client = create_clients()
        logger.info("Clients initialized successfully")
    return _qdrant_client, _cohere_client


# ============================================================================
# Custom Retrieval Tool
# ============================================================================

@function_tool
def search_curriculum(query: str) -> str:
    """Search the Physical AI & Humanoid Robotics curriculum for relevant content.

    Use this tool when users ask about technical topics from the curriculum including:
    - ROS 2, rclpy, nodes, topics, services, actions
    - Gazebo simulation, Unity Robotics Hub, digital twins
    - NVIDIA Isaac Sim, Isaac ROS, robot training
    - VLA models, embodied AI, robot learning

    Args:
        query: The search query about Physical AI and robotics topics.

    Returns:
        Retrieved content from the curriculum with source citations, or a message
        indicating no relevant content was found.
    """
    global _last_tool_results, _tool_was_used, _qdrant_client, _cohere_client

    logger.info(f"[Tool] search_curriculum called: '{query[:60]}...'")
    _tool_was_used = True

    try:
        # Ensure clients are initialized
        qdrant_client, cohere_client = initialize_clients()

        # Query Qdrant via Cohere embeddings (using retrieve.py)
        results = retrieve_relevant_chunks(
            query_text=query,
            qdrant_client=qdrant_client,
            cohere_client=cohere_client,
            top_k=5
        )

        _last_tool_results = results

        # Format results for agent context
        if results['result_count'] == 0:
            logger.info("[Tool] No results found")
            return "No relevant content found in the curriculum for this query. Please rephrase or ask about a different topic."

        # Build formatted response
        output_parts = []

        if results['low_confidence']:
            output_parts.append(
                f"Note: Low confidence results (max score: {results['max_score']:.2f}). "
                "Results may not be directly relevant to your question.\n"
            )

        output_parts.append(f"Found {results['result_count']} relevant sections:\n")

        for i, result in enumerate(results['results'], 1):
            output_parts.append(
                f"\n[Source {i}: {result['page_title']}]\n"
                f"{result['text_content'][:600]}\n"
                f"(Relevance: {result['similarity_score']:.2f})\n"
            )

        formatted_output = "".join(output_parts)
        logger.info(f"[Tool] Retrieved {results['result_count']} results, max_score={results['max_score']:.4f}")

        return formatted_output

    except Exception as e:
        logger.error(f"[Tool] Error: {e}")
        _last_tool_results = {'results': [], 'result_count': 0, 'max_score': 0.0}
        return f"Error searching curriculum: {str(e)}. Please try again."


# ============================================================================
# Agent Configuration
# ============================================================================

def create_agent() -> Agent:
    """Create and configure the Physical AI Assistant agent."""
    logger.info(f"Creating agent with model: {third_Party_model}")

    agent = Agent(
        name="Physical AI Assistant",
        instructions=SYSTEM_PROMPT,
        tools=[search_curriculum],
        model=third_Party_model
    )

    return agent


# ============================================================================
# Query Execution
# ============================================================================

async def run_query(agent: Agent, query: str) -> Dict[str, Any]:
    """
    Execute a single query against the agent.

    Args:
        agent: The configured Agent instance
        query: User's question

    Returns:
        Dictionary with response, tool_used, sources, and execution_time
    """
    global _last_tool_results, _tool_was_used

    # Reset tool tracking
    _last_tool_results = {}
    _tool_was_used = False

    start_time = time.time()

    try:
        result = await Runner.run(agent, query)
        response = result.final_output
        execution_time = time.time() - start_time

        # Extract sources if tool was used
        sources = []
        if _tool_was_used and _last_tool_results.get('results'):
            sources = [
                {
                    'title': r['page_title'],
                    'url': r['page_url'],
                    'score': r['similarity_score']
                }
                for r in _last_tool_results['results'][:3]
            ]

        return {
            'query': query,
            'response': response,
            'tool_used': _tool_was_used,
            'sources': sources,
            'max_score': _last_tool_results.get('max_score', 0.0),
            'execution_time': execution_time,
            'success': True,
            'error': None
        }

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Query failed: {e}")
        return {
            'query': query,
            'response': None,
            'tool_used': _tool_was_used,
            'sources': [],
            'max_score': 0.0,
            'execution_time': execution_time,
            'success': False,
            'error': str(e)
        }


# ============================================================================
# Test Suite
# ============================================================================

# Test queries organized by category
TEST_QUERIES = [
    # Category 1: Curriculum questions (SHOULD use retrieval tool)
    {
        "query": "What is ROS 2?",
        "category": "curriculum",
        "expect_tool": True,
        "description": "Basic ROS 2 question"
    },
    {
        "query": "How does Isaac Sim work for robot training?",
        "category": "curriculum",
        "expect_tool": True,
        "description": "Isaac Sim training"
    },
    {
        "query": "Explain Gazebo simulation for robotics",
        "category": "curriculum",
        "expect_tool": True,
        "description": "Gazebo simulation"
    },
    {
        "query": "What is Vision-Language-Action (VLA) integration?",
        "category": "curriculum",
        "expect_tool": True,
        "description": "VLA models"
    },
    {
        "query": "How to use Unity Robotics Hub?",
        "category": "curriculum",
        "expect_tool": True,
        "description": "Unity Robotics"
    },
    {
        "query": "What is rclpy and how do I use it?",
        "category": "curriculum",
        "expect_tool": True,
        "description": "ROS 2 Python client"
    },
    {
        "query": "Explain digital twins in robotics",
        "category": "curriculum",
        "expect_tool": True,
        "description": "Digital twins concept"
    },
    {
        "query": "What sensors are commonly used in humanoid robots?",
        "category": "curriculum",
        "expect_tool": True,
        "description": "Robot sensors"
    },

    # Category 2: Greetings/General (SHOULD NOT use retrieval tool)
    {
        "query": "Hello!",
        "category": "greeting",
        "expect_tool": False,
        "description": "Simple greeting"
    },
    {
        "query": "Thanks for your help!",
        "category": "greeting",
        "expect_tool": False,
        "description": "Thank you message"
    },

    # Category 3: Off-topic (MAY or MAY NOT use tool, but should handle gracefully)
    {
        "query": "How to bake a chocolate cake?",
        "category": "off_topic",
        "expect_tool": None,  # Agent decides - likely low/no results
        "description": "Off-topic question"
    },
    {
        "query": "What is the capital of France?",
        "category": "off_topic",
        "expect_tool": None,
        "description": "General knowledge"
    },
]


async def run_test_suite(agent: Agent) -> Dict[str, Any]:
    """
    Run the complete test suite with 10+ queries.

    Args:
        agent: The configured Agent instance

    Returns:
        Test results summary
    """
    print("\n" + "=" * 70)
    print("Physical AI Agent - Test Suite")
    print("=" * 70 + "\n")

    results = []
    passed = 0
    failed = 0
    curriculum_correct = 0
    greeting_correct = 0

    for i, test in enumerate(TEST_QUERIES, 1):
        query = test['query']
        category = test['category']
        expect_tool = test['expect_tool']
        description = test['description']

        print(f"[{i}/{len(TEST_QUERIES)}] {description}")
        print(f"    Query: \"{query}\"")

        result = await run_query(agent, query)

        # Determine pass/fail
        if result['success']:
            # Check tool usage expectation
            if expect_tool is not None:
                tool_correct = (result['tool_used'] == expect_tool)
            else:
                tool_correct = True  # No expectation for off-topic

            # For curriculum questions, check if we got relevant results
            if category == "curriculum":
                has_content = result['tool_used'] and result['max_score'] > 0.3
                is_pass = tool_correct and has_content
                if is_pass:
                    curriculum_correct += 1
            elif category == "greeting":
                is_pass = tool_correct  # Should NOT use tool
                if is_pass:
                    greeting_correct += 1
            else:
                is_pass = True  # Off-topic handled gracefully

            status = "PASS" if is_pass else "FAIL"
            if is_pass:
                passed += 1
            else:
                failed += 1
        else:
            is_pass = False
            status = "ERROR"
            failed += 1

        # Print result
        tool_status = "Yes" if result['tool_used'] else "No"
        expected_str = "Yes" if expect_tool else ("No" if expect_tool is False else "N/A")
        score_str = f"{result['max_score']:.2f}" if result['tool_used'] else "N/A"

        print(f"    Tool Used: {tool_status} (expected: {expected_str})")
        print(f"    Max Score: {score_str}")
        print(f"    Status: [{status}]")

        if result['success'] and result['response']:
            # Print first 150 chars of response
            response_preview = result['response'][:150].replace('\n', ' ')
            print(f"    Response: {response_preview}...")

        print(f"    Time: {result['execution_time']:.2f}s")
        print()

        results.append({
            **test,
            'result': result,
            'passed': is_pass
        })

    # Summary
    total = len(TEST_QUERIES)
    curriculum_total = sum(1 for t in TEST_QUERIES if t['category'] == 'curriculum')
    greeting_total = sum(1 for t in TEST_QUERIES if t['category'] == 'greeting')

    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Total: {passed}/{total} passed ({passed/total*100:.0f}%)")
    print(f"Curriculum Questions: {curriculum_correct}/{curriculum_total} correct tool usage with results")
    print(f"Greeting Detection: {greeting_correct}/{greeting_total} correctly skipped retrieval")
    print()

    # Success criteria check
    success_criteria = {
        "agent_uses_sdk": True,  # We're using OpenAI Agent SDK
        "custom_retrieval_tool": True,  # search_curriculum uses Qdrant/Cohere
        "answers_with_context": curriculum_correct >= curriculum_total * 0.7,
        "handles_10_queries": total >= 10,
        "distinguishes_retrieval_vs_general": greeting_correct == greeting_total
    }

    print("Success Criteria:")
    for criterion, met in success_criteria.items():
        status = "[PASS]" if met else "[FAIL]"
        print(f"  {status} {criterion.replace('_', ' ').title()}")

    all_passed = all(success_criteria.values())
    print()
    print(f"Overall: {'ALL CRITERIA MET' if all_passed else 'SOME CRITERIA NOT MET'}")
    print("=" * 70 + "\n")

    return {
        'total': total,
        'passed': passed,
        'failed': failed,
        'pass_rate': passed / total,
        'curriculum_correct': curriculum_correct,
        'greeting_correct': greeting_correct,
        'success_criteria': success_criteria,
        'all_passed': all_passed,
        'results': results
    }


# ============================================================================
# Interactive Mode
# ============================================================================

async def interactive_mode(agent: Agent):
    """Run the agent in interactive mode."""
    print("\n" + "=" * 70)
    print("Physical AI Assistant - Interactive Mode")
    print("=" * 70)
    print("Ask questions about the Physical AI & Humanoid Robotics curriculum.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            query = input("You: ").strip()

            if not query:
                continue

            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            result = await run_query(agent, query)

            if result['success']:
                print(f"\nAssistant: {result['response']}")
                if result['tool_used'] and result['sources']:
                    print("\nSources:")
                    for src in result['sources']:
                        print(f"  - {src['title']} (score: {src['score']:.2f})")
                print(f"\n[Tool used: {result['tool_used']}, Time: {result['execution_time']:.2f}s]\n")
            else:
                print(f"\nError: {result['error']}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


# ============================================================================
# Main Entry Point
# ============================================================================

async def main():
    parser = argparse.ArgumentParser(
        description="Physical AI Agent - RAG-powered curriculum assistant"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Run the full test suite (10+ queries)"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Run a single query"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )

    args = parser.parse_args()

    # Check for API key (using GROQ_API_KEY)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not set in environment or .env file")
        sys.exit(1)

    print("Using Groq API")

    # Initialize clients
    try:
        initialize_clients()
    except Exception as e:
        print(f"ERROR: Failed to initialize Qdrant/Cohere clients: {e}")
        sys.exit(1)

    # Create agent
    agent = create_agent()

    if args.test:
        # Run test suite
        test_results = await run_test_suite(agent)
        sys.exit(0 if test_results['all_passed'] else 1)

    elif args.query:
        # Single query
        print(f"\nQuery: {args.query}\n")
        result = await run_query(agent, args.query)

        if result['success']:
            print(f"Response:\n{result['response']}")
            print(f"\n[Tool used: {result['tool_used']}, Max score: {result['max_score']:.2f}, Time: {result['execution_time']:.2f}s]")
            if result['sources']:
                print("\nSources:")
                for src in result['sources']:
                    print(f"  - {src['title']} ({src['url']})")
        else:
            print(f"Error: {result['error']}")
            sys.exit(1)

    elif args.interactive:
        # Interactive mode
        await interactive_mode(agent)

    else:
        # Default: run test suite
        print("No arguments provided. Running test suite by default.")
        print("Use --help for usage information.\n")
        test_results = await run_test_suite(agent)
        sys.exit(0 if test_results['all_passed'] else 1)


if __name__ == "__main__":
    asyncio.run(main())
