# Agentic Chatbot

A clean architecture AI-powered chatbot built with functional programming principles, featuring Google Gemini integration and a professional web interface.

## 🚀 Features

- **Clean Architecture**: FP-first design with clear separation of concerns
- **AI-Powered Conversations**: Built on Google Gemini for intelligent, contextual responses
- **Interactive Web Interface**: Modern UI powered by Gradio
- **User Engagement Tracking**: Automatically records user interactions and contact information
- **Push Notifications**: Real-time notifications via Pushover (optional)
- **PDF Processing**: Extracts and processes LinkedIn profile data from PDFs
- **Professional Persona**: Designed to represent a professional profile with career-focused interactions
- **Type Safety**: Full mypy type checking with strict configuration
- **Tool Validation**: Pydantic schemas for robust tool argument validation

## 🛠️ Technology Stack

- **Python 3.11+**
- **Google Gemini** - AI language model integration
- **Gradio 4.0+** - Web interface framework
- **Pydantic 2.8+** - Data validation and settings management
- **PyPDF 4.3+** - PDF document processing
- **Requests 2.32+** - HTTP client for API calls
- **MyPy** - Static type checking
- **Ruff** - Fast Python linting and formatting

## 📋 Prerequisites

- Python 3.11 or higher
- Google API key (for Gemini)
- Pushover account (optional, for notifications)

## 🔧 Installation

1. **Install uv (recommended)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   LLM_MODEL=gemini-2.0-flash
   PUSHOVER_TOKEN=your_pushover_token_here
   PUSHOVER_USER=your_pushover_user_key_here
   ```

## 📁 Project Structure

```
agentic-chatbot/
├── src/agentic_chatbot/   # Main package
│   ├── __init__.py
│   ├── __main__.py        # Composition root
│   ├── config/            # Configuration
│   │   └── settings.py    # Pydantic settings
│   ├── domain/            # Domain models
│   │   ├── models.py      # Message, ChatResult types
│   │   └── errors.py      # Domain errors
│   ├── ports/             # Interface definitions
│   │   ├── llm.py         # LLMClient protocol
│   │   ├── notify.py      # Notifier protocol
│   │   └── docs.py        # DocumentReader protocol
│   ├── adapters/          # External service implementations
│   │   ├── gemini_client.py   # Gemini LLM adapter
│   │   ├── pushover.py        # Pushover notifier
│   │   └── pypdf_reader.py    # PDF document reader
│   ├── tools/             # Tool definitions
│   │   └── registry.py    # Tool registry with schemas
│   ├── use_cases/         # Business logic
│   │   ├── chat.py        # Chat use cases
│   │   └── record.py      # Recording use cases
│   └── presentation/      # UI layer
│       └── gradio_app.py  # Gradio interface
├── assets/                # Profile data
│   ├── linkedin.pdf       # LinkedIn profile PDF
│   └── summary.txt        # Professional summary
├── pyproject.toml         # Project configuration
├── .env.example          # Environment variables template
├── main.py               # Main entry point
└── README.md             # This file
```

## 🚀 Usage

1. **Prepare your profile data**
   - Place your LinkedIn profile PDF in `assets/linkedin.pdf`
   - Create a professional summary in `assets/summary.txt`

2. **Run the application**
   ```bash
   # Using Makefile (recommended)
   make dev
   
   # Using direct commands
   uv run python main.py
   ```

3. **Access the interface**
   - Open your browser and navigate to the URL shown in the terminal
   - Typically: `http://127.0.0.1:7860`

## 🎯 How It Works

### Clean Architecture Principles

1. **Domain Layer**: Pure business logic with immutable models
2. **Use Cases**: Functional business operations
3. **Ports**: Abstract interfaces for external dependencies
4. **Adapters**: Concrete implementations of external services
5. **Presentation**: UI layer that orchestrates use cases

### Core Functionality

1. **Persona Creation**: Loads professional profile from PDF and text files
2. **Conversation Management**: Multi-turn conversations with context awareness
3. **Tool Integration**: Uses Gemini function calling with Pydantic validation
4. **Notification System**: Optional Pushover notifications for user interactions

### Key Components

- **Settings**: Centralized configuration with Pydantic validation
- **Domain Models**: Immutable data structures (Message, ChatResult)
- **Use Cases**: Pure functions for business logic
- **Adapters**: Gemini, Pushover, and PyPDF implementations
- **Tool Registry**: Type-safe tool definitions with validation

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google API key for Gemini | Yes |
| `LLM_MODEL` | LLM model to use (e.g., gemini-1.5-flash, gemini-1.5-pro) | No (defaults to gemini-1.5-flash) |
| `PUSHOVER_TOKEN` | Pushover application token | No |
| `PUSHOVER_USER` | Pushover user/group key | No |
| `ASSETS_DIR` | Assets directory path | No (defaults to "assets") |

### Profile Setup

The chatbot requires two files in the `assets/` directory:

1. **`linkedin.pdf`**: Your LinkedIn profile exported as PDF
2. **`summary.txt`**: A text file containing your professional summary

## 🧪 Development

### Available Commands
```bash
# Show all available commands
make help

# Development workflow
make dev          # Start the chatbot
make lint         # Run linting
make format       # Format code
make typecheck    # Run type checking
make test         # Run tests
make clean        # Clean up temporary files

# Using uv directly
uv run python main.py                           # Start chatbot
uv run ruff check src/                          # Lint code
uv run ruff format src/                         # Format code
uv run mypy src/ --ignore-missing-imports      # Type check
uv run pytest                                  # Run tests
```

### Individual Commands
```bash
# Type checking
uv run mypy src/ --ignore-missing-imports

# Linting and formatting
uv run ruff check src/
uv run ruff format src/

# Testing
uv run pytest
```

## 📊 Features in Detail

### User Interaction Tracking
- Automatically captures user email addresses and names
- Records additional notes about conversations
- Sends notifications for each interaction

### Unknown Question Handling
- Tracks questions the AI cannot answer
- Provides insights for improving the knowledge base
- Enables continuous learning and improvement

### Professional Persona
- Maintains consistent professional tone
- Focuses on career-related discussions
- Steers conversations toward meaningful connections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/s-mahdi/Agentic-Chatbot/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for providing the AI capabilities
- [Gradio](https://gradio.app/) for the excellent web interface framework
- [Pushover](https://pushover.net/) for reliable notification delivery

---

**Note**: This project is designed for professional use cases and includes features for tracking user interactions. Please ensure compliance with privacy regulations in your jurisdiction when deploying this application.
