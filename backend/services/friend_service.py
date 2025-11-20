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