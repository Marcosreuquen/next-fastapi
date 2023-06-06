from sqlalchemy.orm import Session
from ..models import models
from pydantic import EmailStr
from uuid import UUID


async def find_user_by_email(db: Session, email: EmailStr):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


async def find_user_by_id(db: Session, id: UUID):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


async def create_new_user(db: Session, user: models.User):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
