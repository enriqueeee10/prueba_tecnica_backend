from abc import ABC
from datetime import datetime
from typing import Dict, Any
import uuid


class DomainEvent(ABC):
    """Base class for Domain Events"""

    def __init__(self):
        self.event_id = str(uuid.uuid4())
        self.occurred_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.__class__.__name__,
            "occurred_at": self.occurred_at.isoformat(),
            "data": self._get_event_data(),
        }

    def _get_event_data(self) -> Dict[str, Any]:
        """Override this method to provide event-specific data"""
        return {}
