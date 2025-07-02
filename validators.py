"""
Input validation utilities for user data.
"""

import re
import logging
from typing import Union

logger = logging.getLogger(__name__)

class Validators:
    def __init__(self):
        """Initialize validators with regex patterns"""
        # Phone number pattern (10 digits, optional country code)
        self.phone_pattern = re.compile(r'^(\+91)?[6-9]\d{9}$')
        
        # Name pattern (letters, spaces, common punctuation)
        self.name_pattern = re.compile(r'^[a-zA-Z\u0900-\u097F\u0600-\u06FF\s\.\-\']{2,50}$')
    
    def validate_name(self, name: str) -> bool:
        """
        Validate user name input.
        
        Args:
            name (str): Name to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not name or not isinstance(name, str):
            return False
        
        name = name.strip()
        
        # Check length
        if len(name) < 2 or len(name) > 50:
            return False
        
        # Check for valid characters (includes Unicode for Hindi/Marathi names)
        if not self.name_pattern.match(name):
            return False
        
        # Additional checks
        if name.isdigit():  # Name shouldn't be all numbers
            return False
        
        if len(name.replace(' ', '')) < 2:  # Must have at least 2 non-space characters
            return False
        
        return True
    
    def validate_age(self, age_input: Union[str, int]) -> bool:
        """
        Validate age input.
        
        Args:
            age_input (Union[str, int]): Age to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if isinstance(age_input, str):
                age_input = age_input.strip()
                if not age_input.isdigit():
                    return False
                age = int(age_input)
            elif isinstance(age_input, int):
                age = age_input
            else:
                return False
            
            # Age should be between 1 and 120
            return 1 <= age <= 120
        
        except (ValueError, TypeError):
            return False
    
    def validate_phone(self, phone: str) -> bool:
        """
        Validate phone number input.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not phone or not isinstance(phone, str):
            return False
        
        # Clean phone number (remove spaces, hyphens, etc.)
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone.strip())
        
        # Check pattern
        if self.phone_pattern.match(cleaned_phone):
            return True
        
        # Also accept 10-digit numbers without country code
        if len(cleaned_phone) == 10 and cleaned_phone.isdigit() and cleaned_phone[0] in '6789':
            return True
        
        return False
    
    def validate_symptoms(self, symptoms: str) -> bool:
        """
        Validate symptoms input.
        
        Args:
            symptoms (str): Symptoms description to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not symptoms or not isinstance(symptoms, str):
            return False
        
        symptoms = symptoms.strip()
        
        # Minimum length check
        if len(symptoms) < 5:
            return False
        
        # Maximum length check (reasonable limit)
        if len(symptoms) > 1000:
            return False
        
        # Check if it's not just whitespace or special characters
        if not re.search(r'[a-zA-Z\u0900-\u097F\u0600-\u06FF]', symptoms):
            return False
        
        return True
    
    def sanitize_input(self, text: str) -> str:
        """
        Sanitize user input by removing potentially harmful characters.
        
        Args:
            text (str): Text to sanitize
            
        Returns:
            str: Sanitized text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remove null bytes and control characters except newlines and tabs
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Limit length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]
        
        return sanitized.strip()
    
    def validate_language_code(self, lang_code: str) -> bool:
        """
        Validate language code input.
        
        Args:
            lang_code (str): Language code to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        valid_codes = ['en', 'hi', 'mr']
        return lang_code in valid_codes
    
    def validate_gender(self, gender: str) -> bool:
        """
        Validate gender input.
        
        Args:
            gender (str): Gender to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        valid_genders = ['male', 'female', 'other']
        return gender.lower() in valid_genders
