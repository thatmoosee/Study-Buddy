"""
Unit tests for ProfileService

Tests all public methods with happy and unhappy paths.
Uses mocking for repositories and models as per rubric requirements.
"""

import unittest
from unittest.mock import Mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from services.profile_service import ProfileService
from models.profile import Profile


class TestProfileService(unittest.TestCase):
    """Test suite for ProfileService"""

    def setUp(self):
        self.mock_profile_repo = Mock()
        self.profile_service = ProfileService(profile_repository=self.mock_profile_repo)


    def test_create_profile_happy_path(self):
        """Test successfully creating a profile"""
        user_id = "user123"
        name = "John Doe"
        major = "Computer Science"
        availability = ["Mon 2-4pm", "Wed 3-5pm"]

        mock_profile = Mock(spec=Profile)
        mock_profile.user_id = user_id
        self.mock_profile_repo.create.return_value = mock_profile

        result = self.profile_service.create_profile(user_id, name, major, availability)

        self.mock_profile_repo.create.assert_called_once()
        self.assertEqual(result, mock_profile)

    def test_create_profile_invalid_user_id(self):
        """Test create profile fails with invalid user_id"""
        with self.assertRaises(ValueError) as context:
            self.profile_service.create_profile(None)

        self.assertIn("Validation failed", str(context.exception))

    def test_create_profile_minimal(self):
        """Test creating profile with only user_id"""
        user_id = "user123"
        mock_profile = Mock(spec=Profile)
        self.mock_profile_repo.create.return_value = mock_profile

        result = self.profile_service.create_profile(user_id)

        self.mock_profile_repo.create.assert_called_once()


    def test_update_profile_happy_path(self):
        """Test successfully updating a profile"""
        profile_id = "profile123"
        data = {"name": "Jane Doe", "major": "Mathematics"}

        mock_profile = Mock(spec=Profile)
        self.mock_profile_repo.update.return_value = mock_profile

        result = self.profile_service.update_profile(profile_id, data)

        self.mock_profile_repo.update.assert_called_once_with(profile_id, data)
        self.assertEqual(result, mock_profile)

    def test_update_profile_empty_data(self):
        """Test updating profile with empty data"""
        profile_id = "profile123"
        data = {}

        result = self.profile_service.update_profile(profile_id, data)

        self.mock_profile_repo.update.assert_called_once_with(profile_id, data)


    def test_get_profile_by_user_id_happy_path(self):
        """Test successfully getting profile by user_id"""
        user_id = "user123"
        mock_profile = Mock(spec=Profile)
        mock_profile.user_id = user_id
        self.mock_profile_repo.find_by_user_id.return_value = mock_profile

        result = self.profile_service.get_profile_by_user_id(user_id)

        self.mock_profile_repo.find_by_user_id.assert_called_once_with(user_id)
        self.assertEqual(result, mock_profile)

    def test_get_profile_by_user_id_not_found(self):
        """Test getting profile when none exists"""
        user_id = "nonexistent"
        self.mock_profile_repo.find_by_user_id.return_value = None

        result = self.profile_service.get_profile_by_user_id(user_id)

        self.assertIsNone(result)


    def test_upload_profile_creates_new(self):
        """Test upload creates new profile when none exists"""
        user_id = "user123"
        data = {"name": "New User", "major": "Physics"}

        self.mock_profile_repo.find_by_user_id.return_value = None
        mock_profile = Mock(spec=Profile)
        self.mock_profile_repo.create.return_value = mock_profile

        result = self.profile_service.upload_profile(user_id, data)

        self.mock_profile_repo.create.assert_called_once()
        self.assertEqual(result, mock_profile)

    def test_upload_profile_updates_existing(self):
        """Test upload updates existing profile"""
        user_id = "user123"
        data = {"name": "Updated Name"}

        existing_profile = Mock(spec=Profile)
        existing_profile.id = "profile123"
        self.mock_profile_repo.find_by_user_id.return_value = existing_profile

        mock_updated = Mock(spec=Profile)
        self.mock_profile_repo.update.return_value = mock_updated

        result = self.profile_service.upload_profile(user_id, data)

        self.mock_profile_repo.update.assert_called_once_with("profile123", data)
        self.assertEqual(result, mock_updated)


if __name__ == '__main__':
    unittest.main()
