"""LLM client port interface."""

from collections.abc import Mapping, Sequence
from typing import Protocol

from ..domain.models import ChatResult, Message


class ToolHandler(Protocol):
    """Protocol for tool handlers."""

    def __call__(self, args: Mapping[str, object]) -> Mapping[str, object]:
        """Execute a tool with given arguments."""
        ...


class LLMClient(Protocol):
    """Protocol for LLM clients with tool support."""

    def chat_with_tools(
        self,
        messages: Sequence[Message],
        tools: Mapping[str, tuple[dict[str, object], ToolHandler]],  # (json_schema, handler)
        model: str,
    ) -> ChatResult:
        """Chat with tool calling support."""
        ...
