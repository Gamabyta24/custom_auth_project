from django.core.management.base import BaseCommand

from access_control.models import Role, BusinessElement, AccessRoleRule


class Command(BaseCommand):
    help = "Seed roles, business elements and access rules"

    def handle(self, *args, **options):
        admin_role, _ = Role.objects.get_or_create(
            name="admin",
            defaults={"description": "System administrator"},
        )
        manager_role, _ = Role.objects.get_or_create(
            name="manager",
            defaults={"description": "Manager"},
        )
        user_role, _ = Role.objects.get_or_create(
            name="user",
            defaults={"description": "Regular user"},
        )

        elements_data = [
            ("users", "Users"),
            ("orders", "Orders"),
            ("products", "Products"),
            ("access_rules", "Access rules"),
        ]

        elements = {}

        for code, name in elements_data:
            element, _ = BusinessElement.objects.get_or_create(
                code=code,
                defaults={"name": name},
            )
            elements[code] = element

        for element in elements.values():
            AccessRoleRule.objects.update_or_create(
                role=admin_role,
                element=element,
                defaults={
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": True,
                    "delete_permission": True,
                    "delete_all_permission": True,
                },
            )

        AccessRoleRule.objects.update_or_create(
            role=manager_role,
            element=elements["orders"],
            defaults={
                "read_permission": True,
                "read_all_permission": True,
                "create_permission": True,
                "update_permission": True,
                "update_all_permission": True,
                "delete_permission": False,
                "delete_all_permission": False,
            },
        )

        AccessRoleRule.objects.update_or_create(
            role=user_role,
            element=elements["orders"],
            defaults={
                "read_permission": True,
                "read_all_permission": False,
                "create_permission": True,
                "update_permission": True,
                "update_all_permission": False,
                "delete_permission": True,
                "delete_all_permission": False,
            },
        )

        AccessRoleRule.objects.update_or_create(
            role=admin_role,
            element=elements["access_rules"],
            defaults={
                "read_permission": True,
                "read_all_permission": True,
                "create_permission": True,
                "update_permission": True,
                "update_all_permission": True,
                "delete_permission": True,
                "delete_all_permission": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS("Access control seed data created successfully")
        )