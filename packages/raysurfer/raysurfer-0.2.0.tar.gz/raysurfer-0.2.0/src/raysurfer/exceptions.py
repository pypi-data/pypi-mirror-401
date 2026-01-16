"""RaySurfer SDK exceptions"""


class RaySurferError(Exception):
    """Base exception for RaySurfer SDK"""

    pass


class APIError(RaySurferError):
    """API returned an error response"""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(RaySurferError):
    """Authentication failed"""

    pass
