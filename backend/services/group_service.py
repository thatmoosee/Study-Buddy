# services/group_service.py
from models.group import Group

class GroupService:
    """Handles group membership logic"""

    def __init__(self, group_repo):
        self.group_repo = group_repo

    def leave_group(self, user_id, group_id):
        group = self.group_repo.get(group_id)
        if not group:
            raise ValueError("Group not found")

        if user_id not in group.members:
            raise ValueError("User is not a member of this group")

        group.remove_member(user_id)
        self.group_repo.update(group_id, group)
        return group
