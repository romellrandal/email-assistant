# Email Assistant

An AI-powered email assistant using OpenAI's Assistant API with Gmail and Google Calendar integration. This intelligent assistant can help you manage emails, schedule meetings, and perform various email-related tasks through natural language commands.

## 🚀 Features

- **Email Management**: Read, compose, and manage Gmail messages
- **Calendar Integration**: Schedule meetings and manage Google Calendar events
- **File Operations**: Read and write files on your system
- **Rich Terminal Interface**: Beautiful, user-friendly command-line interface
- **Conversation Memory**: Remembers your conversation history until you reset
- **Tool Integration**: Extensible tool system for adding new capabilities

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Google Cloud Project with Gmail API enabled
- Google OAuth2 credentials

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/romellrandal/email-assistant.git
   cd email-assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ASSISTANT_ID=your_assistant_id_here
   ```

## 🔐 Google API Setup

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API and Google Calendar API

### 2. Create OAuth2 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Download the credentials JSON file
4. Rename it to `Credentials.json` and place it in the project root

### 3. First Run Setup
On first run, the application will:
- Open a browser window for Google OAuth authentication
- Save the authentication token for future use

## 🚀 Usage

1. **Start the assistant:**
   ```bash
   python main.py
   ```

2. **Available commands:**
   - `reset` - Start a new conversation
   - `quit` - Exit the program
   - `update` - Update assistant configuration

3. **Example interactions:**
   ```
   You: What was the last email I received?
   You: Schedule a meeting with John tomorrow at 2 PM
   You: Read my unread emails from this week
   You: Compose a reply to the latest email
   ```

## 🛠️ Available Tools

### Email Tools
- Read emails (inbox, sent, drafts)
- Compose and send emails
- Search emails by criteria
- Mark emails as read/unread
- Move emails between folders

### Calendar Tools
- Schedule meetings and events
- View calendar events
- Update existing events
- Delete calendar events
- Check availability

### File Tools
- Read text files
- Write content to files
- List directory contents

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `ASSISTANT_ID`: Your OpenAI Assistant ID (auto-generated on first run)

### Google API Files
- `Credentials.json`: Google OAuth2 credentials (excluded from Git)
- `token.pickle`: OAuth2 token cache (excluded from Git)

## 📁 Project Structure

```
email-assistant/
├── main.py                 # Main application entry point
├── prompts.py              # Assistant instructions and prompts
├── terminalstyle.py        # Terminal UI styling
├── tools/                  # Tool implementations
│   ├── gmail_tools.py     # Gmail API integration
│   ├── calendar_tools.py  # Google Calendar integration
│   ├── file_tools.py      # File system operations
│   └── tool_handler.py    # Tool execution handler
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔒 Security

Sensitive files are automatically excluded from Git:
- `.env` - Contains API keys
- `Credentials.json` - Google API credentials
- `token.pickle` - OAuth2 tokens
- `thread_id.txt` - Conversation thread IDs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues:
1. Check that all environment variables are set correctly
2. Ensure Google API credentials are properly configured
3. Verify that required APIs are enabled in Google Cloud Console
4. Check the console output for error messages

---

**Built with ❤️ using OpenAI Assistant API and Google APIs**
