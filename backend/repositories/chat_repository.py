"""
Chat repository for managing user chats updating and making them

Built by: Josh Topp
"""


import json
import os
from models.chat import Chat
from repositories.base_repository import BaseRepository

class ChatRepository(BaseRepository):

    def __init__(self, filepath='data/chat.json'):
        self._json_file = os.path.abspath(filepath)
        self._storage = {}
        self._load_from_file()


    def storage(self):
        return self._storage

    def _load_from_file(self):
        try:
            with open(self._json_file, 'r') as f:
                data = json.load(f)
            for c in data.values():
                chat = Chat(
                    name=c['name'],
                    chat_id=c['chat_id'],
                    messages=c['messages'],
                    members=c['members']
                )
                self._storage[chat.chat_id] = chat
        except (FileNotFoundError, json.JSONDecodeError):
            self._storage = {}

    def _save_to_file(self):
        directory = os.path.dirname(self._json_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

        data = {str(chat.chat_id): {
            'name': chat.name,
            'chat_id': chat.chat_id,
            'messages': chat.messages,
            'members': chat.members
        } for chat in self._storage.values()}

        with open(self._json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def create(self, entity):
        self._storage[entity.chat_id] = entity
        self._save_to_file()

    def find_by_id(self, id):
        return self._storage.get(id)

    def find_all(self):
        return list(self._storage.values())


    def add(self, chat):
        return self.create(chat)

    def get(self, chat_id):
        return self.find_by_id(chat_id)

    def update(self, chat_id, chat):
        if chat_id in self._storage:
            self._storage[chat_id] = chat
            self._save_to_file()
            return chat
        raise ValueError("Chat not found")

    def list_all(self):
        return self.find_all()

