# Local Setup Guide - Telegram Health Chatbot

This guide will help you set up and run the Telegram Health Chatbot on your local machine.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Internet connection for API calls
- Microphone access (for voice testing)

### Required API Keys
1. **Telegram Bot Token**: Get from @BotFather on Telegram
2. **Google Gemini API Key**: Get from Google AI Studio

## Step-by-Step Setup

### 1. Install Python Dependencies

First, create a virtual environment (recommended):
```bash
python -m venv health_chatbot_env
source health_chatbot_env/bin/activate  # On Windows: health_chatbot_env\Scripts\activate
```

Install required packages:
```bash
pip install python-telegram-bot==21.5
pip install google-genai
pip install gtts
pip install pydub
pip install speechrecognition
pip install sift-stack-py
```

### 2. Get Your Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather
3. Send `/newbot` command
4. Follow the prompts to create your bot:
   - Choose a name for your bot (e.g., "My Health Bot")
   - Choose a username ending in "bot" (e.g., "myhealthadvice_bot")
5. BotFather will give you a token like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
6. Save this token - you'll need it in step 4

### 3. Get Your Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Click "Get API Key" in the top right
4. Create a new API key
5. Copy the key (it looks like: `AIzaSyC8_6ar2og06J4YBDXdDRnAxHyPLAGmTGo`)
6. Save this key - you'll need it in step 4

### 4. Set Environment Variables

Create a `.env` file in your project directory:
```bash
# Create .env file
touch .env
```

Add your API keys to the `.env` file:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Download Project Files

Download all the Python files from this project:
- `main.py`
- `bot.py`
- `gemini_client.py`
- `voice_processor.py`
- `data_manager.py`
- `validators.py`
- `constants.py`

Place them all in the same directory.

### 6. Install System Dependencies (Optional)

For better audio processing, install FFmpeg:

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**On macOS:**
```bash
brew install ffmpeg
```

**On Windows:**
- Download FFmpeg from https://ffmpeg.org/download.html
- Add it to your system PATH

### 7. Modify main.py for Local Setup

Update `main.py` to load environment variables from `.env` file:

```python
#!/usr/bin/env python3
"""
Main entry point for the Telegram Health Chatbot.
Starts the bot with polling and handles graceful shutdown.
"""

import logging
import os
import signal
import sys
from bot import HealthChatBot

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Note: python-dotenv not installed. Using system environment variables.")

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def signal_handler(sig, frame):
    """Handle graceful shutdown on SIGINT or SIGTERM"""
    logger.info('Received shutdown signal. Stopping bot...')
    sys.exit(0)

def main():
    """Main function to start the health chatbot"""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Get API keys from environment variables
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not telegram_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        logger.error("Please set your Telegram bot token in .env file")
        sys.exit(1)
    
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY not found in environment variables")
        logger.error("Please set your Gemini API key in .env file")
        sys.exit(1)
    
    # Set Gemini API key in environment for the client
    os.environ["GEMINI_API_KEY"] = gemini_api_key
    
    try:
        # Initialize and start the bot
        bot = HealthChatBot(telegram_token)
        logger.info("Starting Telegram Health Chatbot...")
        bot.start()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 8. Install python-dotenv (Optional)

For easier environment variable management:
```bash
pip install python-dotenv
```

## Running the Bot

### 1. Start the Bot
```bash
python main.py
```

You should see output like:
```
2025-07-02 10:30:15,123 - __main__ - INFO - Starting Telegram Health Chatbot...
2025-07-02 10:30:15,124 - bot - INFO - Bot is starting with polling...
2025-07-02 10:30:15,500 - telegram.ext.Application - INFO - Application started
```

### 2. Test the Bot

1. Open Telegram
2. Search for your bot username (the one you created with BotFather)
3. Start a chat with your bot
4. Send `/start` to begin a health consultation
5. Follow the prompts to test all features

## Troubleshooting

### Common Issues

**1. "ModuleNotFoundError" errors:**
```bash
pip install [missing_module_name]
```

**2. "Conflict" errors:**
- Only one instance of the bot can run at a time
- Stop any other running instances
- Wait 30 seconds and restart

**3. Voice processing not working:**
- Install FFmpeg (see step 6)
- Check microphone permissions
- Ensure internet connection for Google Speech Recognition

**4. Gemini API errors:**
- Verify your API key is correct
- Check your Google AI Studio quota
- Ensure you have billing enabled (if required)

**5. Bot not responding:**
- Check your Telegram bot token
- Ensure the bot is not blocked
- Check internet connection

### Debug Mode

Add debug logging to see more details:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Testing Individual Components

Test Gemini connection:
```python
from gemini_client import GeminiClient
import os

os.environ["GEMINI_API_KEY"] = "your_key_here"
client = GeminiClient()
advice = await client.get_medical_advice("I have a headache", "English")
print(advice)
```

## File Structure

Your project directory should look like:
```
health_chatbot/
├── .env
├── main.py
├── bot.py
├── gemini_client.py
├── voice_processor.py
├── data_manager.py
├── validators.py
├── constants.py
├── users.json (created automatically)
└── temp audio files (created/deleted automatically)
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and private
- Consider using environment-specific API keys for development/production
- The `users.json` file contains user data - handle according to privacy requirements

## Performance Tips

- The bot can handle multiple users simultaneously
- Voice processing may take 5-10 seconds
- AI responses typically take 2-5 seconds
- Consider using webhooks instead of polling for production deployment

## Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review the console logs for error messages
3. Ensure all API keys are correctly set
4. Test individual components separately