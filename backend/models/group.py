from models.base_model import BaseModel
import uuid

class Group(BaseModel):
    def __init__(self, name, owner_id, members=None, id=None, created_at=None):
        # Call parent constructor with id (or generate new UUID)
        super().__init__(id or uuid.uuid4().hex, created_at)
        self._name = name
        self._owner_id = owner_id
        # Ensure owner is in members list, avoid duplicates
        if members is None:
            self._members = [owner_id]
        else:
            # Use set to remove duplicates, then convert to list
            self._members = list(set([owner_id] + members))
            
    @property
    def name(self):
        return self._name

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def members(self):
        """Return copy to prevent external modification"""
        return self._members.copy()

    def add_member(self, user_id):
        if user_id not in self._members:
            self._members.append(user_id)

    def remove_member(self, user_id):
        if user_id in self._members:
            self._members.remove(user_id)
    
    def leave_group(self, user_id, profile=None):
        """
        Handles a user leaving a group.
        Removes them from the group and updates their profile if provided.
        """
        # Remove from group member list
        if user_id in self._members:
            self._members.remove(user_id)

        # Update profile if passed (e.g., clear group association)
        if profile:
            # If profile tracks groups, remove this one
            if hasattr(profile, "_groups"):
                if self._name in profile._groups:
                    profile._groups.remove(self._name)

        return True

    def to_dict(self):
        return {
            'id': self.id,
            'name': self._name,
            'owner_id': self._owner_id,
            'members': self._members
        }

    def validate(self):
        """Validate group data - returns (bool, list) for consistency"""
        errors = []
        if not self._name:
            errors.append("Group name is required")
        return len(errors) == 0, errors
