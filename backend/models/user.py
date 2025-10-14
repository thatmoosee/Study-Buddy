from models.base_model import BaseModel
import hashlib
import re

class User(BaseModel):
    """User model"""
    
    def __init__(self, email, password=None, password_hash=None, 
                 is_active=True, id=None, created_at=None):
        super().__init__(id, created_at)
        self._email = email.lower().strip()
        self._password_hash = password_hash or self._hash_password(password) if password else None
        self._is_active = is_active
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @property
    def email(self):
        return self._email
    
    @property
    def is_active(self):
        return self._is_active
    
    def verify_password(self, password):
        return self._password_hash == self._hash_password(password)
    
    def validate(self):
        errors = []
        
        if not self._email:
            errors.append("Email is required")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self._email):
            errors.append("Invalid email format")
        elif not self._email.endswith('.edu'):
            errors.append("Must use a school email address (.edu)")
        
        if not self._password_hash:
            errors.append("Password is required")
        
        return len(errors) == 0, errors
    
    def to_dict(self):
        return {
            'user_id': self._id,
            'email': self._email,
            'is_active': self._is_active,
            'created_at': self._created_at.isoformat()
        }