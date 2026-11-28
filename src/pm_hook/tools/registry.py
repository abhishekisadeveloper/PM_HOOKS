
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolDefinition:
    name: str
    description: str
    arguments_schema: dict[str, Any]
    execute: Callable[..., Any]


class ToolNotFoundError(Exception):
    pass


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered"
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        tool = self._tools.get(name)

        if tool is None:
            raise ToolNotFoundError(
                f"Tool '{name}' is not registered"
            )

        return tool

    def list_tools(self) -> list[ToolDefinition]:
        return list(self._tools.values())
