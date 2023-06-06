from uuid import UUID
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..models import database, models
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expiration_date": str(expire)})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        id: UUID = payload.get("user_id")

        if id is None:
            raise credentials_exceptions
        token_data: UUID = schemas.TokenData(id=id).id
    except JWTError:
        raise credentials_exceptions
    return token_data


def get_current_user(
    token: UUID = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    id = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == id).first()

    return user
