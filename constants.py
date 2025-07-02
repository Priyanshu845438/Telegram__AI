"""
Constants and configuration for the Telegram Health Chatbot.
"""

# Conversation states
STATES = {
    "LANGUAGE": 0,
    "NAME": 1,
    "AGE": 2,
    "PHONE": 3,
    "GENDER": 4,
    "SYMPTOMS": 5
}

# Supported languages
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi"
}

# Language codes for speech recognition
LANGUAGE_CODES = {
    "en": "en-US",
    "hi": "hi-IN",
    "mr": "mr-IN"
}

# Language codes for text-to-speech (gTTS)
VOICE_LANGUAGES = {
    "en": "en",
    "hi": "hi",
    "mr": "mr"
}

# Gender options by language
GENDERS = {
    "en": {
        "male": "Male",
        "female": "Female", 
        "other": "Other"
    },
    "hi": {
        "male": "पुरुष",
        "female": "महिला",
        "other": "अन्य"
    },
    "mr": {
        "male": "पुरुष",
        "female": "महिला", 
        "other": "इतर"
    }
}

# Messages by language
MESSAGES = {
    "en": {
        "language_selected": "✅ Language set to {language}",
        "ask_name": "👤 Please enter your full name:",
        "invalid_name": "❌ Please enter a valid name (2-50 characters, letters only).",
        "ask_age": "🎂 Please enter your age:",
        "invalid_age": "❌ Please enter a valid age (1-120 years).",
        "ask_phone": "📱 Please enter your phone number (10 digits):",
        "invalid_phone": "❌ Please enter a valid phone number (10 digits).",
        "ask_gender": "⚧ Please select your gender:",
        "ask_symptoms": "🩺 Please describe your symptoms (you can type text or send a voice message):",
        "invalid_symptoms": "❌ Please provide more details about your symptoms (at least 5 characters).",
        "processing_voice": "🎤 Processing your voice message...",
        "voice_transcribed": "✅ Voice transcribed: {symptoms}\n\nProcessing your request...",
        "voice_transcription_failed": "❌ Could not understand the voice message. Please try again or type your symptoms.",
        "voice_processing_error": "❌ Error processing voice message. Please try typing your symptoms instead.",
        "generating_advice": "🔄 Generating medical advice...",
        "advice_generated": "✅ Medical advice generated!",
        "advice_generation_failed": "❌ Could not generate medical advice. Please try again later.",
        "advice_header": "🩺 *Medical Advice:*",
        "voice_advice": "🔊 Voice advice generated",
        "consultation_complete": "✅ Consultation completed! Your data has been saved.\n\n🔄 Use /start to begin a new consultation.",
        "processing_error": "❌ An error occurred while processing your request. Please try again.",
        "cancelled": "❌ Consultation cancelled. Use /start to begin a new consultation.",
    },
    "hi": {
        "language_selected": "✅ भाषा {language} में सेट की गई",
        "ask_name": "👤 कृपया अपना पूरा नाम दर्ज करें:",
        "invalid_name": "❌ कृपया एक वैध नाम दर्ज करें (2-50 अक्षर, केवल अक्षर)।",
        "ask_age": "🎂 कृपया अपनी आयु दर्ज करें:",
        "invalid_age": "❌ कृपया एक वैध आयु दर्ज करें (1-120 वर्ष)।",
        "ask_phone": "📱 कृपया अपना फोन नंबर दर्ज करें (10 अंक):",
        "invalid_phone": "❌ कृपया एक वैध फोन नंबर दर्ज करें (10 अंक)।",
        "ask_gender": "⚧ कृपया अपना लिंग चुनें:",
        "ask_symptoms": "🩺 कृपया अपने लक्षणों का वर्णन करें (आप टेक्स्ट टाइप कर सकते हैं या वॉइस मैसेज भेज सकते हैं):",
        "invalid_symptoms": "❌ कृपया अपने लक्षणों के बारे में अधिक विवरण दें (कम से कम 5 अक्षर)।",
        "processing_voice": "🎤 आपका वॉइस मैसेज प्रोसेस हो रहा है...",
        "voice_transcribed": "✅ वॉइस ट्रांसक्राइब किया गया: {symptoms}\n\nआपका अनुरोध प्रोसेस हो रहा है...",
        "voice_transcription_failed": "❌ वॉइस मैसेज समझ नहीं आया। कृपया फिर से कोशिश करें या अपने लक्षण टाइप करें।",
        "voice_processing_error": "❌ वॉइस मैसेज प्रोसेसिंग में त्रुटि। कृपया अपने लक्षण टाइप करने का प्रयास करें।",
        "generating_advice": "🔄 चिकित्सा सलाह तैयार की जा रही है...",
        "advice_generated": "✅ चिकित्सा सलाह तैयार की गई!",
        "advice_generation_failed": "❌ चिकित्सा सलाह तैयार नहीं की जा सकी। कृपया बाद में फिर से कोशिश करें।",
        "advice_header": "🩺 *चिकित्सा सलाह:*",
        "voice_advice": "🔊 वॉइस सलाह तैयार की गई",
        "consultation_complete": "✅ परामर्श पूरा हुआ! आपका डेटा सेव कर दिया गया है।\n\n🔄 नया परामर्श शुरू करने के लिए /start का उपयोग करें।",
        "processing_error": "❌ आपका अनुरोध प्रोसेस करते समय त्रुटि हुई। कृपया फिर से कोशिश करें।",
        "cancelled": "❌ परामर्श रद्द किया गया। नया परामर्श शुरू करने के लिए /start का उपयोग करें।",
    },
    "mr": {
        "language_selected": "✅ भाषा {language} मध्ये सेट केली",
        "ask_name": "👤 कृपया तुमचे पूर्ण नाव टाका:",
        "invalid_name": "❌ कृपया वैध नाव टाका (2-50 अक्षरे, फक्त अक्षरे)।",
        "ask_age": "🎂 कृपया तुमचे वय टाका:",
        "invalid_age": "❌ कृपया वैध वय टाका (1-120 वर्षे)।",
        "ask_phone": "📱 कृपया तुमचा फोन नंबर टाका (10 अंक):",
        "invalid_phone": "❌ कृपया वैध फोन नंबर टाका (10 अंक)।",
        "ask_gender": "⚧ कृपया तुमचे लिंग निवडा:",
        "ask_symptoms": "🩺 कृपया तुमच्या लक्षणांचे वर्णन करा (तुम्ही मजकूर टाईप करू शकता किंवा व्हॉइस मेसेज पाठवू शकता):",
        "invalid_symptoms": "❌ कृपया तुमच्या लक्षणांबद्दल अधिक तपशील द्या (किमान 5 अक्षरे)।",
        "processing_voice": "🎤 तुमचा व्हॉइस मेसेज प्रोसेस होत आहे...",
        "voice_transcribed": "✅ व्हॉइस ट्रान्सक्राइब केला: {symptoms}\n\nतुमची विनंती प्रोसेस होत आहे...",
        "voice_transcription_failed": "❌ व्हॉइस मेसेज समजला नाही। कृपया पुन्हा प्रयत्न करा किंवा तुमची लक्षणे टाईप करा।",
        "voice_processing_error": "❌ व्हॉइस मेसेज प्रोसेसिंगमध्ये त्रुटी। कृपया तुमची लक्षणे टाईप करण्याचा प्रयत्न करा।",
        "generating_advice": "🔄 वैद्यकीय सल्ला तयार केला जात आहे...",
        "advice_generated": "✅ वैद्यकीय सल्ला तयार केला!",
        "advice_generation_failed": "❌ वैद्यकीय सल्ला तयार करू शकलो नाही। कृपया नंतर पुन्हा प्रयत्न करा।",
        "advice_header": "🩺 *वैद्यकीय सल्ला:*",
        "voice_advice": "🔊 व्हॉइस सल्ला तयार केला",
        "consultation_complete": "✅ सल्लामसलत पूर्ण झाली! तुमचा डेटा सेव्ह केला गेला आहे।\n\n🔄 नवीन सल्लामसलत सुरू करण्यासाठी /start वापरा।",
        "processing_error": "❌ तुमची विनंती प्रोसेस करताना त्रुटी झाली। कृपया पुन्हा प्रयत्न करा।",
        "cancelled": "❌ सल्लामसलत रद्द केली. नवीन सल्लामसलत सुरू करण्यासाठी /start वापरा।",
    }
}
