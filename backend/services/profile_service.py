from models.profile import Profile
from validators.profile_validator import ProfileValidator

class ProfileService:
    """
    Profile management service
    Demonstrates: Encapsulation
    """
    
    def __init__(self, profile_repository):
        self._profile_repository = profile_repository
        self._validator = ProfileValidator()
    
    def create_profile(self, user_id, name=None, major=None, availability=None):
        """Create user profile"""
        # Validate
        is_valid, errors = self._validator.validate({'user_id': user_id})
        if not is_valid:
            raise ValueError(f"Validation failed: {', '.join(errors)}")

        # Create profile
        profile = Profile(user_id=user_id, name=name, major=major, availability=availability)
        created_profile = self._profile_repository.create(profile)

        return created_profile
    
    def update_profile(self, profile_id, data):
        """Update profile"""
        return self._profile_repository.update(profile_id, data)
    
    def get_profile_by_user_id(self, user_id):
        """Get profile by user ID"""
        return self._profile_repository.find_by_user_id(user_id)

    def upload_profile(self, user_id, data):
        """Upload profile"""
        existing = self._profile_repository.find_by_id(user_id)
        if existing:
            return self._profile_repository.update(existing.id, data)

        profile = Profile(user_id=user_id, name=data.get('name'), major=data.get('major'), availability=data.get('availability'))
        return self._profile_repository.create(profile)
