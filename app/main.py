from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, notification, questions, auth, like
from app.database import engine, SessionLocal

#  Description of Dev ASk Api

description = """

Dev Ask Api does the following functions

## Auth

The user can  **sign in** to Dev Ask
The user can **sign out** of Dev Ask
The user is able to **Change Password**

## Users , Questions , Answer

You will be able to perform CRUD Operations on Every Function:

* **GET** 
* **POST ** 
* **Update ** 
* **DELETE ** 
and other operations like :-
* **PATCH** 

"""

app = FastAPI(
    title="DEV ASK",
    description=description,
)


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
app.include_router(like.router)


@app.get("/")
async def root():
    return {"message": "Hello world"}
