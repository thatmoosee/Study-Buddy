"""
Unit tests for AuthService

Tests all public methods with happy and unhappy paths.
Uses mocking for repositories and models as per rubric requirements.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from services.auth_service import AuthService
from models.user import User
from models.password_reset import PasswordResetToken


class TestAuthService(unittest.TestCase):
    """Test suite for AuthService - covers all public methods"""

    def setUp(self):
        """Set up test fixtures before each test"""
        # Mock repositories
        self.mock_user_repo = Mock()
        self.mock_token_repo = Mock()

        # Create service instance with mocked dependencies
        self.auth_service = AuthService(
            user_repository=self.mock_user_repo,
            token_repository=self.mock_token_repo
        )

    def tearDown(self):
        """Clean up after each test"""
        self.mock_user_repo.reset_mock()
        self.mock_token_repo.reset_mock()

    def test_register_happy_path(self):
        """Test successful user registration with valid credentials"""
        # Arrange
        email = "test@university.edu"
        password = "SecurePass123!"
        mock_user = Mock(spec=User)
        mock_user.email = email
        mock_user.id = "user123"
        self.mock_user_repo.create.return_value = mock_user

        # Act
        result = self.auth_service.register(email, password)

        # Assert
        self.mock_user_repo.create.assert_called_once()
        self.assertEqual(result, mock_user)
        self.assertEqual(result.email, email)

    def test_register_invalid_email(self):
        """Test registration fails with invalid email format"""
        # Arrange
        email = "invalid-email"
        password = "SecurePass123!"

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.register(email, password)

        self.assertIn("Validation failed", str(context.exception))
        self.mock_user_repo.create.assert_not_called()

    def test_register_weak_password(self):
        """Test registration fails with weak password"""
        # Arrange
        email = "test@university.edu"
        password = "123"  # Too short

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.register(email, password)

        self.assertIn("Validation failed", str(context.exception))
        self.mock_user_repo.create.assert_not_called()

    def test_register_empty_credentials(self):
        """Test registration fails with empty email or password"""
        # Act & Assert - empty email
        with self.assertRaises(ValueError):
            self.auth_service.register("", "password123")

        # Act & Assert - empty password
        with self.assertRaises(ValueError):
            self.auth_service.register("test@university.edu", "")

    def test_login_happy_path(self):
        """Test successful login with valid credentials"""
        # Arrange
        email = "test@university.edu"
        password = "SecurePass123!"
        mock_user = Mock(spec=User)
        mock_user.email = email
        mock_user.verify_password.return_value = True
        self.mock_user_repo.find_by_email.return_value = mock_user

        # Act
        result = self.auth_service.login(email, password)

        # Assert
        self.mock_user_repo.find_by_email.assert_called_once_with(email)
        mock_user.verify_password.assert_called_once_with(password)
        self.assertEqual(result, mock_user)

    def test_login_user_not_found(self):
        """Test login fails when user does not exist"""
        # Arrange
        email = "nonexistent@university.edu"
        password = "password123"
        self.mock_user_repo.find_by_email.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.login(email, password)

        self.assertIn("Invalid email or password", str(context.exception))

    def test_login_wrong_password(self):
        """Test login fails with incorrect password"""
        # Arrange
        email = "test@university.edu"
        password = "WrongPassword"
        mock_user = Mock(spec=User)
        mock_user.verify_password.return_value = False
        self.mock_user_repo.find_by_email.return_value = mock_user

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.login(email, password)

        self.assertIn("Invalid email or password", str(context.exception))

    def test_logout_happy_path(self):
        """Test successful logout clears session"""
        # Arrange
        mock_session = {'user_id': '123', 'email': 'test@university.edu'}

        # Act
        self.auth_service.logout(mock_session)

        # Assert
        self.assertEqual(len(mock_session), 0, "Session should be cleared")

    def test_logout_empty_session(self):
        """Test logout works with already empty session"""
        # Arrange
        mock_session = {}

        # Act
        self.auth_service.logout(mock_session)

        # Assert
        self.assertEqual(len(mock_session), 0)

    def test_request_password_reset_happy_path(self):
        """Test successful password reset request creates token"""
        # Arrange
        email = "test@university.edu"
        mock_user = Mock(spec=User)
        mock_user.id = "user123"
        mock_user.email = email
        self.mock_user_repo.find_by_email.return_value = mock_user

        mock_token = Mock(spec=PasswordResetToken)
        mock_token.token = "reset-token-123"
        self.mock_token_repo.create.return_value = mock_token

        # Act
        result = self.auth_service.request_password_reset(email)

        # Assert
        self.mock_user_repo.find_by_email.assert_called_once_with(email)
        self.mock_token_repo.delete_expired_tokens.assert_called_once()
        self.mock_token_repo.create.assert_called_once()
        self.assertEqual(result, mock_token)

    def test_request_password_reset_user_not_found(self):
        """Test password reset request with non-existent user returns None"""
        # Arrange
        email = "nonexistent@university.edu"
        self.mock_user_repo.find_by_email.return_value = None

        # Act
        result = self.auth_service.request_password_reset(email)

        # Assert
        self.assertIsNone(result, "Should return None for security (prevent user enumeration)")
        self.mock_token_repo.create.assert_not_called()

    def test_request_password_reset_invalid_email(self):
        """Test password reset request fails with invalid email"""
        # Arrange
        email = "invalid-email"

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.request_password_reset(email)

        self.assertIn("Validation failed", str(context.exception))

    def test_request_password_reset_no_token_repo(self):
        """Test password reset fails when token repository not configured"""
        # Arrange
        service = AuthService(user_repository=self.mock_user_repo, token_repository=None)

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            service.request_password_reset("test@university.edu")

        self.assertIn("not configured", str(context.exception))

    def test_reset_password_happy_path(self):
        """Test successful password reset with valid token"""
        # Arrange
        token_string = "valid-token-123"
        new_password = "NewSecurePass456!"

        mock_token = Mock(spec=PasswordResetToken)
        mock_token.user_id = "user123"
        mock_token.is_valid.return_value = True
        mock_token.is_used = False
        self.mock_token_repo.find_by_token.return_value = mock_token

        mock_user = Mock(spec=User)
        mock_user.id = "user123"
        mock_user._hash_password.return_value = "hashed_new_password"
        self.mock_user_repo.find_by_id.return_value = mock_user

        # Act
        result = self.auth_service.reset_password(token_string, new_password)

        # Assert
        self.mock_token_repo.find_by_token.assert_called_once_with(token_string)
        mock_token.is_valid.assert_called_once()
        self.mock_user_repo.find_by_id.assert_called_once_with("user123")
        self.mock_user_repo.update.assert_called_once()
        self.mock_token_repo.update.assert_called_once()
        self.assertEqual(result, mock_user)

    def test_reset_password_invalid_token(self):
        """Test password reset fails with invalid token"""
        # Arrange
        token_string = "invalid-token"
        new_password = "NewSecurePass456!"
        self.mock_token_repo.find_by_token.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.reset_password(token_string, new_password)

        self.assertIn("Invalid or expired reset token", str(context.exception))

    def test_reset_password_expired_token(self):
        """Test password reset fails with expired token"""
        # Arrange
        token_string = "expired-token"
        new_password = "NewSecurePass456!"

        mock_token = Mock(spec=PasswordResetToken)
        mock_token.is_valid.return_value = False
        self.mock_token_repo.find_by_token.return_value = mock_token

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.reset_password(token_string, new_password)

        self.assertIn("Invalid or expired reset token", str(context.exception))

    def test_reset_password_weak_password(self):
        """Test password reset fails with weak new password"""
        # Arrange
        token_string = "valid-token"
        new_password = "123"  # Too weak

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.reset_password(token_string, new_password)

        self.assertIn("Validation failed", str(context.exception))

    def test_reset_password_user_not_found(self):
        """Test password reset fails when user not found"""
        # Arrange
        token_string = "valid-token"
        new_password = "NewSecurePass456!"

        mock_token = Mock(spec=PasswordResetToken)
        mock_token.user_id = "nonexistent-user"
        mock_token.is_valid.return_value = True
        self.mock_token_repo.find_by_token.return_value = mock_token
        self.mock_user_repo.find_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.reset_password(token_string, new_password)

        self.assertIn("User not found", str(context.exception))


if __name__ == '__main__':
    unittest.main()
