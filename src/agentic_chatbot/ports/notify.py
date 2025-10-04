"""Notification port interface."""

from typing import Protocol


class Notifier(Protocol):
    """Protocol for notification services."""

    def info(self, text: str) -> None:
        """Send an info notification."""
        ...
