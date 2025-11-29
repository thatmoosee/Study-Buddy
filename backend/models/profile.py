"""
User profile model for storing student information and availability

Built by: Max Quirk
"""

from models.base_model import BaseModel

class Profile(BaseModel):
    """Profile model - Features 1.1.4, 1.1.5"""
    
    def __init__(self, user_id, name=None, major=None, availability=None,
                 id=None, created_at=None, preferences=None):
        super().__init__(id, created_at)
        self._user_id = user_id
        self._name = name
        self._major = major
        self._availability = availability or []
        # Fix mutable default argument - create new list each time
        self.preferences = preferences if preferences is not None else [0]*14
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def major(self):
        return self._major
    
    @major.setter
    def major(self, value):
        self._major = value
    
    @property
    def availability(self):
        return self._availability
    
    def changePreferences(self, prefDay, start, end):
        self.preferences[prefDay] = start
        self.preferences[prefDay+7] = end
        

    def add_availability(self, time_slot):
        if time_slot not in self._availability:
            self._availability.append(time_slot)
    
    def validate(self):
        errors = []
        if not self._user_id:
            errors.append("User ID is required")
        return len(errors) == 0, errors
    
    def to_dict(self):
        return {
            'profile_id': self._id,
            'user_id': self._user_id,
            'name': self._name,
            'major': self._major,
            'availability': self._availability,
            'created_at': self._created_at.isoformat()
        }