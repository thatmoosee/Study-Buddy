class FriendService:
    def __init__(self, friend_repository, user_repository=None):
        self.friend_repo = friend_repository

    def add_friend(self, requester_email, friend_email):
        requester_email = requester_email.lower().strip()
        friend_email = friend_email.lower().strip()

        if not requester_email or not friend_email:
            return False, "Missing email."

        if requester_email == friend_email:
            return False, "Cannot add yourself."

        if self.user_repo and not self.user_repo.get_user_by_email(friend_email):
            return False, f"User {friend_email} does not exist."

        self.friend_repo.add_friend(requester_email, friend_email)
        return True, f"{friend_email} added as friend."

    def get_friends(self, email):
        return self.friend_repo.get_friends(email)
    
    def remove_friend(self, requester_email, friend_email):
        requester = requester_email.lower().strip()
        friend = friend_email.lower().strip()

        user = self.user_repo.find_by_email(requester)
        friend_user = self.user_repo.find_by_email(friend)

        if user is None or friend_user is None:
            return False, "User not found"

        removed = self.friend_repo.remove_friend(requester, friend)

        if not removed:
            return False, "Friend not found in list"

        return True, "Friend removed"