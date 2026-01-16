"""Runtime exception for the GeneratePDFs SDK."""


class RuntimeException(Exception):
    """Exception raised when a runtime error occurs."""

    def __init__(self, message: str) -> None:
        """Initialize the exception with a message.

        Args:
            message: The error message
        """
        super().__init__(message)
        self.message = message
