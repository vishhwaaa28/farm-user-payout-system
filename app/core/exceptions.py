class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResourceNotFoundException(AppException):
    """Raised when a requested resource does not exist."""
    pass


class ValidationException(AppException):
    """Raised for invalid business operations."""
    pass


class InsufficientBalanceException(ValidationException):
    """Raised when user attempts to withdraw more than available."""
    pass


class SaleAlreadyReconciledException(ValidationException):
    """Raised when a sale has already been reconciled."""
    pass

class DuplicateAdvancePayoutException(AppException):
    """Raised when an advance payout already exists for a sale."""

    def __init__(self, message: str = "Advance payout already exists for this sale."):
        super().__init__(message, status_code=400)