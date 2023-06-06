from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: UUID
    created_at: datetime
    owner_id: UUID
    owner: UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: Optional[int]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[UUID]
    expiration_date: Optional[datetime]


class Vote(BaseModel):
    post_id: UUID
    dir: conint(le=1)
