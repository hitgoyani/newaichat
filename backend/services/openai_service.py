"""
OpenAI service for interacting with GPT models.
Handles API calls and response generation.
"""

from openai import OpenAI
from config.config import Config

class OpenAIService:
    """Service class for OpenAI GPT API integration."""
    
    def __init__(self):
        """Initialize OpenAI client with API key from configuration."""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.GPT_MODEL
        self.temperature = Config.GPT_TEMPERATURE
        self.max_tokens = Config.GPT_MAX_TOKENS
    
    def get_response(self, system_prompt, user_query, context=""):
        """
        Get response from GPT model.
        
        Args:
            system_prompt (str): The system prompt defining AI behavior
            user_query (str): The user's question
            context (str): Optional knowledge base context to inject
        
        Returns:
            str: The AI-generated response
        
        Raises:
            Exception: If API call fails
        """
        try:
            # Build messages array
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add context if provided (will be enhanced in Phase 3)
            if context:
                messages.append({
                    "role": "system", 
                    "content": f"KNOWLEDGE BASE CONTEXT:\n{context}"
                })
            
            # Add user query
            messages.append({"role": "user", "content": user_query})
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract and return response text
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            # Log error and re-raise with context
            print(f"OpenAI API Error: {str(e)}")
            raise Exception(f"Failed to get response from AI: {str(e)}")
