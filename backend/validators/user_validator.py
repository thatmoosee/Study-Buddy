from validators.base_validator import BaseValidator
import re

class UserValidator(BaseValidator):
    """User data validator"""
    
    def validate(self, data):
        errors = []
        
        email = data.get('email', '')
        if not email:
            errors.append("Email is required")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Invalid email format")
        elif not email.lower().endswith('.edu'):
            errors.append("Must use a school email address (.edu)")
        
        password = data.get('password', '')
        if not password:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        elif not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        elif not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        elif not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        return len(errors) == 0, errors