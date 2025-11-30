class FriendRepository:
    def __init__(self):
        self._storage = {}

    def add_friend(self, user_id, friend_id):
        if user_id not in self._storage:
            self._storage[user_id] = set()

        self._storage[user_id].add(friend_id)
        return True

    def get_friends_list(self, user_id):
        return list(self._storage.get(user_id, []))
    