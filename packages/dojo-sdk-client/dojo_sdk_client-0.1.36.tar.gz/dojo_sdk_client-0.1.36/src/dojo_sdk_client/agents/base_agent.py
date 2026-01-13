from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base agent class for all agents. A new agent will be created for each task."""

    @abstractmethod
    def get_next_action(self, *args, **kwargs) -> tuple[dict, str, str]:
        """Get the next action to take. Returns (action_data, reasoning, raw_response)."""
        raise NotImplementedError
