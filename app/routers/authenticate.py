from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils
from . import oauth2
# we are going to make a small change when it comes to retrieving the user credentials in our login route, 
# instead of passing it in the body, we are going to use a built in utility in fastAPI

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/authenticate", tags=["Authenticate"])

@router.post("/", response_model=schemas.Token)
async def authenticate(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # generate the access token
    access_token = oauth2.create_access_token(data={"user_id": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


