"""
Password reset validator for token validation

Built by: Max Quirk
"""
from validators.base_validator import BaseValidator
import re

class PasswordResetValidator(BaseValidator):
    """Password reset request validator"""

    def validate(self, data):
        """Validate forgot password request"""
        errors = []

        email = data.get('email', '')
        if not email:
            errors.append("Email is required")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Invalid email format")

        return len(errors) == 0, errors

    def validate_reset(self, data):
        """Validate password reset with token"""
        errors = []

        token = data.get('token', '')
        if not token:
            errors.append("Reset token is required")

        new_password = data.get('new_password', '')
        if not new_password:
            errors.append("New password is required")
        elif len(new_password) < 8:
            errors.append("Password must be at least 8 characters long")
        elif not re.search(r'[A-Z]', new_password):
            errors.append("Password must contain at least one uppercase letter")
        elif not re.search(r'[a-z]', new_password):
            errors.append("Password must contain at least one lowercase letter")
        elif not re.search(r'\d', new_password):
            errors.append("Password must contain at least one number")

        return len(errors) == 0, errors
