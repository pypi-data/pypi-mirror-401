import pytest
from guardrails.permissions import check_permission
from guardrails.exceptions import PermissionError


# ✅ Allowed case
def test_permission_allowed():
    rules = {
        "approve": {"admin", "manager"}
    }
    check_permission("admin", "approve", rules)



#❌ Disallowed case
def test_permission_denied():
    rules = {
        "approve": {"admin", "manager"}
    }
    with pytest.raises(PermissionError):
        check_permission("user", "approve", rules)
