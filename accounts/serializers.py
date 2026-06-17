from rest_framework import serializers

from accounts.models import User
from accounts.services import check_password, hash_password
from access_control.models import Role, UserRole


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    middle_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
    )
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists"
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError(
                {"password_repeat": "Passwords do not match"}
            )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_repeat")

        user = User.objects.create(
            **validated_data,
            password_hash=hash_password(password),
        )

        user_role, _ = Role.objects.get_or_create(
            name="user",
            defaults={"description": "Regular user"},
        )

        UserRole.objects.get_or_create(
            user=user,
            role=user_role,
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid email or password"
            )

        if not check_password(password, user.password_hash):
            raise serializers.ValidationError(
                "Invalid email or password"
            )

        attrs["user"] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "email",
            "is_active",
            "created_at",
            "updated_at",
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "middle_name",
        )