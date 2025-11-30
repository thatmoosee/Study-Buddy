"""
Friend service for friendship management

Built by: Max Quirk and Jamie Morrone
"""

from models.friend import Friend

class FriendService:
    """Handles friendship logic"""

    def __init__(self, friend_repo, user_repo):
        self.friend_repo = friend_repo
        self.user_repo = user_repo

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

    def add_friend(self, user_id, friend_id):
        user = self.user_repo.find_by_id(user_id)
        friend_user = self.user_repo.find_by_id(friend_id)

        if user is None or friend_user is None:
            return False, "User not found"

        self.friend_repo.add_friend(user_id, friend_id)
        return True, "Friend added"

    def get_friends_list(self, user_id):
        return self.friend_repo.get_friends_list(user_id)
