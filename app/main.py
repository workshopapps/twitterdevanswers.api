from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware


import model
from app.routers import user, notification, questions
from database import engine, SessionLocal
app = FastAPI()


model.Base.metadata.create_all(bind=engine)
origins = []

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"], 
    allow_headers = ["*"]

)
app.include_router(user.router)

