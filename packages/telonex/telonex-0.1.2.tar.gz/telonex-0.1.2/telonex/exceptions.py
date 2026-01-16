"""Custom exceptions for the Telonex SDK."""


class TelonexError(Exception):
    """Base exception for all Telonex SDK errors."""

    pass


class AuthenticationError(TelonexError):
    """Raised when API key is invalid or missing."""

    pass


class NotFoundError(TelonexError):
    """Raised when requested data is not found."""

    def __init__(self, message: str, exchange: str = "", channel: str = "", date: str = ""):
        super().__init__(message)
        self.exchange = exchange
        self.channel = channel
        self.date = date


class RateLimitError(TelonexError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: int = 0):
        super().__init__(message)
        self.retry_after = retry_after


class ValidationError(TelonexError):
    """Raised when input parameters are invalid."""

    pass


class DownloadError(TelonexError):
    """Raised when a download fails."""

    def __init__(self, message: str, url: str = "", status_code: int = 0):
        super().__init__(message)
        self.url = url
        self.status_code = status_code


class EntitlementError(TelonexError):
    """Raised when user doesn't have access to requested data."""

    def __init__(self, message: str, downloads_remaining: int = 0):
        super().__init__(message)
        self.downloads_remaining = downloads_remaining
