from django.core.management.base import BaseCommand

from accounts.models import User
from accounts.services import hash_password
from access_control.models import Role, UserRole


class Command(BaseCommand):
    help = "Seed demo users"

    def handle(self, *args, **options):
        users_data = [
            {
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "middle_name": "",
                "password": "admin12345",
                "role": "admin",
            },
            {
                "email": "manager@example.com",
                "first_name": "Manager",
                "last_name": "User",
                "middle_name": "",
                "password": "manager12345",
                "role": "manager",
            },
            {
                "email": "user@example.com",
                "first_name": "Regular",
                "last_name": "User",
                "middle_name": "",
                "password": "user12345",
                "role": "user",
            },
        ]

        for user_data in users_data:
            role_name = user_data.pop("role")
            password = user_data.pop("password")

            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    **user_data,
                    "password_hash": hash_password(password),
                    "is_active": True,
                },
            )

            if not created and not user.is_active:
                user.is_active = True
                user.password_hash = hash_password(password)
                user.save(update_fields=["is_active", "password_hash"])

            role = Role.objects.get(name=role_name)

            UserRole.objects.get_or_create(
                user=user,
                role=role,
            )

        self.stdout.write(
            self.style.SUCCESS("Demo users created successfully")
        )