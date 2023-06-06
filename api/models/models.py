from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship
import uuid


class Post(Base):
    __tablename__ = "posts"

    id = Column(
        String, primary_key=True, default=str(uuid.uuid4()), unique=True, index=True
    )
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(
        String, primary_key=True, default=str(uuid.uuid4()), unique=True, index=True
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    post_id = Column(
        String,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
