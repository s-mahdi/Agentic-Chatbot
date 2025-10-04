"""Document reader port interface."""

from typing import Protocol


class DocumentReader(Protocol):
    """Protocol for document reading services."""

    def read_text(self, path: str) -> str:
        """Read text content from a document."""
        ...
