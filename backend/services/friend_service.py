class FriendService:
    def __init__(self, friend_repository, user_repository):
        self.friend_repo = friend_repository
        self.user_repository = user_repository

    def add_friend(self, user_id, friend_id):
        user = self.user_repo.find_by_id(user_id)
        friend_user = self.user_repo.find_by_id(friend_id)

        if user is None or friend_user is None:
            return False, "User not found"

        self.friend_repo.add_friend(user_id, friend_id)
        return True, "Friend added"

    def get_friends_list(self, user_id):
        return self.friend_repo.get_friends_list(user_id)
    