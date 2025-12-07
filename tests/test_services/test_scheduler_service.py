"""
Unit tests for SchedulerService

Tests all public methods with happy and unhappy paths.
Uses mocking for repositories and models as per rubric requirements.
"""

import unittest
from unittest.mock import Mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from services.scheduler_services import SchedulerService
from models.study_scheduler import StudyScheduler


class TestSchedulerService(unittest.TestCase):
    """Test suite for SchedulerService"""

    def setUp(self):
        self.mock_repo = Mock()
        self.scheduler_service = SchedulerService(study_session_repository=self.mock_repo)


    def test_create_study_scheduler_happy_path(self):
        """Test successfully creating a study session"""
        user_id = "user123"
        title = "Math Study Session"
        start_time = "2024-12-15T14:00"
        end_time = "2024-12-15T16:00"

        mock_session = Mock(spec=StudyScheduler)
        mock_session.user_id = user_id
        mock_session.title = title
        self.mock_repo.create.return_value = mock_session

        result = self.scheduler_service.create_study_scheduler(user_id, title, start_time, end_time)

        self.mock_repo.create.assert_called_once()
        self.assertEqual(result, mock_session)

    def test_create_study_scheduler_with_group(self):
        """Test creating study session with group_id"""
        user_id = "user123"
        title = "Group Study"
        start_time = "2024-12-15T10:00"
        end_time = "2024-12-15T12:00"
        group_id = "group456"

        mock_session = Mock(spec=StudyScheduler)
        self.mock_repo.create.return_value = mock_session

        result = self.scheduler_service.create_study_scheduler(
            user_id, title, start_time, end_time, group_id
        )

        self.mock_repo.create.assert_called_once()

    def test_create_study_scheduler_invalid_start_time(self):
        """Test creating session with invalid start time format fails"""
        user_id = "user123"
        title = "Invalid Session"
        start_time = "invalid-date"
        end_time = "2024-12-15T16:00"

        with self.assertRaises(Exception) as context:
            self.scheduler_service.create_study_scheduler(user_id, title, start_time, end_time)

        self.assertIn("Invalid format", str(context.exception))
        self.mock_repo.create.assert_not_called()

    def test_create_study_scheduler_invalid_end_time(self):
        """Test creating session with invalid end time format fails"""
        user_id = "user123"
        title = "Invalid Session"
        start_time = "2024-12-15T14:00"
        end_time = "not-a-date"

        with self.assertRaises(Exception) as context:
            self.scheduler_service.create_study_scheduler(user_id, title, start_time, end_time)

        self.assertIn("Invalid format", str(context.exception))

    def test_create_study_scheduler_various_times(self):
        """Test creating sessions with different time formats"""
        user_id = "user123"
        title = "Morning Study"
        start_time = "2025-01-20T08:30"
        end_time = "2025-01-20T10:30"

        mock_session = Mock(spec=StudyScheduler)
        self.mock_repo.create.return_value = mock_session

        result = self.scheduler_service.create_study_scheduler(user_id, title, start_time, end_time)

        self.mock_repo.create.assert_called_once()


    def test_get_sessions_happy_path(self):
        """Test successfully getting all sessions"""
        mock_session1 = Mock(spec=StudyScheduler)
        mock_session2 = Mock(spec=StudyScheduler)
        mock_session3 = Mock(spec=StudyScheduler)

        self.mock_repo.find_all.return_value = [mock_session1, mock_session2, mock_session3]

        result = self.scheduler_service.get_sessions()

        self.mock_repo.find_all.assert_called_once()
        self.assertEqual(len(result), 3)

    def test_get_sessions_empty(self):
        """Test getting sessions when none exist"""
        self.mock_repo.find_all.return_value = []

        result = self.scheduler_service.get_sessions()

        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)


    def test_get_user_sessions_happy_path(self):
        """Test successfully getting sessions for a specific user"""
        user_id = "user123"

        mock_session1 = Mock(spec=StudyScheduler)
        mock_session1.user_id = user_id
        mock_session2 = Mock(spec=StudyScheduler)
        mock_session2.user_id = user_id

        self.mock_repo.get_sessions_by_user.return_value = [mock_session1, mock_session2]

        result = self.scheduler_service.get_user_sessions(user_id)

        self.mock_repo.get_sessions_by_user.assert_called_once_with(user_id)
        self.assertEqual(len(result), 2)

    def test_get_user_sessions_no_sessions(self):
        """Test getting user sessions when user has none"""
        user_id = "user123"
        self.mock_repo.get_sessions_by_user.return_value = []

        result = self.scheduler_service.get_user_sessions(user_id)

        self.assertEqual(len(result), 0)

    def test_get_user_sessions_nonexistent_user(self):
        """Test getting sessions for non-existent user"""
        user_id = "nonexistent"
        self.mock_repo.get_sessions_by_user.return_value = []

        result = self.scheduler_service.get_user_sessions(user_id)

        self.assertEqual(len(result), 0)


    def test_delete_session_happy_path(self):
        """Test successfully deleting a session"""
        session_id = "session123"

        self.mock_repo.delete.return_value = True

        result = self.scheduler_service.delete_session(session_id)

        self.mock_repo.delete.assert_called_once_with(session_id)
        self.assertTrue(result)

    def test_delete_session_not_found(self):
        """Test deleting non-existent session"""
        session_id = "nonexistent"
        self.mock_repo.delete.return_value = False

        result = self.scheduler_service.delete_session(session_id)

        self.assertFalse(result)

    def test_delete_session_multiple_deletions(self):
        """Test deleting multiple sessions"""
        session_ids = ["session1", "session2", "session3"]
        self.mock_repo.delete.return_value = True

        for session_id in session_ids:
            result = self.scheduler_service.delete_session(session_id)
            self.assertTrue(result)

        self.assertEqual(self.mock_repo.delete.call_count, 3)


if __name__ == '__main__':
    unittest.main()
