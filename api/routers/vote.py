from ..utils import oauth2
from ..models import database, models
from ..utils import schemas
from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from ..controllers import votes

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    response = votes.make_vote(db, vote.post_id, current_user.id)
    return response
