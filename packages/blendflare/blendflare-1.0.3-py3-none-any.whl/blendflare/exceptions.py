"""Exception classes for the Blendflare SDK."""

from typing import Any, Dict, List, Optional


class BlendflareError(Exception):
    """Base exception for all Blendflare SDK errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(BlendflareError):
    """Raised when authentication fails (401)."""
    
    def __init__(self, message: str = "Authentication failed. Check your API key.") -> None:
        super().__init__(message, status_code=401)


class AuthorizationError(BlendflareError):
    """Raised when authorization fails (403).
    
    This is raised for invalid or malformed API keys.
    """
    
    def __init__(self, message: str = "Access forbidden.") -> None:
        super().__init__(message, status_code=403)


class RateLimitError(BlendflareError):
    """Raised when rate limit is exceeded (403).
    
    Note: The API returns 403 for rate limiting, not 429.
    """
    
    def __init__(
        self, 
        message: str = "Rate limit exceeded. Please try again later.",
        retry_after: Optional[int] = None
    ) -> None:
        super().__init__(message, status_code=403)
        self.retry_after = retry_after


class NotFoundError(BlendflareError):
    """Raised when a resource is not found (404)."""
    
    def __init__(self, message: str = "Resource not found.") -> None:
        super().__init__(message, status_code=404)


class ValidationError(BlendflareError):
    """Raised when request validation fails (422).
    
    The details attribute contains a list of validation errors from the API.
    """
    
    def __init__(
        self, 
        message: str, 
        details: Optional[List[Dict[str, str]]] = None
    ) -> None:
        self.details = details or []
        super().__init__(message, status_code=422)
    
    def __str__(self) -> str:
        if self.details:
            details_str = "\n".join(
                f"  - {item.get('field', 'unknown')}: {item.get('message', '')}" 
                for item in self.details
            )
            return f"{self.message}\nValidation errors:\n{details_str}"
        return self.message


class BadRequestError(BlendflareError):
    """Raised when the request is malformed (400)."""
    
    def __init__(self, message: str = "Bad request.") -> None:
        super().__init__(message, status_code=400)


class ServerError(BlendflareError):
    """Raised when the server encounters an error (500)."""
    
    def __init__(self, message: str = "Internal server error.") -> None:
        super().__init__(message, status_code=500)


class APIError(BlendflareError):
    """Raised for general API errors."""
    
    pass


class ConnectionError(BlendflareError):
    """Raised when connection to the API fails."""
    
    def __init__(self, message: str = "Failed to connect to Blendflare API.") -> None:
        super().__init__(message)


class TimeoutError(BlendflareError):
    """Raised when a request times out."""
    
    def __init__(self, message: str = "Request timed out.") -> None:
        super().__init__(message)