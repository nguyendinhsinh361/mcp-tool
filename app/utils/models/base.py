from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional


# Cách sử dụng ví dụ: 
# model = ChatGPTModel.GPT_4_1.value
# price = model.get_pricing()
# input_price = price['input']
# output_price = price['output']

class BaseAIModel(ABC, str, Enum):
    """
    Base abstract class that all AI model enums should inherit from.
    Enforces a consistent interface across different model providers.
    """
    
    @abstractmethod
    def __str__(self) -> str:
        """Returns the string representation of the model"""
        pass
    
    @abstractmethod
    def get_pricing(self) -> Dict[str, float]:
        """
        Return pricing information for the model in USD per 1M tokens.
        Must return a dictionary with at least 'input' and 'output' keys.
        """
        pass
    
    def get_context_window(self) -> int:
        """
        Returns the context window size in tokens. 
        Can be overridden by child classes.
        """
        return 0
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Returns a dictionary of model capabilities.
        Can be overridden by child classes.
        """
        return {}
    
    @classmethod
    def find_by_name(cls, name: str) -> Optional['BaseAIModel']:
        """
        Find a model by its string name
        Returns None if not found
        """
        try:
            return cls(name)
        except ValueError:
            return None
    
    @classmethod
    def list_models(cls) -> Dict[str, 'BaseAIModel']:
        """Returns all available models in this enum as a dictionary"""
        return {model.name: model for model in cls}