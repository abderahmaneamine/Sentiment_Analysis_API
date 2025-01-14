from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User, Sentiment, generate
from Schemas import UserCreate, Token, SentimentRequest, SentimentResponse, User as UserSchema
from auth import get_password_hash, create_access_token, verify_password
from dependencies import get_current_user, get_db
import logging
from Crud import create_sentiment,update_sentiment,delete_sentiment
router = APIRouter()
@router.get("/")
def read_root():
    
    return {"message": "Welcome to the Sentiment analysis API"}

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        logging.error("Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logging.info(f"Creating user: {user.username}")
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            logging.error(f"User {user.username} already registered")
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logging.info(f"User {user.username} created successfully")
        return db_user
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.get("/sentiments/", response_model=SentimentResponse, dependencies=[Depends(get_current_user)])
def read_sentiments(data: str, db: Session = Depends(get_db)):
    sentiment = generate(data)[0]
    return {
        "sentiment": sentiment['label'],
        "sentiment_probability": sentiment['score']
    }

@router.post("/sentiments/", response_model=SentimentResponse, dependencies=[Depends(get_current_user)])
def create_sentiment_route(data: SentimentRequest, db: Session = Depends(get_db)):
    db_sentiment = create_sentiment(db, data)
    return {
        "sentiment": db_sentiment.sentiment,
        "sentiment_probability": db_sentiment.sentiment_probability
    }

@router.put("/sentiments/", response_model=SentimentResponse, dependencies=[Depends(get_current_user)])
def update_sentiment_route(data: str, new_data: str, db: Session = Depends(get_db)):
    db_sentiment = update_sentiment(db, data, new_data)
    if not db_sentiment:
        raise HTTPException(status_code=404, detail="Sentence entry not found")
    return {
        "sentiment": db_sentiment.sentiment,
        "sentiment_probability": db_sentiment.sentiment_probability
    }

@router.delete("/sentiments/", dependencies=[Depends(get_current_user)])
def delete_sentiment_route(data: str, db: Session = Depends(get_db)):
    success = delete_sentiment(db, data)
    if not success:
        raise HTTPException(status_code=404, detail="Sentiment analysis entry not found")
    return {"message": "Sentiment analysis entry deleted successfully"}
