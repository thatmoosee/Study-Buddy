from abc import ABC, abstractmethod

class BaseValidator(ABC):
    """Abstract base validator"""
    
    @abstractmethod
    def validate(self, data):
        pass