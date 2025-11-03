from base_model import BaseModel

class Group(BaseModel):
    #needs other init and models like the profile and user class
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