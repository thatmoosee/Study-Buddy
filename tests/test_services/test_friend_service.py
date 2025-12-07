"""
Unit tests for FriendService

Tests all public methods with happy and unhappy paths.
Uses mocking for repositories and models as per rubric requirements.
"""

import unittest
from unittest.mock import Mock, MagicMock
import sys
import os
from datetime import datetime

# Add backend to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from services.friend_service import FriendService
from models.friend import Friend
from models.user import User


class TestFriendService(unittest.TestCase):
    """Test suite for FriendService - covers all public methods"""

    def setUp(self):
        """Set up test fixtures before each test"""
        # Mock repositories
        self.mock_friend_repo = Mock()
        self.mock_user_repo = Mock()

        # Create service instance with mocked dependencies
        self.friend_service = FriendService(
            friend_repo=self.mock_friend_repo,
            user_repo=self.mock_user_repo
        )

    def tearDown(self):
        """Clean up after each test"""
        self.mock_friend_repo.reset_mock()
        self.mock_user_repo.reset_mock()


    def test_send_friend_request_happy_path(self):
        """Test successfully sending a friend request by email"""
        # Arrange
        user_id = "user123"
        friend_email = "friend@university.edu"

        mock_user = Mock(spec=User)
        mock_user.id = user_id
        self.mock_user_repo.find_by_id.return_value = mock_user

        mock_friend_user = Mock(spec=User)
        mock_friend_user.id = "friend456"
        mock_friend_user.email = friend_email
        self.mock_user_repo.find_by_email.return_value = mock_friend_user

        self.mock_friend_repo.find_friendship.return_value = None

        # Act
        success, message, friend_id = self.friend_service.send_friend_request(user_id, friend_email)

        # Assert
        self.assertTrue(success)
        self.assertEqual(message, "Friend request sent successfully")
        self.assertEqual(friend_id, "friend456")
        self.mock_friend_repo.send_friend_request.assert_called_once_with(user_id, "friend456")

    def test_send_friend_request_user_not_found(self):
        """Test sending friend request fails when current user not found"""
        # Arrange
        user_id = "nonexistent"
        friend_email = "friend@university.edu"
        self.mock_user_repo.find_by_id.return_value = None

        # Act
        success, message, friend_id = self.friend_service.send_friend_request(user_id, friend_email)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "User not found")
        self.assertIsNone(friend_id)
        self.mock_friend_repo.send_friend_request.assert_not_called()

    def test_send_friend_request_friend_email_not_found(self):
        """Test sending friend request fails when friend email not found"""
        # Arrange
        user_id = "user123"
        friend_email = "nonexistent@university.edu"

        mock_user = Mock(spec=User)
        mock_user.id = user_id
        self.mock_user_repo.find_by_id.return_value = mock_user
        self.mock_user_repo.find_by_email.return_value = None

        # Act
        success, message, friend_id = self.friend_service.send_friend_request(user_id, friend_email)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "No user found with that email address")
        self.assertIsNone(friend_id)

    def test_send_friend_request_to_self(self):
        """Test cannot send friend request to yourself"""
        # Arrange
        user_id = "user123"
        friend_email = "myself@university.edu"

        mock_user = Mock(spec=User)
        mock_user.id = user_id
        self.mock_user_repo.find_by_id.return_value = mock_user

        mock_friend_user = Mock(spec=User)
        mock_friend_user.id = user_id  # Same as current user
        self.mock_user_repo.find_by_email.return_value = mock_friend_user

        # Act
        success, message, friend_id = self.friend_service.send_friend_request(user_id, friend_email)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "Cannot send a friend request to yourself")
        self.assertIsNone(friend_id)

    def test_send_friend_request_already_pending(self):
        """Test cannot send duplicate friend request when one is pending"""
        # Arrange
        user_id = "user123"
        friend_email = "friend@university.edu"

        mock_user = Mock(spec=User)
        mock_user.id = user_id
        self.mock_user_repo.find_by_id.return_value = mock_user

        mock_friend_user = Mock(spec=User)
        mock_friend_user.id = "friend456"
        self.mock_user_repo.find_by_email.return_value = mock_friend_user

        mock_friendship = Mock(spec=Friend)
        mock_friendship.status = 'pending'
        self.mock_friend_repo.find_friendship.return_value = mock_friendship

        # Act
        success, message, friend_id = self.friend_service.send_friend_request(user_id, friend_email)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "Friend request already sent or received")
        self.assertIsNone(friend_id)

    def test_send_friend_request_already_friends(self):
        """Test cannot send friend request when already friends"""
        # Arrange
        user_id = "user123"
        friend_email = "friend@university.edu"

        mock_user = Mock(spec=User)
        mock_user.id = user_id
        self.mock_user_repo.find_by_id.return_value = mock_user

        mock_friend_user = Mock(spec=User)
        mock_friend_user.id = "friend456"
        self.mock_user_repo.find_by_email.return_value = mock_friend_user

        mock_friendship = Mock(spec=Friend)
        mock_friendship.status = 'accepted'
        self.mock_friend_repo.find_friendship.return_value = mock_friendship

        # Act
        success, message, friend_id = self.friend_service.send_friend_request(user_id, friend_email)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "Already friends with this user")
        self.assertIsNone(friend_id)


    def test_accept_friend_request_happy_path(self):
        """Test successfully accepting a friend request"""
        # Arrange
        user_id = "user123"
        request_id = "request456"

        mock_friendship = Mock(spec=Friend)
        mock_friendship.friend_id = user_id  # User is recipient
        mock_friendship.status = 'pending'
        self.mock_friend_repo.find_by_id.return_value = mock_friendship

        # Act
        success, message = self.friend_service.accept_friend_request(user_id, request_id)

        # Assert
        self.assertTrue(success)
        self.assertEqual(message, "Friend request accepted")
        self.mock_friend_repo.accept_friend_request.assert_called_once_with(request_id)

    def test_accept_friend_request_not_found(self):
        """Test accepting non-existent friend request fails"""
        # Arrange
        user_id = "user123"
        request_id = "nonexistent"
        self.mock_friend_repo.find_by_id.return_value = None

        # Act
        success, message = self.friend_service.accept_friend_request(user_id, request_id)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "Friend request not found")
        self.mock_friend_repo.accept_friend_request.assert_not_called()

    def test_accept_friend_request_not_recipient(self):
        """Test cannot accept friend request if not the recipient"""
        # Arrange
        user_id = "user123"
        request_id = "request456"

        mock_friendship = Mock(spec=Friend)
        mock_friendship.friend_id = "other_user"  # Different user
        mock_friendship.status = 'pending'
        self.mock_friend_repo.find_by_id.return_value = mock_friendship

        # Act
        success, message = self.friend_service.accept_friend_request(user_id, request_id)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "You cannot accept this friend request")

    def test_accept_friend_request_not_pending(self):
        """Test cannot accept friend request that's not pending"""
        # Arrange
        user_id = "user123"
        request_id = "request456"

        mock_friendship = Mock(spec=Friend)
        mock_friendship.friend_id = user_id
        mock_friendship.status = 'accepted'  # Already accepted
        self.mock_friend_repo.find_by_id.return_value = mock_friendship

        # Act
        success, message = self.friend_service.accept_friend_request(user_id, request_id)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "This friend request is not pending")


    def test_reject_friend_request_happy_path(self):
        """Test successfully rejecting a friend request"""
        # Arrange
        user_id = "user123"
        request_id = "request456"

        mock_friendship = Mock(spec=Friend)
        mock_friendship.friend_id = user_id
        mock_friendship.status = 'pending'
        self.mock_friend_repo.find_by_id.return_value = mock_friendship

        # Act
        success, message = self.friend_service.reject_friend_request(user_id, request_id)

        # Assert
        self.assertTrue(success)
        self.assertEqual(message, "Friend request rejected")
        self.mock_friend_repo.reject_friend_request.assert_called_once_with(request_id)

    def test_reject_friend_request_not_found(self):
        """Test rejecting non-existent friend request fails"""
        # Arrange
        user_id = "user123"
        request_id = "nonexistent"
        self.mock_friend_repo.find_by_id.return_value = None

        # Act
        success, message = self.friend_service.reject_friend_request(user_id, request_id)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "Friend request not found")

    def test_reject_friend_request_not_recipient(self):
        """Test cannot reject friend request if not the recipient"""
        # Arrange
        user_id = "user123"
        request_id = "request456"

        mock_friendship = Mock(spec=Friend)
        mock_friendship.friend_id = "other_user"
        mock_friendship.status = 'pending'
        self.mock_friend_repo.find_by_id.return_value = mock_friendship

        # Act
        success, message = self.friend_service.reject_friend_request(user_id, request_id)

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "You cannot reject this friend request")


    def test_remove_friend_happy_path(self):
        """Test successfully removing a friend"""
        # Arrange
        user_id = "user123"
        friend_id = "friend456"

        mock_friendship = Mock(spec=Friend)
        mock_friendship.id = "friendship789"
        self.mock_friend_repo.find_friendship.return_value = mock_friendship

        # Act
        result = self.friend_service.remove_friend(user_id, friend_id)

        # Assert
        self.assertTrue(result)
        self.mock_friend_repo.find_friendship.assert_called_once_with(user_id, friend_id)
        self.mock_friend_repo.remove.assert_called_once_with("friendship789")

    def test_remove_friend_not_found(self):
        """Test removing non-existent friendship fails"""
        # Arrange
        user_id = "user123"
        friend_id = "friend456"
        self.mock_friend_repo.find_friendship.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.friend_service.remove_friend(user_id, friend_id)

        self.assertIn("Friendship not found", str(context.exception))
        self.mock_friend_repo.remove.assert_not_called()


    def test_get_pending_requests_happy_path(self):
        """Test successfully retrieving pending friend requests"""
        # Arrange
        user_id = "user123"

        mock_request1 = Mock(spec=Friend)
        mock_request1.id = "req1"
        mock_request1.user_id = "sender1"
        mock_request1.created_at = datetime(2024, 1, 1, 12, 0, 0)

        mock_request2 = Mock(spec=Friend)
        mock_request2.id = "req2"
        mock_request2.user_id = "sender2"
        mock_request2.created_at = datetime(2024, 1, 2, 12, 0, 0)

        self.mock_friend_repo.get_pending_requests_received.return_value = [mock_request1, mock_request2]

        mock_sender1 = Mock(spec=User)
        mock_sender1.email = "sender1@university.edu"

        mock_sender2 = Mock(spec=User)
        mock_sender2.email = "sender2@university.edu"

        self.mock_user_repo.find_by_id.side_effect = [mock_sender1, mock_sender2]

        # Act
        result = self.friend_service.get_pending_requests(user_id)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['request_id'], 'req1')
        self.assertEqual(result[0]['from_email'], 'sender1@university.edu')
        self.assertEqual(result[1]['request_id'], 'req2')
        self.assertEqual(result[1]['from_email'], 'sender2@university.edu')

    def test_get_pending_requests_empty_list(self):
        """Test retrieving pending requests when none exist"""
        # Arrange
        user_id = "user123"
        self.mock_friend_repo.get_pending_requests_received.return_value = []

        # Act
        result = self.friend_service.get_pending_requests(user_id)

        # Assert
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    def test_get_pending_requests_sender_deleted(self):
        """Test pending requests when sender user no longer exists"""
        # Arrange
        user_id = "user123"

        mock_request = Mock(spec=Friend)
        mock_request.id = "req1"
        mock_request.user_id = "deleted_sender"
        mock_request.created_at = datetime(2024, 1, 1, 12, 0, 0)

        self.mock_friend_repo.get_pending_requests_received.return_value = [mock_request]
        self.mock_user_repo.find_by_id.return_value = None  # Sender deleted

        # Act
        result = self.friend_service.get_pending_requests(user_id)

        # Assert
        self.assertEqual(len(result), 0, "Should skip requests from deleted users")


    def test_get_friends_list_happy_path(self):
        """Test successfully retrieving user's friends list"""
        # Arrange
        user_id = "user123"
        mock_friends = [
            Mock(id="friend1", email="friend1@university.edu"),
            Mock(id="friend2", email="friend2@university.edu")
        ]
        self.mock_friend_repo.get_friends_list.return_value = mock_friends

        # Act
        result = self.friend_service.get_friends_list(user_id)

        # Assert
        self.mock_friend_repo.get_friends_list.assert_called_once_with(user_id)
        self.assertEqual(result, mock_friends)
        self.assertEqual(len(result), 2)

    def test_get_friends_list_empty(self):
        """Test retrieving friends list when user has no friends"""
        # Arrange
        user_id = "user123"
        self.mock_friend_repo.get_friends_list.return_value = []

        # Act
        result = self.friend_service.get_friends_list(user_id)

        # Assert
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()
