from guardrails.exceptions import ValidationError, PermissionError


def test_validation_error_is_exception():
    assert issubclass(ValidationError, Exception)


def test_permission_error_is_exception():
    assert issubclass(PermissionError, Exception)
