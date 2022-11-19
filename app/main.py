from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware


from app.routers import user, notification, questions, auth
from app.database import engine, SessionLocal


app = FastAPI()


# model.Base.metadata.create_all(bind=engine)
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

app.include_router(user.router)
app.include_router(questions.router)
app.include_router(notification.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello world"}
