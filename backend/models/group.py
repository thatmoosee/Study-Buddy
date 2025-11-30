"""
Study group model for collaborative learning sessions

Built by: Max Quirk
"""

from models.base_model import BaseModel
import uuid

class Group(BaseModel):
    def __init__(self, name, owner_id, members=None, specified_class = None, study_times = None, id=None, created_at=None, rating=0):
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

        self._study_times = study_times
        self._specified_class = specified_class
            
    @property
    def name(self):
        return self._name

    @property
    def owner_id(self):
        return self._owner_id
    
    @property
    def rating(self):
        return self._rating if hasattr(self, '_rating') else 0

    def setRating(self, rate):
        self._rating = rate

    @property
    def specified_class(self):
        # Handle both string and array formats for backward compatibility
        if not self._specified_class or self._specified_class == []:
            return ""
        # If it's a list, join it; otherwise return as string
        return ", ".join(self._specified_class) if isinstance(self._specified_class, list) else self._specified_class

    @property
    def study_times(self):
        # Ensure it's always an array
        if not self._study_times:
            return []
        return self._study_times if isinstance(self._study_times, list) else [self._study_times]

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
        """ Convert group to dictionary for API responses and JSON storage """
        return {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id,
            'members': self.members,
            'study_times': self.study_times,
            'specified_class': self.specified_class
        }

    def validate(self):
        """Validate group data - returns (bool, list) for consistency"""
        errors = []
        if not self._name:
            errors.append("Group name is required")
        return len(errors) == 0, errors
