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
    # Always include persona/system prompt as the first message so it persists across turns
    # Gradio does not retain our locally injected first-turn message in its history,
    # so we must re-prepend the prompt on every invocation to keep the agent in character.
    system_prompt = build_system_prompt(deps.docs)
    msgs = (Message(role="user", content=system_prompt), *history, message)

    return deps.llm.chat_with_tools(messages=msgs, tools=tools, model=model)
