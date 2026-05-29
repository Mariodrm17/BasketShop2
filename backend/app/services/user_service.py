from sqlalchemy.orm import Session
from app.repositories.user_repository import user_repository
from app.services.auth_service import hash_password
from app.schemas.user import UserCreate, UserUpdate
from app.exceptions import NotFoundError, ConflictError


def get_users(db: Session) -> list[dict]:
    users = user_repository.get_all(db)
    return [{"_id": str(u.id), "username": u.username, "role": u.role} for u in users]


def create_user(db: Session, data: UserCreate) -> dict:
    if user_repository.get_by_username(db, data.username):
        raise ConflictError("El nombre de usuario ya existe")
    user = user_repository.create(
        db,
        username=data.username,
        hashed_password=hash_password(data.password),
        role=data.role or "user",
    )
    return {"message": "Usuario creado con éxito", "user": {"username": user.username, "role": user.role}}


def update_user(db: Session, user_id: str, data: UserUpdate) -> dict:
    try:
        uid = int(user_id)
    except ValueError:
        raise NotFoundError("ID de usuario inválido")

    user = user_repository.get_by_id(db, uid)
    if not user:
        raise NotFoundError("Usuario no encontrado")

    update_data: dict = {}
    if data.username is not None:
        existing = user_repository.get_by_username(db, data.username)
        if existing and existing.id != user.id:
            raise ConflictError("El nombre de usuario ya existe")
        update_data["username"] = data.username
    if data.password is not None:
        update_data["password"] = hash_password(data.password)
    if data.role is not None:
        update_data["role"] = data.role

    if update_data:
        user = user_repository.update(db, user, update_data)

    return {"_id": str(user.id), "username": user.username, "role": user.role}


def delete_user(db: Session, user_id: str) -> None:
    try:
        uid = int(user_id)
    except ValueError:
        raise NotFoundError("ID de usuario inválido")

    user = user_repository.get_by_id(db, uid)
    if not user:
        raise NotFoundError("Usuario no encontrado")
    user_repository.delete(db, user)
