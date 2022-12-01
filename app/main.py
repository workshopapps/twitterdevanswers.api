from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from routers import user, notification, questions, auth, like, answer, following, tag,blog


#  Description of Dev ASk Api

description = """

Dev Ask Api does the following functions

## Auth
This endpoint will handle all authorization requests including sign up, sign in, change password etc.

## Users 
These endpoint perform CRUD operations involving the user 

## Questions 
These endpoint perform CRUD operations involving the questions asked by the user 

## Answer
These endpoint perform CRUD operations involving the answer to the questions asked by the user 

## Follow
These endpoint perform CRUD operations involving following a user

Other Endpoints are implemented below 
 
## HTTP Methods
The following methods are used in this api :- 

* **GET** 
* **POST** 
* **UPDATE** 
* **DELETE** 
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
app.include_router(answer.router)
app.include_router(following.router)
app.include_router(tag.router)
app.include_router(blog.router)



app.get("/")


async def root():
    return {"message": "Hello world"}
