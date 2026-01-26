class AppError(Exception):
    """Base class for application-specific errors."""
    pass

class DomainError(AppError):
    """Business rule violation or unsupported domain operation."""
    pass

class TelegramBotTokenError(AppError):
    """Raised when there is an issue with the Telegram bot token."""
    pass

class ValidationError(AppError):
    """User input is invalid."""
    pass

class FoodParsingError(ValidationError):
    """Food input could not be parsed."""
    pass

class FoodNotFoundError(DomainError):
    """Food item not found in the database."""
    pass

class UnitConversionError(DomainError):
    """Error in converting food units."""
    pass