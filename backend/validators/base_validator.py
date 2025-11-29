"""
Base validator providing validation utilities

Built by: Max Quirk
"""
from abc import ABC, abstractmethod

class BaseValidator(ABC):
    """Abstract base validator"""
    
    @abstractmethod
    def validate(self, data):
        pass