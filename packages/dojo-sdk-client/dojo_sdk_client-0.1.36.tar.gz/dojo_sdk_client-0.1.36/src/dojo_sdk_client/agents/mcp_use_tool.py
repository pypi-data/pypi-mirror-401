import json
import logging
from typing import Callable, Optional

from dojo_sdk_client.agents.base_tool import BaseTool

logger = logging.getLogger(__name__)


class MCPUseTool(BaseTool):
    def __init__(self):
        super().__init__(name="mcp_use_tool", openai_definition=None, func=None)


mcp_tool = MCPUseTool()


# ============================================================================
# MCP Tools Extraction and Conversion Utilities
# ============================================================================


def extract_mcp_tools_from_history(
    history: list, verbose: bool = False, fetch_fn: Optional[Callable[[str], str]] = None
) -> Optional[str]:
    """Extract MCP tools list from step 0 of the history.

    Step 0 is special - it always contains the tools list response from the MCP server.
    This method extracts those tools and returns them as a formatted JSON string
    that can be included in the system prompt for agent calls.

    Args:
        history: List of historical steps
        verbose: Whether to log verbose debug information
        fetch_fn: Optional function to fetch tool output from URL (for S3 URLs)

    Returns:
        JSON string of tools list or None if not found

    Example:
        >>> mcp_tools_json = extract_mcp_tools_from_history(history, fetch_fn=agent._get_cached_tool_output)
        >>> if mcp_tools_json:
        ...     mcp_tools = json.loads(mcp_tools_json)
        ...     print(f"Found {len(mcp_tools)} MCP tools")
    """
    if not history or len(history) == 0:
        return None

    # Find step 0 in the history (it might not be the first element)
    step_0 = None
    for step in history:
        if hasattr(step, "step") and step.step == 0:
            step_0 = step
            break

    if step_0 is None:
        logger.warning(
            f"Step 0 not found in history. History has {len(history)} steps. "
            f"First step number: {history[0].step if hasattr(history[0], 'step') else 'unknown'}"
        )
        return None

    if hasattr(step_0, "tool_text_output") and step_0.tool_text_output:
        tool_text_output = step_0.tool_text_output

        # Step 0 tool_text_output is always an S3 URL (https://...), fetch the content
        if fetch_fn:
            if verbose:
                logger.info(f"Fetching step 0 tool output from URL: {tool_text_output}")
            tool_text_output = fetch_fn(tool_text_output)

        try:
            # The tool_text_output should contain the JSON-RPC response with tools list
            tools_data = json.loads(tool_text_output)

            if "result" in tools_data and "tools" in tools_data["result"]:
                num_tools = len(tools_data["result"]["tools"])
                tools_json = json.dumps(tools_data["result"]["tools"], indent=2)
                logger.info(f"✓ Successfully extracted {num_tools} MCP tools from step 0")
                if verbose:
                    logger.debug(f"MCP tools: {tools_json[:1000]}...")
                return tools_json
            else:
                logger.warning(
                    f"Step 0 tools_data missing 'result.tools'. Structure: {json.dumps(tools_data, indent=2)[:100]}..."
                )
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse MCP tools from step 0: {e}")
            logger.warning(f"Raw content: {tool_text_output[:100]}...")
    else:
        logger.warning(f"Step 0 has no tool_text_output. Step 0 attributes: {dir(step_0)}")

    return None


def mcp_tools_to_openai_format(mcp_tools: list[dict]) -> list[dict]:
    """Convert MCP tool definitions to OpenAI function calling format.

    This converts the MCP tool schema format to the OpenAI tools API format,
    which is used by OpenAI-compatible models (including OpenAI, Seed, etc.).

    Args:
        mcp_tools: List of MCP tool definitions (from the MCP server)

    Returns:
        List of OpenAI-formatted tool definitions

    Example:
        >>> mcp_tools = [{"name": "read_file", "description": "Read a file", "inputSchema": {...}}]
        >>> openai_tools = mcp_tools_to_openai_format(mcp_tools)
        >>> # Use openai_tools in your API call
    """
    openai_tools = []

    for tool in mcp_tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool.get("name", ""),
                "description": tool.get("description", ""),
                "parameters": tool.get("inputSchema", {"type": "object", "properties": {}, "required": []}),
            },
        }
        openai_tools.append(openai_tool)

    return openai_tools


def mcp_tools_to_anthropic_format(mcp_tools: list[dict]) -> list[dict]:
    """Convert MCP tool definitions to Anthropic tool calling format.

    This converts the MCP tool schema format to the Anthropic tools API format.

    Args:
        mcp_tools: List of MCP tool definitions (from the MCP server)

    Returns:
        List of Anthropic-formatted tool definitions

    Example:
        >>> mcp_tools = [{"name": "read_file", "description": "Read a file", "inputSchema": {...}}]
        >>> anthropic_tools = mcp_tools_to_anthropic_format(mcp_tools)
        >>> # Use anthropic_tools in your Anthropic API call
    """
    anthropic_tools = []

    for tool in mcp_tools:
        anthropic_tool = {
            "name": tool.get("name", ""),
            "description": tool.get("description", ""),
            "input_schema": tool.get("inputSchema", {"type": "object", "properties": {}, "required": []}),
        }
        anthropic_tools.append(anthropic_tool)

    return anthropic_tools
