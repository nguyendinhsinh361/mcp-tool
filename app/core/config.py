"""
Centralized configuration management for MCP Project.
Handles environment variables and server settings.
"""
import os
from typing import Dict, Any, Optional
from venv import logger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the MCP project"""
    
    def __init__(self):
        # API Keys
        self.OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
        self.GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY", "")
        self.GITHUB_PERSONAL_ACCESS_TOKEN: str = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")
        
        # Model settings
        self.USE_GEMINI: bool = False
        
        # Server settings
        self.IP_HOST: str = os.environ.get("IP_HOST", "0.0.0.0")
        self.SOCIAL_PORT: int = os.environ.get("SOCIAL_PORT", 8000)
        self.GITHUB_PORT: int = os.environ.get("WEATHER_PORT", 8002)
        
        
        # Web search
        self.NAVER_CLIENT_ID: int = os.environ.get("MATH_PORT", 8001)
        self.NAVER_CLIENT_SECRET: int = os.environ.get("WEATHER_PORT", 8002)
        
        
        
        # Server configurations for clients
        self._server_config = None
    
    @property
    def server_config(self) -> Dict[str, Dict[str, Any]]:
        """Get server configuration for multi-client"""
        if self._server_config is None:
            self._server_config = {
                "social": {
                    "url": f"http://{self.IP_HOST}:{self.SOCIAL_PORT}/sse",
                    "transport": "sse",
                },
                "github": {
                    "url": f"http://{self.IP_HOST}:{self.GITHUB_PORT}/sse",
                    "transport": "sse",
                }
            }
                
        return self._server_config
    
    def validate(self) -> bool:
        """Validate that required configuration is present"""
        missing = []
        
        # Check for required API keys based on configuration
        if self.USE_GEMINI and not self.GOOGLE_API_KEY:
            missing.append("GOOGLE_API_KEY (required when USE_GEMINI=true)")
        elif not self.USE_GEMINI and not self.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY (required when USE_GEMINI=false)")
            
        if missing:
            print("Missing required environment variables:")
            for var in missing:
                print(f"  - {var}")
            return False
            
        return True
    
    def get_model_instance(self):
        """Get the appropriate language model instance based on configuration"""
        if self.USE_GEMINI:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=self.GOOGLE_API_KEY,
                temperature=0.3,
            )
        else:            
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-4.1-nano", 
                api_key=self.OPENAI_API_KEY,
                temperature=0.3
            )

# Create a global settings instance
settings = Settings()