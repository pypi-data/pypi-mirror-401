"""
Usefy SDK Exceptions
"""


class UsefyError(Exception):
    """Base exception for all Usefy errors."""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class UsefyAuthError(UsefyError):
    """Raised when API key is invalid or missing."""
    pass


class UsefyBudgetExceeded(UsefyError):
    """Raised when budget limit is exceeded."""
    def __init__(self, message: str, budget_info: dict = None):
        super().__init__(message, status_code=429)
        self.budget_info = budget_info or {}


class UsefyRateLimited(UsefyError):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str, retry_after: int = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class UsefyProviderError(UsefyError):
    """Raised when the AI provider returns an error."""
    def __init__(self, message: str, provider: str, status_code: int = None):
        super().__init__(message, status_code=status_code)
        self.provider = provider


class UsefyTimeoutError(UsefyError):
    """Raised when request times out."""
    pass
