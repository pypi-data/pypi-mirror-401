"""AegisLog SDK Exceptions."""


class AegisLogError(Exception):
    """Base exception for AegisLog SDK."""
    pass


class AegisLogAPIError(AegisLogError):
    """API request failed."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AegisLogValidationError(AegisLogError):
    """Invalid input data."""
    pass
