"""Custom exceptions for the GeneratePDFs SDK."""

from generatepdfs.exceptions.invalid_argument_exception import InvalidArgumentException
from generatepdfs.exceptions.runtime_exception import RuntimeException

__all__ = [
    'InvalidArgumentException',
    'RuntimeException',
]
