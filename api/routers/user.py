from ..utils import jwt, schemas
from fastapi import HTTPException, Response, status, APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.database import get_db
from uuid import UUID
from api.controllers.users import find_user_by_id, create_new_user, find_user_by_email

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exist = await find_user_by_email(db, user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already exists"
        )
    user.password = jwt.hash(user.password)
    new_user = await create_new_user(db, user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
async def get_post(id: UUID, response: Response, db: Session = Depends(get_db)):
    User = await find_user_by_id(db, id)
    if not User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} was not found"
        )
    return User
