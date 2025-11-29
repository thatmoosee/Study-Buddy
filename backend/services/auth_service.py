"""
Authentication service handling login, logout, and session management

Built by: Max Quirk
"""

from models.user import User
from validators.user_validator import UserValidator
from validators.password_reset_validator import PasswordResetValidator

class AuthService:
    """Authentication service"""

    def __init__(self, user_repository, token_repository=None):
        self._user_repository = user_repository
        self._token_repository = token_repository
        self._validator = UserValidator()
        self._reset_validator = PasswordResetValidator()

    def register(self, email, password):
        is_valid, errors = self._validator.validate({
            'email': email,
            'password': password
        })
        if not is_valid:
            raise ValueError(f"Validation failed: {', '.join(errors)}")

        user = User(email=email, password=password)
        created_user = self._user_repository.create(user)
        return created_user

    def login(self, email, password):
        user = self._user_repository.find_by_email(email)
        if not user or not user.verify_password(password):
            raise ValueError("Invalid email or password")
        return user

    def logout(self, session):
        session.clear()

    def request_password_reset(self, email):
        """Initiate password reset process - returns token for in-app display"""
        if not self._token_repository:
            raise ValueError("Password reset functionality not configured")

        # Validate email format
        is_valid, errors = self._reset_validator.validate({'email': email})
        if not is_valid:
            raise ValueError(f"Validation failed: {', '.join(errors)}")

        # Check if user exists (but don't reveal this in the response for security)
        user = self._user_repository.find_by_email(email)
        if not user:
            # Return success anyway to prevent user enumeration
            return None

        # Clean up any expired tokens before creating new one
        self._token_repository.delete_expired_tokens()

        # Create reset token
        from models.password_reset import PasswordResetToken
        reset_token = PasswordResetToken(user_id=user.id)
        created_token = self._token_repository.create(reset_token)

        # Return the token for in-app display (no email needed)
        return created_token
    
    def reset_password(self, token_string, new_password):
        """Reset password using valid token"""
        if not self._token_repository:
            raise ValueError("Password reset functionality not configured")

        # Validate inputs
        is_valid, errors = self._reset_validator.validate_reset({
            'token': token_string,
            'new_password': new_password
        })
        if not is_valid:
            raise ValueError(f"Validation failed: {', '.join(errors)}")

        # Find token
        token = self._token_repository.find_by_token(token_string)
        if not token:
            raise ValueError("Invalid or expired reset token")

        # Check if token is valid (not expired and not used)
        if not token.is_valid():
            raise ValueError("Invalid or expired reset token")

        # Find user
        user = self._user_repository.find_by_id(token.user_id)
        if not user:
            raise ValueError("User not found")

        # Update password (User model handles hashing)
        user._password_hash = user._hash_password(new_password)

        # Save updated user
        self._user_repository.update(user.id, {})

        # Mark token as used
        token.is_used = True
        self._token_repository.update(token.id, {'is_used': True})

        return user
