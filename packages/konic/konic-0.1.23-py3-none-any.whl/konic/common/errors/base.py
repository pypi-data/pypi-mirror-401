"""Base error classes for Konic."""

__all__ = ["KonicError", "KonicRuntimeError"]


class KonicError(Exception):
    """Base exception for all Konic-specific errors."""

    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        self.message = message


class KonicAssertionError(AssertionError):
    """Konic-specific assertion failure."""

    pass


class KonicRuntimeError(KonicError):
    """Runtime error during execution."""

    def __init__(self, message: str, operation: str | None = None):
        super().__init__(message)
        self.operation = operation
