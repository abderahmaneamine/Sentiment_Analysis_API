from fastapi import APIRouter, HTTPException 
from models import  SentimentRequest,Generate
from Extensions import app
router = APIRouter()
@router.get('/')
def get_root():
  return {'message': 'Welcome to Sentiment Analysis API'}
@router.get("/api/v1/sentiment")
def SentimentAnalyzer(data: str):
  sentiment = Generate(data)[0]
  return {sentiment[0]['label'],
  sentiment[1]['score']}          
@router.post("/api/v2/postsentiment")
def SentimentAnalyzerPost(data: str):
  sentiment = Generate(data)
  return{ sentiment[0]['label'],
         sentiment[1]['score']}
         
@router.put("/api/v1/update-sentiment") 
def update_sentiment(data: str, new_data: str): 
  if data not in sentiments: 
    raise HTTPException(status_code=404, detail="Sentiment analysis entry not found") 
    new_sentiment = nlp(new_data)
    sentiments[data] = new_sentiment[0] 
    return new_sentiment[0]
@router.delete("/api/v1/delete-sentiment") 
def delete_sentiment(data: str): 
  if data not in sentiments: 
    raise HTTPException(status_code=404, detail="Sentiment analysis entry not found")
    del sentiments[data] 
    return {"message": "Sentiment analysis entry deleted successfully"}