"""Chat use case implementation."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from ..domain.models import ChatResult, Message
from ..ports.docs import DocumentReader
from ..ports.llm import LLMClient, ToolHandler


@dataclass(frozen=True)
class Deps:
    """Dependencies for chat use cases."""

    llm: LLMClient
    docs: DocumentReader


def build_system_prompt(docs: DocumentReader) -> str:
    """Build system prompt from documents."""
    summary = docs.read_text("summary.txt")
    linkedin = docs.read_text("linkedin.pdf")
    name = "Mahdi Hoseini"
    return (
        f"You are acting as {name}. Answer questions about {name}'s career, background, "
        f"skills and experience. Be professional and engaging. "
        f"If you can't answer, call the record_unknown_question tool. "
        f"If the user is engaged, ask for their email and call record_user_details.\n\n"
        f"## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
        f"Always stay in character as {name}."
    )


def handle_message(
    history: Sequence[Message],
    message: Message,
    deps: Deps,
    model: str,
    tools: Mapping[str, tuple[dict[str, Any], ToolHandler]],
) -> ChatResult:
    """Handle a chat message with tool support."""
    # For Gemini, prepend system prompt to first user message instead of using system role
    system_prompt = build_system_prompt(deps.docs)
    if not history:
        # First message - prepend system prompt
        enhanced_message = Message(
            role="user", content=f"{system_prompt}\n\nUser: {message.content}"
        )
        msgs = (enhanced_message,)
    else:
        # Subsequent messages - just use the message as-is
        msgs = (*history, message)

    return deps.llm.chat_with_tools(messages=msgs, tools=tools, model=model)
