"""
Unit tests for ChatService

Tests all public methods with happy and unhappy paths.
Uses mocking for repositories and models as per rubric requirements.
"""

import unittest
from unittest.mock import Mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from services.chat_service import ChatService
from models.chat import Chat


class TestChatService(unittest.TestCase):
    """Test suite for ChatService"""

    def setUp(self):
        self.mock_chat_repo = Mock()
        self.chat_service = ChatService(chat_repo=self.mock_chat_repo)


    def test_create_chat_happy_path(self):
        """Test successfully creating a chat"""
        name = "Study Chat"
        owner_id = "user123"
        members = ["user456", "user789"]

        self.mock_chat_repo.storage.return_value = []

        result = self.chat_service.create_chat(name, owner_id, members)

        self.mock_chat_repo.add.assert_called_once()
        self.assertIsInstance(result, Chat)
        self.assertEqual(result.name, name)

    def test_create_chat_with_group_id(self):
        """Test creating chat with specific group_id"""
        name = "Group Chat"
        owner_id = "user123"
        group_id = "group456"

        result = self.chat_service.create_chat(name, owner_id, group_id=group_id)

        self.assertEqual(result.chat_id, group_id)

    def test_create_chat_minimal(self):
        """Test creating chat with minimal parameters"""
        self.mock_chat_repo.storage.return_value = []

        result = self.chat_service.create_chat("Test", "user123")

        self.mock_chat_repo.add.assert_called_once()

    def test_join_chat_happy_path(self):
        """Test successfully joining a chat"""
        user_id = "user456"
        chat_id = "chat123"

        mock_chat = Mock(spec=Chat)
        mock_chat.members = []
        self.mock_chat_repo.get.return_value = mock_chat

        result = self.chat_service.join_chat(user_id, chat_id)

        self.assertIn(user_id, mock_chat.members)
        self.mock_chat_repo.update.assert_called_once()

    def test_join_chat_already_member(self):
        """Test joining chat when already a member fails"""
        user_id = "user123"
        chat_id = "chat123"

        mock_chat = Mock(spec=Chat)
        mock_chat.members = ["user123"]
        self.mock_chat_repo.get.return_value = mock_chat

        with self.assertRaises(ValueError) as context:
            self.chat_service.join_chat(user_id, chat_id)

        self.assertIn("User is in chat", str(context.exception))

    def test_join_chat_not_found(self):
        """Test joining non-existent chat fails"""
        self.mock_chat_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.chat_service.join_chat("user123", "nonexistent")

        self.assertIn("Chat not found", str(context.exception))


    def test_leave_chat_happy_path(self):
        """Test successfully leaving a chat"""
        user_id = "user456"
        chat_id = "chat123"

        mock_chat = Mock(spec=Chat)
        mock_chat.members = ["user123", "user456"]
        self.mock_chat_repo.get.return_value = mock_chat

        result = self.chat_service.leave_chat(user_id, chat_id)

        self.assertNotIn(user_id, mock_chat.members)
        self.mock_chat_repo.update.assert_called_once()

    def test_leave_chat_not_member(self):
        """Test leaving chat when not a member fails"""
        user_id = "user999"
        chat_id = "chat123"

        mock_chat = Mock(spec=Chat)
        mock_chat.members = ["user123"]
        self.mock_chat_repo.get.return_value = mock_chat

        with self.assertRaises(ValueError) as context:
            self.chat_service.leave_chat(user_id, chat_id)

        self.assertIn("User not in chat", str(context.exception))

    def test_leave_chat_not_found(self):
        """Test leaving non-existent chat fails"""
        self.mock_chat_repo.get.return_value = None

        with self.assertRaises(KeyError):
            self.chat_service.leave_chat("user123", "nonexistent")


    def test_create_dm_happy_path(self):
        """Test successfully creating a DM"""
        user_id = "user123"
        friend_id = "user456"

        self.mock_chat_repo.find_all.return_value = []
        self.mock_chat_repo.storage.return_value = []

        result = self.chat_service.create_DM(user_id, friend_id)

        self.mock_chat_repo.add.assert_called_once()
        self.assertIn("DM_", result.name)

    def test_create_dm_already_exists(self):
        """Test creating DM when it already exists returns existing"""
        user_id = "user123"
        friend_id = "user456"

        existing_dm = Mock(spec=Chat)
        existing_dm.name = f"DM_{user_id}_{friend_id}"
        self.mock_chat_repo.find_all.return_value = [existing_dm]

        result = self.chat_service.create_DM(user_id, friend_id)

        self.mock_chat_repo.add.assert_not_called()
        self.assertEqual(result, existing_dm)

    def test_create_dm_bidirectional_check(self):
        """Test DM creation checks both user order combinations"""
        user_id = "user123"
        friend_id = "user456"

        existing_dm = Mock(spec=Chat)
        existing_dm.name = f"DM_{friend_id}_{user_id}"  # Reverse order
        self.mock_chat_repo.find_all.return_value = [existing_dm]

        result = self.chat_service.create_DM(user_id, friend_id)

        self.assertEqual(result, existing_dm)


    def test_send_message_happy_path(self):
        """Test successfully sending a message"""
        user_id = "user123"
        chat_id = "chat123"
        message = "Hello, world!"

        mock_chat = Mock(spec=Chat)
        mock_chat.messages = []
        self.mock_chat_repo.get.return_value = mock_chat

        result = self.chat_service.send_message(user_id, chat_id, message)

        self.assertEqual(len(mock_chat.messages), 1)
        self.assertIn(message, mock_chat.messages[0])
        self.mock_chat_repo.update.assert_called_once()

    def test_send_message_with_email(self):
        """Test sending message with email as sender"""
        user_id = "user123"
        user_email = "test@university.edu"
        chat_id = "chat123"
        message = "Hi there"

        mock_chat = Mock(spec=Chat)
        mock_chat.messages = []
        self.mock_chat_repo.get.return_value = mock_chat

        result = self.chat_service.send_message(user_id, chat_id, message, user_email)

        # Check that email was used in the message
        self.assertEqual(len(mock_chat.messages), 1)
        self.assertIn(user_email, mock_chat.messages[0])

    def test_send_message_chat_not_found(self):
        """Test sending message to non-existent chat fails"""
        self.mock_chat_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.chat_service.send_message("user123", "nonexistent", "message")

        self.assertIn("Chat not found", str(context.exception))


    def test_list_all_chats_happy_path(self):
        """Test successfully listing all user chats"""
        user_id = "user123"

        mock_chat1 = Mock(spec=Chat)
        mock_chat1.chat_id = "chat1"
        mock_chat1.members = ["user123", "user456"]
        mock_chat1.to_dict.return_value = {"chat_id": "chat1"}

        mock_chat2 = Mock(spec=Chat)
        mock_chat2.chat_id = "chat2"
        mock_chat2.members = ["user123"]
        mock_chat2.to_dict.return_value = {"chat_id": "chat2"}

        self.mock_chat_repo.find_all.return_value = [mock_chat1, mock_chat2]

        result = self.chat_service.list_all_chats(user_id)

        self.assertEqual(len(result), 2)
        self.assertIn("chat1", result)

    def test_list_all_chats_no_chats(self):
        """Test listing chats when user has none"""
        user_id = "user123"

        mock_chat = Mock(spec=Chat)
        mock_chat.members = ["user456"]
        self.mock_chat_repo.find_all.return_value = [mock_chat]

        result = self.chat_service.list_all_chats(user_id)

        self.assertEqual(len(result), 0)

    def test_get_chat_happy_path(self):
        """Test successfully getting a chat"""
        chat_id = "chat123"
        mock_chat = Mock(spec=Chat)
        self.mock_chat_repo.get.return_value = mock_chat

        result = self.chat_service.get_chat(chat_id)

        self.assertEqual(result, mock_chat)

    def test_get_chat_not_found(self):
        """Test getting non-existent chat returns None"""
        self.mock_chat_repo.get.return_value = None

        result = self.chat_service.get_chat("nonexistent")

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()