class HsClientError(Exception): ...


class ObjectNotFoundError(HsClientError):
    """Raised when a requested object does not exist (404)."""

    pass


class NonUniqueObjectError(HsClientError):
    """Raised when a request returns multiple results when only one was expected."""

    pass


class InvalidRequestError(HsClientError):
    """Raised when the request is malformed or contains invalid fields (400)."""

    pass


class AuthenticationError(HsClientError):
    """Raised when authentication fails (401)."""

    pass


class PermissionDeniedError(HsClientError):
    """Raised when access to a resource is forbidden (403)."""

    pass


class RateLimitExceededError(HsClientError):
    """Raised when HubSpot rate limits the client (429)."""

    def __init__(self, message: str = "", retry_after: int | None = None):
        self.retry_after = retry_after
        super().__init__(message)


class ServerError(HsClientError):
    """Raised for 5xx errors returned by HubSpot."""

    pass
