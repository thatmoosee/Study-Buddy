"""
Notification model for user alerts and updates

Built by: Josh Topp
"""

class Notification:
    def __init__(self, user_id, message, read=False, id=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.message = message
        self.read = read
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'read': self.read,
            'created_at': self.created_at
        }