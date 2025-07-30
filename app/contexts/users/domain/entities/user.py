from typing import Optional
from app.contexts.users.domain.value_objects.user_id import UserId
from app.contexts.users.domain.value_objects.email import Email
from app.contexts.users.domain.value_objects.password import Password


class User:
    def __init__(
        self,
        user_id: UserId,
        name: str,
        email: Email,
        hashed_password: str,
        is_active: bool = True,
    ):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._hashed_password = hashed_password
        self._is_active = is_active

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> Email:
        return self._email

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    @property
    def is_active(self) -> bool:
        return self._is_active

    def change_name(self, new_name: str):
        self._name = new_name

    def change_email(self, new_email: Email):
        self._email = new_email

    def change_password(self, new_password: Password):
        self._hashed_password = new_password.hashed_value

    def deactivate(self):
        self._is_active = False

    def activate(self):
        self._is_active = True

    @classmethod
    def create(cls, name: str, email: Email, hashed_password: str) -> "User":
        return cls(
            user_id=UserId(), name=name, email=email, hashed_password=hashed_password
        )
