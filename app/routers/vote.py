from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, utils
from sqlalchemy.orm import Session
from ..database import get_db
from . import oauth2

router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} doesn't exist")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already voted for this post")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created successfully"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully"}