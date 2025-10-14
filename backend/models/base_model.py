from abc import ABC, abstractmethod
from datetime import datetime

class BaseModel(ABC):
    """Abstract base class for all models"""
    
    def __init__(self, id=None, created_at=None):
        self._id = id
        self._created_at = created_at or datetime.now()
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @abstractmethod
    def to_dict(self):
        pass
    
    @abstractmethod
    def validate(self):
        pass