"""Gemini LLM client adapter (OpenAI-compatible endpoint)."""

import json
from collections.abc import Mapping, Sequence
from typing import Any

from openai import OpenAI

from ..config.settings import Settings
from ..domain.models import ChatResult, Message
from ..ports.llm import LLMClient, ToolHandler


class GeminiLLM(LLMClient):
    """Gemini LLM client with tool calling support."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the Gemini client using OpenAI-compatible endpoint."""
        self._timeout = settings.request_timeout_secs
        self._client = OpenAI(
            api_key=settings.google_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    def _to_gemini(self, message: Message) -> dict[str, Any]:
        """Convert Message to Gemini format."""
        return {"role": message.role, "parts": [message.content]}

    def chat_with_tools(
        self,
        messages: Sequence[Message],
        tools: Mapping[str, tuple[dict[str, Any], ToolHandler]],
        model: str,
    ) -> ChatResult:
        """Chat with tool calling support using OpenAI-compatible Chat Completions API."""

        # Build OpenAI-compatible tools list
        tools_list = [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": f"Tool for {name.replace('_', ' ')}",
                    "parameters": schema,
                },
            }
            for name, (schema, _handler) in tools.items()
        ]

        # Build initial payload from messages (system/user/assistant/tool)
        payload: list[dict[str, Any]] = [
            {
                "role": m.role,
                "content": m.content,
                **({"name": m.name} if getattr(m, "name", None) else {}),
                **({"tool_call_id": m.tool_call_id} if getattr(m, "tool_call_id", None) else {}),
            }
            for m in messages
        ]
        max_iters = 8

        for _ in range(max_iters):
            try:
                resp = self._client.chat.completions.create(
                    model=model,
                    messages=payload,
                    tools=tools_list if tools_list else None,
                    tool_choice="auto",
                    timeout=self._timeout,
                )
            except Exception as e:
                text = f"(API error: {e!s})"
                return ChatResult(messages=tuple(messages), final_text=text)

            choice = resp.choices[0]
            msg = choice.message

            if getattr(msg, "tool_calls", None):
                # Append assistant message with tool_calls to payload
                payload.append(
                    {
                        "role": "assistant",
                        "content": msg.content or "",
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments,
                                },
                            }
                            for tc in msg.tool_calls
                        ],
                    }
                )

                # Execute tools and append tool results messages with tool_call_id
                for tc in msg.tool_calls:
                    name = tc.function.name
                    args = (
                        json.loads(tc.function.arguments)
                        if isinstance(tc.function.arguments, str)
                        else dict(tc.function.arguments)
                    )
                    _schema, handler = tools.get(name, ({}, lambda _a: {}))
                    try:
                        result = handler(args)
                        payload.append(
                            {
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "name": name,
                                "content": json.dumps(result),
                            }
                        )
                    except Exception as e:
                        error_result = {"error": str(e)}
                        payload.append(
                            {
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "name": name,
                                "content": json.dumps(error_result),
                            }
                        )

                # Continue loop to allow the model to read tool outputs
                continue

            # Regular assistant text
            text = msg.content or ""
            return ChatResult(messages=tuple(messages), final_text=text)

        text = "(tool loop exceeded)"
        return ChatResult(messages=tuple(messages), final_text=text)
