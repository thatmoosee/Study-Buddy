from repositories.base_repository import BaseRepository
from models.user import User

class UserRepository(BaseRepository):
    """User repository"""
    
    def __init__(self, storage):
        super().__init__(storage)
        self._id_counter = 1
    
    def create(self, entity):
        if not isinstance(entity, User):
            raise ValueError("Entity must be a User instance")
        
        is_valid, errors = entity.validate()
        if not is_valid:
            raise ValueError(f"Validation failed: {', '.join(errors)}")
        
        if self.find_by_email(entity.email):
            raise ValueError("User with this email already exists")
        
        entity.id = self._id_counter
        self._id_counter += 1
        
        self._storage[entity.email] = entity
        return entity
    
    def find_by_id(self, user_id):
        for user in self._storage.values():
            if user.id == user_id:
                return user
        return None
    
    def find_by_email(self, email):
        return self._storage.get(email.lower().strip())
    
    def find_all(self):
        return list(self._storage.values())