# repositories/group_repository.py
class GroupRepository:
    """Simple in-memory group repository"""

    def __init__(self, storage):
        self.storage = storage  # dict of {group_id: Group}

    def add(self, group):
        self.storage[group.id] = group

    def get(self, group_id):
        return self.storage.get(group_id)

    def update(self, group_id, group):
        if group_id in self.storage:
            self.storage[group_id] = group
    
    def list_all(self):
        return list(self.storage.values())
    
    def get_groups_for_user(self, user_id):
        result = []
        for group in self.storage.values():
            if hasattr(group, 'members') and user_id in group.members:
                result.append(group)
        return result
