#!/bin/bash

echo "Setting up Telegram Health Chatbot locally..."
echo

echo "Creating virtual environment..."
python3 -m venv health_chatbot_env
echo

echo "Activating virtual environment..."
source health_chatbot_env/bin/activate
echo

echo "Installing required packages..."
pip install python-telegram-bot==21.5
pip install google-genai
pip install gtts
pip install pydub
pip install speechrecognition
pip install python-dotenv
echo

echo "Setup complete!"
echo
echo "Next steps:"
echo "1. Create a .env file with your API keys"
echo "2. Add your TELEGRAM_BOT_TOKEN and GEMINI_API_KEY to .env"
echo "3. Run: python main.py"
echo
echo "To activate environment in future:"
echo "source health_chatbot_env/bin/activate"