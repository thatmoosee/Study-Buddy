"""
Group service for study group operations

Built by: Max Quirk
"""

from models.group import Group

class GroupService:
    """Handles group membership logic"""

    def __init__(self, group_repo):
        self.group_repo = group_repo
        
    def create_group(self, name, owner_id, members=None, study_times=None, class_name=None):
        """Create a new group"""
        # Group constructor already adds owner to members, no need to do it again
        group = Group(name, owner_id, members, class_name, study_times)
        self.group_repo.add(group)
        return group

    def join_group(self, user_id, group_identifier):
        """Add a user to a group by ID or name"""
        # Try to find by ID first, then by name
        group = self.group_repo.get(group_identifier)
        if not group:
            raise ValueError("Group not found")

        if user_id in group._members:
            raise ValueError("User already in the group")

        group.add_member(user_id)
        self.group_repo.update(group.id, group)
        return group

    def leave_group(self, user_id, group_identifier):
        """Remove a user from a group by ID or name"""
        # Try to find by ID first, then by name
        group = self.group_repo.get(group_identifier)
        if not group:
            raise ValueError("Group not found")

        if user_id not in group._members:
            raise ValueError("User not in this group")

        group.remove_member(user_id)

        # Clean up orphan groups - delete if no members remain
        if len(group._members) == 0:
            self.group_repo.remove(group.id)
        else:
            self.group_repo.update(group.id, group)

        return group

    def list_all_groups(self):
        """List all groups"""
        return self.group_repo.find_all()

    def get_user_groups(self, user_id):
        """Get all groups for a specific user"""
        return self.group_repo.get_groups_for_user(user_id)

    def edit_group(self, group_id, specified_class=None, study_times=None):
        group = self.group_repo.get(group_id)
        if not group:
            raise ValueError("Group not found")
        if specified_class is not None:
            group.specified_class = specified_class
        if study_times is not None:
            group.study_times = study_times
        self.save_group(group)
        return group

    def filter_by_specified_class(self, specified_class):
        """Filter groups by specific class"""
        return self.group_repo.filter_by(specified_class=specified_class)

    def filter_by_study_times(self, study_times):
        """Filter groups by specific study times"""
        return self.group_repo.filter_by(None, study_times=study_times)

    def get_group(self, group_id):
        return self.group_repo.find_by_id(group_id)