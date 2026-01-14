import pytest
from guardrails.validators import require_non_empty, require_positive
from guardrails.exceptions import ValidationError

#✅ Valid cases
def test_require_non_empty_valid():
    require_non_empty("hello", "name")


def test_require_positive_valid():
    require_positive(10, "age")


# ❌ Invalid cases
def test_require_non_empty_raises_error():
    with pytest.raises(ValidationError):
        require_non_empty("", "name")


def test_require_positive_raises_error():
    with pytest.raises(ValidationError):
        require_positive(0, "age")
