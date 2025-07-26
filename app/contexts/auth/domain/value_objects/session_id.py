from app.shared.domain.value_objects import ValueObject
import uuid


class SessionId(ValueObject):
    def __init__(self, value: str = None):
        if value is None:
            value = str(uuid.uuid4())
        self._value = value

    @property
    def value(self) -> str:
        return self._value
