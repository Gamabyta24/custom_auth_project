from rest_framework.permissions import BasePermission

from access_control.services import has_access


class AccessRulesPermission(BasePermission):
    def has_permission(self, request, view):
        action = self.get_action(request.method)

        if action is None:
            return False

        return has_access(
            user=request.user,
            element_code="access_rules",
            action=action,
        )

    def get_action(self, method):
        if method == "GET":
            return "read"
        if method == "POST":
            return "create"
        if method in ("PUT", "PATCH"):
            return "update"
        if method == "DELETE":
            return "delete"

        return None