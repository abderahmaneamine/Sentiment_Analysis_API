import uvicorn
from fastapi import FastAPI,APIRouter
from Extensions import Base, engine  # Ensure this import matches the file and class names
from routes import router
app = FastAPI()
app.include_router(router)


# Create database tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)


