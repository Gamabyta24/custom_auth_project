import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from django.conf import settings
from django.utils import timezone as django_timezone

from accounts.models import Session, User


JWT_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")


def check_password(password: str, password_hash: str) -> bool:
    password_bytes = password.encode("utf-8")
    password_hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, password_hash_bytes)


def create_token_for_user(user: User) -> str:
    jti = str(uuid.uuid4())

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=settings.JWT_EXPIRE_HOURS)

    Session.objects.create(
        user=user,
        jti=jti,
        expires_at=expires_at,
    )

    payload = {
        "user_id": user.id,
        "jti": jti,
        "iat": now,
        "exp": expires_at,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return token


def deactivate_user_sessions(user: User) -> None:
    Session.objects.filter(user=user, is_active=True).update(
        is_active=False,
    )


def deactivate_session(session: Session) -> None:
    session.is_active = False
    session.save(update_fields=["is_active"])


def is_session_valid(session: Session) -> bool:
    return (
        session.is_active
        and session.expires_at > django_timezone.now()
    )