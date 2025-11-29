"""
Abstract base repository defining data access interface

Built by: Max Quirk
"""

from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """Abstract base repository"""
    
    def __init__(self, storage):
        self._storage = storage
    
    @abstractmethod
    def create(self, entity):
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id):
        pass
    
    @abstractmethod
    def find_all(self):
        pass