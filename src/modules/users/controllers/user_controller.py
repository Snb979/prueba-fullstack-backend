from fastapi import HTTPException

from src.modules.users.services.user_service import (
    get_all_users,
    get_user_by_id
)


def get_users_controller(db):

    return get_all_users(db)


def get_user_controller(id, db):

    user = get_user_by_id(id, db)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user