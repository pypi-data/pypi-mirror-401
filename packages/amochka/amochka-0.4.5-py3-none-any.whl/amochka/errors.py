"""
Кастомные исключения для библиотеки amochka.
"""


class AmoCRMError(Exception):
    """Базовое исключение для всех ошибок amoCRM API."""
    pass


class AuthenticationError(AmoCRMError):
    """Исключение при ошибках авторизации и работы с токенами."""
    pass


class RateLimitError(AmoCRMError):
    """Исключение при превышении лимита запросов (429 Too Many Requests)."""

    def __init__(self, message="Rate limit exceeded", retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


class NotFoundError(AmoCRMError):
    """Исключение при отсутствии запрашиваемого ресурса (404 Not Found)."""
    pass


class APIError(AmoCRMError):
    """Общее исключение для ошибок API."""

    def __init__(self, status_code, message):
        self.status_code = status_code
        super().__init__(f"API error {status_code}: {message}")


class ValidationError(AmoCRMError):
    """Исключение при некорректных входных данных."""
    pass


__all__ = [
    "AmoCRMError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "APIError",
    "ValidationError",
]
