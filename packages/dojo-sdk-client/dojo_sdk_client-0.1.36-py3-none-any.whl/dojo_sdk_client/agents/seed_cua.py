# flake8: noqa: E501
import base64
import enum
import io
import json
import logging
import time
from typing import Dict

from dojo_sdk_core.types import Action, DoneAction, WaitAction
from dojo_sdk_core.ws_types import HistoryStep
from openai import OpenAI
from PIL import Image

from dojo_sdk_client.agents.base_tool import BaseTool
from dojo_sdk_client.agents.mcp_use_tool import (
    extract_mcp_tools_from_history,
    mcp_tools_to_openai_format,
)

from .basic_cua import BasicCUA, get_tools_prompt
from .prompts import COMPUTER_USE_SYSTEM_PROMPT, MCP_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


class ThinkingType(enum.Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    AUTO = "auto"


THINKING_PROMPT_BASE = """
You should begin by detailing the internal reasoning process, and then present the answer to the user. The reasoning process should be enclosed within <think_never_used_51bce0c785ca2f68081bfa7d91973934> and </think_never_used_51bce0c785ca2f68081bfa7d91973934> tags, as follows:
<think_never_used_51bce0c785ca2f68081bfa7d91973934> reasoning process here </think_never_used_51bce0c785ca2f68081bfa7d91973934> answer here.
You have different modes of thinking:
Unrestricted think mode: Engage in an internal thinking process with thorough reasoning and reflections. You have an unlimited budget for thinking tokens and can continue thinking until you fully solve the problem.
Efficient think mode: Provide a concise internal thinking process with efficient reasoning and reflections. You don't have a strict token budget but be less verbose and more direct in your thinking.
No think mode: Respond directly to the question without any internal reasoning process or extra thinking tokens. Still follow the template with the minimum required thinking tokens to justify the answer.
Budgeted think mode: Limit your internal reasoning and reflections to stay within the specified token budget
Based on the complexity of the problem, select the appropriate mode for reasoning among the provided options listed below.
Provided Mode(s):
{mode}
"""


class ThinkingMode(enum.Enum):
    NO_THINK = "NO_THINK"
    UNRESTRICTED_THINK = "UNRESTRICTED_THINK"


class SeedCUA(BasicCUA):
    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str,
        thinking_mode: ThinkingMode = ThinkingMode.NO_THINK,
        image_context_length: int = 3,
        max_tokens: int = 4096,
        system_prompt_suffix: str = "",
        screen_size: tuple[int, int] = (1280, 800),
        verbose: bool = False,
    ):
        super().__init__(
            image_context_length=image_context_length,
            max_tokens=max_tokens,
            system_prompt_suffix=system_prompt_suffix,
            screen_size=screen_size,
            verbose=verbose,
        )

        self.provider = "seed"
        self._model_name = model

        if thinking_mode.value == ThinkingMode.UNRESTRICTED_THINK.value:
            self.model = f"{model}-unrestricted-thinking"
        elif thinking_mode.value == ThinkingMode.NO_THINK.value:
            self.model = f"{model}-no-thinking"
        else:
            raise ValueError(f"Invalid thinking mode: {thinking_mode}")

        self.api_key = api_key
        self.base_url = base_url
        self.thinking_mode = thinking_mode
        self.model_screen_size = (1000, 1000)

        self.client = OpenAI(api_key=api_key, base_url=base_url)

        # Track MCP tool names for proper action formatting
        self.mcp_tool_names = set()

        if self.verbose:
            logger.info(f"CustomCUA initialized with model: {model}, image_context_length: {image_context_length}")

    def history_to_messages(
        self, history: list[HistoryStep], current_obs: Dict = None, task_instruction: str = None
    ) -> list[dict]:
        """Convert history steps to OpenAI message format, handling tool calls and results.

        Only includes screenshots for the most recent `image_context_length` steps to avoid
        exceeding token limits. Older steps get text only.

        Args:
            history: List of historical steps
            current_obs: Current observation containing the screenshot
            task_instruction: The task instruction to include with the current screenshot
        """
        messages = []
        total_steps = len(history)

        for i, step in enumerate(history):
            # Only include actual images for the most recent steps
            include_image = (total_steps - i) < self.image_context_length

            tool_call_id = self._get_previous_tool_call_id(history, i)

            # Add tool result (text only) and screenshot as user message
            if tool_call_id:
                # Check if last tool call failed
                if step.raw_response and "tool_call_err" in json.loads(step.raw_response):
                    tool_result_content = json.loads(step.raw_response)["tool_call_err"]
                    if self.verbose:
                        logger.info(f"Step {step.step}: Tool call error: {tool_result_content[:200]}...")
                # For MCP tasks, use the tool_text_output if available
                elif hasattr(step, "tool_text_output") and step.tool_text_output:
                    tool_result_content = self._get_cached_tool_output(step.tool_text_output)
                    if self.verbose:
                        logger.info(f"Step {step.step}: MCP tool response: {tool_result_content[:300]}...")
                else:
                    tool_result_content = "Action executed successfully."
                    if self.verbose:
                        logger.info(f"Step {step.step}: Generic success message (no tool output)")
                # Tool result is always text-only
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": tool_result_content,
                    }
                )
                # Add screenshot as user message if within context window
                if include_image and step.after_screenshot != "":
                    screenshot_base64 = self._get_cached_image(step.after_screenshot)
                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"},
                                }
                            ],
                        }
                    )
            else:
                # No tool call - add screenshot as user message
                if include_image and step.after_screenshot != "":
                    screenshot_base64 = self._get_cached_image(step.after_screenshot)
                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"},
                                }
                            ],
                        }
                    )

            # Add assistant message from raw response
            if step.raw_response:
                assistant_message = self._parse_assistant_message(step)
                if assistant_message:
                    messages.append(assistant_message)

        # Handle current observation and add screenshot
        if current_obs:
            screenshot = current_obs.get("screenshot")
            screenshot_base64 = None

            # Only process screenshot if it exists (GUI tasks have screenshots, MCP tasks don't)
            if screenshot is not None:
                resized = screenshot.resize(self.screen_size, Image.Resampling.LANCZOS)

                buffer = io.BytesIO()
                resized.save(buffer, format="PNG")
                screenshot_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            if not messages:
                content = []
                if screenshot_base64:
                    content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"}})
                if task_instruction:
                    content.append({"type": "text", "text": task_instruction})
                if content:  # Only add message if we have content
                    messages.append({"role": "user", "content": content})
            # Add tool result if previous message had tool call without result
            elif messages[-1]["role"] == "assistant":
                tool_calls = messages[-1].get("tool_calls")
                if tool_calls:
                    tool_call_id = tool_calls[0]["id"]

                    # Check if tool result already exists
                    has_result = any(msg.get("role") == "tool" and msg.get("tool_call_id") == tool_call_id for msg in messages)
                    if not has_result:
                        # Check if the previous tool call had wrong formatting
                        if history and history[-1].raw_response and "tool_call_err" in json.loads(history[-1].raw_response):
                            tool_result_content = json.loads(history[-1].raw_response)["tool_call_err"]
                        # For MCP tasks, use the tool_text_output if available from last history step
                        elif history and hasattr(history[-1], "tool_text_output") and history[-1].tool_text_output:
                            tool_result_content = self._get_cached_tool_output(history[-1].tool_text_output)
                        else:
                            tool_result_content = "Action executed successfully."
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "content": tool_result_content,
                            }
                        )
                        content = []
                        if screenshot_base64:
                            content.append(
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"}}
                            )
                        if task_instruction:
                            content.append({"type": "text", "text": task_instruction})
                        if content:  # Only add message if we have content
                            messages.append({"role": "user", "content": content})

        return messages

    def _get_previous_tool_call_id(self, history: list[HistoryStep], current_index: int) -> str | None:
        """Extract tool call ID from previous step's raw response."""
        if current_index == 0:
            return None

        prev_step = history[current_index - 1]
        if not prev_step.raw_response:
            return None

        try:
            prev_raw_data = json.loads(prev_step.raw_response)
            message = prev_raw_data.get("choices", [{}])[0].get("message", {})
            tool_calls = message.get("tool_calls", [])
            return tool_calls[0]["id"] if tool_calls else None
        except (json.JSONDecodeError, KeyError, IndexError):
            return None

    def _parse_assistant_message(self, step: HistoryStep) -> dict | None:
        """Parse assistant message from raw response."""
        try:
            raw_data = json.loads(step.raw_response)

            if "choices" not in raw_data or not raw_data["choices"]:
                logger.error(f"No choices found in raw_response for step {step.step}")
                return None

            message = raw_data["choices"][0]["message"]
            assistant_message = {
                "role": message["role"],
                "content": message.get("content", ""),
            }

            if "tool_calls" in message:
                assistant_message["tool_calls"] = message["tool_calls"]

            return assistant_message
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse raw_response for step {step.step}: {e}")
            return None

    def get_next_action(self, prompt: str, image: Image.Image, history: list, tools: list[BaseTool]) -> tuple[Action, str, str]:
        """Get the next action to take based on the current state.

        This method is designed to be robust - it will return errors to the model
        instead of raising exceptions, allowing the model to learn from mistakes.
        """
        try:
            obs = {"screenshot": image}

            # Extract MCP tools from step 0 BEFORE trimming history
            # This ensures we always have access to the tools list even if history is trimmed
            mcp_tools_json = extract_mcp_tools_from_history(history, self.verbose, self._get_cached_tool_output)

            trimmed_history = self._trim_history_to_context_window(history)
            messages = self.history_to_messages(trimmed_history, current_obs=obs, task_instruction=prompt)
            reasoning, actions, action_tool_name, raw_response = self.predict(
                messages, tools, mcp_tools_json, task_instruction=prompt
            )

            if self.verbose:
                logger.info(
                    f"\nPREDICT OUTPUT\n{'=' * 32}\nREASONING: {reasoning}\nACTIONS: {actions}\nTOOL: {action_tool_name}\n"
                )

            if not actions:
                tool_names = ", ".join([t.name for t in tools])
                error_msg = f"No actions provided in model response. Please provide an action using one of: {tool_names}."
                return self._create_error_response(error_msg, reasoning, raw_response)

            # Check if this is an MCP tool call
            if action_tool_name in self.mcp_tool_names:
                # Format as MCP action: {"tool": "tool_name", "arguments": {...}}
                mcp_action = {"tool": action_tool_name, "arguments": actions[0] if isinstance(actions[0], dict) else {}}
                logger.info(f"MCP tool call detected: {action_tool_name}, formatted action: {mcp_action}")
                return mcp_action, reasoning, raw_response

            # Find the tool that was used
            tool = self._find_tool_by_name(tools, action_tool_name)
            if not tool:
                tool_names = ", ".join([t.name for t in tools])
                mcp_tools = ", ".join(self.mcp_tool_names) if self.mcp_tool_names else "none"
                error_msg = f"Unknown tool '{action_tool_name}'. Available tools: {tool_names}. MCP tools: {mcp_tools}."
                return self._create_error_response(error_msg, reasoning, raw_response)

            # Process the action using the identified tool
            return self._process_action_with_tool(actions[0], tool, image, reasoning, raw_response)

        except Exception as e:
            logger.error(f"Unexpected error in get_next_action: {e}", exc_info=True)
            raise ValueError(f"Error in get_next_action: {e}") from e

    def _process_action_with_tool(
        self, action_data, tool: BaseTool, image: Image.Image, reasoning: str, raw_response: str
    ) -> tuple[Action, str, str]:
        """Process an action using the specified tool.

        This method handles both computer_tool (which needs coordinate scaling) and
        mcp_tool (which doesn't). It's designed to be reusable across different agent implementations.
        """
        print(f"Processing action with tool: {tool.name}, action_data: {action_data}")
        # Handle string actions (fallback cases)
        if isinstance(action_data, str):
            return self._process_string_action(action_data, tool, reasoning, raw_response)

        # Handle dictionary actions
        if isinstance(action_data, dict):
            # For computer_tool, we need to scale coordinates
            if self._tool_needs_coordinate_scaling(tool):
                return self._process_computer_action(action_data, tool, image, reasoning, raw_response)
            # For other tools (like mcp_tool), execute directly
            else:
                return self._process_non_computer_action(action_data, tool, reasoning, raw_response)

        # Handle unexpected action format
        error_msg = f"Action has unexpected type: {type(action_data).__name__}. Expected dict or string. Please use the {tool.name} to provide actions."
        return self._create_error_response(error_msg, reasoning, raw_response)

    def _process_string_action(
        self, action_data: str, tool: BaseTool, reasoning: str, raw_response: str
    ) -> tuple[Action, str, str]:
        """Process string-based actions like DONE or WAIT.

        For MCP tasks, returns dict format: {"tool": "done"/"wait", "arguments": {...}}
        For GUI tasks, returns DoneAction()/WaitAction()
        """
        # Check if this is an MCP task
        is_mcp_task = len(self.mcp_tool_names) > 0

        if action_data == "DONE":
            if is_mcp_task:
                return {"tool": "done", "arguments": {}}, reasoning, raw_response
            return DoneAction(), reasoning, raw_response
        elif action_data == "WAIT":
            if is_mcp_task:
                return {"tool": "wait", "arguments": {"seconds": 1}}, reasoning, raw_response
            return WaitAction(seconds=1), reasoning, raw_response
        else:
            error_msg = f"Unknown string action: '{action_data}'. Please use the {tool.name} with a valid action type."
            return self._create_error_response(error_msg, reasoning, raw_response)

    def _process_computer_action(
        self, action_data: dict, tool: BaseTool, image: Image.Image, reasoning: str, raw_response: str
    ) -> tuple[dict, str, str]:
        """Process computer_tool actions that need coordinate scaling."""
        action_type = action_data.get("action", "")

        if not action_type:
            error_msg = "Action dictionary is missing 'action' field. Please provide an 'action' field with a valid action type (e.g., 'click', 'type', 'key', etc.)."
            return self._create_error_response(error_msg, reasoning, raw_response)

        # Handle wait/done actions specially (don't need coordinate scaling)
        if action_type == "wait":
            duration = action_data.get("duration", 1)
            # For MCP tasks, return dict format; for GUI tasks, return WaitAction
            is_mcp_task = len(self.mcp_tool_names) > 0
            if is_mcp_task:
                return {"tool": "wait", "arguments": {"seconds": duration}}, reasoning, raw_response
            return WaitAction(seconds=duration), reasoning, raw_response

        if action_type == "done":
            # For MCP tasks, return dict format; for GUI tasks, return DoneAction
            is_mcp_task = len(self.mcp_tool_names) > 0
            if is_mcp_task:
                return {"tool": "done", "arguments": {}}, reasoning, raw_response
            return DoneAction(), reasoning, raw_response

        # Calculate scale factors from model's screen size to original image size
        original_width, original_height = image.size
        scale_x = original_width / self.model_screen_size[0]
        scale_y = original_height / self.model_screen_size[1]

        # Scale coordinates from model's reference frame to original screen size
        scaled_data, scale_error = self._scale_coordinates_safe(action_data, scale_x, scale_y)

        if scale_error:
            error_msg = f"Coordinate scaling error: {scale_error}. Please ensure coordinates are in the format [x, y] where x and y are numbers within the screen bounds (0-{self.model_screen_size[0]}, 0-{self.model_screen_size[1]})."
            return self._create_error_response(error_msg, reasoning, raw_response)

        # Try to execute the action
        try:
            return tool.func(**scaled_data), reasoning, raw_response
        except (ValueError, TypeError, KeyError, IndexError) as e:
            # Provide detailed error message to help the model correct itself
            error_msg = self._create_detailed_action_error(action_type, scaled_data, e)
            logger.warning(f"Error calling {tool.name}: {e}. Returning error to model.")
            return self._create_error_response(error_msg, reasoning, raw_response)

    def _process_non_computer_action(
        self, action_data: dict, tool: BaseTool, reasoning: str, raw_response: str
    ) -> tuple[dict, str, str]:
        """Process non-computer tool actions (like mcp_tool) that don't need coordinate scaling."""
        try:
            result = tool.func(**action_data)
            return result, reasoning, raw_response
        except (ValueError, TypeError, KeyError) as e:
            error_msg = f"{tool.name} call failed: {e}. Please check the parameters."
            logger.warning(f"Error calling {tool.name}: {e}. Returning error to model.")
            return self._create_error_response(error_msg, reasoning, raw_response)

    def _scale_coordinates(self, action_data: dict, scale_x: float, scale_y: float) -> dict:
        """Scale coordinates from model's reference frame to original screen size.

        DEPRECATED: Use _scale_coordinates_safe instead for better error handling.
        """
        scaled = action_data.copy()

        if "coordinate" in scaled and scaled["coordinate"]:
            scaled["coordinate"] = [
                int(float(scaled["coordinate"][0]) * scale_x),
                int(float(scaled["coordinate"][1]) * scale_y),
            ]

        if "start_coordinate" in scaled and scaled["start_coordinate"]:
            scaled["start_coordinate"] = [
                int(float(scaled["start_coordinate"][0]) * scale_x),
                int(float(scaled["start_coordinate"][1]) * scale_y),
            ]

        return scaled

    def _scale_coordinates_safe(self, action_data: dict, scale_x: float, scale_y: float) -> tuple[dict, str | None]:
        """Safely scale coordinates from model's reference frame to original screen size.

        Returns:
            tuple: (scaled_action_data, error_message)
                   error_message is None if successful, otherwise contains description of the error
        """
        scaled = action_data.copy()

        # Scale regular coordinate if present
        if "coordinate" in scaled:
            coord = scaled["coordinate"]
            scaled_coord, error = self._parse_and_scale_coordinate(coord, scale_x, scale_y, "coordinate")
            if error:
                return scaled, error
            scaled["coordinate"] = scaled_coord

        # Scale start_coordinate if present
        if "start_coordinate" in scaled:
            coord = scaled["start_coordinate"]
            scaled_coord, error = self._parse_and_scale_coordinate(coord, scale_x, scale_y, "start_coordinate")
            if error:
                return scaled, error
            scaled["start_coordinate"] = scaled_coord

        return scaled, None

    def _parse_and_scale_coordinate(
        self, coord, scale_x: float, scale_y: float, field_name: str
    ) -> tuple[list[int] | None, str | None]:
        """Parse and scale a single coordinate pair.

        Returns:
            tuple: (scaled_coordinate, error_message)
        """
        # Handle None or empty values
        if coord is None:
            return None, None

        # Validate coordinate is a list/array
        if not isinstance(coord, (list, tuple)):
            return None, f"{field_name} must be a list/array, got {type(coord).__name__}: {repr(coord)}"

        # Validate coordinate has exactly 2 elements
        if len(coord) != 2:
            return None, f"{field_name} must have exactly 2 elements [x, y], got {len(coord)} elements: {coord}"

        try:
            # Try to parse as numbers
            x = float(coord[0])
            y = float(coord[1])

            # Validate bounds (should be within model screen size)
            if x < 0 or y < 0:
                return None, f"{field_name} has negative values: [{x}, {y}]. Coordinates must be positive."

            if x > self.model_screen_size[0] or y > self.model_screen_size[1]:
                return (
                    None,
                    f"{field_name} [{x}, {y}] exceeds model screen size [{self.model_screen_size[0]}, {self.model_screen_size[1]}]",
                )

            # Scale to actual screen size
            scaled_x = int(x * scale_x)
            scaled_y = int(y * scale_y)

            return [scaled_x, scaled_y], None

        except (ValueError, TypeError) as e:
            return None, f"{field_name} contains non-numeric values: {coord}. Error: {e}"

    def _create_error_response(self, error_msg: str, reasoning: str, raw_response: str) -> tuple[Action, str, str]:
        """Create a standardized error response to send back to the model.

        Returns a WAIT action with the error message embedded in the raw_response
        so the model receives the error in its next turn.

        For MCP tasks, returns dict format: {"tool": "wait", "arguments": {"seconds": 1}}
        For GUI tasks, returns WaitAction(seconds=1)
        """
        try:
            raw_response_dict = json.loads(raw_response)
        except json.JSONDecodeError:
            raw_response_dict = {}

        raw_response_dict["tool_call_err"] = error_msg
        updated_raw_response = json.dumps(raw_response_dict)

        logger.info(f"Returning error to model: {error_msg}")

        # Check if this is an MCP task
        is_mcp_task = len(self.mcp_tool_names) > 0
        if is_mcp_task:
            return {"tool": "wait", "arguments": {"seconds": 1}}, reasoning, updated_raw_response
        else:
            return WaitAction(seconds=1), reasoning, updated_raw_response

    def _create_detailed_action_error(self, action_type: str, action_data: dict, error: Exception) -> str:
        """Create a detailed error message based on the action type and error.

        This helps the model understand what went wrong and how to fix it.
        """
        error_str = str(error)

        # Provide action-specific guidance
        action_requirements = {
            "click": "requires 'coordinate' field with [x, y] values",
            "left_click": "requires 'coordinate' field with [x, y] values",
            "right_click": "requires 'coordinate' field with [x, y] values",
            "double_click": "requires 'coordinate' field with [x, y] values",
            "triple_click": "requires 'coordinate' field with [x, y] values",
            "middle_click": "requires 'coordinate' field with [x, y] values",
            "mouse_move": "requires 'coordinate' field with [x, y] values",
            "left_click_drag": "requires 'start_coordinate' and 'coordinate' fields with [x, y] values",
            "key": "requires 'text' field with the key(s) to press (use + to separate multiple keys)",
            "type": "requires 'text' field with the text to type",
            "scroll": "requires 'scroll_amount' field with a positive integer, and optional 'scroll_direction' ('up' or 'down')",
        }

        requirement = action_requirements.get(action_type, "check the action requirements")

        # Build detailed error message
        msg = f"Action '{action_type}' failed: {error_str}. "
        msg += f"This action {requirement}. "

        # Add the actual parameters received for debugging
        relevant_params = {k: v for k, v in action_data.items() if k != "action"}
        if relevant_params:
            msg += f"Received parameters: {json.dumps(relevant_params)}. "

        msg += "Please correct the action parameters and try again."

        return msg

    def predict(
        self,
        messages: list[dict],
        tools: list[BaseTool],
        mcp_tools_json: str | None = None,
        task_instruction: str = "",
    ):
        """Make a prediction using the OpenAI API.

        Args:
            messages: List of messages in OpenAI format (already processed with screenshots)
            tools: List of tools to make available to the model
            mcp_tools_json: JSON string of available MCP tools from step 0
            task_instruction: The task instruction to include in the system prompt

        Returns:
            tuple: (reasoning, actions, tool_name, raw_response)
        """
        if self.thinking_mode.value == ThinkingMode.NO_THINK.value:
            thinking_prompt = THINKING_PROMPT_BASE.format(mode="No think")
        elif self.thinking_mode.value == ThinkingMode.UNRESTRICTED_THINK.value:
            thinking_prompt = THINKING_PROMPT_BASE.format(mode="Unrestricted think")
        else:
            raise ValueError(f"Invalid thinking mode: {self.thinking_mode}")

        # Select appropriate system prompt based on task type
        base_prompt = MCP_SYSTEM_PROMPT if mcp_tools_json else COMPUTER_USE_SYSTEM_PROMPT
        system_content = f"{thinking_prompt}\n\n{base_prompt}"
        if task_instruction:
            system_content += f"\n\n## Your Task\n{task_instruction}"

        # Don't include mcp_use_tool in the tool prompt since we're exposing MCP tools directly
        non_mcp_tools = [t for t in tools if t.name != "mcp_use_tool"]
        if non_mcp_tools:
            tool_prompt = get_tools_prompt(non_mcp_tools)
            system_content += f"\n{tool_prompt}"

        if self.system_prompt_suffix:
            system_content += f" {self.system_prompt_suffix}"

        # Prepare final messages with system prompt
        final_messages = [{"role": "system", "content": system_content}] + messages

        # Prepare tool definitions based on which tools were passed in
        # Check if this is an MCP task (has mcp_tools_json) or GUI task (computer_tool in tools)
        if mcp_tools_json:
            # MCP task - extract real MCP tools from history and use them
            try:
                mcp_tools = json.loads(mcp_tools_json)
                if isinstance(mcp_tools, list) and len(mcp_tools) > 0:
                    tool_definitions = mcp_tools_to_openai_format(mcp_tools)

                    # Track MCP tool names for action formatting
                    self.mcp_tool_names = {tool.get("name", "") for tool in mcp_tools if tool.get("name")}

                    logger.info(f"MCP task: Using {len(tool_definitions)} MCP tools")
                    if self.verbose:
                        tool_names = [t["function"]["name"] for t in tool_definitions]
                        logger.info(f"MCP tools: {tool_names}")
                else:
                    raise ValueError("MCP tools list is empty")
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.error(f"Failed to load MCP tools: {e}")
                raise ValueError(f"MCP task but failed to load tools: {e}") from e
        else:
            # GUI task - use computer_tool
            # Filter out tools with None openai_definition (e.g., mcp_use_tool placeholder)
            tool_definitions = [tool.openai_definition for tool in tools if tool.openai_definition is not None]
            logger.info("GUI task: Using computer_tool")

        try:
            now = time.time()
            attempts = 1
            while True:
                if self.verbose and attempts > 1:
                    logger.info(f"Attempt {attempts} for predict request. Retrying...")

                try:
                    response = self.client.chat.completions.create(
                        model=self._model_name,
                        messages=final_messages,
                        max_tokens=self.max_tokens,
                        tools=tool_definitions,
                        tool_choice="auto",
                        extra_body={"thinking": {"type": ThinkingType.DISABLED.value}},
                        timeout=150,
                    )
                    break
                except TimeoutError as e:
                    logger.error(f"Timeout in predict: {e}")
                    attempts += 1
                    if attempts > 2:
                        raise ValueError("Error in predict: Maximum number of attempts reached") from e
                    time.sleep(2 * attempts)

            if self.verbose:
                logger.info(f"Predict took {time.time() - now:.2f} seconds")

            # Track token usage
            if hasattr(response, "usage") and response.usage:
                total_tokens = response.usage.total_tokens
                self._track_tokens(total_tokens)

            message = response.choices[0].message

            # Extract reasoning and actions
            reasoning = message.content or ""
            actions, tool_name, tool_call_err = self._extract_actions_from_message(message, tools)

            # Build raw_response with parse error if present
            raw_response_dict = response.model_dump()
            if tool_call_err:
                raw_response_dict["tool_call_err"] = tool_call_err
                logger.info(f"Added tool_call_err to raw_response: {tool_call_err}")
            raw_response = json.dumps(raw_response_dict)

            return reasoning, actions, tool_name, raw_response

        except Exception as e:
            logger.error(f"Error in predict: {e}")
            raise ValueError(f"Error in predict: {e}") from e

    def _extract_actions_from_message(self, message, tools: list[BaseTool]) -> tuple[list, str, str | None]:
        """Extract actions from tool calls in the message with robust error handling.

        This method tries multiple strategies to parse tool call arguments:
        1. Direct JSON parsing
        2. JSON repair for common formatting issues
        3. Manual parsing for known patterns

        Args:
            message: The message containing tool calls
            tools: List of available tools

        Returns:
            tuple: (actions, tool_name, error_message) where error_message is None if successful
        """
        actions = []
        tool_name = None
        error_message = None

        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                raw_args = tool_call.function.arguments

                # Validate that the tool is in our available tools (including MCP tools)
                is_mcp_tool = tool_name in self.mcp_tool_names
                is_base_tool = self._find_tool_by_name(tools, tool_name)

                if not is_mcp_tool and not is_base_tool:
                    tool_names = ", ".join([t.name for t in tools])
                    mcp_tools = ", ".join(self.mcp_tool_names) if self.mcp_tool_names else "none"
                    error_message = f"Unknown tool '{tool_name}'. Available tools: {tool_names}. MCP tools: {mcp_tools}"
                    logger.error(error_message)
                    break

                # Strategy 1: Try direct JSON parsing
                try:
                    args = json.loads(raw_args)
                    # Validate that it's a dictionary
                    if isinstance(args, dict):
                        actions.append(args)
                        continue
                    else:
                        logger.warning(f"Tool arguments parsed but not a dict: {type(args).__name__}")
                except json.JSONDecodeError as e:
                    logger.debug(f"Direct JSON parsing failed: {e}")

                # Strategy 2: Try JSON repair
                logger.warning("Attempting to repair malformed JSON tool arguments")
                repaired_args = self._repair_tool_arguments(raw_args)
                if repaired_args and isinstance(repaired_args, dict):
                    logger.info("Successfully repaired tool arguments")
                    actions.append(repaired_args)
                    continue

                # Strategy 3: Try manual parsing for common patterns (mainly for computer_tool)
                if tool_name == "computer_tool":
                    manual_args = self._manual_parse_tool_arguments(raw_args)
                    if manual_args:
                        logger.info("Successfully manually parsed tool arguments")
                        actions.append(manual_args)
                        continue

                # All strategies failed - create detailed error message
                if not raw_args or raw_args.strip() == "":
                    error_details = "(empty string)"
                    error_message = "Tool call had empty arguments. Please provide action parameters."
                elif len(raw_args) > 300:
                    error_details = repr(raw_args[:300]) + "... (truncated)"
                    error_message = f"Failed to parse tool call arguments. Arguments too long or malformed: {error_details}. Please ensure arguments are valid JSON."
                else:
                    error_details = repr(raw_args)
                    if tool_name == "computer_tool":
                        error_message = f"Failed to parse tool call arguments: {error_details}. Please ensure arguments are valid JSON format, e.g., {{'action': 'click', 'coordinate': [100, 200]}}."
                    elif tool_name == "mcp_use_tool":
                        error_message = f"Failed to parse tool call arguments: {error_details}. Please ensure arguments are valid JSON format, e.g., {{'server_name': 'filesystem', 'tool_name': 'read_file', 'arguments': {{'path': '/path/to/file'}}}}."
                    else:
                        error_message = (
                            f"Failed to parse tool call arguments: {error_details}. Please ensure arguments are valid JSON."
                        )

                logger.error(f"All parsing strategies failed for tool arguments: {error_details}")

        # If no tool was called, default to first available tool (usually computer_tool)
        if not tool_name and tools:
            tool_name = tools[0].name

        # Return WAIT action if no actions were successfully parsed
        return (actions or ["WAIT"], tool_name, error_message)
