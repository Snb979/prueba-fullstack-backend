from sqlalchemy.orm import Session

from src.modules.users.user_model import User


def get_all_users(db: Session):

    return db.query(User).all()


def get_user_by_id(id: int, db: Session):

    return db.query(User).filter(
        User.id == id
    ).first()