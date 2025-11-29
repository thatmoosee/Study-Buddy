"""
Friendship model for managing user relationships

Built by: Max Quirk
"""

from models.base_model import BaseModel
import uuid

class Friend(BaseModel):
    """
    Model representing a friendship between two users.
    Supports different states: pending (for future AddFriend), accepted, blocked
    """

    # Friendship status constants
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_BLOCKED = 'blocked'

    #Init friendship between two users w status code for managing the request and relationship
    def __init__(self, user_id, friend_id, status=STATUS_ACCEPTED, id=None, created_at=None):
        super().__init__(id or uuid.uuid4().hex, created_at)
        self._user_id = user_id
        self._friend_id = friend_id
        self._status = status


    #User ID getter to access who initiated friendship
    @property
    def user_id(self):
        return self._user_id

    # Getter to access the friend's user ID
    @property
    def friend_id(self):
        return self._friend_id

    # Property getter to get access the friendship status
    @property
    def status(self):
        return self._status

    # Sets the status update for future addFriend functionality
    @status.setter
    def status(self, value):
        """Allow status updates for future AddFriend functionality"""
        if value not in [self.STATUS_PENDING, self.STATUS_ACCEPTED, self.STATUS_BLOCKED]:
            raise ValueError(f"Invalid status: {value}")
        self._status = value


    # TO check if a specific user is involved in this friendship (bidirectional check)
    def involves_user(self, user_id):
        """Check if this friendship involves a specific user"""
        return user_id in [self._user_id, self._friend_id]


    # Get the other user ID in this relationship
    def get_other_user(self, user_id):
        """Get the other user in this friendship"""
        if user_id == self._user_id:
            return self._friend_id
        elif user_id == self._friend_id:
            return self._user_id
        return None


    #Convert friendship to dictionary and JSON storage
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self._user_id,
            'friend_id': self._friend_id,
            'status': self._status,
            'created_at': self._created_at.isoformat() if self._created_at else None
        }


    #Validate friendship data ensuring both users exist, are different and status is valid
    def validate(self):
        """Validate friendship data"""
        errors = []

        if not self._user_id:
            errors.append("User ID is required")

        if not self._friend_id:
            errors.append("Friend ID is required")

        if self._user_id == self._friend_id:
            errors.append("Cannot be friends with yourself")

        if self._status not in [self.STATUS_PENDING, self.STATUS_ACCEPTED, self.STATUS_BLOCKED]:
            errors.append(f"Invalid status: {self._status}")

        return len(errors) == 0, errors