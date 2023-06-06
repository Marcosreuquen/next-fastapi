from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.utils import schemas
from ..utils import jwt
from ..models import database
from ..utils import oauth2
from api.controllers.users import find_user_by_email

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = await find_user_by_email(db, user_credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    verification = jwt.verify(user_credentials.password, user.password)

    if not verification:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
