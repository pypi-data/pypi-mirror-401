"""Exceptions for MCE CLI."""


class MCEError(Exception):
    """Base exception for MCE CLI."""
    pass


class MCEClientError(MCEError):
    """Client-side error."""
    pass


class MCEServerError(MCEError):
    """Server-side error."""
    
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


class MCEConfigError(MCEError):
    """Configuration error."""
    pass