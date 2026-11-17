class S3CopyException(Exception):
    """Base exception."""


class InvalidConfigurationException(S3CopyException):
    """Invalid request configuration."""


class ObjectNotFoundException(S3CopyException):
    """No objects found."""


class CopyFailedException(S3CopyException):
    """Copy operation failed."""