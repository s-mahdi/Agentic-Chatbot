"""Composition root and application entry point."""

from .adapters.gemini_client import GeminiLLM
from .adapters.pushover import PushoverNotifier
from .adapters.pypdf_reader import LocalDocReader
from .config.settings import Settings
from .presentation.gradio_app import build_ui
from .tools.registry import make_tools
from .use_cases.chat import Deps


def main() -> None:
    """Main application entry point."""
    settings = Settings()

    # Compose dependencies
    deps = Deps(
        llm=GeminiLLM(settings),
        docs=LocalDocReader(settings),
    )

    # Create notifier and tools
    notifier = PushoverNotifier(settings)
    tools = make_tools(notifier)

    # Build and launch UI
    ui = build_ui(settings, deps, tools)
    ui.launch()


if __name__ == "__main__":
    main()
