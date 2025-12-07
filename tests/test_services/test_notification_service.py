"""
Unit tests for NotificationService

Tests all public methods with happy and unhappy paths.
Uses mocking for repositories and models as per rubric requirements.
"""

import unittest
from unittest.mock import Mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from services.notification_service import NotificationService
from models.notification import Notification


class TestNotificationService(unittest.TestCase):
    """Test suite for NotificationService"""

    def setUp(self):
        self.mock_repo = Mock()
        self.notification_service = NotificationService(repo=self.mock_repo)

    def test_send_notification_happy_path(self):
        """Test successfully sending a notification"""
        user_id = "user123"
        message = "You have a new friend request"

        mock_notification = Mock(spec=Notification)
        mock_notification.user_id = user_id
        mock_notification.message = message
        self.mock_repo.create.return_value = mock_notification

        result = self.notification_service.send_notification(user_id, message)

        self.mock_repo.create.assert_called_once()
        self.assertEqual(result, mock_notification)
        self.assertEqual(result.user_id, user_id)

    def test_send_notification_empty_message(self):
        """Test sending notification with empty message"""
        user_id = "user123"
        message = ""

        mock_notification = Mock(spec=Notification)
        self.mock_repo.create.return_value = mock_notification

        result = self.notification_service.send_notification(user_id, message)

        self.mock_repo.create.assert_called_once()

    def test_send_notification_long_message(self):
        """Test sending notification with long message"""
        user_id = "user123"
        message = "A" * 500  # Long message

        mock_notification = Mock(spec=Notification)
        self.mock_repo.create.return_value = mock_notification

        result = self.notification_service.send_notification(user_id, message)

        self.mock_repo.create.assert_called_once()

    def test_get_notifications_happy_path(self):
        """Test successfully getting user notifications"""
        user_id = "user123"

        mock_notif1 = Mock(spec=Notification)
        mock_notif1.message = "Notification 1"
        mock_notif2 = Mock(spec=Notification)
        mock_notif2.message = "Notification 2"

        self.mock_repo.find_by_user_id.return_value = [mock_notif1, mock_notif2]

        result = self.notification_service.get_notifications(user_id)

        self.mock_repo.find_by_user_id.assert_called_once_with(user_id)
        self.assertEqual(len(result), 2)

    def test_get_notifications_empty_list(self):
        """Test getting notifications when user has none"""
        user_id = "user123"
        self.mock_repo.find_by_user_id.return_value = []

        result = self.notification_service.get_notifications(user_id)

        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    def test_get_notifications_nonexistent_user(self):
        """Test getting notifications for non-existent user"""
        user_id = "nonexistent"
        self.mock_repo.find_by_user_id.return_value = []

        result = self.notification_service.get_notifications(user_id)

        self.assertEqual(len(result), 0)

    def test_mark_notifications_as_read_happy_path(self):
        """Test successfully marking notification as read"""
        notif_id = "notif123"

        mock_notification = Mock(spec=Notification)
        mock_notification.read = True
        self.mock_repo.mark_as_read.return_value = mock_notification

        result = self.notification_service.mark_notifications_as_read(notif_id)

        self.mock_repo.mark_as_read.assert_called_once_with(notif_id)
        self.assertEqual(result, mock_notification)

    def test_mark_notifications_as_read_invalid_id(self):
        """Test marking non-existent notification as read"""
        notif_id = "nonexistent"
        self.mock_repo.mark_as_read.return_value = None

        result = self.notification_service.mark_notifications_as_read(notif_id)

        self.assertIsNone(result)

    def test_mark_notifications_as_read_already_read(self):
        """Test marking already-read notification"""
        notif_id = "notif123"

        mock_notification = Mock(spec=Notification)
        mock_notification.read = True
        self.mock_repo.mark_as_read.return_value = mock_notification

        result = self.notification_service.mark_notifications_as_read(notif_id)

        self.mock_repo.mark_as_read.assert_called_once()

    def test_delete_notification_happy_path(self):
        """Test successfully deleting a notification"""
        notif_id = "notif123"

        self.mock_repo.delete.return_value = True

        result = self.notification_service.delete_notification(notif_id)

        self.mock_repo.delete.assert_called_once_with(notif_id)
        self.assertTrue(result)

    def test_delete_notification_not_found(self):
        """Test deleting non-existent notification"""
        notif_id = "nonexistent"
        self.mock_repo.delete.return_value = False

        result = self.notification_service.delete_notification(notif_id)

        self.assertFalse(result)

    def test_delete_notification_multiple_calls(self):
        """Test deleting multiple notifications"""
        notif_ids = ["notif1", "notif2", "notif3"]
        self.mock_repo.delete.return_value = True

        for notif_id in notif_ids:
            result = self.notification_service.delete_notification(notif_id)
            self.assertTrue(result)

        self.assertEqual(self.mock_repo.delete.call_count, 3)


if __name__ == '__main__':
    unittest.main()
