import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import Session, User
from accounts.services import JWT_ALGORITHM, is_session_valid


class CustomJWTAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != self.keyword:
            raise AuthenticationFailed("Invalid Authorization header")

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        user_id = payload.get("user_id")
        jti = payload.get("jti")

        if not user_id or not jti:
            raise AuthenticationFailed("Invalid token payload")

        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found or inactive")

        try:
            session = Session.objects.get(
                user=user,
                jti=jti,
            )
        except Session.DoesNotExist:
            raise AuthenticationFailed("Session not found")

        if not is_session_valid(session):
            raise AuthenticationFailed("Session is inactive or expired")

        return user, session

    def authenticate_header(self, request):
        return self.keyword