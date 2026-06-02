from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import get_users, create_user, update_user, delete_user
from app.dependencies.auth import get_current_admin, get_current_user
from app.exceptions import NotFoundError, ConflictError

router = APIRouter()


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"_id": str(current_user.id), "username": current_user.username, "role": current_user.role}


@router.get("/users")
def list_users(
    current_user=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return get_users(db)


@router.post("/users", status_code=201)
def create_user_endpoint(
    data: UserCreate,
    current_user=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    try:
        return create_user(db, data)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.put("/users/{user_id}")
def update_user_endpoint(
    user_id: str,
    data: UserUpdate,
    current_user=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    try:
        return update_user(db, user_id, data)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.delete("/users/{user_id}")
def delete_user_endpoint(
    user_id: str,
    current_user=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    try:
        delete_user(db, user_id)
        return {"message": "Usuario eliminado"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
