from rest_framework import serializers

from access_control.models import AccessRoleRule, BusinessElement, Role, UserRole


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            "id",
            "name",
            "description",
        )


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = (
            "id",
            "code",
            "name",
        )


class AccessRoleRuleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)
    element_code = serializers.CharField(source="element.code", read_only=True)

    class Meta:
        model = AccessRoleRule
        fields = (
            "id",
            "role",
            "role_name",
            "element",
            "element_code",
            "read_permission",
            "read_all_permission",
            "create_permission",
            "update_permission",
            "update_all_permission",
            "delete_permission",
            "delete_all_permission",
        )


class UserRoleSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = UserRole
        fields = (
            "id",
            "user",
            "user_email",
            "role",
            "role_name",
        )