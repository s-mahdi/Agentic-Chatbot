"""Gemini LLM client adapter."""

import json
from collections.abc import Mapping, Sequence
from typing import Any

import google.generativeai as genai

from ..config.settings import Settings
from ..domain.models import ChatResult, Message
from ..ports.llm import LLMClient, ToolHandler


class GeminiLLM(LLMClient):
    """Gemini LLM client with tool calling support."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the Gemini client."""
        genai.configure(api_key=settings.google_api_key)
        self._timeout = settings.request_timeout_secs

    def _to_gemini(self, message: Message) -> dict[str, Any]:
        """Convert Message to Gemini format."""
        return {"role": message.role, "parts": [message.content]}

    def chat_with_tools(
        self,
        messages: Sequence[Message],
        tools: Mapping[str, tuple[dict[str, Any], ToolHandler]],
        model: str,
    ) -> ChatResult:
        """Chat with tool calling support."""
        # Define tool schemas for Gemini function calling
        tool_defs = []
        for name, (schema, _handler) in tools.items():
            tool_defs.append(
                {
                    "function_declarations": [
                        {
                            "name": name,
                            "description": f"Tool for {name.replace('_', ' ')}",
                            "parameters": schema,
                        }
                    ]
                }
            )

        # Build the chat session
        model_obj = genai.GenerativeModel(model_name=model, tools=tool_defs)
        transcript = list(messages)
        max_iters = 8

        for _ in range(max_iters):
            try:
                resp = model_obj.generate_content(
                    [self._to_gemini(m) for m in transcript],
                    request_options={"timeout": self._timeout},
                )
            except Exception as e:
                # Handle API errors gracefully
                text = f"(API error: {e!s})"
                transcript.append(Message(role="assistant", content=text))
                return ChatResult(messages=tuple(transcript), final_text=text)

            if not resp.candidates:
                text = "(No response from model)"
                transcript.append(Message(role="assistant", content=text))
                return ChatResult(messages=tuple(transcript), final_text=text)

            cand = resp.candidates[0]
            if not cand.content or not cand.content.parts:
                text = "(Empty response)"
                transcript.append(Message(role="assistant", content=text))
                return ChatResult(messages=tuple(transcript), final_text=text)

            parts = cand.content.parts
            did_call_tool = False

            for part in parts:
                if hasattr(part, "function_call") and part.function_call:
                    did_call_tool = True
                    fc = part.function_call
                    name = fc.name
                    args = json.loads(fc.args) if isinstance(fc.args, str) else dict(fc.args)
                    _schema, handler = tools.get(name, ({}, lambda _a: {}))

                    try:
                        result = handler(args)
                        transcript.append(Message(role="assistant", content="", name=name))
                        transcript.append(
                            Message(
                                role="tool",
                                name=name,
                                content=json.dumps(result),
                            )
                        )
                    except Exception as e:
                        # Handle tool execution errors
                        error_result = {"error": str(e)}
                        transcript.append(Message(role="assistant", content="", name=name))
                        transcript.append(
                            Message(
                                role="tool",
                                name=name,
                                content=json.dumps(error_result),
                            )
                        )

            if did_call_tool:
                continue

            # Regular assistant text
            text = cand.content.parts[0].text if cand.content.parts else ""
            transcript.append(Message(role="assistant", content=text))
            return ChatResult(messages=tuple(transcript), final_text=text)

        # Safety valve - tool loop exceeded
        text = "(tool loop exceeded)"
        transcript.append(Message(role="assistant", content=text))
        return ChatResult(messages=tuple(transcript), final_text=text)
