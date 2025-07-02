@echo off
echo Setting up Telegram Health Chatbot locally...
echo.

echo Creating virtual environment...
python -m venv health_chatbot_env
echo.

echo Activating virtual environment...
call health_chatbot_env\Scripts\activate
echo.

echo Installing required packages...
pip install python-telegram-bot==21.5
pip install google-genai
pip install gtts
pip install pydub
pip install speechrecognition
pip install python-dotenv
echo.

echo Setup complete!
echo.
echo Next steps:
echo 1. Create a .env file with your API keys
echo 2. Add your TELEGRAM_BOT_TOKEN and GEMINI_API_KEY to .env
echo 3. Run: python main.py
echo.
pause