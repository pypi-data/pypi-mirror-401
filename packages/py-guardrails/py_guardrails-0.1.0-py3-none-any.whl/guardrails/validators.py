from .exceptions import ValidationError


def require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")


def require_positive(value: int, field_name: str) -> None:
    if value <= 0:
        raise ValidationError(f"{field_name} must be positive")
