"""
Data management module for storing and retrieving user health data.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any
from threading import Lock

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self, data_file: str = "users.json"):
        """
        Initialize data manager with JSON file for storage.
        
        Args:
            data_file (str): Path to JSON file for data storage
        """
        self.data_file = data_file
        self.lock = Lock()  # Thread safety for file operations
        
        # Ensure data file exists
        self._initialize_data_file()
    
    def _initialize_data_file(self):
        """Initialize JSON data file if it doesn't exist"""
        if not os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                logger.info(f"Created new data file: {self.data_file}")
            except Exception as e:
                logger.error(f"Error creating data file: {e}")
                raise
    
    def save_user_data(self, user_data: Dict[str, Any]) -> bool:
        """
        Save user health consultation data to JSON file.
        
        Args:
            user_data (Dict): User data from bot conversation
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with self.lock:
                # Prepare data record
                record = self._prepare_user_record(user_data)
                
                # Load existing data
                existing_data = self._load_data()
                
                # Add new record
                existing_data.append(record)
                
                # Save updated data
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(existing_data, f, ensure_ascii=False, indent=2)
                
                logger.info(f"Saved user data for {record['name']} (ID: {record.get('user_id', 'unknown')})")
                return True
        
        except Exception as e:
            logger.error(f"Error saving user data: {e}")
            return False
    
    def _prepare_user_record(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare user data record for storage"""
        record = {
            "user_id": user_data.get('user_id'),
            "username": user_data.get('username'),
            "name": user_data.get('name', ''),
            "age": user_data.get('age', 0),
            "phone": user_data.get('phone', ''),
            "gender": user_data.get('gender', ''),
            "language": user_data.get('language_name', 'English'),
            "symptoms": user_data.get('symptoms', ''),
            "advice": user_data.get('advice', ''),
            "date": datetime.now().isoformat()
        }
        
        return record
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load existing data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    else:
                        logger.warning("Data file contains invalid format, resetting")
                        return []
            return []
        
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return []
    
    def get_user_history(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get consultation history for a specific user.
        
        Args:
            user_id (int): Telegram user ID
            
        Returns:
            List[Dict]: List of user's consultation records
        """
        try:
            with self.lock:
                data = self._load_data()
                user_records = [record for record in data if record.get('user_id') == user_id]
                return user_records
        
        except Exception as e:
            logger.error(f"Error getting user history: {e}")
            return []
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all user consultation records.
        
        Returns:
            List[Dict]: All consultation records
        """
        try:
            with self.lock:
                return self._load_data()
        
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get basic statistics about consultations.
        
        Returns:
            Dict: Statistics about stored data
        """
        try:
            with self.lock:
                data = self._load_data()
                
                total_consultations = len(data)
                unique_users = len(set(record.get('user_id') for record in data if record.get('user_id')))
                
                # Language distribution
                languages = {}
                for record in data:
                    lang = record.get('language', 'Unknown')
                    languages[lang] = languages.get(lang, 0) + 1
                
                # Gender distribution
                genders = {}
                for record in data:
                    gender = record.get('gender', 'Unknown')
                    genders[gender] = genders.get(gender, 0) + 1
                
                stats = {
                    "total_consultations": total_consultations,
                    "unique_users": unique_users,
                    "language_distribution": languages,
                    "gender_distribution": genders,
                    "data_file": self.data_file,
                    "file_size_bytes": os.path.getsize(self.data_file) if os.path.exists(self.data_file) else 0
                }
                
                return stats
        
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
