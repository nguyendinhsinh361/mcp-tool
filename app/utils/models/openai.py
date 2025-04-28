from typing import Dict
from app.utils.models.base import BaseAIModel  # Correction du chemin d'import

class ChatGPTModel(BaseAIModel):
    """Enum containing all ChatGPT (OpenAI) models"""
    
    # GPT-4 Models
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1_NANO = "gpt-4.1-nano"
    
    def __str__(self) -> str:
        return self.value
    
    def get_pricing(self) -> Dict[str, float]:
        """
        Get model pricing in USD/1M tokens
        Returns dictionary with 'input' and 'output' keys
        """
        pricing = {
            ChatGPTModel.GPT_4_1: {"input": 2.0, "output": 8.0},
            ChatGPTModel.GPT_4_1_MINI: {"input": 0.4, "output": 1.6},
            ChatGPTModel.GPT_4_1_NANO: {"input": 0.1, "output": 0.4},
        }
        
        return pricing.get(self, {"input": 0.0, "output": 0.0})
    
    def get_context_window(self) -> int:
        """Returns the context window size in tokens"""
        context_windows = {
            ChatGPTModel.GPT_4_1: 1047576,
            ChatGPTModel.GPT_4_1_MINI: 1047576,
            ChatGPTModel.GPT_4_1_NANO: 1047576,
        }
        
        return context_windows.get(self, 0)