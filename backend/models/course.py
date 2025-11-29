"""
Course model representing academic classes

Built by:
"""
from models.base_model import BaseModel

class Course(BaseModel):
    """Course model"""

    def __init__(self, field, number, section, id=None, created_at=None):
        super().__init__(id, created_at)
        self.field = field
        self.number = number
        self.section = section

    def validate(self):
        """Validate course data"""
        errors = []
        if not self.field:
            errors.append("Field is required")
        if not self.number:
            errors.append("Number is required")
        return len(errors) == 0, errors

    def to_dict(self):
        """Convert course to dictionary"""
        return {
            'id': self._id,
            'field': self.field,
            'number': self.number,
            'section': self.section,
            'created_at': self._created_at.isoformat() if self._created_at else None
        }
