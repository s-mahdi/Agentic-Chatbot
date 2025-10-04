"""Domain models and types."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

Role = Literal["system", "user", "assistant", "tool"]


@dataclass(frozen=True)
class Message:
    """Immutable chat message."""

    role: Role
    content: str
    tool_call_id: str | None = None
    name: str | None = None


@dataclass(frozen=True)
class ChatResult:
    """Result of a chat interaction with tools."""

    messages: Sequence[Message]
    final_text: str
