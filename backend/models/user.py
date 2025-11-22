from models.base_model import BaseModel
import bcrypt
import re

class User(BaseModel):
    """User model"""
    
    def __init__(self, email, password=None, password_hash=None, 
                 is_active=True, id=None, created_at=None):
        super().__init__(id, created_at)
        self._email = email.lower().strip()
        
        # FIXED: Clear logic for password vs password_hash
        if password_hash:
            # Loading from database - use existing hash
            self._password_hash = password_hash
        elif password:
            # New user - hash the password
            self._password_hash = self._hash_password(password)
        else:
            self._password_hash = None
        
        self._is_active = is_active
    
    def _hash_password(self, password):
        """Hash password using bcrypt with automatic salting"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        """Allow email to be updated"""
        self._email = value.lower().strip()
    
    @property
    def is_active(self):
        return self._is_active
    
    def verify_password(self, password):
        """Verify password matches stored hash"""
        if not password or not self._password_hash:
            return False
        try:
            return bcrypt.checkpw(password.encode(), self._password_hash.encode())
        except (ValueError, AttributeError):
            return False
    
    def validate(self):
        """Validate user data"""
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
        """Convert user to dictionary"""
        return {
            'user_id': self._id,
            'email': self._email,
            'is_active': self._is_active,
            'created_at': self._created_at.isoformat() if self._created_at else None
        }