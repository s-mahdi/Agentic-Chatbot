# Agentic Chatbot

An intelligent AI-powered chatbot built with Gradio and OpenAI that provides interactive conversations with built-in user engagement tracking and notification systems.

## 🚀 Features

- **AI-Powered Conversations**: Built on OpenAI's GPT-4o-mini for intelligent, contextual responses
- **Interactive Web Interface**: Clean, modern UI powered by Gradio
- **User Engagement Tracking**: Automatically records user interactions and contact information
- **Push Notifications**: Real-time notifications via Pushover for user interactions and unknown questions
- **PDF Processing**: Extracts and processes LinkedIn profile data from PDFs
- **Professional Persona**: Designed to represent a professional profile with career-focused interactions

## 🛠️ Technology Stack

- **Python 3.13+**
- **Gradio 5.49.0** - Web interface framework
- **OpenAI 2.1.0** - AI language model integration
- **PyPDF 6.1.1** - PDF document processing
- **Requests 2.32.5** - HTTP client for API calls
- **Python-dotenv 1.1.1** - Environment variable management

## 📋 Prerequisites

- Python 3.13 or higher
- OpenAI API key
- Pushover account (for notifications)

## 🔧 Installation

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PUSHOVER_TOKEN=your_pushover_token_here
   PUSHOVER_USER=your_pushover_user_key_here
   ```

## 📁 Project Structure

```
agentic-chatbot/
├── app.py                 # Main application file
├── main.py               # Entry point
├── pyproject.toml        # Project configuration
├── requirements.txt      # Development dependencies
├── requirements-prod.txt # Production dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore rules
├── me/                  # Personal profile data (excluded from git)
│   ├── linkedin.pdf     # LinkedIn profile PDF
│   └── summary.txt      # Professional summary
└── README.md           # This file
```

## 🚀 Usage

1. **Prepare your profile data**
   - Place your LinkedIn profile PDF in `me/linkedin.pdf`
   - Create a professional summary in `me/summary.txt`

2. **Run the application**
   ```bash
   python app.py
   ```

3. **Access the interface**
   - Open your browser and navigate to the URL shown in the terminal
   - Typically: `http://127.0.0.1:7860`

## 🎯 How It Works

### Core Functionality

1. **Persona Creation**: The chatbot loads your professional profile from PDF and text files to create an authentic representation
2. **Conversation Management**: Handles multi-turn conversations with context awareness
3. **Tool Integration**: Uses OpenAI's function calling to record user interactions and unknown questions
4. **Notification System**: Sends real-time notifications via Pushover for:
   - User contact information collection
   - Questions that couldn't be answered

### Key Components

- **Me Class**: Manages the AI persona, loads profile data, and handles conversations
- **Tool Functions**: Record user details and unknown questions
- **Gradio Interface**: Provides the web-based chat interface
- **Pushover Integration**: Handles notification delivery

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `PUSHOVER_TOKEN` | Pushover application token | Yes |
| `PUSHOVER_USER` | Pushover user/group key | Yes |

### Profile Setup

The chatbot requires two files in the `me/` directory:

1. **`linkedin.pdf`**: Your LinkedIn profile exported as PDF
2. **`summary.txt`**: A text file containing your professional summary

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

- [OpenAI](https://openai.com/) for providing the AI capabilities
- [Gradio](https://gradio.app/) for the excellent web interface framework
- [Pushover](https://pushover.net/) for reliable notification delivery

---

**Note**: This project is designed for professional use cases and includes features for tracking user interactions. Please ensure compliance with privacy regulations in your jurisdiction when deploying this application.
