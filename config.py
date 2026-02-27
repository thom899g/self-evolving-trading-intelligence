"""
Configuration management for the trading intelligence system.
Uses environment variables with fallbacks for local development.
Firebase integration is prioritized for production state management.
"""
import os
from dataclasses import dataclass
from typing import Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class TradingConfig:
    """Centralized configuration for trading system."""
    # Firebase Configuration
    FIREBASE_CREDENTIALS_PATH: str = os.getenv('FIREBASE_CREDENTIALS_PATH', './firebase-credentials.json')
    FIREBASE_DATABASE_URL: str = os.getenv('FIREBASE_DATABASE_URL', '')
    
    # Exchange Configuration
    EXCHANGE_NAME: str = os.getenv('EXCHANGE_NAME', 'binance')
    EXCHANGE_API_KEY: str = os.getenv('EXCHANGE_API_KEY', '')
    EXCHANGE_SECRET_KEY: str = os.getenv('EXCHANGE_SECRET_KEY', '')
    
    # Trading Parameters
    TRADING_PAIR: str = os.getenv('TRADING_PAIR', 'BTC/USDT')
    TIMEFRAME: str = os.getenv('TIMEFRAME', '1h')
    INITIAL_CAPITAL: float = float(os.getenv('INITIAL_CAPITAL', 10000.0))
    
    # RL Configuration
    RL_MODEL_PATH: str = os.getenv('RL_MODEL_PATH', './models/rl_agent')
    RL_LEARNING_RATE: float = float(os.getenv('RL_LEARNING_RATE', 0.001))
    RL_GAMMA: float = float(os.getenv('RL_GAMMA', 0.99))
    
    # Sentiment Analysis
    SENTIMENT_MODEL_PATH: str = os.getenv('SENTIMENT_MODEL_PATH', './models/sentiment')
    NEWS_API_KEY: str = os.getenv('NEWS_API_KEY', '')
    SOCIAL_MEDIA_ENABLED: bool = os.getenv('SOCIAL_MEDIA_ENABLED', 'False').lower() == 'true'
    
    # Risk Management
    MAX_POSITION_SIZE: float = float(os.getenv('MAX_POSITION_SIZE', 0.1))
    STOP_LOSS_PERCENT: float = float(os.getenv('STOP_LOSS_PERCENT', 2.0))
    TAKE_PROFIT_PERCENT: float = float(os.getenv('TAKE_PROFIT_PERCENT', 5.0))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    ENABLE_FIREBASE_LOGGING: bool = os.getenv('ENABLE_FIREBASE_LOGGING', 'True').lower() == 'true'

def validate_config(config: TradingConfig) -> bool:
    """Validate critical configuration parameters."""
    errors = []
    
    # Validate Firebase configuration
    if config.ENABLE_FIREBASE_LOGGING:
        if not config.FIREBASE_CREDENTIALS_PATH:
            errors.append("FIREBASE_CREDENTIALS_PATH is required when Firebase logging is enabled")
        elif not os.path.exists(config.FIREBASE_CREDENTIALS_PATH):
            errors.append(f"Firebase credentials file not found: {config.FIREBASE_CREDENTIALS_PATH}")
    
    # Validate exchange credentials if trading is enabled
    if not config.EXCHANGE_API_KEY or not config.EXCHANGE_SECRET_KEY:
        logging.warning("Exchange API credentials not configured - running in simulation mode only")
    
    # Validate risk parameters
    if config.MAX_POSITION_SIZE <= 0 or config.MAX_POSITION_SIZE > 1:
        errors.append("MAX_POSITION_SIZE must be between 0 and 1")
    if config.STOP_LOSS_PERCENT <= 0:
        errors.append("STOP_LOSS_PERCENT must be positive")
    
    if errors:
        for error in errors:
            logging.error(f"Configuration error: {error}")
        return False
    
    logging.info("Configuration validated successfully")
    return True

# Global configuration instance
CONFIG = TradingConfig()