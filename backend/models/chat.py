"""
Chat model for group messaging functionality

Built by: Josh Topp
"""
from models.base_model import BaseModel

class Chat(BaseModel):

    def __init__(self, chat_id, name, messages=None, members=None):
        self.chat_id = chat_id
        self.name = name
        self.messages = messages
        self.members = members


    def validate(self):
        if not self.name:
            raise ValueError("Chat name is required.")
        if not self.members:
            raise ValueError("chat must have at least one member.")


    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "name": self.name,
            "members": self.members,
            'messages': self.messages
        }