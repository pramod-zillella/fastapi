from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from . import oauth2
from typing import Optional
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])

# @router.get("/", response_model = List[schemas.Post])

@router.get("/")
def get_posts(db: Session = Depends(get_db), limit=10, skip=0, search: Optional[str] = ""):
    posts_with_votes = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    
    # Convert to dictionary format
    results = [
        {
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "user_id": post.owner_id,
                # Add other fields as necessary
            },
            "votes": votes
        }
        for post, votes in posts_with_votes
    ]
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{post_id}", response_model=schemas.Post)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own posts")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post_by_id(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    # print(post.owner_id)
    # print(current_user.id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own posts")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()