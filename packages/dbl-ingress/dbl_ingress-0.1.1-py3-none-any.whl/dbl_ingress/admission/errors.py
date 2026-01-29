class AdmissionError(Exception):
    """Base exception for all admission-related errors."""

    def __init__(self, message: str, *, reason_code: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


class InvalidInputError(AdmissionError):
    """Raised when input data fails validation."""

    def __init__(self, message: str, *, reason_code: str) -> None:
        super().__init__(message, reason_code=reason_code)
