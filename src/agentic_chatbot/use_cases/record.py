"""Record use case helpers."""

from collections.abc import Mapping

from ..ports.notify import Notifier


def record_user_details(
    email: str,
    name: str | None,
    notes: str | None,
    notifier: Notifier,
) -> Mapping[str, str]:
    """Record user details via notifier."""
    notifier.info(
        f"Recording {name or 'Name not provided'} with email {email} and notes {notes or 'not provided'}"
    )
    return {"recorded": "ok"}


def record_unknown_question(question: str, notifier: Notifier) -> Mapping[str, str]:
    """Record unknown question via notifier."""
    notifier.info(f"Recording {question}")
    return {"recorded": "ok"}
