"""Custom exceptions for Gibberifire."""


class GibberifireError(Exception):
    """Base exception for Gibberifire errors."""


class InvalidMethodError(GibberifireError):
    """Raised when an invalid protection method is specified."""


class InvalidLevelError(GibberifireError):
    """Raised when an invalid protection level is specified."""


class FileOperationError(GibberifireError):
    """Raised when a file operation fails."""


class ConfigurationError(GibberifireError):
    """Raised when there is an error in configuration."""
