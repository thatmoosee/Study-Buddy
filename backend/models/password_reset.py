"""
Password reset token model for secure account recovery

Built by: Max Quirk
"""

from models.base_model import BaseModel
from datetime import datetime, timedelta
import secrets

class PasswordResetToken(BaseModel):
    """Password reset token model"""

    def __init__(self, user_id, token=None, expires_at=None,
                 is_used=False, id=None, created_at=None):
        super().__init__(id, created_at)
        self._user_id = user_id
        self._token = token or self._generate_token()
        self._expires_at = expires_at or self._calculate_expiration()
        self._is_used = is_used

    @property
    def user_id(self):
        return self._user_id

    @property
    def token(self):
        return self._token

    @property
    def expires_at(self):
        return self._expires_at

    @property
    def is_used(self):
        return self._is_used

    @is_used.setter
    def is_used(self, value):
        """Allow marking token as used"""
        self._is_used = value

    def is_valid(self):
        """Check if token is valid (not expired and not used)"""
        if self._is_used:
            return False

        if isinstance(self._expires_at, str):
            # Parse string timestamp if loaded from JSON
            expires_at = datetime.fromisoformat(self._expires_at)
        else:
            expires_at = self._expires_at

        return datetime.now() < expires_at

    def validate(self):
        """Validate token data"""
        errors = []

        if not self._user_id:
            errors.append("User ID is required")

        if not self._token:
            errors.append("Token is required")

        if not self._expires_at:
            errors.append("Expiration time is required")

        return len(errors) == 0, errors

    def to_dict(self):
        """Convert token to dictionary"""
        return {
            'id': self._id,
            'user_id': self._user_id,
            'token': self._token,
            'expires_at': self._expires_at.isoformat() if isinstance(self._expires_at, datetime) else self._expires_at,
            'is_used': self._is_used,
            'created_at': self._created_at.isoformat() if self._created_at else None
        }
    def _generate_token(self):
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)

    def _calculate_expiration(self):
        """Calculate expiration time (15 minutes from now)"""
        return datetime.now() + timedelta(minutes=15)
