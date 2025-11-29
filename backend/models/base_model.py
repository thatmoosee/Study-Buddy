"""
Abstract base model providing common functionality for all data models

Built by: Max Quirk
"""

from abc import ABC, abstractmethod
from datetime import datetime

class BaseModel(ABC):
    """Abstract base class for all models"""
    
    #Initialize the base model with optional ID and the timestamp for tracking 
    def __init__(self, id=None, created_at=None):
        self._id = id
        self._created_at = created_at or datetime.now()

    #Getting id
    @property
    def id(self):
        return self._id
    
    #Set ID
    @id.setter
    def id(self, value):
        self._id = value

    #Must implmenet to dictionairty for JSON
    @abstractmethod
    def to_dict(self):
        pass

    #Child class must implement to validate model data before saving
    @abstractmethod
    def validate(self):
        pass