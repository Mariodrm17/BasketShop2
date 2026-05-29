from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt
from sqlalchemy.orm import Session

from app.config import settings
from app.repositories.user_repository import user_repository
from app.exceptions import UnauthorizedError, ConflictError


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expire
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise UnauthorizedError("Token inválido o expirado")


def login(db: Session, username: str, password: str) -> str:
    user = user_repository.get_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise UnauthorizedError("Credenciales inválidas")
    return create_access_token({"id": str(user.id), "username": user.username, "role": user.role})


def register(db: Session, username: str, password: str) -> None:
    if user_repository.get_by_username(db, username):
        raise ConflictError("El nombre de usuario ya existe")
    user_repository.create(db, username=username, hashed_password=hash_password(password), role="user")
