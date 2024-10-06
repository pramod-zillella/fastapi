from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi.security import OAuth2PasswordBearer
from ..database import get_db   
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# we are going to provide the secret key to encode and decode the token
# then also include the algorithm to be used to encode the token
# provide the expiration time for the token 

def create_access_token(data: dict):
    to_encode = data.copy()
    # we are going to add the expiration time to the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    
    return token_data

# we can pass the function as a dependency into any one of our path operations, when we do that, what it's goign to do is it's going to take the token from the
# request automatically extract the ID for us, verfiy that the token is correct by calling the verify access token and then it's going to extract the ID 
# and then we want we can automatically fetch the user from the database and then add it into as a parameter into our path operations function 
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.email == token.id).first()
    return user
    # user = db.query(models.User).filter(models.User.email == token_data.id).first()
    # if user is None:
    #     raise credentials_exception
    # return user