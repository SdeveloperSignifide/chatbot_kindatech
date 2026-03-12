# Chatbot

A comprehensive AI-powered chatbot application for Frappe framework that provides intelligent conversational capabilities for various use cases.

## Features

- **Multi-Provider Support**: Compatible with OpenAI, Groq, DeepSeek, and Grok AI providers
- **Document Processing**: Support for PDF, DOCX, and image file processing using OCR
- **Conversation Management**: Complete conversation history and context management
- **Intent Recognition**: Advanced intent classification for better user understanding
- **Memory System**: Persistent memory for maintaining conversation context
- **Settings Management**: Configurable chatbot settings through Frappe desk
- **Web Interface**: Clean and responsive web interface for user interactions

## Requirements

The chatbot app requires the following Python packages:

- `docx2txt==0.9` - For processing Microsoft Word documents
- `Markdown==3.10.2` - For markdown text processing
- `Pillow==12.1.1` - For image processing and manipulation
- `pypdf==6.8.0` - For PDF document processing
- `pytesseract==0.3.13` - For OCR (Optical Character Recognition)
- `Requests==2.32.5` - For HTTP requests to AI providers

## Installation

### Prerequisites

- Frappe bench setup
- Python 3.8+
- Active Frappe site

### Step-by-Step Installation

1. **Navigate to your bench directory:**
   ```bash
   cd $PATH_TO_YOUR_BENCH
   ```

2. **Get the chatbot app:**
   ```bash
   bench get-app $URL_OF_THIS_REPO --branch develop
   ```

3. **Install the app on your site:**
   ```bash
   bench install-app chatbot
   ```

4. **Install Python requirements:**
   ```bash
   ./env/bin/pip install -r apps/chatbot/chatbot/requirements.txt
   ```

5. **Migrate the database:**
   ```bash
   bench migrate
   ```

6. **Restart the bench:**
   ```bash
   bench restart
   ```

## Configuration

### Initial Setup

1. **Access Chatbot Settings:**
   - Go to Frappe Desk
   - Navigate to Chatbot > Chatbot Settings
   - Create a new settings record

2. **Configure AI Provider:**
   - Select your preferred AI provider (OpenAI, Groq, DeepSeek, or Grok)
   - Enter your API key
   - Configure model parameters (temperature, max_tokens, etc.)
   - Set the settings as active

3. **Enable Chatbot:**
   - Set the chatbot status to "Active"
   - Configure response templates and prompts
   - Set up conversation limits and restrictions

### Supported AI Providers

- **OpenAI**: GPT models with full feature support
- **Groq**: Fast inference with various model options
- **DeepSeek**: Advanced reasoning capabilities
- **Grok**: Real-time information processing

## Usage

### Web Interface

1. Access the chatbot through your Frappe site
2. Start conversations using the web interface
3. Upload documents (PDF, DOCX, images) for context
4. View conversation history and manage settings

### API Integration

The chatbot provides REST APIs for integration:

```python
# Example API call
import frappe

# Send message to chatbot
response = frappe.call(
    "chatbot.api.chatbot_api.send_message",
    message="Hello, how can you help me?",
    conversation_id="your-conversation-id"
)
```

### Document Processing

The chatbot can process various document types:

- **PDF Files**: Extract text content using PyPDF
- **DOCX Files**: Process Microsoft Word documents
- **Images**: Extract text using OCR (Tesseract)

## Development

### Project Structure

```
chatbot/
├── chatbot/
│   ├── api/                 # API endpoints
│   ├── core/                # Core chatbot engine
│   ├── providers/           # AI provider implementations
│   ├── services/            # Business logic services
│   ├── utils/               # Utility functions
│   ├── templates/           # Web templates
│   └── doctypes/           # Frappe doctypes
├── public/                  # Static assets
└── config/                  # Configuration files
```

### Core Components

- **Engine**: Main chatbot processing engine
- **Intent Classifier**: Natural language understanding
- **Document Classifier**: Document type recognition
- **Memory System**: Context management
- **Response Router**: Response generation and routing

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/chatbot
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- **ruff**: Python linting and formatting
- **eslint**: JavaScript linting
- **prettier**: Code formatting
- **pyupgrade**: Python syntax upgrading

### Development Setup

1. Clone the repository
2. Install development dependencies
3. Set up pre-commit hooks
4. Run tests and linting before submitting PRs

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your AI provider API key is correctly configured in Chatbot Settings
2. **Document Processing**: Verify that Tesseract OCR is installed for image processing
3. **Memory Issues**: Check conversation limits and memory settings
4. **Performance**: Monitor response times and adjust model parameters

### Logs

Check the following logs for debugging:

```bash
# Frappe logs
bench --site [site-name] logs

# Chatbot specific logs
tail -f logs/chatbot.log
```

## License

This project is licensed under the MIT License - see the [license.txt](license.txt) file for details.

## Support

For support and questions:

- **Email**: simomutu8@gmail.com
- **Issues**: Create an issue in the repository
- **Documentation**: Check the Frappe community forums

## Changelog

### Version 1.0.0
- Initial release with multi-provider support
- Document processing capabilities
- Web interface and API endpoints
- Conversation management system
<img width="1444" height="839" alt="Screenshot from 2026-03-12 13-01-36" src="https://github.com/user-attachments/assets/294f6447-7eed-4716-9c2e-4551efa15752" />
<img width="1444" height="839" alt="Screenshot from 2026-03-12 13-00-41" src="https://github.com/user-attachments/assets/d7c65585-4afc-4cbf-9cdf-2c0b2d84c02b" />
<img width="865" height="875" alt="Screenshot from 2026-03-12 13-06-52" src="https://github.com/user-attachments/assets/0d7ab873-46cb-4a1e-960d-7135f3929155" />
