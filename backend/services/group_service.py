# services/group_service.py
from models.group import Group

class GroupService:
    """Handles group membership logic"""

    def __init__(self, group_repo):
        self.group_repo = group_repo
        
    def create_group(self, name, user_id, members):
        group = Group(name, user_id, members)
        self.group_repo.add(group)
        return group

    def join_group(self, user_id, group_id):
        group = self.group_repo.get(group_id)   # FIXED
        if not group:
            raise ValueError("Group not found")

        if user_id in group._members:
            raise ValueError("User already in the group")

        group.add_member(user_id)
        self.group_repo.update(group_id, group)
        return group
        
    def leave_group(self, user_id, group_id):
        group = self.group_repo.get(group_id)   # FIXED
        if not group:
            raise ValueError("Group not found")

        if user_id not in group._members:
            raise ValueError("User not in this group")

        group.remove_member(user_id)
        self.group_repo.update(group_id, group)
        return group

    def list_all_groups(self):
        return list(self.group_repo.storage.values())  # FIXED
