class OrmError(Exception): ...


class NotFoundError(OrmError):
    """Raised when a requested object does not exist (404)."""

    pass


class InvalidQueryError(OrmError):
    """Raised when a request returns multiple results when only one was expected."""

    pass


class AuthenticationError(OrmError):
    """Raised when authentication fails (401)."""

    pass


class PermissionDeniedError(OrmError):
    """Raised when access to a resource is forbidden (403)."""

    pass


class RateLimitExceededError(OrmError):
    """Raised when HubSpot rate limits the client (429)."""

    def __init__(self, message: str = "", retry_after: int | None = None):
        self.retry_after = retry_after
        super().__init__(message)


class BackendError(OrmError):
    """Raised for 5xx errors returned by HubSpot."""

    pass
