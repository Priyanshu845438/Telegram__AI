"""
Telegram Health Chatbot implementation with voice processing and AI medical advice.
"""

import logging
import os
import tempfile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, filters, ContextTypes
)

from gemini_client import GeminiClient
from voice_processor import VoiceProcessor
from data_manager import DataManager
from validators import Validators
from constants import (
    STATES, LANGUAGES, GENDERS, MESSAGES,
    LANGUAGE_CODES, VOICE_LANGUAGES
)

logger = logging.getLogger(__name__)

class HealthChatBot:
    def __init__(self, token: str):
        """Initialize the health chatbot with necessary components"""
        self.token = token
        self.application = Application.builder().token(token).build()
        self.gemini_client = GeminiClient()
        self.voice_processor = VoiceProcessor()
        self.data_manager = DataManager()
        self.validators = Validators()
        
        # Setup conversation handler
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all message and command handlers"""
        # Conversation handler for data collection flow
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start_command)],
            states={
                STATES["LANGUAGE"]: [CallbackQueryHandler(self.handle_language_selection)],
                STATES["NAME"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_name)],
                STATES["AGE"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_age)],
                STATES["PHONE"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_phone)],
                STATES["GENDER"]: [CallbackQueryHandler(self.handle_gender_selection)],
                STATES["SYMPTOMS"]: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_symptoms_text),
                    MessageHandler(filters.VOICE, self.handle_symptoms_voice)
                ],
            },
            fallbacks=[
                CommandHandler('cancel', self.cancel_command),
                CommandHandler('help', self.help_command)
            ],
            per_message=False,
            per_chat=True,
            per_user=True
        )
        
        self.application.add_handler(conv_handler)
        self.application.add_handler(CommandHandler('help', self.help_command))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle /start command - begin conversation flow"""
        user = update.effective_user
        logger.info(f"User {user.id} started conversation")
        
        # Initialize user data in context
        context.user_data.clear()
        context.user_data['user_id'] = user.id
        context.user_data['username'] = user.username or user.first_name
        
        # Create language selection keyboard
        keyboard = [
            [InlineKeyboardButton("English", callback_data="en")],
            [InlineKeyboardButton("हिंदी (Hindi)", callback_data="hi")],
            [InlineKeyboardButton("मराठी (Marathi)", callback_data="mr")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🏥 Welcome to Health Chatbot!\n\n"
            "I can help you with medical advice based on your symptoms. "
            "Please select your preferred language:\n\n"
            "कृपया अपनी भाषा चुनें / कृपया आपली भाषा निवडा",
            reply_markup=reply_markup
        )
        
        return STATES["LANGUAGE"]
    
    async def handle_language_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle language selection"""
        query = update.callback_query
        await query.answer()
        
        language_code = query.data
        language_name = LANGUAGES.get(language_code, "English")
        
        context.user_data['language'] = language_code
        context.user_data['language_name'] = language_name
        
        message = MESSAGES[language_code]["language_selected"].format(language=language_name)
        await query.edit_message_text(message)
        
        # Ask for name
        name_message = MESSAGES[language_code]["ask_name"]
        await query.message.reply_text(name_message)
        
        return STATES["NAME"]
    
    async def handle_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle name input"""
        name = update.message.text.strip()
        language_code = context.user_data.get('language', 'en')
        
        if not self.validators.validate_name(name):
            error_message = MESSAGES[language_code]["invalid_name"]
            await update.message.reply_text(error_message)
            return STATES["NAME"]
        
        context.user_data['name'] = name
        
        # Ask for age
        age_message = MESSAGES[language_code]["ask_age"]
        await update.message.reply_text(age_message)
        
        return STATES["AGE"]
    
    async def handle_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle age input with validation"""
        age_text = update.message.text.strip()
        language_code = context.user_data.get('language', 'en')
        
        if not self.validators.validate_age(age_text):
            error_message = MESSAGES[language_code]["invalid_age"]
            await update.message.reply_text(error_message)
            return STATES["AGE"]
        
        context.user_data['age'] = int(age_text)
        
        # Ask for phone number
        phone_message = MESSAGES[language_code]["ask_phone"]
        await update.message.reply_text(phone_message)
        
        return STATES["PHONE"]
    
    async def handle_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle phone number input with validation"""
        phone = update.message.text.strip()
        language_code = context.user_data.get('language', 'en')
        
        if not self.validators.validate_phone(phone):
            error_message = MESSAGES[language_code]["invalid_phone"]
            await update.message.reply_text(error_message)
            return STATES["PHONE"]
        
        context.user_data['phone'] = phone
        
        # Create gender selection keyboard
        keyboard = [
            [InlineKeyboardButton(GENDERS[language_code]["male"], callback_data="male")],
            [InlineKeyboardButton(GENDERS[language_code]["female"], callback_data="female")],
            [InlineKeyboardButton(GENDERS[language_code]["other"], callback_data="other")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        gender_message = MESSAGES[language_code]["ask_gender"]
        await update.message.reply_text(gender_message, reply_markup=reply_markup)
        
        return STATES["GENDER"]
    
    async def handle_gender_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle gender selection"""
        query = update.callback_query
        await query.answer()
        
        gender_code = query.data
        language_code = context.user_data.get('language', 'en')
        gender_name = GENDERS[language_code][gender_code]
        
        context.user_data['gender'] = gender_name
        
        await query.edit_message_text(f"Gender: {gender_name}")
        
        # Ask for symptoms
        symptoms_message = MESSAGES[language_code]["ask_symptoms"]
        await query.message.reply_text(symptoms_message)
        
        return STATES["SYMPTOMS"]
    
    async def handle_symptoms_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle text symptoms input"""
        symptoms = update.message.text.strip()
        language_code = context.user_data.get('language', 'en')
        
        if not symptoms or len(symptoms) < 5:
            error_message = MESSAGES[language_code]["invalid_symptoms"]
            await update.message.reply_text(error_message)
            return STATES["SYMPTOMS"]
        
        context.user_data['symptoms'] = symptoms
        await self._process_user_data(update, context)
        
        return ConversationHandler.END
    
    async def handle_symptoms_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle voice symptoms input"""
        language_code = context.user_data.get('language', 'en')
        
        try:
            # Show processing message
            processing_message = MESSAGES[language_code]["processing_voice"]
            status_msg = await update.message.reply_text(processing_message)
            
            # Download voice file
            voice_file = await update.message.voice.get_file()
            
            # Create temporary file for voice
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
                await voice_file.download_to_drive(temp_file.name)
                temp_file_path = temp_file.name
            
            try:
                # Transcribe voice to text
                symptoms = await self.voice_processor.transcribe_voice(
                    temp_file_path, 
                    LANGUAGE_CODES.get(language_code, 'en')
                )
                
                if not symptoms or len(symptoms.strip()) < 5:
                    error_message = MESSAGES[language_code]["voice_transcription_failed"]
                    await status_msg.edit_text(error_message)
                    return STATES["SYMPTOMS"]
                
                context.user_data['symptoms'] = symptoms.strip()
                
                # Update status message
                transcription_message = MESSAGES[language_code]["voice_transcribed"].format(symptoms=symptoms)
                await status_msg.edit_text(transcription_message)
                
                # Process the user data
                await self._process_user_data(update, context)
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        
        except Exception as e:
            logger.error(f"Error processing voice message: {e}")
            error_message = MESSAGES[language_code]["voice_processing_error"]
            await update.message.reply_text(error_message)
            return STATES["SYMPTOMS"]
        
        return ConversationHandler.END
    
    async def _process_user_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process collected user data: get AI advice, generate voice, save data"""
        language_code = context.user_data.get('language', 'en')
        
        try:
            # Show processing message
            processing_message = MESSAGES[language_code]["generating_advice"]
            status_msg = await update.message.reply_text(processing_message)
            
            # Get AI medical advice from Gemini
            symptoms = context.user_data['symptoms']
            language_name = context.user_data['language_name']
            
            advice = await self.gemini_client.get_medical_advice(symptoms, language_name)
            
            if not advice:
                error_message = MESSAGES[language_code]["advice_generation_failed"]
                await status_msg.edit_text(error_message)
                return
            
            context.user_data['advice'] = advice
            
            # Update status
            await status_msg.edit_text(MESSAGES[language_code]["advice_generated"])
            
            # Send text advice
            advice_message = MESSAGES[language_code]["advice_header"] + "\n\n" + advice
            await update.message.reply_text(advice_message)
            
            # Generate and send voice advice
            voice_lang = VOICE_LANGUAGES.get(language_code, 'en')
            voice_file_path = await self.voice_processor.text_to_speech(advice, voice_lang)
            
            if voice_file_path and os.path.exists(voice_file_path):
                with open(voice_file_path, 'rb') as voice_file:
                    voice_message = MESSAGES[language_code]["voice_advice"]
                    await update.message.reply_voice(
                        voice=voice_file,
                        caption=voice_message
                    )
                
                # Clean up voice file
                os.unlink(voice_file_path)
            
            # Save user data to JSON
            self.data_manager.save_user_data(context.user_data)
            
            # Send completion message
            completion_message = MESSAGES[language_code]["consultation_complete"]
            await update.message.reply_text(completion_message)
            
        except Exception as e:
            logger.error(f"Error processing user data: {e}")
            error_message = MESSAGES[language_code]["processing_error"]
            await update.message.reply_text(error_message)
    
    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle /cancel command"""
        language_code = context.user_data.get('language', 'en')
        cancel_message = MESSAGES[language_code]["cancelled"]
        await update.message.reply_text(cancel_message)
        context.user_data.clear()
        return ConversationHandler.END
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle /help command"""
        help_text = (
            "🏥 *Health Chatbot Help*\n\n"
            "*Available Commands:*\n"
            "/start - Start health consultation\n"
            "/cancel - Cancel current consultation\n"
            "/help - Show this help message\n\n"
            "*How it works:*\n"
            "1. Select your language\n"
            "2. Provide personal information\n"
            "3. Describe your symptoms (text or voice)\n"
            "4. Receive AI-powered medical advice\n"
            "5. Get voice response in your language\n\n"
            "*Supported Languages:*\n"
            "• English\n"
            "• हिंदी (Hindi)\n"
            "• मराठी (Marathi)\n\n"
            "_Note: This bot provides general health advice only. "
            "For serious conditions, please consult a qualified doctor._"
        )
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
        return ConversationHandler.END
    
    def start(self):
        """Start the bot with polling"""
        logger.info("Bot is starting with polling...")
        try:
            self.application.run_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES,
                close_loop=False
            )
        except Exception as e:
            logger.error(f"Error running bot: {e}")
            if "Conflict" in str(e):
                logger.info("Bot conflict detected. This usually means another instance is running.")
                logger.info("Waiting 30 seconds and retrying...")
                import time
                time.sleep(30)
                try:
                    self.application.run_polling(
                        drop_pending_updates=True,
                        allowed_updates=Update.ALL_TYPES,
                        close_loop=False
                    )
                except Exception as retry_error:
                    logger.error(f"Retry failed: {retry_error}")
                    raise
            else:
                raise
