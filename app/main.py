from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
#import sys
# sys.path.append('..')
# from app.routers import googleauth

from app.routers import user, notification, questions, auth, like, answer, following, tag, blog, wallet, admin

import sentry_sdk

##DO NOT COMMENT OUT SENTRY PACKAGE, IF YOUR CODE DOESNT WORK, pip install --upgrade 'sentry-sdk[fastapi]' WOULD INSTALL NECESSARY PACKAGES.

# Integration of Sentry Monitoring

sentry_sdk.init(
    dsn="https://45476b789dc3420faec99388d0e830c3@o4504279440097280.ingest.sentry.io/4504279970676736",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)



#  Description of Dev ASk Api
description = """

Dev Ask Api does the following functions

## Auth
This endpoint will handle all authorization and authentication requests including sign up, sign in, change password, Forgot Password,  etc.

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

origins = ['*', 'http://localhost:3000/']

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
app.include_router(admin.router)
# app.include_router(googleauth.router)
app.include_router(wallet.router)


@app.get("/")
async def root():
    return {"message": "Hello world"}
