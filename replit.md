# Telegram Health Chatbot

## Overview

This is a Telegram-based health consultation chatbot that uses AI to provide medical advice. The bot supports multilingual conversations (English, Hindi, Marathi), voice message processing, and stores user health data. It integrates with Google's Gemini AI for generating medical responses and includes comprehensive voice processing capabilities for speech-to-text and text-to-speech functionality.

## System Architecture

The application follows a modular, event-driven architecture built around the Telegram Bot API. It uses a conversation flow pattern to collect user health data and provide AI-generated medical advice.

### Core Components:
- **Bot Handler**: Main conversation orchestrator using Telegram's ConversationHandler
- **AI Integration**: Google Gemini API for medical advice generation
- **Voice Processing**: Speech recognition and text-to-speech capabilities
- **Data Storage**: JSON file-based user data persistence
- **Validation Layer**: Input validation for user data integrity

## Key Components

### 1. HealthChatBot (bot.py)
- **Purpose**: Main bot controller managing conversation flow and user interactions
- **Key Features**: Multi-state conversation handling, command processing, callback query management
- **Dependencies**: Telegram Bot API, Gemini client, voice processor, data manager

### 2. GeminiClient (gemini_client.py)
- **Purpose**: Interface with Google's Gemini AI for medical advice generation
- **Key Features**: Contextual prompt creation, temperature-controlled responses, multilingual support
- **Configuration**: Uses environment variable for API key, optimized for medical use cases

### 3. VoiceProcessor (voice_processor.py)
- **Purpose**: Handle voice message transcription and audio file generation
- **Key Features**: OGG to WAV conversion, speech recognition, text-to-speech synthesis
- **Technologies**: SpeechRecognition library, gTTS, pydub for audio processing

### 4. DataManager (data_manager.py)
- **Purpose**: User data persistence and retrieval
- **Storage**: JSON file-based with thread-safe operations
- **Features**: User session management, conversation history tracking

### 5. Validators (validators.py)
- **Purpose**: Input validation for user data
- **Validation Types**: Name validation (multilingual), phone number validation, age validation
- **Pattern Matching**: Regex-based validation with Unicode support

## Data Flow

1. **User Interaction**: User starts conversation with /start command
2. **Language Selection**: Bot presents language options (English, Hindi, Marathi)
3. **Data Collection**: Sequential collection of name, age, phone, gender
4. **Symptom Input**: Text or voice message describing health symptoms
5. **AI Processing**: Gemini AI generates medical advice based on symptoms and language
6. **Response Delivery**: Text and optional voice response to user
7. **Data Storage**: Complete conversation saved to JSON file

## External Dependencies

### APIs and Services:
- **Telegram Bot API**: Core messaging platform
- **Google Gemini AI**: Medical advice generation
- **Google Text-to-Speech**: Voice response generation

### Python Libraries:
- `python-telegram-bot`: Telegram Bot API wrapper
- `google-genai`: Google Gemini AI client
- `speech_recognition`: Voice-to-text conversion
- `gtts`: Google Text-to-Speech
- `pydub`: Audio file manipulation

### System Requirements:
- Environment variables for API keys (TELEGRAM_BOT_TOKEN, GEMINI_API_KEY)
- File system access for temporary audio files and data storage
- Internet connectivity for API calls

## Deployment Strategy

### Environment Setup:
- Python 3.8+ runtime environment
- Environment variables configuration for API keys
- File system permissions for data storage and temp files

### Configuration:
- JSON-based data storage (users.json)
- Logging configuration with appropriate levels
- Signal handling for graceful shutdown

### Scaling Considerations:
- Single-instance deployment with file-based storage
- Thread-safe data operations for concurrent users
- Temporary file cleanup for voice processing

## Changelog

- July 02, 2025: Complete implementation of voice-enabled Telegram health chatbot
  - ✅ Multi-language support (English, Hindi, Marathi)
  - ✅ Voice message processing (speech-to-text)
  - ✅ AI-powered medical advice using Google Gemini
  - ✅ Text-to-speech responses
  - ✅ Local JSON data storage
  - ✅ Input validation and error handling
  - ✅ Conversation flow management
- July 02, 2025: Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.