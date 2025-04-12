# app/services/translation_service.py
from deep_translator import GoogleTranslator
from langdetect import detect
import logging
from typing import Optional

class TranslationService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        try:
            # No initialization needed for deep_translator
            self.logger.info("Translation service initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize translation service: {str(e)}")
            raise
        
        # Supported Indian languages with ISO 639-1 codes
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'mr': 'Marathi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'gu': 'Gujarati',
            'ml': 'Malayalam',
            'bn': 'Bengali',
            'or': 'Odia'
        }

    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text
        Args:
            text (str): Input text
        Returns:
            str: Language code (e.g., 'hi' for Hindi)
        """
        try:
            detected_lang = detect(text)
            
            if detected_lang in self.supported_languages:
                return detected_lang
            
            self.logger.warning(f"Detected unsupported language: {detected_lang}")
            return 'en'
            
        except Exception as e:
            self.logger.error(f"Language detection failed: {str(e)}")
            return 'en'

    def translate_to_english(self, text: str, source_lang: str) -> str:
        """
        Translate text from Indian language to English
        Args:
            text (str): Text to translate
            source_lang (str): Source language code
        Returns:
            str: Translated text
        """
        if source_lang == 'en':
            return text
            
        try:
            translator = GoogleTranslator(source=source_lang, target='en')
            return translator.translate(text)
            
        except Exception as e:
            self.logger.error(f"Translation to English failed: {str(e)}")
            return text

    def translate_from_english(self, text: str, target_lang: str) -> str:
        """
        Translate text from English to Indian language
        Args:
            text (str): Text to translate
            target_lang (str): Target language code
        Returns:
            str: Translated text
        """
        if target_lang == 'en':
            return text
            
        try:
            translator = GoogleTranslator(source='en', target=target_lang)
            return translator.translate(text)
            
        except Exception as e:
            self.logger.error(f"Translation from English failed: {str(e)}")
            return text

    def is_supported_language(self, lang_code: str) -> bool:
        """Check if language is supported"""
        return lang_code in self.supported_languages

    def get_language_name(self, lang_code: str) -> str:
        """Get full language name from code"""
        return self.supported_languages.get(lang_code, 'Unknown')


# Test the service if run directly
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize the service
    translator = TranslationService()
    
    # Test translations
    test_texts = {
        "en": "Hello, how are you?",
        "hi": "नमस्ते, आप कैसे हैं?",
        "ta": "வணக்கம், எப்படி இருக்கிறீர்கள்?"
    }
    
    for lang, text in test_texts.items():
        print(f"\nTesting {translator.get_language_name(lang)} text: {text}")
        
        # Detect language
        detected = translator.detect_language(text)
        print(f"Detected language: {translator.get_language_name(detected)}")
        
        # Translate to English
        english = translator.translate_to_english(text, detected)
        print(f"English translation: {english}")
        
        # Translate back to original language
        back = translator.translate_from_english(english, lang)
        print(f"Back translation: {back}")