"""
Chat service for messaging functionality

Built by:
"""

from models.chat import Chat


class ChatService:

    def __init__(self, chat_repo):
        self.chat_repo = chat_repo

    def create_chat(self, name, owner_id, members=None, group_id=None):
        members = members or []
        if group_id is not None:
            chat_id = group_id
        else:
            chat_id = str(len(self.chat_repo.storage()) + 1)

        chat = Chat(name, chat_id)
        chat.members = [owner_id] + members
        self.chat_repo.add(chat)
        return chat

    def leave_chat(self, user_id, chat_id):
        chat = self.chat_repo.get(chat_id)
        if chat:
            if user_id in chat.members:
                chat.members.remove(user_id)
                self.chat_repo.update(chat_id, chat)
                return chat
            raise ValueError("User not in chat.")
        raise KeyError("Chat not found.")

    def join_chat(self, user_id, chat_id):
        chat = self.chat_repo.get(chat_id)
        if chat:
            if user_id not in chat.members:
                chat.members.append(user_id)
                self.chat_repo.update(chat_id, chat)
                return chat
            else:
                raise ValueError("User is in chat.")
        raise ValueError("Chat not found.")

    def create_DM(self, user_id, friend_id):
        # Check if DM already exists (bidirectional check)
        all_chats = self.chat_repo.find_all()
        for chat in all_chats:
            # Check if it's a DM between these two users (in either direction)
            if (chat.name == f"DM_{user_id}_{friend_id}" or
                chat.name == f"DM_{friend_id}_{user_id}"):
                # DM already exists, return it
                return chat

        # Create new DM if it doesn't exist
        chat_id = str(len(self.chat_repo.storage()) + 1)
        chat_name = f"DM_{user_id}_{friend_id}"
        chat = Chat(name=chat_name, chat_id=chat_id, members=[user_id, friend_id])
        self.chat_repo.add(chat)
        return chat

    def leave_DM(self, chat_id, user_id):
        chat = self.chat_repo.get(chat_id)
        if chat:
            if user_id in chat.members:
                chat.members.remove(user_id)
                self.chat_repo.update(chat_id, chat)
                return chat
            raise ValueError("User not in chat.")
        raise ValueError("Chat not found.")

    def send_message(self, user_id, chat_id, message, user_email=None):
        chat = self.chat_repo.get(chat_id)
        if chat:
            if chat.messages is None:
                chat.messages = []
            # Use email if provided, otherwise fallback to user_id
            sender = user_email if user_email else user_id
            new_message = f"{sender}: {message}"
            chat.messages.append(new_message)
            self.chat_repo.update(chat_id, chat)
            return chat
        raise ValueError("Chat not found.")

    def list_all_chats(self, user_id):
        user_chats = {}
        for chat in self.chat_repo.find_all():
            if user_id in chat.members:
                user_chats[chat.chat_id] = chat.to_dict()
        return user_chats

    def get_chat(self, chat_id):
        chat = self.chat_repo.get(chat_id)
        return chat



