from app.shared.domain.value_objects import ValueObject
from app.shared.domain.exceptions import ValidationError
import re


class Email(ValueObject):
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValidationError(f"Invalid email format: {value}")
        self._value = value.lower()

    @property
    def value(self) -> str:
        return self._value

    def _is_valid(self, email: str) -> bool:
        return bool(re.match(self.EMAIL_REGEX, email))

    def __str__(self) -> str:
        return self._value
