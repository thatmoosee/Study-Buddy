import json
import os
from datetime import datetime
from models.password_reset_token import PasswordResetToken
from repositories.base_repository import BaseRepository

class PasswordResetTokenRepository(BaseRepository):
    """Password reset token repository with JSON persistence"""

    def __init__(self, json_file):
        self._json_file = os.path.abspath(json_file)
        self._storage = {}
        self._id_counter = 1
        self._load_from_file()

    def _load_from_file(self):
        """Load tokens from JSON file"""
        try:
            with open(self._json_file, 'r') as f:
                data = json.load(f)
            for t in data.values():
                token = PasswordResetToken(
                    user_id=t['user_id'],
                    token=t['token'],
                    expires_at=t['expires_at'],
                    is_used=t.get('is_used', False),
                    id=t['id'],
                    created_at=t.get('created_at')
                )
                self._storage[token.token] = token
                if token.id >= self._id_counter:
                    self._id_counter = token.id + 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"No existing token data or error loading: {e}")
            self._storage = {}
            self._id_counter = 1

    def _save_to_file(self):
        """Save tokens to JSON file"""
        directory = os.path.dirname(self._json_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

        data = {token.token: {
            'id': token.id,
            'user_id': token.user_id,
            'token': token.token,
            'expires_at': token.expires_at.isoformat() if isinstance(token.expires_at, datetime) else token.expires_at,
            'is_used': token.is_used,
            'created_at': token._created_at.isoformat() if token._created_at else None
        } for token in self._storage.values()}

        with open(self._json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def create(self, entity):
        """Create new reset token"""
        if not isinstance(entity, PasswordResetToken):
            raise ValueError("Entity must be a PasswordResetToken instance")

        is_valid, errors = entity.validate()
        if not is_valid:
            raise ValueError(f"Validation failed: {', '.join(errors)}")

        entity.id = self._id_counter
        self._id_counter += 1

        self._storage[entity.token] = entity
        self._save_to_file()
        return entity

    def find_by_id(self, entity_id):
        """Find token by ID"""
        for token in self._storage.values():
            if token.id == entity_id:
                return token
        return None

    def find_all(self):
        """Return all tokens"""
        return list(self._storage.values())

    def find_by_token(self, token_string):
        """Find token by token string"""
        return self._storage.get(token_string)

    def find_by_user_id(self, user_id):
        """Find all tokens for a user"""
        return [token for token in self._storage.values() if token.user_id == user_id]

    def update(self, entity_id, updated_data):
        """Update token by ID"""
        token = self.find_by_id(entity_id)
        if not token:
            raise ValueError("Token not found")

        if 'is_used' in updated_data:
            token.is_used = updated_data['is_used']

        self._save_to_file()
        return token

    def delete(self, entity_id):
        """Delete token by ID"""
        token = self.find_by_id(entity_id)
        if not token:
            raise ValueError("Token not found")

        del self._storage[token.token]
        self._save_to_file()
        return True

    def delete_expired_tokens(self):
        """Clean up expired and used tokens"""
        tokens_to_delete = []
        for token in self._storage.values():
            if not token.is_valid() or token.is_used:
                tokens_to_delete.append(token.token)

        for token_string in tokens_to_delete:
            del self._storage[token_string]

        if tokens_to_delete:
            self._save_to_file()

        return len(tokens_to_delete)
