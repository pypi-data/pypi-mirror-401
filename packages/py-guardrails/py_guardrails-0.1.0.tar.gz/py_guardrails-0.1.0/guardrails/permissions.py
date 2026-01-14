from .exceptions import PermissionError


def check_permission(role: str, action: str, rules: dict[str, set[str]]) -> None:
    allowed_roles = rules.get(action, set())
    if role not in allowed_roles:
        raise PermissionError(
            f"Role '{role}' not allowed to perform action '{action}'"
        )
