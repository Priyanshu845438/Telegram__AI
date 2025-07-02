"""
Google Gemini AI client for generating medical advice.
"""

import logging
import os
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        """Initialize Gemini client with API key"""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
    
    async def get_medical_advice(self, symptoms: str, language: str) -> str:
        """
        Get medical advice from Gemini AI based on symptoms and preferred language.
        
        Args:
            symptoms (str): User's reported symptoms
            language (str): Preferred language for response
            
        Returns:
            str: Medical advice from AI
        """
        try:
            # Create a safe, responsible prompt for medical advice
            prompt = self._create_medical_prompt(symptoms, language)
            
            logger.info(f"Requesting medical advice for symptoms in {language}")
            
            # Generate content using Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,  # Lower temperature for more consistent medical advice
                    max_output_tokens=500,
                    top_p=0.8
                )
            )
            
            if response.text:
                advice = response.text.strip()
                logger.info("Successfully generated medical advice")
                return advice
            else:
                logger.warning("Empty response from Gemini API")
                return self._get_fallback_advice(language)
        
        except Exception as e:
            logger.error(f"Error getting medical advice from Gemini: {e}")
            return self._get_fallback_advice(language)
    
    def _create_medical_prompt(self, symptoms: str, language: str) -> str:
        """Create a responsible medical advice prompt"""
        prompt = f"""You are a helpful medical assistant providing general health guidance. 

IMPORTANT GUIDELINES:
- Provide general health advice only, not medical diagnosis
- Always recommend consulting a qualified doctor for serious concerns
- Be supportive and helpful while maintaining medical responsibility
- Keep response concise but informative (under 300 words)
- Respond in {language} language

USER SYMPTOMS: {symptoms}

Please provide safe, general health advice and recommendations for these symptoms. Include when to seek professional medical care. Remember to emphasize that this is general guidance only and not a medical diagnosis.

Respond in {language}."""
        
        return prompt
    
    def _get_fallback_advice(self, language: str) -> str:
        """Provide fallback advice when AI fails"""
        fallback_messages = {
            "English": (
                "I'm sorry, I'm currently unable to provide specific advice for your symptoms. "
                "Here are some general health recommendations:\n\n"
                "• Stay hydrated and get adequate rest\n"
                "• Monitor your symptoms closely\n"
                "• Consider consulting a healthcare professional if symptoms persist or worsen\n"
                "• Seek immediate medical attention for severe or emergency symptoms\n\n"
                "Please consult with a qualified doctor for proper medical evaluation and treatment."
            ),
            "Hindi": (
                "मुझे खुशी है कि आपने संपर्क किया। फिलहाल मैं आपके लक्षणों के लिए विशिष्ट सलाह नहीं दे पा रहा हूं। "
                "यहां कुछ सामान्य स्वास्थ्य सुझाव हैं:\n\n"
                "• पर्याप्त पानी पिएं और आराम करें\n"
                "• अपने लक्षणों पर ध्यान रखें\n"
                "• यदि लक्षण बने रहें या बढ़ें तो डॉक्टर से सलाह लें\n"
                "• गंभीर लक्षणों के लिए तुरंत चिकित्सा सहायता लें\n\n"
                "कृपया उचित चिकित्सा मूल्यांकन के लिए किसी योग्य डॉक्टर से सलाह लें।"
            ),
            "Marathi": (
                "मला खुशी आहे की तुम्ही संपर्क केला। सध्या मी तुमच्या लक्षणांसाठी विशिष्ट सल्ला देऊ शकत नाही। "
                "येथे काही सामान्य आरोग्य सूचना आहेत:\n\n"
                "• पुरेसे पाणी प्या आणि आराम करा\n"
                "• तुमच्या लक्षणांवर लक्ष ठेवा\n"
                "• लक्षणे कायम राहिल्यास किंवा वाढल्यास डॉक्टरांचा सल्ला घ्या\n"
                "• गंभीर लक्षणांसाठी तात्काळ वैद्यकीय मदत घ्या\n\n"
                "कृपया योग्य वैद्यकीय तपासणीसाठी पात्र डॉक्टरांचा सल्ला घ्या।"
            )
        }
        
        return fallback_messages.get(language, fallback_messages["English"])
