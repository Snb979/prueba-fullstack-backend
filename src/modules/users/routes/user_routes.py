from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.modules.auth.current_user import get_current_user
from src.modules.users.login_schema import LoginSchema
from src.config.dependencies import get_db
from src.modules.users.login_response import LoginResponse
from src.modules.auth.auth_handler import (
    verify_password,
    create_access_token,
    hash_password
)

from src.modules.auth.auth_bearer import JWTBearer

from src.modules.users.user_model import User

from src.modules.users.schema import (
    UserCreate,
    UserResponse
)

from src.modules.auth.role_verifier import RoleChecker

from src.modules.users.controllers.user_controller import (
    get_users_controller,
    get_user_controller
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponse],
    dependencies=[
        Depends(JWTBearer()),
        Depends(RoleChecker(["admin"]))
    ]
)
def get_users(
    db: Session = Depends(get_db)
):

    return get_users_controller(db)

@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(JWTBearer())]
)
def get_me(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == current_user["id"]
    ).first()

    return user

@router.get(
    "/{id}",
    response_model=UserResponse,
    dependencies=[
        Depends(JWTBearer()),
        Depends(RoleChecker(["admin"]))
    ]
)
def get_user(
    id: int,
    db: Session = Depends(get_db)
):

    return get_user_controller(id, db)

    user = db.query(User).filter(
        User.id == id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


@router.post(
    "/",
    response_model=UserResponse
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put(
    "/{id}",
    response_model=UserResponse,
    dependencies=[
        Depends(JWTBearer()),
        Depends(RoleChecker(["admin"]))
    ]
)
def update_user(
    id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):

    user_db = db.query(User).filter(
        User.id == id
    ).first()

    if not user_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    existing_user = db.query(User).filter(
        User.email == user.email,
        User.id != id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = hash_password(user.password)
    user_db.role = user.role

    db.commit()
    db.refresh(user_db)

    return user_db


@router.delete(
    "/{id}",
    dependencies=[
        Depends(JWTBearer()),
        Depends(RoleChecker(["admin"]))
    ]
)
def delete_user(
    id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "Usuario eliminado"
    }


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):

    user_db = db.query(User).filter(
        User.email == user.email
    ).first()

    if not user_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if not verify_password(
        user.password,
        user_db.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )

    token = create_access_token(
        data={
            "id": user_db.id,
            "email": user_db.email,
            "role": user_db.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_db.id,
            "username": user_db.username,
            "email": user_db.email,
            "role": user_db.role
        }
    }
    
