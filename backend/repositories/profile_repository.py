"""
Profile repository for storing and retrieving user profiles

Built by: Max Quirk
"""

import json
import os
from models.profile import Profile
from repositories.base_repository import BaseRepository

class ProfileRepository(BaseRepository):
    """Profile repository with JSON persistence"""

    def __init__(self, json_file):
        self._json_file = os.path.abspath(json_file)
        self._storage = {}
        self._id_counter = 1
        self._load_from_file()

    def _load_from_file(self):
        """Load profiles from JSON file"""
        try:
            with open(self._json_file, 'r') as f:
                data = json.load(f)
            for p in data.values():
                profile = Profile(
                    user_id=p['user_id'],
                    name=p.get('name'),
                    major=p.get('major'),
                    availability=p.get('availability', []),
                    id=p['id'],
                    created_at=None,
                    preferences=p.get('preferences')
                )
                self._storage[profile.id] = profile
                if profile.id >= self._id_counter:
                    self._id_counter = profile.id + 1
        except (FileNotFoundError, json.JSONDecodeError):
            self._storage = {}
            self._id_counter = 1

    def _save_to_file(self):
        """Save profiles to JSON file"""
        # Ensure directory exists
        directory = os.path.dirname(self._json_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

        data = {str(profile.id): {
            'id': profile.id,
            'user_id': profile.user_id,
            'name': profile.name,
            'major': profile.major,
            'availability': profile.availability,
            'preferences': profile.preferences
        } for profile in self._storage.values()}

        with open(self._json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def create(self, entity):
        """Create a new profile"""
        if not isinstance(entity, Profile):
            raise ValueError("Entity must be a Profile instance")

        is_valid, errors = entity.validate()
        if not is_valid:
            raise ValueError(f"Validation failed: {', '.join(errors)}")

        # Check if profile already exists for this user
        if self.find_by_user_id(entity.user_id):
            raise ValueError("Profile already exists for this user")

        entity.id = self._id_counter
        self._id_counter += 1

        self._storage[entity.id] = entity
        self._save_to_file()
        return entity

    def find_by_id(self, entity_id):
        """Find profile by ID"""
        return self._storage.get(entity_id)

    def find_all(self):
        """Return all profiles"""
        return list(self._storage.values())

    def find_by_user_id(self, user_id):
        """Find profile by user ID"""
        for profile in self._storage.values():
            if profile.user_id == user_id:
                return profile
        return None

    def update(self, entity_id, updated_data):
        """Update profile by ID"""
        profile = self.find_by_id(entity_id)
        if not profile:
            raise ValueError("Profile not found")

        # Update profile attributes
        if 'name' in updated_data:
            profile._name = updated_data['name']

        if 'major' in updated_data:
            profile._major = updated_data['major']

        if 'availability' in updated_data:
            profile._availability = updated_data['availability']

        if 'preferences' in updated_data:
            profile.preferences = updated_data['preferences']

        self._save_to_file()
        return profile

    def delete(self, entity_id):
        """Delete profile by ID"""
        if entity_id not in self._storage:
            raise ValueError("Profile not found")

        del self._storage[entity_id]
        self._save_to_file()
        return True
