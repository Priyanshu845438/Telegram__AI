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
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "7881650666:AAGpX2vniGLdltgYjbRHylc-fxkio2hpS5g")
    gemini_api_key = os.getenv("GEMINI_API_KEY", "AIzaSyC8_6ar2og06J4YBDXdDRnAxHyPLAGmTGo")
    
    if not telegram_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        sys.exit(1)
    
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY not found in environment variables")
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
