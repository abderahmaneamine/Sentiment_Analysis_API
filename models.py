from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from utils import generate
from Extensions import Base


from sqlalchemy import Column, Integer, String
from Extensions import Base
#SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Sentiment(Base):
    __tablename__ = "sentiments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    sentiment = Column(String)
    sentiment_probability = Column(Float)

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    sentiment_probability: float



