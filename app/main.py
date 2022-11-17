from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware


import app.models
#from app.routers import users, auth, question
from app.database import engine, SessionLocal
app = FastAPI()


#models.Base.metadata.create_all(bind=engine)
origins = []

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"], 
    allow_headers = ["*"]

)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()