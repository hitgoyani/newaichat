"""
Configuration management for the University Helpdesk backend.
Loads environment variables and system prompt.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for managing application settings."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GPT_MODEL = os.getenv('GPT_MODEL', 'gpt-3.5-turbo')
    GPT_TEMPERATURE = float(os.getenv('GPT_TEMPERATURE', '0.3'))
    GPT_MAX_TOKENS = int(os.getenv('GPT_MAX_TOKENS', '500'))
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # System Prompt Path
    SYSTEM_PROMPT_PATH = os.path.join(
        os.path.dirname(__file__), 
        'system_prompt.txt'
    )
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            print("⚠️ WARNING: OPENAI_API_KEY is not set")
            print("  The system will run in LOCAL MODE (offline)")
            print("  Answers will be generated from knowledge base only")
            print("  To use OpenAI, add your API key to .env file")
            # Don't raise error - allow local mode
        
        if not os.path.exists(cls.SYSTEM_PROMPT_PATH):
            raise FileNotFoundError(
                f"System prompt file not found at: {cls.SYSTEM_PROMPT_PATH}"
            )
    
    @classmethod
    def load_system_prompt(cls):
        """Load and return the system prompt from file."""
        with open(cls.SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
