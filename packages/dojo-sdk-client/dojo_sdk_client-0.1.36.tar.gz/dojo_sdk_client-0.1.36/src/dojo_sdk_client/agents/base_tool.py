from typing import Any, Callable


class BaseTool:
    def __init__(self, name: str, openai_definition: dict, func: Callable):
        self.name = name
        self.openai_definition = openai_definition
        self.func = func

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)
