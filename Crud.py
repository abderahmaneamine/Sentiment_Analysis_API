from sqlalchemy.orm import Session
from models import Sentiment, SentimentRequest, SentimentResponse, generate

def create_sentiment(db: Session, sentiment_request: SentimentRequest):
    sentiment = generate(sentiment_request.text)[0]
    db_sentiment = Sentiment(
        text=sentiment_request.text,
        sentiment=sentiment['label'],
        sentiment_probability=sentiment['score']
    )
    db.add(db_sentiment)
    db.commit()
    db.refresh(db_sentiment)
    return db_sentiment

def get_sentiment(db: Session, text: str):
    return db.query(Sentiment).filter(Sentiment.text == text).first()

def update_sentiment(db: Session, text: str, new_text: str):
    db_sentiment = get_sentiment(db, text)
    if db_sentiment:
        new_sentiment = generate(new_text)[0]
        db_sentiment.text = new_text
        db_sentiment.sentiment = new_sentiment['label']
        db_sentiment.sentiment_probability = new_sentiment['score']
        db.commit()
        db.refresh(db_sentiment)
        return db_sentiment
    return None

def delete_sentiment(db: Session, text: str):
    db_sentiment = get_sentiment(db, text)
    if db_sentiment:
        db.delete(db_sentiment)
        db.commit()
        return True
    return False
