from ..utils import oauth2
from ..models import models
from fastapi import Depends, HTTPException, Response, status, APIRouter
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from ..utils import schemas
from ..controllers import posts
from ..models import database

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
    db: Session = Depends(database.get_db),
):
    results = await posts.get_posts(db, limit, offset, search)
    return results


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(
    id: UUID,
    response: Response,
    db: Session = Depends(database.get_db),
):
    post = await posts.get_post(db, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found"
        )
    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
async def create_post(
    post: schemas.PostCreate,
    user: models.User = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    new_post: models.Post = await posts.create_post(
        db, **{"data": post.dict(), "user_id": user.id}
    )
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: UUID,
    user: models.User = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    return await posts.delete_post(db, id, user)


@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: UUID,
    data: schemas.PostCreate,
    user: models.User = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    updated_post = posts.update_post(db, id, data.dict(), user.id)
    return updated_post
