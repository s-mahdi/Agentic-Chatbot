"""Gradio presentation layer."""

from typing import Any

import gradio as gr

from ..config.settings import Settings
from ..domain.models import Message
from ..use_cases.chat import Deps, handle_message


def build_ui(settings: Settings, deps: Deps, tools: Any) -> gr.ChatInterface:
    """Build Gradio UI that calls use cases through dependencies."""

    def _convert(history: list[dict[str, Any]]) -> list[Message]:
        """Convert Gradio history format to domain Message objects."""
        return [Message(role=h["role"], content=h["content"]) for h in history]

    def chat_fn(message: str, history: list[dict[str, str]]) -> str:
        """Chat function that interfaces with use cases."""
        try:
            result = handle_message(
                history=_convert(history),
                message=Message(role="user", content=message),
                deps=deps,
                model=settings.model,
                tools=tools,
            )
            return result.final_text
        except Exception as e:
            return f"Error: {e!s}"

    return gr.ChatInterface(chat_fn, type="messages")
