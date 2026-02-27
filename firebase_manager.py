"""
Firebase integration for state management, logging, and real-time data streaming.
Primary database choice as per ecosystem requirements.
"""
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, db
from firebase_admin.exceptions import FirebaseError

class FirebaseManager:
    """Manages Firebase connections and operations with robust error handling."""
    
    def __init__(self, credentials_path: str, database_url: Optional[str] = None):
        """
        Initialize Firebase connection.
        
        Args:
            credentials_path: Path to Firebase service account credentials
            database_url: Firebase Realtime Database URL (optional)
            
        Raises:
            FileNotFoundError: If credentials file doesn't exist
            FirebaseError: If Firebase initialization fails
        """
        self.logger = logging.getLogger(__name__)
        
        # Validate credentials file exists
        if not credentials_path or not isinstance(credentials_path, str):
            raise ValueError("Credentials path must be a non-empty string")
        
        if not os.path.exists(credentials_path):
            self.logger.error(f"Firebase credentials file not found: {credentials_path}")
            raise FileNotFoundError(f"Firebase credentials file not found: {credentials_path}")
        
        try:
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(credentials_path)
                app_options = {'credential': cred}
                if database_url:
                    app_options['databaseURL'] = database_url
                
                self.app = firebase_admin.initialize_app(**app_options)
                self.logger.info("Firebase app initialized successfully")
            else:
                self.app = firebase_admin.get_app()
                self.logger.info("Using existing Firebase app instance")
            
            # Initialize Firestore and Realtime Database clients
            self.firestore = firestore.client()
            self.realtime_db = db.reference() if database_url else None
            
        except FirebaseError as e:
            self.logger.error(f"Firebase initialization failed: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during Firebase initialization: {str(e)}")
            raise
    
    def log_trading_event(self, 
                         event_type: str, 
                         data: Dict[str, Any],
                         collection: str = "trading_events") -> bool:
        """
        Log trading event to Firestore with timestamp.
        
        Args:
            event_type: Type of event (trade_executed, signal_generated, etc.)
            data: Event data dictionary
            collection: