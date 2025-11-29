"""
Friend service for friendship management

Built by: Max Quirk
"""

from models.friend import Friend

class FriendService:
    """Handles friendship logic"""

    def __init__(self, friend_repo):
        self.friend_repo = friend_repo

    def remove_friend(self, user_id, friend_id):
        """
        Remove a friend relationship.
        Works regardless of who initiated the friendship.
        """
        # Find the friendship
        friendship = self.friend_repo.find_friendship(user_id, friend_id)
        if not friendship:
            raise ValueError("Friendship not found")

        # Remove the friendship
        self.friend_repo.remove(friendship.id)
        return True

    # PLACEHOLDER: Foundation for future AddFriend feature
    def add_friend(self, user_id, friend_id):
        """
        PLACEHOLDER: Add friend functionality.
        To be implemented when AddFriend feature is ready.
        """
        raise NotImplementedError("AddFriend feature not yet implemented")

    # PLACEHOLDER: Foundation for future FriendsList feature
    def get_friends_list(self, user_id):
        """
        PLACEHOLDER: Get friends list functionality.
        To be implemented when FriendsList feature is ready.
        """
        raise NotImplementedError("FriendsList feature not yet implemented")
