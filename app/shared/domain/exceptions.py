class DomainException(Exception):
    """Base exception for domain errors"""

    pass


class ValidationError(DomainException):
    """Raised when domain validation fails"""

    pass


class NotFoundError(DomainException):
    """Raised when an entity is not found"""

    pass


class DuplicateError(DomainException):
    """Raised when trying to create a duplicate entity"""

    pass
