from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)

    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"


class Session(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    jti = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.email} - {self.jti}"

    class Meta:
        db_table = "sessions"