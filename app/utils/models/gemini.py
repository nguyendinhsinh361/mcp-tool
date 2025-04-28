from typing import Dict
from app.utils.models.base import BaseAIModel  # Correction du chemin d'import

class GeminiModel(BaseAIModel):
    """Enum containing all Google Gemini models"""
    
    # Gemini 2 Models
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    
    def __str__(self) -> str:
        return self.value
    
    def get_pricing(self) -> Dict[str, float]:
        """
        Get model pricing in USD/1M tokens
        Returns dictionary with 'input' and 'output' keys
        """
        pricing = {
            GeminiModel.GEMINI_2_0_FLASH: {"input": 0.1, "output": 0.4},
        }
        
        return pricing.get(self, {"input": 0.0, "output": 0.0})
    
    def get_context_window(self) -> int:
        """Returns the context window size in tokens"""
        context_windows = {
            GeminiModel.GEMINI_2_0_FLASH: 1000000,
        }
        
        return context_windows.get(self, 0)