from models.profile import Profile

class ProfileEditor:
    """Profile editor - Feature 1.1.5"""

    _storage = {}
    _id_counter = 1

    def __init__(self, profile: Profile):
        if not isinstance(profile, Profile):
            raise TypeError("ProfileEditor requires a Profile instance")
        self._profile = profile

    def update_name(self, new_name: str):
        if not new_name or not new_name.strip():
            raise ValueError("Name cannot be empty.")
        self._profile.name = new_name.strip()

    def update_major(self, new_major: str):
        if not new_major or not new_major.strip():
            raise ValueError("Major cannot be empty.")
        self._profile.major = new_major.strip()

    def update_availability(self, new_slots: list):
        if not isinstance(new_slots, list):
            raise TypeError("Availability must be a list of time slots.")
        self._profile._availability = list(set(new_slots))

    def add_time_slot(self, time_slot: str):
        self._profile.add_availability(time_slot)

    def remove_time_slot(self, time_slot: str):
        if time_slot in self._profile.availability:
            self._profile._availability.remove(time_slot)

    def validate_profile(self):
        return self._profile.validate()

    def save(self): # TODO figure out what storage to save to
        valid, errors = self._profile.validate()
        if not valid:
            raise ValueError(f"Cannot save profile: {', '.join(errors)}")

        ProfileEditor._storage[self._profile.user_id] = self._profile
        return self._profile.to_dict()

    @property
    def profile(self):
        return self._profile