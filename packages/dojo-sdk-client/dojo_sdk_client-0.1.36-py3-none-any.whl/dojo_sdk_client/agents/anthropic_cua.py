import base64
import io
import json
import logging
from typing import Any, Dict

from anthropic import Anthropic
from anthropic.types.beta import (
    BetaMessageParam,
    BetaTextBlockParam,
)
from dojo_sdk_core.settings import settings
from dojo_sdk_core.types import (
    Action,
    DoneAction,
    WaitAction,
)
from dojo_sdk_core.ws_types import HistoryStep
from PIL import Image

from .basic_cua import BasicCUA
from .computer_use_tool import computer_tool
from .mcp_use_tool import (
    extract_mcp_tools_from_history,
    mcp_tools_to_anthropic_format,
)
from .prompts import COMPUTER_USE_SYSTEM_PROMPT, MCP_SYSTEM_PROMPT

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

API_RETRY_TIMES = 4
API_RETRY_INTERVAL = 2


class AnthropicCUA(BasicCUA):
    def __init__(
        self,
        model: str,
        image_context_length: int = 10,
        max_tokens: int = 2 * 4096,
        system_prompt_suffix: str = "",
        screen_size: tuple[int, int] = (1920, 1080),
        verbose: bool = False,
    ):
        super().__init__(
            image_context_length=image_context_length,
            max_tokens=max_tokens,
            system_prompt_suffix=system_prompt_suffix,
            screen_size=screen_size,
            verbose=verbose,
        )
        self.max_image_dimms = (1280, 720)
        self.provider = "anthropic"
        self.model = model
        self.client = Anthropic(api_key=settings.anthropic_api_key)

        # Track MCP tool names for proper action formatting
        self.mcp_tool_names = set()

        if self.verbose:
            logger.info(f"AnthropicCUA initialized with model: {model}, image_context_length: {image_context_length}")

    def history_to_messages(self, history: list[HistoryStep]) -> list[BetaMessageParam]:
        """Convert history to messages, reconstructing original message format from raw responses."""
        messages = []

        for i, step in enumerate(history):
            screenshot_base64 = self._get_cached_image(step.after_screenshot)

            # Check if previous step had tool_use(s) that need tool_result(s)
            # Anthropic requires a tool_result for EVERY tool_use in a message
            tool_use_ids = []
            if i > 0:
                prev_step = history[i - 1]
                if prev_step.raw_response:
                    try:
                        prev_raw_data = json.loads(prev_step.raw_response)
                        if "content" in prev_raw_data:
                            for content_block in prev_raw_data["content"]:
                                if isinstance(content_block, dict) and content_block.get("type") == "tool_use":
                                    tool_use_ids.append(content_block.get("id"))
                    except (json.JSONDecodeError, KeyError):
                        pass

            if tool_use_ids:
                # This step needs tool_results for all previous tool_uses
                # Build content with tool_results for each tool_use_id
                tool_results = []

                # For each tool_use, we need a tool_result
                # The first one gets the actual response content, others get generic success
                for idx, tool_use_id in enumerate(tool_use_ids):
                    if idx == 0:
                        # First tool_use gets the actual response
                        tool_result_content = []

                        # For MCP tasks, use the tool_text_output if available
                        if hasattr(step, "tool_text_output") and step.tool_text_output:
                            tool_output = self._get_cached_tool_output(step.tool_text_output)
                            tool_result_content.append({"type": "text", "text": tool_output})
                            if self.verbose:
                                logger.info(f"Step {step.step}: MCP tool response: {step.tool_text_output[:300]}...")

                        # Add screenshot if available (GUI tasks have screenshots, MCP tasks don't)
                        if screenshot_base64:
                            tool_result_content.append(
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": screenshot_base64,
                                    },
                                }
                            )

                        # If no content, add a generic success message
                        if not tool_result_content:
                            tool_result_content.append({"type": "text", "text": "Action executed successfully."})

                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use_id,
                                "content": tool_result_content,
                            }
                        )
                    else:
                        # Additional tool_uses get generic success (we only execute the first one)
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use_id,
                                "content": [{"type": "text", "text": "Action executed successfully."}],
                            }
                        )

                messages.append({"role": "user", "content": tool_results})
            else:
                # Regular user message with screenshot (only if screenshot exists)
                # For MCP tasks, there are no screenshots, so we skip adding a message here
                if screenshot_base64:
                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": screenshot_base64,
                                    },
                                }
                            ],
                        }
                    )

            # Reconstruct assistant message from raw response
            if step.raw_response:
                try:
                    raw_data = json.loads(step.raw_response)

                    if "content" not in raw_data:
                        raise ValueError(f"No content found in raw_response for step {step.step}")

                    assistant_message = {
                        "role": raw_data["role"],
                        "content": raw_data["content"],
                    }

                    messages.append(assistant_message)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse raw_response for step {step.step}: {e}")
                    # Skip this step if we can't parse the raw response
                    continue

        return messages

    def get_next_action(self, prompt: str, image: Image.Image, history: list, tools: list = None) -> tuple[Action, str, str]:
        """Get the next action to take based on the current state."""
        reasoning = None
        raw_response = ""
        try:
            obs = {"screenshot": image}

            # Extract MCP tools from step 0 BEFORE trimming history
            # This ensures we always have access to the tools list even if history is trimmed
            mcp_tools_json = extract_mcp_tools_from_history(history, self.verbose, self._get_cached_tool_output)

            trimmed_history = self._trim_history_to_context_window(history)
            messages = self.history_to_messages(trimmed_history)
            reasoning, actions, action_tool_name, raw_response = self.predict(
                prompt, obs, messages=messages, mcp_tools_json=mcp_tools_json
            )

            if self.verbose:
                logger.info(
                    f"""

             PREDICT OUTPUT
             ================================

             REASONING: {reasoning}

             ACTIONS: {actions}

             TOOL: {action_tool_name}

             """
                )

            if not actions or len(actions) == 0:
                raise ValueError("No actions provided")

            # Check if this is an MCP task (we have MCP tools loaded)
            is_mcp_task = len(self.mcp_tool_names) > 0

            # Check if this is an MCP tool call
            if action_tool_name and action_tool_name in self.mcp_tool_names:
                # Format as MCP action: {"tool": "tool_name", "arguments": {...}}
                action_data = actions[0]
                if isinstance(action_data, dict):
                    # Extract input from tool_use block
                    tool_input = action_data.get("input", {})
                    mcp_action = {"tool": action_tool_name, "arguments": tool_input}
                    logger.info(f"MCP tool call detected: {action_tool_name}, formatted action: {mcp_action}")
                    return mcp_action, reasoning, raw_response

            # Convert first action to Dojo Action format
            action_data = actions[0]
            if isinstance(action_data, str):
                if action_data == "DONE":
                    # For MCP tasks, return dict format; for GUI tasks, return DoneAction
                    if is_mcp_task:
                        return {"tool": "done", "arguments": {}}, reasoning, raw_response
                    return DoneAction(), reasoning, raw_response
                if action_data == "WAIT":
                    # For MCP tasks, return dict format; for GUI tasks, return WaitAction
                    if is_mcp_task:
                        return {"tool": "wait", "arguments": {"seconds": 1}}, reasoning, raw_response
                    return WaitAction(seconds=1), reasoning, raw_response
                else:
                    raise ValueError(f"Unknown action: {action_data}, only DONE is supported")

            if isinstance(action_data, dict):
                # Check if this is a wait action in dict format
                input_data = action_data.get("input", {})
                action_type = input_data.get("action", "")

                if action_type == "wait":
                    duration = input_data.get("duration", 1)
                    return WaitAction(seconds=duration), reasoning, raw_response

                try:
                    return (
                        self._convert_to_dojo_action(action_data),
                        reasoning,
                        raw_response,
                    )
                except (ValueError, TypeError) as e:
                    if "Screenshot" in str(e):
                        return self.get_next_action(prompt, image, history)
                    # Handle unsupported action or malformed parameters
                    error_msg = f"Invalid action: {e}"
                    logger.warning(f"Error calling computer_tool with {action_data}: {e}. Returning wait action.")
                    # Add error to raw_response so it's reported back to the model
                    raw_response_dict = json.loads(raw_response)
                    raw_response_dict["tool_call_err"] = error_msg
                    raw_response = json.dumps(raw_response_dict)
                    return WaitAction(seconds=1), reasoning, raw_response

        except Exception as e:
            raise ValueError(f"Error in get_next_action: {e}") from e

    def _convert_to_dojo_action(self, action_data: dict) -> Action:
        """Convert Claude's action format to Dojo Action format."""
        input_data = action_data.get("input", {})
        action = input_data.get("action", "")
        coordinate = input_data.get("coordinate")
        text = input_data.get("text")
        scroll_direction = input_data.get("scroll_direction")
        scroll_amount = input_data.get("scroll_amount")
        start_coordinate = input_data.get("start_coordinate")

        # Scale coordinates from screenshot_size to screen_size
        scale_x = self.screen_size[0] / self.max_image_dimms[0]
        scale_y = self.screen_size[1] / self.max_image_dimms[1]

        if coordinate:
            coordinate = [int(float(coordinate[0]) * scale_x), int(float(coordinate[1]) * scale_y)]
        if start_coordinate:
            start_coordinate = [int(float(start_coordinate[0]) * scale_x), int(float(start_coordinate[1]) * scale_y)]

        return computer_tool(action, coordinate, text, scroll_direction, scroll_amount, start_coordinate)

    def predict(
        self,
        task_instruction: str,
        obs: Dict = None,
        system: Any = None,
        messages: list[BetaMessageParam] = None,
        mcp_tools_json: str | None = None,
    ):
        """Main prediction method adapted from your implementation."""
        # Select appropriate system prompt based on task type
        base_prompt = MCP_SYSTEM_PROMPT if mcp_tools_json else COMPUTER_USE_SYSTEM_PROMPT
        suffix = f" {self.system_prompt_suffix}" if self.system_prompt_suffix else ""
        system_text = f"{base_prompt}{suffix}\n\n## Your Task\n{task_instruction}"
        system = BetaTextBlockParam(type="text", text=system_text)

        # Resize screenshot if needed (MCP tasks don't have screenshots)
        if obs and "screenshot" in obs and obs["screenshot"] is not None:
            screenshot_image = obs["screenshot"]

            # Resize to screenshot size for sending to model
            new_width, new_height = self.max_image_dimms
            resized_image = screenshot_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert back to bytes
            output_buffer = io.BytesIO()
            resized_image.save(output_buffer, format="PNG")
            obs["screenshot"] = output_buffer.getvalue()

        # Initialize messages as empty list if None
        if messages is None:
            messages = []

        # Initialize conversation if empty
        if len(messages) == 0:
            content = []
            # Add screenshot if available (GUI tasks have screenshots, MCP tasks don't)
            if obs and "screenshot" in obs and obs["screenshot"] is not None:
                init_screenshot_base64 = base64.b64encode(obs["screenshot"]).decode("utf-8")
                content.append(
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": init_screenshot_base64,
                        },
                    }
                )
            # Always add task instruction
            content.append({"type": "text", "text": task_instruction})

            messages.append({"role": "user", "content": content})

        # Add tool results if previous message had tool use(s) and no tool_result was already added
        # Anthropic requires a tool_result for EVERY tool_use in a message
        if messages and messages[-1]["role"] == "assistant":
            last_content = messages[-1]["content"]
            if isinstance(last_content, list):
                # Collect all tool_use IDs from the assistant message
                tool_use_ids = [
                    block["id"] for block in last_content if isinstance(block, dict) and block.get("type") == "tool_use"
                ]

                if tool_use_ids:
                    # Check which tool_use_ids already have tool_results
                    existing_tool_result_ids = set()
                    for msg in messages:
                        if msg["role"] == "user" and isinstance(msg["content"], list):
                            for content_block in msg["content"]:
                                if content_block.get("type") == "tool_result":
                                    existing_tool_result_ids.add(content_block.get("tool_use_id"))

                    # Add tool_results for any tool_use that doesn't have one
                    missing_tool_use_ids = [tid for tid in tool_use_ids if tid not in existing_tool_result_ids]

                    if missing_tool_use_ids:
                        self._add_tool_results_to_messages(
                            messages,
                            missing_tool_use_ids,
                            "Success",
                            screenshot=obs.get("screenshot") if obs else None,
                        )

        beta = "computer-use-2025-01-24"

        if mcp_tools_json:
            try:
                mcp_tools = json.loads(mcp_tools_json)
                if isinstance(mcp_tools, list) and len(mcp_tools) > 0:
                    tool_definitions = mcp_tools_to_anthropic_format(mcp_tools)

                    # Track MCP tool names for action formatting
                    self.mcp_tool_names = {tool.get("name", "") for tool in mcp_tools if tool.get("name")}

                    logger.info(f"MCP task: Using {len(tool_definitions)} MCP tools")
                    if self.verbose:
                        tool_names = [t["name"] for t in tool_definitions]
                        logger.info(f"MCP tools: {tool_names}")
                else:
                    raise ValueError("MCP tools list is empty")
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.error(f"Failed to load MCP tools: {e}")
                raise ValueError(f"MCP task but failed to load tools: {e}") from e
        else:
            # GUI task - use computer_tool
            computer_tool = {
                "name": "computer",
                "type": "computer_20250124",
                "display_width_px": self.max_image_dimms[0],
                "display_height_px": self.max_image_dimms[1],
                "display_number": 1,
            }
            if self.model == "claude-3-5-sonnet-20241022":
                computer_tool["type"] = "computer_20241022"
                beta = "computer-use-2024-10-22"

            tool_definitions = [computer_tool]
            logger.info("GUI task: Using computer_tool")

        try:
            response = self.client.beta.messages.create(
                max_tokens=self.max_tokens,
                messages=messages,
                model=self.model,
                system=[system],
                tools=tool_definitions,
                betas=[beta],
            )

            # Store raw response for history
            raw_response = response.model_dump_json()

            # Extract reasoning from response
            response_params = self._response_to_params(response)
            reasonings = []
            for content_block in response_params:
                if content_block["type"] == "text":
                    reasonings.append(content_block["text"])
            reasoning = reasonings[0] if reasonings else ""

            # Extract actions with robust error handling
            actions, tool_name, tool_call_err = self._extract_actions_from_message(response)

            # Build raw_response with parse error if present
            raw_response_dict = json.loads(raw_response)
            if tool_call_err:
                raw_response_dict["tool_call_err"] = tool_call_err
                logger.info(f"Added tool_call_err to raw_response: {tool_call_err}")
            raw_response = json.dumps(raw_response_dict)

            return reasoning, actions, tool_name, raw_response

        except Exception as e:
            logger.error(f"Error in predict: {e}")
            raise ValueError(f"Error in predict: {e}") from e

    def _add_tool_results_to_messages(self, messages: list, tool_call_ids: list[str], result: str, screenshot: bytes = None):
        """Add tool results for multiple tool_use blocks to message list.

        Anthropic requires a tool_result for EVERY tool_use in a message.
        The first tool_use gets the actual result and screenshot, others get generic success.
        """
        tool_results = []

        for idx, tool_call_id in enumerate(tool_call_ids):
            if idx == 0:
                # First tool_use gets the actual result with screenshot
                content = [{"type": "text", "text": result}]
                if screenshot is not None:
                    screenshot_base64 = base64.b64encode(screenshot).decode("utf-8")
                    content.append(
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": screenshot_base64,
                            },
                        }
                    )
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_call_id,
                        "content": content,
                    }
                )
            else:
                # Additional tool_uses get generic success
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_call_id,
                        "content": [{"type": "text", "text": "Action executed successfully."}],
                    }
                )

        messages.append({"role": "user", "content": tool_results})

    def _response_to_params(self, response):
        """Convert response to parameters format."""
        result = []
        for content_block in response.content:
            if content_block.type == "text":
                result.append({"type": "text", "text": content_block.text})
            elif content_block.type == "tool_use":
                result.append(
                    {
                        "type": "tool_use",
                        "id": content_block.id,
                        "name": content_block.name,
                        "input": content_block.input,
                    }
                )
        return result

    def _extract_actions_from_message(self, response) -> tuple[list, str | None, str | None]:
        """Extract actions from response with robust error handling.

        This method tries multiple strategies to parse tool use blocks:
        1. Direct access to structured input (Anthropic SDK typically provides this)
        2. JSON repair for malformed input
        3. Manual parsing for known patterns

        Returns:
            tuple: (actions, tool_name, error_message) where error_message is None if successful
        """
        actions = []
        tool_name = None
        error_message = None

        response_params = self._response_to_params(response)

        for content_block in response_params:
            if content_block["type"] == "tool_use":
                tool_name = content_block.get("name")
                tool_input = content_block.get("input")

                # Strategy 1: Direct access to structured input
                if isinstance(tool_input, dict):
                    actions.append(content_block)
                    continue

                # Strategy 2: Try to parse if input is a string
                if isinstance(tool_input, str):
                    # Try JSON repair
                    logger.warning("Attempting to repair malformed tool input")
                    repaired_input = self._repair_tool_arguments(tool_input)
                    if repaired_input and isinstance(repaired_input, dict):
                        logger.info("Successfully repaired tool input")
                        content_block["input"] = repaired_input
                        actions.append(content_block)
                        continue

                    # Strategy 3: Try manual parsing
                    manual_input = self._manual_parse_tool_arguments(tool_input)
                    if manual_input:
                        logger.info("Successfully manually parsed tool input")
                        content_block["input"] = manual_input
                        actions.append(content_block)
                        continue

                    # All strategies failed
                    if not tool_input or tool_input.strip() == "":
                        error_details = "(empty string)"
                        error_message = "Tool use had empty input. Please provide action parameters."
                    else:
                        error_details = repr(tool_input[:300]) if len(tool_input) > 300 else repr(tool_input)
                        error_message = (
                            f"Failed to parse tool input: {error_details}. Please ensure input is valid JSON format."
                        )

                    logger.error(f"All parsing strategies failed for tool input: {error_details}")

                # Handle None or other unexpected types
                elif tool_input is None:
                    error_message = "Tool use had None input. Please provide action parameters."
                    logger.error("Tool input is None")
                else:
                    error_message = f"Tool input has unexpected type: {type(tool_input).__name__}"
                    logger.error(f"Unexpected tool input type: {type(tool_input).__name__}")

        # Return DONE action if no actions were successfully parsed
        return (actions or ["DONE"], tool_name, error_message)
