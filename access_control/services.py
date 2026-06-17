from access_control.models import AccessRoleRule


PERMISSION_FIELDS = {
    "read": {
        "own": "read_permission",
        "all": "read_all_permission",
    },
    "create": {
        "own": "create_permission",
        "all": "create_permission",
    },
    "update": {
        "own": "update_permission",
        "all": "update_all_permission",
    },
    "delete": {
        "own": "delete_permission",
        "all": "delete_all_permission",
    },
}


def has_access(user, element_code: str, action: str, owner_id=None) -> bool:
    if not user or not getattr(user, "is_authenticated", False):
        return False

    if not user.is_active:
        return False

    if action not in PERMISSION_FIELDS:
        return False

    role_ids = user.user_roles.values_list("role_id", flat=True)

    rules = AccessRoleRule.objects.filter(
        role_id__in=role_ids,
        element__code=element_code,
    )

    permission_config = PERMISSION_FIELDS[action]
    own_permission = permission_config["own"]
    all_permission = permission_config["all"]

    if action == "create":
        return rules.filter(create_permission=True).exists()

    if rules.filter(**{all_permission: True}).exists():
        return True

    if owner_id is not None and owner_id == user.id:
        return rules.filter(**{own_permission: True}).exists()

    return False