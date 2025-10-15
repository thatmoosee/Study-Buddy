from models.user import User
from validators.user_validator import UserValidator

class AuthService:
    """Authentication service"""

    def __init__(self, user_repository):
        self._user_repository = user_repository
        self._validator = UserValidator()

    def register(self, email, password):
        is_valid, errors = self._validator.validate({
            'email': email,
            'password': password
        })
        if not is_valid:
            raise ValueError(f"Validation failed: {', '.join(errors)}")

        user = User(email=email, password=password)
        created_user = self._user_repository.create(user)
        return created_user

    def login(self, email, password):
        user = self._user_repository.find_by_email(email)
        if not user or not user.verify_password(password):
            raise ValueError("Invalid email or password")
        return user

    def logout(self, session):
        session.clear()
