"""PyPDF document reader adapter."""

from pathlib import Path

from pypdf import PdfReader

from ..config.settings import Settings
from ..ports.docs import DocumentReader


class LocalDocReader(DocumentReader):
    """Local document reader with caching."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the document reader."""
        self._assets = settings.assets_dir
        self._cache: dict[str, str] = {}

    def read_text(self, path: str) -> str:
        """Read text content from a document with caching."""
        if path in self._cache:
            return self._cache[path]

        file_path = Path(path)
        if not file_path.is_absolute():
            file_path = self._assets / file_path

        if not file_path.exists():
            result = f"(File not found: {file_path})"
            self._cache[path] = result
            return result

        try:
            if file_path.suffix.lower() == ".pdf":
                result = self._read_pdf(file_path)
            else:
                result = file_path.read_text(encoding="utf-8")
            self._cache[path] = result
            return result
        except Exception as e:
            result = f"(Error reading {file_path}: {e!s})"
            self._cache[path] = result
            return result

    def _read_pdf(self, file_path: Path) -> str:
        """Read text from PDF file."""
        try:
            reader = PdfReader(str(file_path))
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n".join(text_parts)
        except Exception as e:
            return f"(Error reading PDF {file_path}: {e!s})"
