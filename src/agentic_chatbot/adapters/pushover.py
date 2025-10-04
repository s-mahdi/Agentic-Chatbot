"""Pushover notification adapter."""

import requests

from ..config.settings import Settings
from ..ports.notify import Notifier


class PushoverNotifier(Notifier):
    """Pushover notification service implementation."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the Pushover notifier."""
        self._token = settings.pushover_token
        self._user = settings.pushover_user
        self._timeout = settings.request_timeout_secs

    def info(self, text: str) -> None:
        """Send an info notification via Pushover."""
        if not (self._token and self._user):
            return  # Graceful degradation when credentials are missing

        try:
            response = requests.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": self._token,
                    "user": self._user,
                    "message": text,
                },
                timeout=self._timeout,
            )
            response.raise_for_status()
        except Exception:
            # Swallow and move on; do not crash the chat
            pass
