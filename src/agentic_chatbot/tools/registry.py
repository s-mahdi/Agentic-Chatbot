"""Tool definitions and registry."""

from collections.abc import Callable, Mapping
from typing import Any

from pydantic import BaseModel, EmailStr, Field

from ..ports.notify import Notifier


class RecordUserDetails(BaseModel):
    """Schema for recording user details."""

    email: EmailStr
    name: str | None = Field(None, description="Optional user name")
    notes: str | None = Field(None, description="Context notes")


class RecordUnknownQuestion(BaseModel):
    """Schema for recording unknown questions."""

    question: str


def _clean_schema_for_gemini(schema: dict[str, Any]) -> dict[str, Any]:
    """Clean Pydantic schema for Gemini compatibility."""

    def clean_property(prop: dict[str, Any]) -> dict[str, Any]:
        """Recursively clean a property schema."""
        cleaned = {}
        for key, value in prop.items():
            if key in ["type", "format", "description", "enum", "items"]:
                cleaned[key] = value
            elif key == "anyOf" and isinstance(value, list):
                # Convert anyOf to a simple nullable type for Gemini
                # Find the non-null type and make it nullable
                non_null_types = [item for item in value if item.get("type") != "null"]
                if non_null_types:
                    # Take the first non-null type and make it optional
                    cleaned.update(non_null_types[0])
                    # Don't add required constraint for optional fields
            elif key == "properties" and isinstance(value, dict):
                # Recursively clean nested properties
                cleaned[key] = {k: clean_property(v) for k, v in value.items()}
        return cleaned

    # Remove fields that Gemini doesn't support
    cleaned = {
        "type": schema.get("type", "object"),
    }

    # Clean properties recursively
    if "properties" in schema:
        cleaned["properties"] = {k: clean_property(v) for k, v in schema["properties"].items()}

    # Add required fields if they exist
    if "required" in schema:
        cleaned["required"] = schema["required"]

    # Add description if it exists
    if "description" in schema:
        cleaned["description"] = schema["description"]

    return cleaned


def make_tools(
    notifier: Notifier,
) -> Mapping[str, tuple[dict[str, Any], Callable[[Mapping[str, Any]], Mapping[str, Any]]]]:
    """Create tool registry with handlers."""

    def record_user_details(args: Mapping[str, object]) -> Mapping[str, object]:
        """Record user details via notifier."""
        try:
            payload = RecordUserDetails.model_validate(args)
            notifier.info(
                f"Recording {payload.name or 'Name not provided'} "
                f"({payload.email}) — {payload.notes or 'not provided'}"
            )
            return {"recorded": "ok"}
        except Exception as e:
            return {"error": str(e)}

    def record_unknown_question(args: Mapping[str, object]) -> Mapping[str, object]:
        """Record unknown question via notifier."""
        try:
            payload = RecordUnknownQuestion.model_validate(args)
            notifier.info(f"Unknown question: {payload.question}")
            return {"recorded": "ok"}
        except Exception as e:
            return {"error": str(e)}

    return {
        "record_user_details": (
            _clean_schema_for_gemini(
                {
                    **RecordUserDetails.model_json_schema(),
                    "description": "Record user contact details and notes for follow-up",
                }
            ),
            record_user_details,
        ),
        "record_unknown_question": (
            _clean_schema_for_gemini(
                {
                    **RecordUnknownQuestion.model_json_schema(),
                    "description": "Record questions that couldn't be answered for improvement",
                }
            ),
            record_unknown_question,
        ),
    }
