"""
Profile data validator for user profiles

Built by: Max Quirk
"""
from validators.base_validator import BaseValidator

class ProfileValidator(BaseValidator):
    """Profile data validator"""

    def validate(self, data):
        """Validate profile data"""
        errors = []

        user_id = data.get('user_id')
        if not user_id:
            errors.append("User ID is required")

        return len(errors) == 0, errors
