from ..models import models
from ..utils import schemas
from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from ..models.database import get_db
from typing import Optional
from uuid import UUID
from sqlalchemy import func


async def get_posts(
    db: Session,
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )
    return results


async def get_post(db: Session, id: UUID):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    return post


async def create_post(db: Session, data: dict, user_id: UUID):
    new_post = models.Post(data)
    new_post.owner_id = user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


async def delete_post(db: Session, id: UUID, user: models.User):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} does not exist"
        )

    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update_post(
    db: Session,
    id: UUID,
    data: schemas.PostCreate,
    user_id: UUID,
):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} does not exist"
        )
    if post.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    query.update(data, synchronize_session=False)
    db.commit()
    return query.first()
