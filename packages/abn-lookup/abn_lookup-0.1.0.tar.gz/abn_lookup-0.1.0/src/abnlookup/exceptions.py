"""
Custom exceptions for the ABN Lookup wrapper.
"""

class ABNLookupError(Exception):
    """Base exception for ABN Lookup errors."""
    pass

class APIConnectionError(ABNLookupError):
    """Raised when the client cannot connect to the API."""
    pass

class InvalidABNError(ABNLookupError):
    """Raised when the provided ABN is invalid."""
    pass

class ABNNotFoundError(ABNLookupError):
    """Raised when the ABN is valid but not found in the register."""
    pass

class APIExceptionError(ABNLookupError):
    """Raised when the API returns an explicit exception message."""
    pass