from models.chat import Chat


class ChatService:

    def __init__(self, chat_repo):
        self.chat_repo = chat_repo

    def create_chat(self, name, owner_id, members=None):
        members = members or []
        chat_id = len(self.chat_repo.storage()) + 1
        chat = Chat(chat_id, name, messages=[])
        chat.members = [owner_id] + members
        self.chat_repo.add(chat)
        return chat

    def leave_chat(self, chat_id, user_id):
        chat = self.chat_repo.get(chat_id)
        if chat:
            if user_id in chat.members:
                chat.members.remove(user_id)
                self.chat_repo.update(chat_id, chat)
                return chat
            raise ValueError("User not in chat.")
        raise KeyError("Chat not found.")

    def join_chat(self, chat_id, user_id):
        chat = self.chat_repo.get(chat_id)
        if chat:
            if user_id not in chat.members:
                chat.members.append(user_id)
                self.chat_repo.update(chat_id, chat)
                return chat
            else:
                raise ValueError("User is in chat.")
        raise ValueError("Chat not found.")

    def send_message(self, chat_id, message):
        chat = self.chat_repo.get(chat_id)
        if chat:
            chat.messages.append(message)
            self.chat_repo.update(chat_id, chat)
            return chat
        raise ValueError("Chat not found.")

    def list_all_chats(self, user_id):
        user_chats = {}
        for chat in self.chat_repo.find_all():
            if user_id in chat.members:
                user_chats[chat.chat_id] = chat.to_dict()
        return user_chats




