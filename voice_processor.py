"""
Voice processing module for speech-to-text and text-to-speech functionality.
"""

import logging
import os
import tempfile
import asyncio
from typing import Optional
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment

logger = logging.getLogger(__name__)

class VoiceProcessor:
    def __init__(self):
        """Initialize voice processor with speech recognition"""
        self.recognizer = sr.Recognizer()
        
        # Configure speech recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
    
    async def transcribe_voice(self, ogg_file_path: str, language: str = 'en') -> Optional[str]:
        """
        Transcribe voice message from OGG file to text.
        
        Args:
            ogg_file_path (str): Path to the OGG voice file
            language (str): Language code for speech recognition
            
        Returns:
            Optional[str]: Transcribed text or None if failed
        """
        try:
            # Convert OGG to WAV for better compatibility with speech_recognition
            wav_file_path = await self._convert_ogg_to_wav(ogg_file_path)
            
            if not wav_file_path:
                logger.error("Failed to convert OGG to WAV")
                return None
            
            try:
                # Perform speech recognition in a thread to avoid blocking
                loop = asyncio.get_event_loop()
                text = await loop.run_in_executor(
                    None, 
                    self._perform_speech_recognition,
                    wav_file_path,
                    language
                )
                
                logger.info(f"Successfully transcribed voice message: {text[:50]}...")
                return text
            
            finally:
                # Clean up WAV file
                if os.path.exists(wav_file_path):
                    os.unlink(wav_file_path)
        
        except Exception as e:
            logger.error(f"Error transcribing voice: {e}")
            return None
    
    async def _convert_ogg_to_wav(self, ogg_file_path: str) -> Optional[str]:
        """Convert OGG file to WAV format"""
        try:
            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                wav_file_path = temp_wav.name
            
            # Convert using pydub in a thread
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._convert_audio_file,
                ogg_file_path,
                wav_file_path
            )
            
            return wav_file_path
        
        except Exception as e:
            logger.error(f"Error converting OGG to WAV: {e}")
            return None
    
    def _convert_audio_file(self, input_path: str, output_path: str):
        """Convert audio file using pydub"""
        audio = AudioSegment.from_ogg(input_path)
        audio.export(output_path, format="wav")
    
    def _perform_speech_recognition(self, wav_file_path: str, language: str) -> str:
        """Perform speech recognition on WAV file"""
        with sr.AudioFile(wav_file_path) as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Record the audio
            audio = self.recognizer.record(source)
        
        try:
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            raise ValueError("Could not understand audio")
        
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            raise ValueError(f"Speech recognition service error: {e}")
    
    async def text_to_speech(self, text: str, language: str = 'en') -> Optional[str]:
        """
        Convert text to speech and save as audio file.
        
        Args:
            text (str): Text to convert to speech
            language (str): Language code for TTS
            
        Returns:
            Optional[str]: Path to generated audio file or None if failed
        """
        try:
            # Create temporary file for audio output
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
                audio_file_path = temp_audio.name
            
            # Generate TTS in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._generate_tts,
                text,
                language,
                audio_file_path
            )
            
            logger.info("Successfully generated TTS audio")
            return audio_file_path
        
        except Exception as e:
            logger.error(f"Error generating TTS: {e}")
            return None
    
    def _generate_tts(self, text: str, language: str, output_path: str):
        """Generate TTS using gTTS"""
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_path)
