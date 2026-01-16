"""RAG Memory ReAct agent with MCP + Python tools.

Following patterns from:
- Link Scout agent (Lumentor)
- Email Digest agent (agent-architecture-platform)
- ReAct agent pattern documentation
"""

import json
import logging
from pathlib import Path

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

from ..tools import web_search, validate_url, fetch_url, open_file_upload_dialog
from ..config import get_settings
from .prompts import RAG_MEMORY_SYSTEM_PROMPT

settings = get_settings()
logger = logging.getLogger(__name__)

# Global MCP client and tools cache
_mcp_client = None
_mcp_tools = []


async def get_mcp_tools(mcp_config_path: str = None):
    """
    Load MCP tools from RAG Memory MCP server.

    Following email_digest pattern (lines 405-442).

    Args:
        mcp_config_path: Path to mcp.json config file. If None, uses cached tools.

    Returns:
        Tuple of (MCP client, list of tools)
    """
    global _mcp_client, _mcp_tools

    # Return cached if already loaded
    if mcp_config_path is None and _mcp_client is not None:
        logger.info(f"Using cached MCP client with {len(_mcp_tools)} tools")
        return _mcp_client, _mcp_tools

    # Resolve config path
    if mcp_config_path is None:
        mcp_config_path = settings.MCP_CONFIG_PATH

    config_path = Path(mcp_config_path)
    if not config_path.exists():
        logger.warning(f"mcp.json not found at {config_path}")
        return None, []

    # Load MCP config
    logger.info(f"Loading MCP config from {config_path}")
    with open(config_path) as f:
        mcp_config = json.load(f)

    # Create MCP client and connect to server
    logger.info("Creating MultiServerMCPClient...")
    client = MultiServerMCPClient(mcp_config)

    logger.info("Loading tools from MCP server...")
    tools = await client.get_tools()

    logger.info(f"Loaded {len(tools)} MCP tools from RAG Memory server")

    # Cache for reuse
    if mcp_config_path == settings.MCP_CONFIG_PATH:
        _mcp_client = client
        _mcp_tools = tools
        logger.info("Cached MCP client and tools for future use")

    return client, tools


async def create_rag_agent(mcp_config_path: str = None, checkpointer=None):
    """
    Create RAG Memory ReAct agent with MCP + Python tools.

    Following patterns from Link Scout and email_digest agents.

    Args:
        mcp_config_path: Path to mcp.json config file
        checkpointer: PostgresSaver instance for state persistence

    Returns:
        Compiled LangGraph agent

    Raises:
        RuntimeError: If no MCP tools loaded from RAG Memory server
    """
    logger.info("Creating RAG Memory agent...")

    # Load 17 MCP tools from RAG Memory server
    _, mcp_tools = await get_mcp_tools(mcp_config_path)
    if not mcp_tools:
        raise RuntimeError(
            "No MCP tools loaded from RAG Memory server. "
            "Ensure RAG Memory MCP server is running: uv run rag-mcp-http"
        )

    logger.info(f"Loaded {len(mcp_tools)} MCP tools")

    # 4 Python tools: 3 for web search + 1 for UI control
    python_tools = [web_search, validate_url, fetch_url, open_file_upload_dialog]
    logger.info(f"Added {len(python_tools)} Python tools (web search + UI control)")

    # Combine all tools (20 total)
    all_tools = mcp_tools + python_tools
    logger.info(f"Total tools available to agent: {len(all_tools)}")

    # Create ChatOpenAI model with configured settings
    # NOTE: GPT-5 series models only support temperature=1.0
    # CRITICAL: streaming=True enables token-by-token generation for SSE streaming
    logger.info(f"Initializing LLM: model={settings.LLM_MODEL}, temperature={settings.LLM_TEMPERATURE}, streaming=True")
    model = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        streaming=True,  # Required for token-by-token SSE streaming
    )

    # Create ReAct agent - LLM decides which tools to use
    # Using LangGraph 1.0 API: create_react_agent from langgraph.prebuilt
    # interrupt_before=["tools"] pauses BEFORE any tool execution for user approval
    logger.info("Creating ReAct agent with langgraph.prebuilt.create_react_agent...")
    agent = create_react_agent(
        model,
        all_tools,  # LLM chooses from all 20 tools dynamically
        checkpointer=checkpointer,  # PostgresSaver for conversation persistence
        prompt=RAG_MEMORY_SYSTEM_PROMPT,  # System prompt guides LLM behavior
        interrupt_before=["tools"],  # Pause before tool execution for user approval
    )

    logger.info("RAG Memory agent created successfully")
    return agent
