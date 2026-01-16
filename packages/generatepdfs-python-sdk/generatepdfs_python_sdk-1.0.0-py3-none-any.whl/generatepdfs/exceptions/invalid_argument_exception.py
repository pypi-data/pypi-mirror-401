"""Invalid argument exception for the GeneratePDFs SDK."""


class InvalidArgumentException(Exception):
    """Exception raised when an invalid argument is provided."""

    def __init__(self, message: str) -> None:
        """Initialize the exception with a message.

        Args:
            message: The error message
        """
        super().__init__(message)
        self.message = message
