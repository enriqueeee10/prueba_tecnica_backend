from app.shared.domain.value_objects import ValueObject
from app.shared.domain.exceptions import ValidationError


class Token(ValueObject):
    def __init__(self, value: str):
        if not value or len(value) < 10:
            raise ValidationError("Invalid token")
        self._value = value

    @property
    def value(self) -> str:
        return self._value
