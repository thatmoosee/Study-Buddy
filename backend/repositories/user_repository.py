"""
User repository for database operations on user accounts

Built by: Max Quirk
"""

import json
import os
from models.user import User
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    """User repository with JSON persistence"""

    def __init__(self, json_file):
        self._json_file = os.path.abspath(json_file)
        self._storage = {}
        self._id_counter = 1
        self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self._json_file, 'r') as f:
                data = json.load(f)
            for u in data.values():
                user = User(
                    email=u['email'],
                    password_hash=u.get('_password_hash'),  # Pass the hash directly
                    is_active=u.get('_is_active', True),
                    id=u['id'],
                    created_at=None  # Or parse from JSON if you're storing it
                )
                self._storage[user.email] = user
                if user.id >= self._id_counter:
                    self._id_counter = user.id + 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"No existing user data or error loading: {e}")
            self._storage = {}
            self._id_counter = 1

    def _save_to_file(self):
        # Ensure directory exists
        directory = os.path.dirname(self._json_file)
        if directory:
            os.makedirs(directory, exist_ok=True)
            
        data = {str(user.id): {
            'id': user.id,
            'email': user.email,
            '_password_hash': user._password_hash,
            '_is_active': user.is_active
        } for user in self._storage.values()}
        
        with open(self._json_file, 'w') as f:
            json.dump(data, f, indent=4)

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
        self._save_to_file()
        return entity

    def find_by_id(self, entity_id):
        """Find user by ID"""
        for user in self._storage.values():
            if user.id == entity_id:
                return user
        return None

    def find_all(self):
        """Return all users"""
        return list(self._storage.values())

    def find_by_email(self, email):
        """Find user by email"""
        return self._storage.get(email.lower().strip())

    def update(self, entity_id, updated_data):
        """Update user by ID"""
        user = self.find_by_id(entity_id)
        if not user:
            raise ValueError("User not found")
        
        # Update user attributes
        if 'email' in updated_data:
            # Remove old email key and add new one
            old_email = user.email
            user.email = updated_data['email']
            del self._storage[old_email]
            self._storage[user.email] = user
        
        if 'is_active' in updated_data:
            user._is_active = updated_data['is_active']
        
        self._save_to_file()
        return user

    def delete(self, entity_id):
        """Delete user by ID"""
        user = self.find_by_id(entity_id)
        if not user:
            raise ValueError("User not found")
        
        del self._storage[user.email]
        self._save_to_file()
        return True