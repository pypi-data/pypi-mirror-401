from dojo_sdk_core.ws_types import HistoryStep


class ResponseProcessor:
    def __init__(self, response: str):
        self.response = response

    def process(self, history: list[HistoryStep], category: str) -> str:
        if category == "mcp":
            return self.process_mcp(history)
        else:
            return self.process_gui(history)

    def process_mcp(self, history: list[HistoryStep]) -> str:
        return self.response

    # Download the screenshot from the history step
    def process_gui(self, history: list[HistoryStep]) -> str:
        return self.response
