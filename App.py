import uvicorn
import transformers 
from transformers import pipeline
from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
