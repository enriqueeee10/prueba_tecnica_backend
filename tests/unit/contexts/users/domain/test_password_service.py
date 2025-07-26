import pytest
from app.contexts.users.domain.services.password_service import PasswordService


class TestPasswordService:
    def setup_method(self):
        self.password_service = PasswordService()

    def test_hash_password(self):
        """Test password hashing"""
        password = "test_password"
        hashed = self.password_service.hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_success(self):
        """Test successful password verification"""
        password = "test_password"
        hashed = self.password_service.hash_password(password)

        assert self.password_service.verify_password(password, hashed) is True

    def test_verify_password_failure(self):
        """Test failed password verification"""
        password = "test_password"
        wrong_password = "wrong_password"
        hashed = self.password_service.hash_password(password)

        assert self.password_service.verify_password(wrong_password, hashed) is False
