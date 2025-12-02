"""
Chat model for group messaging functionality

Built by: Josh Topp
"""
from models.base_model import BaseModel
import uuid
class Chat(BaseModel):

    def __init__(self, name, chat_id=None, messages=None, members=None):
        self.chat_id = chat_id or str(uuid.uuid4())
        self.name = name
        if messages is None:
            self.messages = []
        else:
            self.messages = messages
        if members is None:
            self.members = []
        else:
            self.members = members


    def validate(self):
        if not self.name:
            raise ValueError("Chat name is required.")
        if not self.members:
            raise ValueError("chat must have at least one member.")


    def to_dict(self):
        return {
            "name": self.name,
            "chat_id": self.chat_id,
            "members": self.members,
            'messages': self.messages
        }