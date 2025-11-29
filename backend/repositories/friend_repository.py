"""
Friend repository for managing friendship relationships

Built by: Max Quirk
"""

import json
import os
from models.friend import Friend
from repositories.base_repository import BaseRepository

class FriendRepository(BaseRepository):
    """Friend repository that persists to JSON"""

    # Internal helper method to init
    def __init__(self, filepath='data/friends.json'):
        self.filepath = os.path.abspath(filepath)
        self._storage = {}
        self._load_data()

    @property
    # Storage to perform required operation
    def storage(self):
        """Expose storage for backward compatibility"""
        return self._storage

    # Load data from storage into memory for processing
    def _load_data(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    data = json.load(f)
                for f_data in data.values():
                    friend = Friend(
                        user_id=f_data['user_id'],
                        friend_id=f_data['friend_id'],
                        status=f_data.get('status', Friend.STATUS_ACCEPTED)
                    )
                    friend.id = f_data['id']
                    self._storage[friend.id] = friend
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading friends: {e}")
                self._storage = {}

    # Save data from memory to persistent storage
    def _save_data(self):
        # Ensure directory exists
        directory = os.path.dirname(self.filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.filepath, 'w') as f:
            json.dump(
                {fid: friend.to_dict() for fid, friend in self._storage.items()},
                f,
                indent=4
            )

    # Abstract method implementations
    def create(self, entity):
        """Create/add a new friendship"""
        if not isinstance(entity, Friend):
            raise ValueError("Entity must be a Friend instance")
        self._storage[entity.id] = entity
        self._save_data()
        return entity

    # Find and return entity by its unique identifier
    def find_by_id(self, entity_id):
        """Find friendship by ID"""
        return self._storage.get(entity_id)

    # Retrieve and return all entities from storage
    def find_all(self):
        """Return all friendships"""
        return list(self._storage.values())

    # Friend-specific methods
    def add(self, friend):
        """Add a friendship (alias for create)"""
        return self.create(friend)

    # Find and return entity matching criteria
    def get(self, friend_id):
        """Get friendship by ID (alias for find_by_id)"""
        return self.find_by_id(friend_id)

    # Update entity data and persist changes to storage
    def update(self, friend_id, friend):
        """Update an existing friendship"""
        if friend_id in self._storage:
            self._storage[friend_id] = friend
            self._save_data()
            return friend
        raise ValueError("Friendship not found")

    # Remove entity from storage permanently or from collection
    def remove(self, friend_id):
        """Delete a friendship"""
        if friend_id in self._storage:
            del self._storage[friend_id]
            self._save_data()
            return True
        raise ValueError("Friendship not found")

    # Find and return entity matching criteria
    def get_friends_for_user(self, user_id, status=None):
        """
        Get all friendships for a user, optionally filtered by status.
        Returns Friend objects where user is involved.
        """
        friends = [
            f for f in self._storage.values()
            if f.involves_user(user_id)
        ]

        if status:
            friends = [f for f in friends if f.status == status]

        return friends

    # Find and return entity matching criteria
    def find_friendship(self, user_id, friend_id):
        """
        Find a friendship between two users (bidirectional).
        Returns the Friend object if exists, None otherwise.
        """
        for friendship in self._storage.values():
            if friendship.involves_user(user_id) and friendship.involves_user(friend_id):
                return friendship
        return None

    # Find and return entity matching criteria
    def get_friend_ids(self, user_id, status=Friend.STATUS_ACCEPTED):
        """
        Get list of friend user IDs for a specific user.
        Returns just the IDs of the friends, not the Friend objects.
        """
        friendships = self.get_friends_for_user(user_id, status)
        return [f.get_other_user(user_id) for f in friendships]
