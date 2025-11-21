import json
import os
from models.group import Group
from repositories.base_repository import BaseRepository

class GroupRepository(BaseRepository):
    """Group repository that persists to JSON"""

    def __init__(self, filepath='data/groups.json'):
        self.filepath = os.path.abspath(filepath)  # Make absolute
        self._storage = {}
        self._load_data()

    @property
    def storage(self):
        """Expose storage for backward compatibility"""
        return self._storage

    def _load_data(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    data = json.load(f)
                for g in data.values():
                    group = Group(
                        name=g['_name'],
                        owner_id=g['_owner_id'],
                        members=g['_members']
                    )
                    group.id = g['id']
                    self._storage[group.id] = group
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading groups: {e}")
                self._storage = {}

    def _save_data(self):
        # Ensure directory exists
        directory = os.path.dirname(self.filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        with open(self.filepath, 'w') as f:
            json.dump(
                {gid: group.to_dict() for gid, group in self._storage.items()}, 
                f, 
                indent=4
            )

    # Abstract method implementations
    def create(self, entity):
        """Create/add a new group"""
        if not isinstance(entity, Group):
            raise ValueError("Entity must be a Group instance")
        self._storage[entity.id] = entity
        self._save_data()
        return entity

    def find_by_id(self, entity_id):
        """Find group by ID"""
        return self._storage.get(entity_id)

    def find_all(self):
        """Return all groups"""
        return list(self._storage.values())

    # Original methods (keeping for backward compatibility)
    def add(self, group):
        """Add a group (alias for create)"""
        return self.create(group)

    def get(self, group_id):
        """Get group by ID (alias for find_by_id)"""
        return self.find_by_id(group_id)

    def update(self, group_id, group):
        """Update an existing group"""
        if group_id in self._storage:
            self._storage[group_id] = group
            self._save_data()
            return group
        raise ValueError("Group not found")

    def list_all(self):
        """List all groups (alias for find_all)"""
        return self.find_all()

    def get_groups_for_user(self, user_id):
        """Get all groups that a user is a member of"""
        return [g for g in self._storage.values() if user_id in g._members]

    def remove(self, group_id):
        """Delete a group"""
        if group_id in self._storage:
            del self._storage[group_id]
            self._save_data()
            return True
        raise ValueError("Group not found")