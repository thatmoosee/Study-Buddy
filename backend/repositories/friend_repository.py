class FriendRepository:
    def __init__(self):
        self._storage = {}

    def add_friend(self, user_email, friend_email):
        user_email = user_email.lower().strip()
        friend_email = friend_email.lower().strip()

        if user_email not in self._storage:
            self._storage[user_email] = set()
        self._storage[user_email].add(friend_email)

    def get_friends(self, user_email):
        return list(self._storage.get(user_email.lower().strip(), []))
    
    def remove_friend(self, user_email, friend_email):
        user_email = user_email.lower().strip()
        friend_email = friend_email.lower().strip()

        if user_email not in self._storage:
            return False

        if friend_email not in self._storage[user_email]:
            return False

        self._storage[user_email].remove(friend_email)
        return True
