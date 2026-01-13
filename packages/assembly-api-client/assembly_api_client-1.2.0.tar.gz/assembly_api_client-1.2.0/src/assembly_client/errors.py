class AssemblyAPIError(Exception):
    """
    Base exception for all Assembly API Client errors.

    All exceptions raised by this library inherit from this class.
    """

    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        self.message = message


class SpecParseError(AssemblyAPIError):
    """
    Raised when parsing the API specification fails.

    This can happen if the Excel file format changes or contains unexpected data.
    """

    def __init__(self, message: str, original_error: Exception | None = None):
        super().__init__(message)
        self.original_error = original_error


class APIRequestError(AssemblyAPIError):
    """
    Raised when an API request fails or returns an error code.

    Attributes:
        code (str): The error code returned by the API (e.g., 'INFO-200', 'ERROR-500').
        message (str): The error message description.
    """

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")
