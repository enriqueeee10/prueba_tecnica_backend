from app.shared.domain.value_objects import ValueObject
from app.shared.domain.exceptions import ValidationError


class Password(ValueObject):
    MIN_LENGTH = 8

    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValidationError(
                f"Password must be at least {self.MIN_LENGTH} characters long"
            )
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def _is_valid(self, password: str) -> bool:
        return len(password) >= self.MIN_LENGTH

    def __str__(self) -> str:
        return "*" * len(self._value)
